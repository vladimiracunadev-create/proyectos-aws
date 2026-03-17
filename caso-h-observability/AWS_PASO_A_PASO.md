# Guía Paso a Paso AWS — Caso H: Observability & Health

Estado actual validado el **17 de marzo de 2026**:

- `sam build` ejecutado con éxito.
- Stack desplegado: `caso-h-observability`.
- Región: `us-east-2`.
- API Base URL: `https://z7evf8mrzf.execute-api.us-east-2.amazonaws.com`.
- Dashboard URL: `https://us-east-2.console.aws.amazon.com/cloudwatch/home?region=us-east-2#dashboards:name=caso-h-observability`.
- Alarma Errores: `caso-h-lambda-errors` (Estado: OK).
- Alarma Latencia: `caso-h-lambda-duration-p99` (Estado: OK).

---

## 1. Requisitos previos

```bash
# Verificar herramientas instaladas
aws sts get-caller-identity
sam --version
python --version
```

Necesitas:

- AWS CLI configurado con cuenta válida y región `us-east-2`
- AWS SAM CLI >= 1.100
- Python 3.12 (para `sam local`)
- Docker (optional, necesario para `sam local start-api`)

---

## 2. Arquitectura que vas a desplegar

Dentro de `caso-h-observability/backend/template.yaml` se crean:

- 1 HTTP API Gateway con CORS
- 1 Lambda `HealthDashboardFunction` con **X-Ray Tracing: Active**
- 1 CloudWatch Dashboard `caso-h-observability` (Widget de invocaciones, errores, latencia y métricas custom)
- 1 Alarma sobre errores Lambda (`Errors ≥ 1 en 60s`)
- 1 Alarma sobre latencia p99 (`Duration p99 > 3000ms`)

El namespace de métricas custom es `CasoH` con dimensión `Service=caso-h-observability`.

---

## 3. Compilar la aplicación

```bash
cd caso-h-observability/backend
sam build
```

Esto valida la plantilla SAM y empaqueta la Lambda.
No requiere dependencias externas: solo `boto3` (incluido en el runtime Lambda).

---

## 4. Desplegar por primera vez

```bash
sam deploy --guided
```

Valores sugeridos cuando el CLI los pida:

- `Stack Name`: `caso-h-observability`
- `AWS Region`: `us-east-2`
- `Confirm changes before deploy`: `Y`
- `Allow SAM CLI IAM role creation`: `Y`
- `Disable rollback`: `N`
- `Save arguments to samconfig.toml`: `Y`

### Versión no interactiva (recomendada para CI)

```bash
sam deploy \
  --stack-name caso-h-observability \
  --region us-east-2 \
  --resolve-s3 \
  --capabilities CAPABILITY_IAM \
  --no-confirm-changeset \
  --no-fail-on-empty-changeset
```

---

## 5. Obtener los outputs del stack

```bash
aws cloudformation describe-stacks \
  --stack-name caso-h-observability \
  --region us-east-2 \
  --query "Stacks[0].Outputs"
```

Outputs esperados:

| Output | Descripción |
|---|---|
| `ApiBaseUrl` | URL base del HTTP API |
| `DashboardName` | Nombre del dashboard CloudWatch |
| `DashboardUrl` | URL directa a la consola de CloudWatch |
| `FunctionName` | Nombre de la Lambda desplegada |

Guarda el `ApiBaseUrl` para los pasos siguientes:

```bash
API_BASE_URL=$(aws cloudformation describe-stacks \
  --stack-name caso-h-observability \
  --region us-east-2 \
  --query "Stacks[0].Outputs[?OutputKey=='ApiBaseUrl'].OutputValue" \
  --output text)
echo $API_BASE_URL
```

---

## 6. Probar los endpoints

### Landing principal

```bash
curl "$API_BASE_URL/"
# → HTML de la landing interactiva
```

### Health check JSON

```bash
curl "$API_BASE_URL/health?format=json"
```

Respuesta esperada:

```json
{
  "status": "ok",
  "service": "caso-h-observability",
  "xray": "active",
  "metricNamespace": "CasoH",
  "timestamp": "2026-03-17T22:00:00+00:00"
}
```

### Health check HTML (navegador)

```bash
# Abre en navegador:
echo "$API_BASE_URL/health"
```

### Publicar métrica custom

```bash
curl -X POST "$API_BASE_URL/metrics"
```

Respuesta esperada:

```json
{
  "message": "Metrica publicada correctamente.",
  "namespace": "CasoH",
  "metricName": "HealthChecks",
  "service": "caso-h-observability",
  "timestamp": "2026-03-17T22:00:00+00:00"
}
```

---

## 7. Verificar en la consola AWS

### CloudWatch Dashboard

```bash
# Abre la URL del dashboard en tu navegador:
aws cloudformation describe-stacks \
  --stack-name caso-h-observability \
  --region us-east-2 \
  --query "Stacks[0].Outputs[?OutputKey=='DashboardUrl'].OutputValue" \
  --output text
```

En el dashboard verás:

1. **Widget de Invocaciones y Errores**: barras de invocaciones (azul) y errores (rojo).
2. **Widget de Duración**: promedio y p99 de la latencia Lambda.
3. **Widget de Métricas Custom**: contador de `CasoH/HealthChecks` (verde).
4. **Widget de Alarmas**: estado de las 2 alarmas configuradas.
5. **Widget de Logs**: últimas 20 líneas de logs de la Lambda.

### AWS X-Ray Service Map

1. Abre [AWS X-Ray Console](https://console.aws.amazon.com/xray/home?region=us-east-2).
2. Haz clic en **Service map**.
3. Deberías ver el nodo `caso-h-observability` conectado a `AWS::CloudWatch`.
4. Haz clic en **Traces** para ver las trazas individuales.
5. Cada trace muestra: API Gateway → Lambda → CloudWatch con tiempos detallados.

### CloudWatch Alarms

```bash
aws cloudwatch describe-alarms \
  --alarm-names "caso-h-lambda-errors" "caso-h-lambda-duration-p99" \
  --region us-east-2 \
  --query "MetricAlarms[*].{Alarm:AlarmName,State:StateValue}" \
  --output table
```

Estado esperado: ambas en `OK` si no hay errores.

### Forzar una alarma (simulación)

Para disparar la alarma de errores manualmente:

```bash
aws cloudwatch set-alarm-state \
  --alarm-name "caso-h-lambda-errors" \
  --state-value ALARM \
  --state-reason "Prueba manual de alarma" \
  --region us-east-2

# Restaurar:
aws cloudwatch set-alarm-state \
  --alarm-name "caso-h-lambda-errors" \
  --state-value OK \
  --state-reason "Restaurado para demostración" \
  --region us-east-2
```

### Verificar métricas custom en CloudWatch

```bash
# Publicar 5 veces para tener datos suficientes en el dashboard
for i in 1 2 3 4 5; do
  curl -X POST "$API_BASE_URL/metrics"
  echo "Métrica $i publicada"
done

# Consultar la métrica desde CLI
aws cloudwatch get-metric-statistics \
  --namespace CasoH \
  --metric-name HealthChecks \
  --dimensions Name=Service,Value=caso-h-observability \
  --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -v-1H +%Y-%m-%dT%H:%M:%SZ) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%SZ) \
  --period 300 \
  --statistics Sum \
  --region us-east-2
```

---

## 8. Probar en local (opcional)

```bash
cd caso-h-observability/backend

# Invocar directamente con evento de prueba
sam local invoke HealthDashboardFunction --event events/health-check.json

# Levantar API local completa
sam local start-api
```

Luego:

```bash
# En otra terminal:
curl http://127.0.0.1:3000/health?format=json
curl -X POST http://127.0.0.1:3000/metrics
```

> **Nota**: `sam local` simulará la Lambda pero `PutMetricData` llamará a AWS real
> si tienes credenciales configuradas. X-Ray solo funciona en AWS real.

---

## 9. CloudWatch Logs Insights — queries útiles

Abre [CloudWatch Logs Insights](https://console.aws.amazon.com/cloudwatch/home?region=us-east-2#logsV2:logs-insights) y selecciona el log group `/aws/lambda/{FunctionName}`.

### Últimas invocaciones

```
fields @timestamp, @message
| sort @timestamp desc
| limit 20
```

### Errores únicamente

```
fields @timestamp, @message
| filter @message like /ERROR/
| sort @timestamp desc
| limit 20
```

### Duración promedio por ruta

```
fields @timestamp, @duration, @message
| stats avg(@duration) as avg_ms, count() as total by bin(5m)
| sort @timestamp desc
```

---

## 10. Limpieza

Cuando termines el laboratorio:

```bash
sam delete --stack-name caso-h-observability --region us-east-2
```

Esto elimina:

- API Gateway
- Lambda `HealthDashboardFunction`
- CloudWatch Dashboard `caso-h-observability`
- CloudWatch Alarms (2)
- IAM Role de la Lambda
- Bucket S3 de artefactos SAM (si se creó con `--resolve-s3`)

> Las métricas y logs permanecen en CloudWatch según la política de retención
> (por defecto nunca expiran, salvo que configures retención manual).

---

## 11. Siguiente paso natural

La evolución natural de este caso es:

- Conectar X-Ray con los Lambdas del **Caso G** para ver el service map completo EventBridge → SQS → Lambda.
- Añadir métricas de la cola SQS (profundidad, mensajes en DLQ) del Caso G en el dashboard.
- Implementar el **Caso F (Cognito + WAF)** y añadir métricas de autenticación y requests bloqueados.
