# Caso 06 — Guia paso a paso: DynamoDB + Matrix Builds

> Estado: Implementacion proyectada — Q3 2026.
> Tiempo estimado: 60 minutos.

---

## Que resuelve este caso

Añade persistencia real (DynamoDB) a la Lambda del Caso 05 y demuestra
matrix strategy: el mismo codigo probado en multiples runtimes y regiones
en paralelo, con `fail-fast: false` para que un fallo no cancele el resto.

---

## Prerrequisitos

| Requisito | Verificacion |
|:---|:---|
| Caso 05 funcionando | Lambda + API Gateway activos |
| Permisos DynamoDB en el rol IAM | `dynamodb:GetItem`, `PutItem`, etc. |
| boto3 instalado (Python) | `pip show boto3` |

---

## Paso 1 — Crear la tabla DynamoDB

```bash
aws dynamodb create-table \
  --table-name caso-06-items \
  --attribute-definitions \
    AttributeName=PK,AttributeType=S \
    AttributeName=SK,AttributeType=S \
  --key-schema \
    AttributeName=PK,KeyType=HASH \
    AttributeName=SK,KeyType=RANGE \
  --billing-mode PAY_PER_REQUEST \
  --stream-specification StreamEnabled=true,StreamViewType=NEW_AND_OLD_IMAGES \
  --region us-east-1
```

Verificar que la tabla esta activa:

```bash
aws dynamodb describe-table \
  --table-name caso-06-items \
  --query "Table.TableStatus" \
  --output text
# ACTIVE
```

---

## Paso 2 — Actualizar la Lambda con acceso a DynamoDB

```python
# src/handler.py
import json, boto3, os
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
TABLE_NAME = os.environ.get('TABLE_NAME', 'caso-06-items')

def lambda_handler(event, context):
    table = dynamodb.Table(TABLE_NAME)
    method = event.get('httpMethod', 'GET')

    if method == 'POST':
        body = json.loads(event.get('body', '{}'))
        item = {
            'PK': f"USER#{body.get('user', 'anon')}",
            'SK': f"ITEM#{datetime.utcnow().isoformat()}",
            'data': body.get('data', ''),
            'caso': '06'
        }
        table.put_item(Item=item)
        return {'statusCode': 201, 'body': json.dumps({'created': True})}

    elif method == 'GET':
        user = event.get('queryStringParameters', {}).get('user', 'anon')
        result = table.query(
            KeyConditionExpression='PK = :pk',
            ExpressionAttributeValues={':pk': f'USER#{user}'}
        )
        return {'statusCode': 200, 'body': json.dumps(result['Items'])}

    return {'statusCode': 405, 'body': 'Method not allowed'}
```

---

## Paso 3 — Politica IAM minima para DynamoDB

Añadir al rol del Caso 03:

```json
{
  "Effect": "Allow",
  "Action": [
    "dynamodb:GetItem",
    "dynamodb:PutItem",
    "dynamodb:DeleteItem",
    "dynamodb:Query",
    "dynamodb:Scan"
  ],
  "Resource": "arn:aws:dynamodb:*:*:table/caso-06-items"
}
```

---

## Paso 4 — Workflow con matrix strategy

```yaml
name: Caso 06 — DynamoDB + Matrix

on:
  push:
    branches: [main]
    paths:
      - 'caso-06-dynamodb-matrix/**'

permissions:
  id-token: write
  contents: read

jobs:
  test-matrix:
    name: Test ${{ matrix.python }} en ${{ matrix.region }}
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false        # una celda fallida no cancela las demas
      matrix:
        python: ['3.11', '3.12']
        region: ['us-east-1', 'us-east-2']
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python }}
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ vars.AWS_ROLE_ARN }}
          aws-region: ${{ matrix.region }}
      - run: pip install boto3 pytest moto
        working-directory: caso-06-dynamodb-matrix
      - run: pytest tests/ -v
        working-directory: caso-06-dynamodb-matrix
        env:
          AWS_REGION: ${{ matrix.region }}
          TABLE_NAME: caso-06-items

  deploy:
    name: Deploy
    runs-on: ubuntu-latest
    needs: test-matrix       # espera a que TODAS las celdas de la matrix pasen
    environment: production
    steps:
      - uses: actions/checkout@v4
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ vars.AWS_ROLE_ARN }}
          aws-region: us-east-1
      - uses: aws-actions/setup-sam@v2
      - run: sam build && sam deploy --no-confirm-changeset --no-fail-on-empty-changeset
        working-directory: caso-06-dynamodb-matrix
```

---

## Paso 5 — Tests con moto (DynamoDB mock)

Para no necesitar AWS real en los tests unitarios:

```python
# tests/test_handler.py
import pytest, boto3, json, os
from moto import mock_aws
from src.handler import lambda_handler

@pytest.fixture
def dynamodb_table():
    with mock_aws():
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        table = dynamodb.create_table(
            TableName='caso-06-items',
            KeySchema=[
                {'AttributeName': 'PK', 'KeyType': 'HASH'},
                {'AttributeName': 'SK', 'KeyType': 'RANGE'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'PK', 'AttributeType': 'S'},
                {'AttributeName': 'SK', 'AttributeType': 'S'}
            ],
            BillingMode='PAY_PER_REQUEST'
        )
        os.environ['TABLE_NAME'] = 'caso-06-items'
        yield table

def test_post_item(dynamodb_table):
    with mock_aws():
        event = {
            'httpMethod': 'POST',
            'body': json.dumps({'user': 'vladimir', 'data': 'test'})
        }
        response = lambda_handler(event, None)
        assert response['statusCode'] == 201
```

---

## Paso 6 — Interpretar el workflow summary

GitHub muestra los resultados de la matrix en una tabla en el workflow summary:

```text
Matrix results:
  python=3.11, region=us-east-1  -> PASS
  python=3.11, region=us-east-2  -> PASS
  python=3.12, region=us-east-1  -> PASS
  python=3.12, region=us-east-2  -> PASS
```

Si una celda falla con `fail-fast: false`, el resto continua y el summary muestra
cuales pasaron y cuales fallaron, facilitando el diagnostico.

---

## Errores comunes y soluciones

### `ResourceNotFoundException` en DynamoDB

Causa: El nombre de tabla en el codigo no coincide con la tabla creada.

Solucion: Usar una variable de entorno `TABLE_NAME` en lugar de hardcodear
el nombre en el codigo:

```bash
aws dynamodb list-tables --region us-east-1
```

---

### La matrix lanza mas jobs de los esperados

Causa: El producto cartesiano de 2 runtimes x 2 regiones = 4 jobs es correcto.
Con 3 runtimes y 3 regiones serian 9 jobs en paralelo.

Solucion: Reducir la matrix durante desarrollo y expandir en CI:

```yaml
matrix:
  python: ['3.12']      # reducida para desarrollo
  region: ['us-east-1']
```

---

## Siguiente paso

-> [Caso 07 — Reusable Workflows](../caso-07-reusable-workflows/AWS_PASO_A_PASO.md): eliminar la duplicacion entre casos.
