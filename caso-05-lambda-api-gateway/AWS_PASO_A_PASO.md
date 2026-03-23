# Caso 05 — Guia paso a paso: Lambda + API Gateway

> Estado: Implementacion proyectada — Q2-Q3 2026.
> Tiempo estimado: 60-90 minutos.

---

## Que resuelve este caso

Hasta aqui solo hemos desplegado archivos estaticos. Este caso introduce el primer
backend real: una funcion Lambda expuesta via API Gateway, con un pipeline
que garantiza que el artefacto que se prueba es el mismo que llega a produccion.

---

## Prerrequisitos

| Requisito | Verificacion |
|:---|:---|
| AWS SAM CLI instalado | `sam --version` |
| Python 3.11+ o Node.js 20+ | `python --version` o `node --version` |
| OIDC configurado (Caso 03) | Rol IAM para GitHub Actions activo |
| pytest o jest instalado | `pip show pytest` o `npm list jest` |

---

## Paso 1 — Estructura del proyecto

```text
caso-05-lambda-api-gateway/
├── src/
│   ├── handler.py          (o handler.js)
│   └── requirements.txt    (o package.json)
├── tests/
│   └── test_handler.py     (o handler.test.js)
└── template.yaml           (SAM template)
```

---

## Paso 2 — Escribir la Lambda

Ejemplo minimo en Python:

```python
# src/handler.py
import json

def lambda_handler(event, context):
    name = event.get('queryStringParameters', {}).get('name', 'mundo')
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({'message': f'Hola, {name}!', 'caso': '05'})
    }
```

Test unitario:

```python
# tests/test_handler.py
from src.handler import lambda_handler

def test_respuesta_basica():
    event = {'queryStringParameters': {'name': 'Vladimir'}}
    response = lambda_handler(event, None)
    assert response['statusCode'] == 200
    assert 'Vladimir' in response['body']

def test_nombre_por_defecto():
    event = {'queryStringParameters': None}
    response = lambda_handler(event, None)
    assert response['statusCode'] == 200
    assert 'mundo' in response['body']
```

---

## Paso 3 — SAM template

```yaml
# template.yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Globals:
  Function:
    Runtime: python3.12
    Timeout: 10
    MemorySize: 128

Resources:
  HolaFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: src/
      Handler: handler.lambda_handler
      Events:
        ApiGet:
          Type: Api
          Properties:
            Path: /hola
            Method: get

Outputs:
  ApiUrl:
    Description: URL del endpoint
    Value: !Sub "https://${ServerlessRestApi}.execute-api.${AWS::Region}.amazonaws.com/Prod/hola"
```

---

## Paso 4 — Workflow multi-job

```yaml
name: Caso 05 — Lambda + API Gateway

on:
  push:
    branches: [main]
    paths:
      - 'caso-05-lambda-api-gateway/**'

permissions:
  id-token: write
  contents: read

jobs:
  test:
    name: Tests unitarios
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: caso-05-lambda-api-gateway
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install -r src/requirements.txt pytest
      - run: pytest tests/ -v

  build:
    name: Build artefacto SAM
    runs-on: ubuntu-latest
    needs: test          # solo corre si test pasa
    defaults:
      run:
        working-directory: caso-05-lambda-api-gateway
    steps:
      - uses: actions/checkout@v4
      - uses: aws-actions/setup-sam@v2
      - run: sam build
      - uses: actions/upload-artifact@v4
        with:
          name: sam-build
          path: caso-05-lambda-api-gateway/.aws-sam/

  deploy:
    name: Deploy a AWS
    runs-on: ubuntu-latest
    needs: build         # descarga el artefacto del job build
    environment: production
    steps:
      - uses: actions/checkout@v4
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ vars.AWS_ROLE_ARN }}
          aws-region: us-east-1
      - uses: aws-actions/setup-sam@v2
      - uses: actions/download-artifact@v4
        with:
          name: sam-build
          path: caso-05-lambda-api-gateway/.aws-sam/
      - name: Deploy
        working-directory: caso-05-lambda-api-gateway
        run: |
          sam deploy \
            --no-confirm-changeset \
            --no-fail-on-empty-changeset \
            --stack-name caso-05-lambda-api-gateway \
            --capabilities CAPABILITY_IAM \
            --region us-east-1
```

---

## Paso 5 — Verificacion

Obtener la URL del endpoint tras el deploy:

```bash
aws cloudformation describe-stacks \
  --stack-name caso-05-lambda-api-gateway \
  --query "Stacks[0].Outputs[?OutputKey=='ApiUrl'].OutputValue" \
  --output text
```

Probar el endpoint:

```bash
API_URL=$(aws cloudformation describe-stacks \
  --stack-name caso-05-lambda-api-gateway \
  --query "Stacks[0].Outputs[?OutputKey=='ApiUrl'].OutputValue" \
  --output text)

curl "${API_URL}?name=Vladimir"
# {"message": "Hola, Vladimir!", "caso": "05"}

curl "${API_URL}"
# {"message": "Hola, mundo!", "caso": "05"}
```

---

## Errores comunes y soluciones

### `Error: No artifacts folder`

Causa: El job `deploy` no encuentra el artefacto porque `download-artifact` lo puso
en un path diferente al que `sam deploy` espera.

Solucion: Verificar que el `path` en `download-artifact` coincide con el directorio
donde `sam build` genera `.aws-sam/`.

---

### Los tests pasan en CI pero la Lambda falla en AWS

Causa: Diferencia entre el entorno de tests y el runtime de Lambda.

Solucion: Usar `sam local invoke` para probar localmente con el mismo runtime
antes de hacer push:

```bash
cd caso-05-lambda-api-gateway
sam local invoke HolaFunction --event '{"queryStringParameters":{"name":"test"}}'
```

---

### `CAPABILITY_IAM is required`

Causa: SAM necesita crear un rol IAM para la Lambda y CloudFormation requiere
confirmacion explicita de ese permiso.

Solucion: El flag `--capabilities CAPABILITY_IAM` ya esta en el comando de deploy.
Si sigue fallando, verificar que el rol de GitHub Actions tiene permiso `iam:CreateRole`.

---

## Permisos IAM adicionales para el rol de GitHub Actions

El rol del Caso 03 necesita permisos adicionales para este caso:

```json
{
  "Effect": "Allow",
  "Action": [
    "cloudformation:*",
    "lambda:*",
    "apigateway:*",
    "iam:CreateRole",
    "iam:DeleteRole",
    "iam:AttachRolePolicy",
    "iam:DetachRolePolicy",
    "iam:GetRole",
    "iam:PassRole",
    "s3:CreateBucket",
    "s3:PutObject",
    "s3:GetObject"
  ],
  "Resource": "*"
}
```

---

## Siguiente paso

-> [Caso 06 — DynamoDB + Matrix](../caso-06-dynamodb-matrix/AWS_PASO_A_PASO.md): añadir persistencia real y matrix builds.
