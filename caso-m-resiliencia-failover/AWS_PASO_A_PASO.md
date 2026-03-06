# ☁️ Guía de Ingeniería: Caso M (Resiliencia & Failover)

> **ESTADO ACTUAL: Fase 0 — Scaffold y Documentación**
> Esta guía documenta los pasos completos de implementación para cuando se ejecuten las
> Fases 1-3. En Fase 0 **no se requieren credenciales ni recursos AWS**.

---

## 🎯 Qué Construirás

Al completar esta guía tendrás:

- **Fase 1**: Aplicación corriendo con ALB multi-AZ en `us-east-1` sin downtime ante caídas.
- **Fase 2**: Failover automático regional hacia `us-west-2` en < 120 segundos.
- **Fase 3** *(opcional)*: Automatización de GameDay y Global Accelerator.

---

## ⚠️ Advertencia de Costos (Leer antes de iniciar Fase 1)

> [!CAUTION]
> Esta arquitectura **sí genera cargos en AWS**. Estrategia recomendada: **Deploy → Valida → Destroy**.
> Duración estimada de cada sesión: 2-4 horas. Costo aproximado por sesión: **$2-5 USD**.
>
> Recursos con mayor impacto:
>
> - ALB: ~$0.022/hora
> - NAT Gateway: ~$0.045/hora + datos
> - ECS Fargate: ~$0.01-0.04/hora por task
>
> Antes de empezar: verifica que tienes una alerta activa en **AWS Budgets** (Caso L).

---

## 🪜 Fase 0: Validación Local (Sin AWS — Activa Ahora)

Puedes ejecutar estos pasos **sin credenciales AWS** para validar que el código Terraform es correcto.

### Paso 0.1: Inicializar Terraform (backend local)

```bash
cd caso-m-resiliencia-failover/infra/terraform
terraform init
```

Esperado: `Terraform has been successfully initialized!`

### Paso 0.2: Validar formato

```bash
terraform fmt -check -recursive
```

Si hay diferencias de formato: `terraform fmt -recursive` las corrige automáticamente.

### Paso 0.3: Validar sintaxis

```bash
terraform validate
```

Esperado: `Success! The configuration is valid.`

### Paso 0.4: Ver output de diagnóstico (sin AWS)

```bash
# No requiere credenciales porque el output `current_config` siempre está activo
terraform output current_config
```

---

## 🪜 Fase 1: Multi-AZ en Región Única (`us-east-1`)

> [!IMPORTANT]
> Antes de iniciar la Fase 1, necesitas:
>
> - Cuenta AWS activa con permisos sobre: ALB, ECS, ECR, VPC, IAM.
> - Credenciales configuradas (ver sección "Configurar credenciales" más abajo).
> - Imagen Docker disponible (puedes reutilizar la del Caso J o usar `nginx:alpine` como placeholder).

### Paso 1.1: Configurar credenciales AWS

**Opción A — Perfil local (recomendado para desarrollo)**:

```bash
aws configure --profile case-m-lab
# AWS Access Key ID: AKIA...
# AWS Secret Access Key: ...
# Default region: us-east-1
# Default output format: json

export AWS_PROFILE=case-m-lab
```

**Opción B — Variables de entorno (CI/CD)**:

```bash
export AWS_ACCESS_KEY_ID="..."
export AWS_SECRET_ACCESS_KEY="..."
export AWS_DEFAULT_REGION="us-east-1"
```

**Opción C — OIDC via GitLab (recomendada para pipeline, hereda config del Caso L)**:

Las variables `AWS_ROLE_ARN` y `GITLAB_OIDC_TOKEN` ya están configuradas en el proyecto.
El job CI `case_m_validate` no las requiere, pero el `plan` en Fase 1 sí.

### Paso 1.2: Completar módulos Terraform

Abre `infra/terraform/main.tf` y descomenta el bloque `module "alb_primary"` y
`module "ecs_service_primary"`. Sigue los comentarios en el archivo.

Crea el archivo de variables de entorno:

```bash
cat > caso-m-resiliencia-failover/infra/terraform/envs/lab.tfvars << 'EOF'
primary_region          = "us-east-1"
environment             = "lab"
app_name                = "caso-m-app"
desired_count           = 2
container_image         = "public.ecr.aws/nginx/nginx:alpine"
health_check_path       = "/healthz"
enable_secondary_region = false
EOF
```

### Paso 1.3: Revisar el plan (sin aplicar)

```bash
cd caso-m-resiliencia-failover/infra/terraform
terraform init
terraform plan -var-file=envs/lab.tfvars -out=tfplan-phase1.bin
```

> **Revisa el plan cuidadosamente** antes de continuar. Busca el conteo de
> `Plan: X to add, 0 to change, 0 to destroy`.

### Paso 1.4: Aplicar la infraestructura

```bash
terraform apply tfplan-phase1.bin
```

Guarda los outputs que aparecen al final:

```
alb_primary_dns       = "caso-m-app-primary-xxxx.us-east-1.elb.amazonaws.com"
ecs_cluster_primary   = "caso-m-app-cluster"
ecs_service_primary   = "caso-m-app-service"
```

### Paso 1.5: Verificar que el endpoint responde

```bash
# Reemplaza con el DNS real del output anterior
export ALB_DNS="caso-m-app-primary-xxxx.us-east-1.elb.amazonaws.com"

curl -f http://$ALB_DNS/healthz
# Esperado: {"status":"healthy","region":"us-east-1","az":"us-east-1a"}
```

### Paso 1.6: Verificar distribución Multi-AZ

```bash
# Hacer 10 requests y observar que responden desde distintas AZs
for i in {1..10}; do
  curl -s http://$ALB_DNS/healthz | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('az','?'))"
done
# Esperado: alternancia entre us-east-1a, us-east-1b, us-east-1c
```

### Paso 1.7: GameDay Multi-AZ — Simular fallo de instancia

```bash
export ECS_CLUSTER="caso-m-app-cluster"
export ECS_SERVICE="caso-m-app-service"
export ENDPOINT="http://$ALB_DNS/healthz"

# En una terminal: monitoreo continuo (cliente / observer)
./caso-m-resiliencia-failover/scripts/check.sh --continuous --endpoint $ENDPOINT

# En otra terminal: simular la caída
export ECS_CLUSTER="caso-m-app-cluster"
./caso-m-resiliencia-failover/scripts/drill-failover.sh --mode task
# (Cuando esté activo en Fase 1: quita el modo dry-run del script)
```

**Qué observar**:

- El script de monitoreo NO debe mostrar errores durante la caída.
- CloudWatch → ALB → `UnHealthyHostCount` debe subir a 1 por ~30s y luego volver a 0.
- ECS reemplaza el task en < 2 minutos.

### Paso 1.8: 🚨 Destruir la infraestructura (obligatorio)

```bash
cd caso-m-resiliencia-failover/infra/terraform
terraform destroy -var-file=envs/lab.tfvars
```

Confirma con `yes`. Verifica que el output diga `Destroy complete! Resources: X destroyed.`

---

## 🪜 Fase 2: Multi-Región + Route 53 Failover

> [!IMPORTANT]
> Requisitos adicionales para Fase 2:
>
> - Dominio registrado en Route 53 (o transferido a Route 53).
> - `Hosted Zone ID` de ese dominio.
> - Fase 1 completada y documentada.

### Paso 2.1: Habilitar la región secundaria en variables

```bash
# Editar envs/lab.tfvars
enable_secondary_region = true
route53_zone_id         = "Z1234567890ABCD"  # Tu Hosted Zone ID real
api_domain              = "api.tudominio.com"
```

### Paso 2.2: Descomentar módulo Route 53 en `main.tf`

Abre `infra/terraform/main.tf` y descomenta el bloque `module "route53_failover"`.

### Paso 2.3: Aplicar infraestructura completa (2 regiones)

```bash
terraform plan -var-file=envs/lab.tfvars -out=tfplan-phase2.bin
terraform apply tfplan-phase2.bin
```

Nuevos outputs:

```
api_endpoint              = "https://api.tudominio.com"
route53_health_check_id   = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
alb_secondary_dns         = "caso-m-app-secondary-xxxx.us-west-2.elb.amazonaws.com"
```

### Paso 2.4: Verificar resolución DNS

```bash
# Verificar que el DNS apunta al primario
dig +short api.tudominio.com
# Esperado: IP del ALB en us-east-1

# Consultar desde distintos resolvers
dig +short api.tudominio.com @8.8.8.8
dig +short api.tudominio.com @1.1.1.1
```

### Paso 2.5: GameDay Multi-Región — Simular caída regional

```bash
# Forzar caída del servicio primario
export ECS_CLUSTER_PRIMARY="caso-m-app-cluster"
./caso-m-resiliencia-failover/scripts/drill-failover.sh --mode regional

# En otra terminal: observar el cambio de DNS (puede tardar 60-120s)
watch -n 5 'dig +short api.tudominio.com'
# Se verá el IP cambiando de us-east-1 a us-west-2
```

**Qué mirar en AWS Console**:

1. **Route 53** → Health Checks → Estado del HC primario cambia a `Unhealthy`.
2. **Route 53** → Hosted Zones → Record del Failover activa el secundario.
3. **CloudWatch** → ALB secundario → `RequestCount` sube (tráfico llegando).
4. **CloudWatch** → ALB primario → `RequestCount` cae a 0.

### Paso 2.6: Failback controlado

```bash
./caso-m-resiliencia-failover/scripts/drill-failback.sh

# Verificar retorno del DNS al primario (~60s después)
watch -n 5 'dig +short api.tudominio.com'
```

### Paso 2.7: 🚨 Destruir (obligatorio)

```bash
terraform destroy -var-file=envs/lab.tfvars
```

---

## 🪜 Fase 3: Automatización + Observabilidad (Opcional)

Esta fase se planifica cuando las Fases 1 y 2 estén documentadas con resultados reales.
Ver el [Roadmap Detallado](./docs/roadmap.md) para la lista de tareas.

Considera en esta fase:

- **AWS Fault Injection Simulator (FIS)**: tests de caos más realistas que los scripts manuales.
- **Global Accelerator**: alternativa a Route 53 con RTO < 30s (sin depender de TTL DNS).
- **CloudWatch Dashboard**: métricas de failover en tiempo real.

---

## 🧹 Limpieza y Verificación Post-GameDay

Después de cada sesión, verifica que no quedan recursos huérfanos:

```bash
# Verificar que no hay ALBs activos
aws elbv2 describe-load-balancers \
  --query 'LoadBalancers[?contains(LoadBalancerName, `caso-m`)].{name:LoadBalancerName,state:State.Code}' \
  --output table

# Verificar que no hay ECS clusters activos con tasks
aws ecs list-clusters --query 'clusterArns[?contains(@, `caso-m`)]'

# Verificar en la segunda región también
aws elbv2 describe-load-balancers --region us-west-2 \
  --query 'LoadBalancers[?contains(LoadBalancerName, `caso-m`)].LoadBalancerName' \
  --output table
```

---

## 🔗 Referencias y Siguientes Pasos

- 🏗️ [Arquitectura Objetivo](./docs/architecture.md)
- 📋 [Runbook Completo de Failover](./docs/runbook-failover.md)
- 🗺️ [Roadmap por Fases](./docs/roadmap.md)
- ⬅️ [Regresar al README Principal](../README.md)

---

_Guía preparada por Vladimir Acuña — Staff Platform Engineer / SRE._
_Última actualización: 2026-03-05_
