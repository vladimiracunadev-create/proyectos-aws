# 📋 Runbook: Failover & Failback — Caso M

> **Estado**: Runbook futuro para Fase 2+. Los comandos con placeholders (`<VAR>`) se completan
> cuando la infraestructura esté activa. Los marcados con `[FASE 1]`/`[FASE 2]` indican en qué
> fase se ejecutan por primera vez.

---

## 👤 Roles y Responsabilidades

| Rol | Responsabilidad durante GameDay |
|---|---|
| **Incident Commander** | Coordina el ejercicio, valida objetivos de RTO/RPO |
| **SRE On-Call** | Ejecuta los scripts de simulación, observa métricas |
| **Observer** | Valida desde el cliente que el servicio sigue respondiendo |

---

## 🎯 Objetivo del GameDay

Demostrar **end-to-end** que el sistema:

1. Detecta el fallo automáticamente (sin intervención manual).
2. Redirige el tráfico a instancias/AZs/regiones sanas.
3. El cliente experimenta **cero downtime** (o downtime dentro del RTO acordado).
4. El retorno al primario (**failback**) es controlado y seguro.

---

## ⏱️ Duración Estimada del GameDay

| Fase | Duración | Costo Estimado |
|---|---|---|
| Preparación | 30 min | Solo tiempo (infraestructura ya up) |
| Ejercicio Multi-AZ (Fase 1) | 30-45 min | Incluido en uptime normal |
| Ejercicio Multi-Región (Fase 2) | 60-90 min | ~$2-5 USD extra por NAT/ALB secundario |
| Análisis post-mortem | 30-60 min | Solo tiempo |

---

## 🔧 SECCIÓN 1: Pre-requisitos (Checklist pre-GameDay)

```bash
# [FASE 1] Verificar que ambas AZs tienen tasks saludables
aws ecs describe-tasks \
  --cluster <ECS_CLUSTER_NAME> \
  --tasks $(aws ecs list-tasks --cluster <ECS_CLUSTER_NAME> --query 'taskArns[]' --output text) \
  --query 'tasks[*].{id:taskArn,az:availabilityZone,status:lastStatus}' \
  --output table

# [FASE 1] Verificar que el ALB tiene targets saludables en 2+ AZs
aws elbv2 describe-target-health \
  --target-group-arn <TARGET_GROUP_ARN> \
  --query 'TargetHealthDescriptions[*].{target:Target.Id,az:Target.AvailabilityZone,health:TargetHealth.State}' \
  --output table

# [FASE 2] Verificar resolución DNS apunta al primario
dig +short <API_DOMAIN>
# Esperado: IP del ALB primario (us-east-1)

# Verificar que check.sh funciona como baseline
./scripts/check.sh
```

---

## 🔴 SECCIÓN 2: Simular Caída de Instancia/Task (Fase 1)

### Paso 2.1: Identificar una task objetivo

```bash
# Listar tasks con su AZ
TASK_ARN=$(aws ecs list-tasks \
  --cluster <ECS_CLUSTER_NAME> \
  --query 'taskArns[0]' \
  --output text)

echo "Task objetivo: $TASK_ARN"
```

### Paso 2.2: Forzar el fallo (bajar 1 task)

```bash
# [SEGURO] Detener 1 task. ECS la reemplaza automáticamente (desired_count se mantiene).
aws ecs stop-task \
  --cluster <ECS_CLUSTER_NAME> \
  --task "$TASK_ARN" \
  --reason "GameDay: simulación de fallo de instancia"

echo "⏱️ Iniciando cronómetro de RTO..."
START_TIME=$(date +%s)
```

### Paso 2.3: Observar el Health Check

```bash
# Observar en tiempo real cómo el ALB marca el target como UNHEALTHY
watch -n 5 'aws elbv2 describe-target-health \
  --target-group-arn <TARGET_GROUP_ARN> \
  --query "TargetHealthDescriptions[*].{id:Target.Id,health:TargetHealth.State,reason:TargetHealth.Reason}" \
  --output table'
```

**Qué mirar**: El target de la task detenida pasa de `healthy` → `draining` → `unhealthy`.

### Paso 2.4: Verificar que el cliente NO siente el fallo

```bash
# En otra terminal, el observer ejecuta continuamente:
./scripts/check.sh --continuous
# Esperado: No se interrumpe ninguna request (0 errores en log)
```

### Paso 2.5: Medir RTO real

```bash
END_TIME=$(date +%s)
RTO=$((END_TIME - START_TIME))
echo "✅ RTO medido: ${RTO} segundos"
echo "🎯 RTO objetivo (Fase 1): < 30 segundos"

# ECS debe estar reemplazando la task. Verificar:
aws ecs list-tasks --cluster <ECS_CLUSTER_NAME> --query 'taskArns | length(@)'
# Debe volver al desired_count en < 2 minutos
```

---

## 🔴 SECCIÓN 3: Simular Caída de AZ Completa (Fase 1 avanzado)

### Paso 3.1: Enfoque de simulación (sin romper la infraestructura)

> ⚠️ No se puede "apagar" una AZ de AWS. La simulación se hace a nivel de Security Groups o
> modificando el Target Group para excluir los targets de una AZ específica.

```bash
# Opción A: Forzar 5xx en todos los tasks de una AZ
# (Requiere endpoint de control en la app: POST /admin/simulate-failure)
# curl -X POST http://<TASK_IP_AZ_A>:3000/admin/simulate-failure
# Esto activa returns de HTTP 503 en el /healthz de esa AZ

# Opción B: Desregistrar targets de la AZ objetivo del Target Group
aws elbv2 deregister-targets \
  --target-group-arn <TARGET_GROUP_ARN> \
  --targets Id=<INSTANCE_ID_AZ_A>

# El ALB deja de enviar tráfico a esa AZ automáticamente
```

### Paso 3.2: Observación de métricas en CloudWatch

**Métricas a observar** durante el ejercicio:

| Métrica | Namespace | Umbral de Alarma |
|---|---|---|
| `UnHealthyHostCount` | `AWS/ApplicationELB` | > 0 → WARNING |
| `HTTPCode_Target_5XX_Count` | `AWS/ApplicationELB` | > 0 → WARNING |
| `TargetResponseTime` | `AWS/ApplicationELB` | > 2s → WARNING |
| `RequestCount` | `AWS/ApplicationELB` | Validar que no cae a 0 |

```bash
# Ver métricas en tiempo real (último minuto)
aws cloudwatch get-metric-statistics \
  --namespace AWS/ApplicationELB \
  --metric-name UnHealthyHostCount \
  --dimensions Name=LoadBalancer,Value=<ALB_ARN_SUFFIX> \
  --start-time $(date -u -d '5 minutes ago' +%Y-%m-%dT%H:%M:%SZ) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%SZ) \
  --period 60 \
  --statistics Maximum \
  --output table
```

---

## 🌎 SECCIÓN 4: Simular Caída Regional (Fase 2)

### Paso 4.1: Forzar failure del Health Check primario en Route 53

```bash
# Opción más segura: Modificar el Health Check para que falle
# (sin tocar la infraestructura real de us-east-1)

# Ver el ID del Health Check del ALB primario
HC_ID=$(aws route53 list-health-checks \
  --query 'HealthChecks[?HealthCheckConfig.FullyQualifiedDomainName==`<ALB_PRIMARY_DNS>`].Id' \
  --output text)

echo "📋 Health Check ID: $HC_ID"

# Alternativa más directa: bajar todos los tasks del ECS primario
aws ecs update-service \
  --cluster <ECS_CLUSTER_PRIMARY> \
  --service <SERVICE_NAME> \
  --desired-count 0

echo "⏱️ Iniciando cronómetro de failover regional..."
START_TIME=$(date +%s)
```

### Paso 4.2: Observar el cambio de DNS (failover automático)

```bash
# Observar el cambio de resolución DNS cada 10 segundos
watch -n 10 'dig +short <API_DOMAIN>; echo "---"; date'

# Qué mirar:
# - Inicialmente: IP del ALB primario (us-east-1)
# - Después de ~60-120 segundos: IP del ALB secundario (us-west-2)
# El cambio confirma que Route 53 completó el failover
```

### Paso 4.3: Verificar respuesta desde la región secundaria

```bash
# Verificar que el endpoint responde desde us-west-2
curl -v https://<API_DOMAIN>/healthz 2>&1 | grep -E "region|az|status|HTTP"
# Esperado: {"status":"healthy","region":"us-west-2"}

# Medir el RTO real
end_time=$(date +%s)
echo "✅ RTO regional medido: $((end_time - START_TIME)) segundos"
echo "🎯 RTO objetivo (Fase 2): < 120 segundos"
```

**Qué mirar en logs/métricas**:

- CloudWatch → ALB Primario: `UnHealthyHostCount` = cantidad de tasks = targets totales.
- Route 53 → Health Checks: Estado del HC primario cambia a "Unhealthy".
- Route 53 → Hosted Zone: Registro Failover activa el secundario.
- CloudWatch → ALB Secundario: `RequestCount` sube (tráfico empezó a llegar).

---

## 🟢 SECCIÓN 5: Failback Controlado (Fase 2)

> **Regla de oro**: El failback siempre es **MANUAL Y CONTROLADO**. Nunca automático sin validación.

### Paso 5.1: Restaurar el servicio primario

```bash
# Restaurar ECS Service primario a desired_count original
aws ecs update-service \
  --cluster <ECS_CLUSTER_PRIMARY> \
  --service <SERVICE_NAME> \
  --desired-count 2

echo "⏳ Esperando tasks saludables en us-east-1..."

# Esperar hasta que los targets vuelvan a estar healthy en el ALB primario
aws elbv2 wait target-in-service \
  --target-group-arn <TARGET_GROUP_PRIMARY_ARN>

echo "✅ ALB Primario restaurado"
```

### Paso 5.2: Validar que el primario responde correctamente

```bash
# Validar endpoint directo del ALB primario (bypass DNS)
curl -f http://<ALB_PRIMARY_DNS>/healthz
# Esperado: {"status":"healthy","region":"us-east-1"}

# Esperar que Route 53 Health Check vuelva a verde (hasta 60s)
aws route53 get-health-check-status \
  --health-check-id $HC_ID \
  --query 'HealthCheckObservations[*].{region:Region,status:StatusReport.Status}' \
  --output table
```

### Paso 5.3: Confirmar retorno del DNS al primario

```bash
# Route 53 debe conmutar automáticamente de vuelta al primario
watch -n 10 'dig +short <API_DOMAIN>'
# El IP debe volver a apuntar al ALB de us-east-1

echo "✅ Failback completado. Sistema restaurado al estado normal."
```

---

## 📝 SECCIÓN 6: Post-GameDay Checklist

```markdown
## Checklist Post-Mortem GameDay — Caso M

**Fecha**: ___________  **Duración Total**: ___________

### Métricas Medidas

| Escenario | RTO Medido | RTO Objetivo | ✅/❌ |
|---|---|---|---|
| Caída de instancia (Fase 1) | ___ seg | < 30 seg | |
| Caída de AZ (Fase 1 adv.) | ___ seg | < 60 seg | |
| Caída de región (Fase 2) | ___ seg | < 120 seg | |
| Failback (Fase 2) | ___ seg | < 300 seg | |

### Hallazgos

- ¿Se detectaron SPOFs no previstos?
- ¿El cliente (observer) experimentó algún error?
- ¿Las alarmas CloudWatch se dispararon en tiempo?
- ¿El DNS TTL fue suficientemente bajo?

### Acciones de Mejora

- [ ] Acción 1: ___________
- [ ] Acción 2: ___________

**Firma Incident Commander**: ___________
```

---

## 🔗 Referencias

- [Arquitectura Objetivo](./architecture.md)
- [Roadmap por Fases](./roadmap.md)
- [Scripts de Simulación](../scripts/)
- [AWS Fault Injection Simulator (FIS)](https://docs.aws.amazon.com/fis/latest/userguide/what-is.html) — alternativa en Fase 3
