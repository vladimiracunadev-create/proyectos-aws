# Especificaciones Tecnicas y Requerimientos

Este documento resume que necesitas para ejecutar, validar y extender el monorepo, incluyendo todos los casos con backend Lambda ya completados: D, E, F, G y H.

---

## Requerimientos de hardware

### Minimos

- **Sistema operativo**: Windows 10/11, macOS 11+ o Linux moderno
- **Procesador**: 2 nucleos
- **Memoria RAM**: 4 GB
- **Conectividad**: acceso a Internet para proveedores, imagenes y despliegues

### Recomendados

- **Procesador**: 4 nucleos o mas
- **Memoria RAM**: 8 GB o superior
- **Espacio libre**: al menos 2 GB para dependencias, builds, Docker y artefactos SAM

---

## Requerimientos de software

Para operar el repositorio completo:

1. **Git**
2. **Node.js LTS**
3. **AWS CLI** configurado con credenciales validas
4. **Terraform** 1.14 o superior
5. **Docker Desktop** o Docker Engine
6. **kubectl** para el Caso K
7. **Make**

Para trabajar con los casos Lambda (D, E, F, G, H):

1. **Python 3.12** o compatible
2. **AWS SAM CLI**
3. **pytest** y **boto3** para tests unitarios locales (`pip install pytest boto3`)
4. **Docker** si usaras `sam local`

Comandos de verificacion recomendados:

```bash
git --version
aws --version
sam --version
python --version
terraform version
docker --version
kubectl version --client
pytest --version
```

---

## Permisos AWS requeridos

El usuario o rol que despliegue debe tener permisos suficientes segun el caso.

### Base general

- `s3:*` acotado a buckets del proyecto o al bucket de artefactos/estado
- `cloudfront:*` donde aplique el Caso C
- `iam:CreateRole`, `iam:AttachRolePolicy`, `iam:PassRole` para despliegues controlados
- `cloudformation:*` para stacks administrados por Terraform o SAM

### Caso D: Serverless Basic

- `apigateway:*` o permisos equivalentes sobre HTTP API
- `lambda:*` o permisos de creacion/actualizacion/invocacion de funciones
- `dynamodb:*` o permisos sobre tabla y escritura/lectura
- `logs:*` para CloudWatch Logs de Lambda
- `cloudformation:*` para crear y actualizar el stack
- `s3:*` sobre el bucket temporal que usa SAM para empaquetado

### Caso E: DynamoDB Persistence Pro

- `apigateway:*` o permisos equivalentes sobre HTTP API
- `lambda:*` o permisos de creacion/actualizacion/invocacion de funciones
- `dynamodb:*` o permisos sobre tabla, indices y escritura/lectura
- `logs:*` para CloudWatch Logs de Lambda
- `cloudformation:*` para crear y actualizar el stack `caso-e-dynamodb-persistence`
- `s3:*` sobre el bucket temporal que usa SAM para empaquetado

### Caso F: Security First (Cognito + JWT + WAF)

- `cognito-idp:*` o permisos sobre User Pool, App Client y flujos de auth
- `apigateway:*` o permisos equivalentes sobre HTTP API con JWT Authorizer
- `lambda:*` o permisos de creacion/actualizacion/invocacion de funciones
- `lambda:AddPermission` para el trigger Pre-Signup de Cognito
- `wafv2:*` solo si se despliega con `DeployWAF=true` (opcional)
- `logs:*` para CloudWatch Logs de Lambda
- `cloudformation:*` para crear y actualizar el stack `caso-f-security-cognito`
- `s3:*` sobre el bucket temporal que usa SAM para empaquetado

### Caso G: Event Driven

- `apigateway:*` o permisos equivalentes sobre HTTP API
- `lambda:*` o permisos de creacion/actualizacion/invocacion de funciones
- `events:*` o permisos sobre custom bus, reglas y `PutEvents`
- `sqs:*` o permisos sobre cola principal y DLQ
- `sns:*` o permisos sobre el topic de notificaciones
- `logs:*` para CloudWatch Logs de Lambda
- `cloudformation:*` para crear y actualizar el stack `caso-g-event-driven`
- `s3:*` sobre el bucket temporal que usa SAM para empaquetado

### Caso H: Observability & Health

- `apigateway:*` o permisos equivalentes sobre HTTP API
- `lambda:*` o permisos de creacion/actualizacion/invocacion de funciones
- `cloudwatch:PutMetricData` para metricas custom desde Lambda
- `cloudwatch:PutDashboard` para el dashboard IaC
- `cloudwatch:PutMetricAlarm` para las alarmas CloudWatch
- `xray:PutTraceSegments`, `xray:PutTelemetryRecords` para trazas X-Ray
- `logs:*` para CloudWatch Logs de Lambda
- `cloudformation:*` para crear y actualizar el stack `caso-h-observability`
- `s3:*` sobre el bucket temporal que usa SAM para empaquetado

### FinOps y auditoria

- `budgets:ViewBudget`
- `ce:GetCostAndUsage`
- `ce:GetCostForecast`
- `ec2:Describe*`
- `eks:ListClusters`
- `rds:DescribeDBInstances`

---

## Instalacion en otra maquina

```bash
# 1. Clonar repositorio
git clone <url-del-repo>
cd proyectos-aws-gitlab

# 2. Instalar tooling general
make install

# 3. Configurar AWS
aws configure

# 4. Validar herramientas
make lint
aws sts get-caller-identity
sam --version
```

---

## Flujos minimos por caso Lambda

### Caso E

```bash
cd caso-e-dynamodb-persistence/backend
sam build && sam deploy --guided
curl "$API_BASE_URL/orders/status/PENDING"
```

Ver: [caso-e-dynamodb-persistence/AWS_PASO_A_PASO.md](../caso-e-dynamodb-persistence/AWS_PASO_A_PASO.md)

### Caso F

```bash
cd caso-f-security-cognito/backend
sam build && sam deploy --guided
# DeployWAF: false (por defecto — sin costo base)

# Registrar usuario
curl -s -X POST "$API_F_URL/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@demo.com","password":"Demo1234"}'

# Login y perfil protegido con JWT
TOKEN=$(curl -s -X POST "$API_F_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@demo.com","password":"Demo1234"}' | python3 -c "import sys,json; print(json.load(sys.stdin)['accessToken'])")
curl -s "$API_F_URL/profile" -H "Authorization: $TOKEN"
```

Ver: [caso-f-security-cognito/AWS_PASO_A_PASO.md](../caso-f-security-cognito/AWS_PASO_A_PASO.md)

### Caso G

```bash
cd caso-g-event-driven/backend
sam build && sam deploy --guided
curl "$API_BASE_URL/"
curl "$API_BASE_URL/health"
curl "$API_BASE_URL/health?format=json"
```

Ver: [caso-g-event-driven/AWS_PASO_A_PASO.md](../caso-g-event-driven/AWS_PASO_A_PASO.md)

### Caso H

```bash
cd caso-h-observability/backend
sam build && sam deploy --guided
curl "$API_BASE_URL/health"
curl -s -X POST "$API_BASE_URL/metrics" \
  -H "Content-Type: application/json" \
  -d '{"service":"caso-h","checks":1}'
```

Ver: [caso-h-observability/AWS_PASO_A_PASO.md](../caso-h-observability/AWS_PASO_A_PASO.md)

---

## Tests unitarios (sin credenciales AWS)

```bash
# Todos los casos Lambda de una vez
make test

# Por caso individual
make test-d   # Caso D
make test-e   # Caso E
make test-f   # Caso F (Cognito + JWT)
make test-g   # Caso G (EventBridge + SQS)
make test-h   # Caso H (CloudWatch + X-Ray)
```

---

## Nota operativa

El repositorio debe reflejar siempre el estado real del despliegue. Si un caso ya esta desplegado y validado, su documentacion global, roadmap y resumen tecnico deben indicarlo explicitamente.
