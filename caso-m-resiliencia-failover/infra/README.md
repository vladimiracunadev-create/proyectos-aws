# 🔧 Infraestructura: Caso M (Resiliencia & Failover)

> **IMPORTANTE**: Esta carpeta contiene **plantillas skeleton** de Terraform.
> En Fase 0 (actual), **NO se ejecuta `terraform apply`**.
>
> Comandos **permitidos** en esta fase:
>
> - `terraform fmt` — Formateo de código (sin conexión AWS).
> - `terraform validate` — Validación de sintaxis (sin conexión AWS).
> - `terraform plan` — Ver cambios planeados (requiere credenciales, se hace en Fase 1+).
>
> Comandos **NO recomendados como camino principal**:
>
> - `terraform apply` — Solo cuando la Fase 1 esté formalmente aprobada e iniciada.

---

## 📂 Estructura

```
infra/
└── terraform/
    ├── main.tf            # Providers y configuración raíz
    ├── variables.tf       # Variables configurables (región, entorno, etc.)
    ├── outputs.tf         # Outputs útiles (DNS del ALB, ARN del TG, etc.)
    ├── backend.tf         # Backend LOCAL por defecto (sin S3/DynamoDB en Fase 0)
    └── modules/
        ├── alb/           # ALB + Target Group + Health Check
        ├── ecs-service/   # ECS Service Multi-AZ
        └── route53-failover/  # Route 53 Failover Routing (Fase 2+)
```

---

## 🚀 Inicio Rápido (Fase 0 — Solo validación local)

```bash
cd caso-m-resiliencia-failover/infra/terraform

# 1. Inicializar con backend local
terraform init

# 2. Verificar formato (sin AWS)
terraform fmt -check -recursive

# 3. Validar sintaxis (sin AWS)
terraform validate

# 4. [FUTURO — Fase 1] Ver plan de cambios (requiere credenciales)
# export AWS_PROFILE=case-m-lab
# terraform plan -var-file=envs/lab.tfvars
```

---

## ⚙️ Variables Principales

Ver [`variables.tf`](./terraform/variables.tf) para la lista completa.

Las más importantes:

| Variable | Default | Descripción |
|---|---|---|
| `primary_region` | `us-east-1` | Región AWS primaria |
| `secondary_region` | `us-west-2` | Región AWS secundaria (Fase 2) |
| `environment` | `lab` | Nombre del entorno (`lab`/`staging`/`prod`) |
| `app_name` | `caso-m-app` | Nombre de la aplicación |
| `desired_count` | `2` | Número de tasks ECS (mínimo 2 para Multi-AZ) |
| `enable_secondary_region` | `false` | Activar Fase 2 (Multi-Región) |
| `route53_zone_id` | `""` | ID de la Hosted Zone (requerido en Fase 2) |

---

## 💰 Nota de Costos

Este módulo **no genera costos hasta que se ejecute `terraform apply`**.

Activar solo los módulos necesarios con la variable `enable_secondary_region = false` hasta que
la Fase 2 esté formalmente iniciada.

Antes de dejar estos recursos corriendo sin supervisión, configura una Alerta de Presupuesto
en AWS Budgets (ya disponible en Caso L del repo).
