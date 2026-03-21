# Centro de Control de Costos AWS

> Objetivo: convertir el control de costos del monorepo en un flujo profesional, repetible y facil de operar desde Windows PowerShell, Bash y Claude Code.

---

## Que resuelve este documento

Este documento responde, en simple, las preguntas que mas confunden al trabajar con AWS:

- Estoy en cuenta free o paid
- Me quedan creditos
- Que servicios del repositorio estan activos ahora
- Que parte del gasto corresponde a billing y que parte a recursos reales
- Que comandos debo correr antes de cerrar una sesion
- Que recursos puedo dejar vivos y cuales debo destruir

No reemplaza a [docs/FINOPS_COSTOS.md](./FINOPS_COSTOS.md), que explica el costo esperado por caso. Este archivo se enfoca en operacion real y control diario.

---

## Modelo mental correcto

AWS mezcla cuatro conceptos que conviene separar:

| Concepto | Que significa | Como se consulta |
|---|---|---|
| `Account plan` | Si la cuenta opera como `FREE` o `PAID` | `aws freetier get-account-plan-state` |
| `Credits` | Dinero promocional disponible para absorber cargos | `aws freetier get-account-plan-state` |
| `Free Tier` | Beneficios gratuitos por servicio | `aws freetier get-free-tier-usage` |
| `Real cost` | Lo que efectivamente se acumula en el mes | `aws ce get-cost-and-usage` |

Regla profesional: no asumas que "tener Free Tier" significa "todo cuesta cero". Un servicio puede seguir cobrando aunque la cuenta tenga creditos o beneficios gratuitos parciales.

---

## Regiones: por que `us-east-1` y `us-east-2` al mismo tiempo

En este repositorio la region operativa principal es `us-east-2`, pero billing y Free Tier no se consultan ahi.

| Tipo de consulta | Region recomendada |
|---|---|
| Recursos del monorepo | `us-east-2` |
| Billing, Cost Explorer, Free Tier, Budgets | `us-east-1` |
| Auditoria multi-region preventiva | `us-east-1`, `us-east-2`, `sa-east-1` |

Esto no es un error. AWS expone varias APIs financieras en `us-east-1` aunque tus workloads vivan en otra region.

---

## Lo minimo que debes saber leer

### 1. `accountPlanType`

- `FREE`: cuenta dentro de plan free
- `PAID`: cuenta de cobro normal

### 2. `accountPlanRemainingCredits`

- Si el valor es mayor que `0`, todavia tienes creditos absorbiendo parte del gasto
- Si es `0`, cualquier cargo real empezara a pegar completo en billing

### 3. `Free Tier usage`

No te dice el costo del mes. Te dice cuanto has usado del beneficio gratuito por servicio.

### 4. `Cost Explorer`

Es la fuente mas util para responder: "que me esta cobrando AWS ahora mismo".

Punto fino importante: en Cost Explorer, la fecha `End` es exclusiva. Para ver el mes actual completo hasta hoy, conviene usar manana como fecha final.

---

## Mapa de casos y servicios a vigilar

| Caso | Servicios principales | Nivel de vigilancia |
|---|---|---|
| A | Amplify | Bajo |
| B | S3 Website | Bajo |
| C | CloudFront, S3, DynamoDB state lock | Bajo |
| D | API Gateway, Lambda, DynamoDB | Bajo |
| E | API Gateway, Lambda, DynamoDB, GSI | Bajo |
| F | Cognito, API Gateway, Lambda, WAF opcional | Medio |
| G | EventBridge, SQS, SNS, Lambda | Bajo |
| H | CloudWatch Dashboard, Alarms, X-Ray | Medio |
| J | ECS, ECR, ALB | Alto |
| K | EKS, NAT Gateway, ALB, EC2/Fargate | Critico |
| L | Budgets, OIDC, S3 | Bajo |
| M futuro | Route 53, ECS, ALB, failover | Alto |

---

## Flujo profesional recomendado

### Antes de desplegar

1. Verifica identidad y cuenta activa.
2. Revisa si ya hay recursos viejos encendidos.
3. Confirma si estas en modo demo barato o en modo evidencia temporal.

### Antes de cerrar una sesion

1. Revisa `Cost Explorer` del mes actual.
2. Busca recursos de costo fijo:
   - `WAF`
   - `CloudWatch Dashboard`
   - `ALB`
   - `NAT Gateway`
   - `EKS`
   - `EC2 running`
   - `RDS`
3. Destruye lo que corresponda a labs temporales.

### Cada viernes

1. Ejecuta `make finops-check`
2. Ejecuta `make finops-control`
3. Revisa si hay recursos fuera de CloudFormation o Terraform

### Cerca de fin de mes

1. Ejecuta de nuevo el reporte completo
2. Revisa el costo mensual estimado
3. Si hay WAF, Dashboard, ALB o EKS activos sin necesidad, destruyelos

---

## Variables base para Windows PowerShell

```powershell
$BillingRegion = "us-east-1"
$WorkloadRegion = "us-east-2"
$AuditRegions = @("us-east-2", "us-east-1", "sa-east-1")
$Start = (Get-Date -Day 1).ToString("yyyy-MM-dd")
$End = (Get-Date).AddDays(1).ToString("yyyy-MM-dd")
```

Si usas perfiles:

```powershell
$env:AWS_PROFILE = "portfolio"
```

---

## Comandos clave para control personal en Windows

### 1. Identidad real de AWS

```powershell
aws sts get-caller-identity --region $WorkloadRegion
```

Esto responde:

- que cuenta esta activa
- con que usuario o rol estas operando
- si de verdad estas autenticado

### 2. Estado de cuenta, plan y creditos

```powershell
aws freetier get-account-plan-state --region $BillingRegion
```

Busca especialmente:

- `accountPlanType`
- `accountPlanStatus`
- `accountPlanRemainingCredits`

### 3. Uso de Free Tier

```powershell
aws freetier get-free-tier-usage --region $BillingRegion
```

Consulta filtrada para los servicios que mas usa este monorepo:

```powershell
aws freetier get-free-tier-usage --region $BillingRegion `
  --query "freeTierUsages[?contains(service, 'Lambda') || contains(service, 'DynamoDB') || contains(service, 'CloudWatch') || contains(service, 'Simple Queue Service') || contains(service, 'Simple Notification Service') || contains(service, 'X-Ray') || contains(service, 'API Gateway') || contains(service, 'Cognito')].[service,freeTierType,usageType,currentUsage.amount,currentUsage.unit,limit.amount,limit.unit]" `
  --output table
```

### 4. Costo mensual real por servicio

```powershell
aws ce get-cost-and-usage --region $BillingRegion `
  --time-period Start=$Start,End=$End `
  --granularity MONTHLY `
  --metrics UnblendedCost `
  --group-by Type=DIMENSION,Key=SERVICE
```

Version lista para leer como tabla:

```powershell
aws ce get-cost-and-usage --region $BillingRegion `
  --time-period Start=$Start,End=$End `
  --granularity MONTHLY `
  --metrics UnblendedCost `
  --group-by Type=DIMENSION,Key=SERVICE `
  --query "ResultsByTime[0].Groups[].[Keys[0],Metrics.UnblendedCost.Amount,Metrics.UnblendedCost.Unit]" `
  --output table
```

### 5. Budgets y gobernanza del Caso L

```powershell
$AccountId = (aws sts get-caller-identity --region $WorkloadRegion --query Account --output text)
aws budgets describe-budgets --region $BillingRegion --account-id $AccountId `
  --query "Budgets[].[BudgetName,BudgetType,TimeUnit,BudgetLimit.Amount,BudgetLimit.Unit,CalculatedSpend.ActualSpend.Amount]" `
  --output table
```

```powershell
aws iam list-open-id-connect-providers --output table
```

### 6. Casos A, B, C y L: hosting estatico, buckets y CDN

```powershell
aws s3api list-buckets --query "Buckets[].[Name,CreationDate]" --output table
aws cloudfront list-distributions --query "DistributionList.Items[].[Id,DomainName,Enabled,Origins.Quantity]" --output table
aws amplify list-apps --region $WorkloadRegion --query "apps[].[name,platform,defaultDomain]" --output table
```

### 7. Casos D, E, F, G y H: serverless y seguridad

```powershell
aws cloudformation list-stacks --region $WorkloadRegion `
  --stack-status-filter CREATE_COMPLETE UPDATE_COMPLETE UPDATE_ROLLBACK_COMPLETE `
  --query "StackSummaries[].[StackName,StackStatus]" --output table

aws apigatewayv2 get-apis --region $WorkloadRegion `
  --query "Items[].[Name,ProtocolType,ApiEndpoint]" --output table

aws apigateway get-rest-apis --region $WorkloadRegion `
  --query "items[].[name,id]" --output table

aws lambda list-functions --region $WorkloadRegion `
  --query "Functions[].[FunctionName,Runtime,LastModified]" --output table

aws dynamodb list-tables --region $WorkloadRegion --output table
aws cognito-idp list-user-pools --region $WorkloadRegion --max-results 60 `
  --query "UserPools[].[Name,Id]" --output table

aws wafv2 list-web-acls --scope REGIONAL --region $WorkloadRegion `
  --query "WebACLs[].[Name,Id]" --output table

aws cloudwatch list-dashboards --region $WorkloadRegion `
  --query "DashboardEntries[].[DashboardName,LastModified]" --output table

aws cloudwatch describe-alarms --region $WorkloadRegion `
  --query "MetricAlarms[].[AlarmName,StateValue,Namespace]" --output table

aws logs describe-log-groups --region $WorkloadRegion `
  --query "logGroups[].[logGroupName,retentionInDays,storedBytes]" --output table
```

### 8. Caso G: event-driven

```powershell
aws events list-event-buses --region $WorkloadRegion `
  --query "EventBuses[].[Name,Arn]" --output table

aws sqs list-queues --region $WorkloadRegion --output table
aws sns list-topics --region $WorkloadRegion --query "Topics[].[TopicArn]" --output table
```

Si tienes un bus custom, revisa tambien sus reglas:

```powershell
aws events list-rules --region $WorkloadRegion --event-bus-name caso-g-orders-bus `
  --query "Rules[].[Name,State,EventPattern]" --output table
```

### 9. Casos J, K y M: contenedores, balanceadores y red

```powershell
aws ecr describe-repositories --region $WorkloadRegion `
  --query "repositories[].[repositoryName,repositoryUri,imageScanningConfiguration.scanOnPush]" --output table

aws ecs list-clusters --region $WorkloadRegion --output table
aws eks list-clusters --region $WorkloadRegion --output table

aws elbv2 describe-load-balancers --region $WorkloadRegion `
  --query "LoadBalancers[].[LoadBalancerName,Type,Scheme,State.Code]" --output table

aws ec2 describe-nat-gateways --region $WorkloadRegion `
  --filter Name=state,Values=available,pending `
  --query "NatGateways[].[NatGatewayId,State,SubnetId,NatGatewayAddresses[0].PublicIp]" `
  --output table

aws ec2 describe-instances --region $WorkloadRegion `
  --filters Name=instance-state-name,Values=running,stopped `
  --query "Reservations[].Instances[].[InstanceId,State.Name,InstanceType,PublicIpAddress,Tags[?Key==\`Name\`].Value|[0]]" `
  --output table

aws ec2 describe-volumes --region $WorkloadRegion `
  --query "Volumes[].[VolumeId,State,Size,VolumeType,Attachments[0].InstanceId]" `
  --output table

aws ec2 describe-addresses --region $WorkloadRegion `
  --query "Addresses[].[PublicIp,AllocationId,AssociationId,InstanceId,NetworkInterfaceId]" `
  --output table

aws rds describe-db-instances --region $WorkloadRegion `
  --query "DBInstances[].[DBInstanceIdentifier,DBInstanceStatus,Engine,DBInstanceClass]" `
  --output table
```

### 10. Casos C y M con dominios: Route 53 y ACM

```powershell
aws route53 list-hosted-zones --query "HostedZones[].[Name,ResourceRecordSetCount,Config.PrivateZone]" --output table
aws acm list-certificates --region us-east-1 --query "CertificateSummaryList[].[DomainName,Status]" --output table
aws acm list-certificates --region $WorkloadRegion --query "CertificateSummaryList[].[DomainName,Status]" --output table
```

---

## Scripts nuevos del repositorio

### Auditoria rapida

```powershell
make finops-check
```

Sirve para una pasada corta sobre recursos de alto costo.

### Auditoria completa

```powershell
make finops-control
```

Sin pasar ningun parametro de salida, el flujo ya genera automaticamente un reporte local en:

```text
.tmp/skill-output/finops-report-YYYYMMDD-HHMMSS.txt
```

Alternativas directas:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\aws-cost-control-report.ps1
```

```bash
./scripts/aws-cost-control-report.sh
```

Con parametros:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\aws-cost-control-report.ps1 `
  -Regions us-east-2,us-east-1,sa-east-1 `
  -BillingRegion us-east-1 `
  -StartDate 2026-03-01 `
  -EndDate 2026-04-01 `
  -OutputPath .\.tmp\skill-output\finops-report.txt
```

```bash
./scripts/aws-cost-control-report.sh \
  --regions us-east-2,us-east-1,sa-east-1 \
  --billing-region us-east-1 \
  --start-date 2026-03-01 \
  --end-date 2026-04-01 \
  --output-path ./.tmp/skill-output/finops-report.txt
```

---

## Uso con Claude Code skill

El skill del repositorio para esto es:

```text
/finops-audit-and-budgeting
```

Usalo cuando quieras:

- revisar costo mensual
- detectar recursos vivos
- preparar una limpieza segura
- actualizar dashboards o documentacion FinOps

La idea del skill no es adivinar precios: es apoyarse en estos scripts y en las APIs reales de AWS para leer la cuenta.

Para no ensuciar el repositorio, este flujo genera por defecto la salida local dentro de:

```text
.tmp/skill-output/
```

Esa ruta vive bajo `.tmp/`, que esta bloqueada en `.gitignore` y no se sube al repositorio.

---

## Como interpretar resultados sin volverte loco

### Senales sanas

- `Lambda`, `DynamoDB`, `SQS`, `SNS`, `EventBridge` con costo cero o casi cero
- `CloudFront`, `S3`, `Amplify` con gasto minimo en demos
- `Cognito` sin costo relevante en laboratorio

### Senales para revisar hoy

- `WAF` activo en Caso F
- `CloudWatch Dashboard` activo en Caso H
- `ALB` activo en Caso J o M
- `NAT Gateway` activo en Caso K o M
- `EKS` activo en Caso K
- `EC2 running` o `RDS` vivos sin razon clara

### Regla por caso

- Casos `A, B, C, D, E, G, L`: normalmente se pueden dejar vivos
- Caso `F`: dejar vivo el `DEMO`; destruir WAF cuando termine la ventana de evidencia
- Caso `H`: destruir el dashboard cuando termine la captura
- Casos `J, K, M`: levantar, validar, capturar y destruir

---

## Rutina profesional de cierre

Usa esta secuencia:

```powershell
aws sts get-caller-identity --region us-east-2
aws freetier get-account-plan-state --region us-east-1
aws ce get-cost-and-usage --region us-east-1 --time-period Start=$Start,End=$End --granularity MONTHLY --metrics UnblendedCost --group-by Type=DIMENSION,Key=SERVICE --query "ResultsByTime[0].Groups[].[Keys[0],Metrics.UnblendedCost.Amount,Metrics.UnblendedCost.Unit]" --output table
make finops-check
make finops-control
```

Si ves `WAF`, `Dashboard`, `ALB`, `NAT` o `EKS` activos sin necesidad, actua el mismo dia.

---

## Que archivo leer en cada situacion

| Necesidad | Archivo |
|---|---|
| Entender costo esperado por caso | [docs/FINOPS_COSTOS.md](./FINOPS_COSTOS.md) |
| Hacer una auditoria corta | [docs/FINOPS_MANUAL.md](./FINOPS_MANUAL.md) |
| Operar costos, billing, creditos y recursos activos | `docs/COST_CONTROL_COMMAND_CENTER.md` |
| Ejecutar reporte completo desde Windows | `scripts/aws-cost-control-report.ps1` |
| Ejecutar reporte completo desde Bash | `scripts/aws-cost-control-report.sh` |
