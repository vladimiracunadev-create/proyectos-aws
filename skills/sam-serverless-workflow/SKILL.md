---
name: sam-serverless-workflow
description: Flujo completo de AWS SAM para este monorepo: build, deploy, prueba de endpoints, testing local con event files y troubleshooting de errores frecuentes. Usar cuando se trabaja con cualquier caso serverless (D, E, F, G, H o futuros) que use AWS SAM y template.yaml.
---

# SAM Serverless Workflow

Este skill cubre el ciclo completo de trabajo con AWS SAM en este repositorio.

## Casos que usan SAM

| Caso | Stack name | Region |
|---|---|---|
| D — Serverless Basic | `caso-d-serverless-basic` | us-east-2 |
| E — DynamoDB Persistence | `caso-e-dynamodb-persistence` | us-east-2 |
| F — Security Cognito | `caso-f-security-cognito` | us-east-2 |
| G — Event Driven | `caso-g-event-driven` | us-east-2 |
| H — Observability | `caso-h-observability` | us-east-2 |

---

## Flujo estandar de despliegue

### 1. Siempre hacer build antes de deploy

```bash
cd caso-X-nombre/backend
sam build
```

`sam build` compila el codigo, instala dependencias y genera `.aws-sam/build/`. Sin este paso, `sam deploy` usa el build anterior o falla.

### 2. Primer despliegue (stack nuevo)

```bash
sam deploy \
  --stack-name caso-X-nombre \
  --region us-east-2 \
  --capabilities CAPABILITY_IAM \
  --resolve-s3
```

`--resolve-s3` crea automaticamente el bucket de staging de SAM. No crear uno manual.

### 3. Redespliegues posteriores

```bash
sam build && sam deploy \
  --stack-name caso-X-nombre \
  --region us-east-2 \
  --capabilities CAPABILITY_IAM \
  --resolve-s3 \
  --no-confirm-changeset
```

`--no-confirm-changeset` evita la confirmacion interactiva. Util para iteraciones rapidas.

### 4. Deploy con parametros de override

Cuando el template tiene parametros (ejemplo: Caso F con DeployWAF):

```bash
sam deploy \
  --stack-name caso-f-security-cognito \
  --region us-east-2 \
  --capabilities CAPABILITY_IAM \
  --resolve-s3 \
  --parameter-overrides DeployWAF=false
```

Siempre revisar `Parameters:` en el `template.yaml` antes de desplegar.

### 5. Verificar outputs del stack

Despues del deploy, los outputs contienen las URLs y ARNs utiles:

```bash
aws cloudformation describe-stacks \
  --stack-name caso-X-nombre \
  --region us-east-2 \
  --query 'Stacks[0].Outputs' \
  --output table
```

### 6. Destruir el stack

```bash
sam delete \
  --stack-name caso-X-nombre \
  --region us-east-2 \
  --no-prompts
```

`--no-prompts` confirma la eliminacion sin interaccion. Usar con cuidado.

---

## Testing local con event files

Los casos tienen archivos en `backend/events/` para invocar Lambda localmente sin desplegar:

```bash
cd caso-X-nombre/backend
sam build
sam local invoke NombreDeLaFuncion --event events/nombre-evento.json
```

Ejemplos por caso:
- `caso-d`: `events/create-lead.json`
- `caso-e`: `events/create-order.json`, `events/get-customer-orders.json`
- `caso-f`: `events/register.json`, `events/login.json`
- `caso-g`: `events/publish-order.json`
- `caso-h`: `events/health-check.json`

El nombre de la funcion (`NombreDeLaFuncion`) es el nombre del recurso `AWS::Serverless::Function` en el `template.yaml`, no el handler de Python.

---

## Targets del Makefile

Este repositorio tiene targets unificados:

```bash
make build-X     # sam build del caso X
make deploy-X    # sam build + sam deploy del caso X
make delete-X    # sam delete del caso X
make smoke-X     # ejecuta scripts/smoke/smoke_caso_X.sh
make test-X      # pytest del caso X
```

Verificar siempre el Makefile antes de usar comandos manuales. Si el target existe, usarlo.

---

## Errores frecuentes y solucion

### Error: "No changes to deploy"

El changeset no tiene diferencias. Puede ser que:
- El codigo no cambio realmente
- Se olvido hacer `sam build` antes del deploy

Solucion: `sam build` y volver a intentar.

### Error: "CAPABILITY_IAM is required"

El template crea roles IAM y SAM pide confirmacion explicita.

Solucion: agregar `--capabilities CAPABILITY_IAM` al comando.

### Error: "Stack is in ROLLBACK_COMPLETE state"

El stack fallo en un deploy anterior y quedo en estado invalido.

Solucion:
```bash
aws cloudformation delete-stack --stack-name caso-X-nombre --region us-east-2
# Esperar que se elimine, luego redesplegar
sam deploy ...
```

### Error: "Export ... already exists"

Otro stack exporta un valor con el mismo nombre.

Solucion: revisar `Outputs:` en el template.yaml y asegurarse que los `Export.Name` sean unicos (incluir el nombre del stack como prefijo).

### Error en Lambda: timeout

El timeout por defecto en SAM es 3 segundos. Para casos con DynamoDB o Cognito, aumentar:

```yaml
Globals:
  Function:
    Timeout: 10
```

---

## Estructura estandar del template.yaml en este repositorio

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Description: Caso X — descripcion breve

Parameters:
  # Solo si hay configuracion variable

Globals:
  Function:
    Runtime: python3.12
    MemorySize: 128
    Timeout: 10
    Environment:
      Variables:
        TABLE_NAME: !Ref NombreDeLaTabla

Resources:
  # API Gateway primero
  # Funciones Lambda
  # DynamoDB / Cognito / otros recursos

Outputs:
  ApiUrl:
    Value: !Sub "https://${NombreApi}.execute-api.${AWS::Region}.amazonaws.com"
    Export:
      Name: !Sub "${AWS::StackName}-ApiUrl"
```

---

## Verificar que el deploy funciono

Despues de un deploy exitoso, siempre verificar con curl o smoke test:

```bash
# Obtener la URL del stack
API_URL=$(aws cloudformation describe-stacks \
  --stack-name caso-X-nombre --region us-east-2 \
  --query 'Stacks[0].Outputs[?OutputKey==`ApiUrl`].OutputValue' \
  --output text)

# Health check basico
curl -s "$API_URL/health" | python -m json.tool

# O ejecutar el smoke test del caso
make smoke-X
```
