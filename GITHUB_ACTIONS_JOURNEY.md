# GitHub Actions Journey — Evolución del Pipeline como Plataforma

> **Repositorio complementario:** [proyectos-aws-gitlab](https://gitlab.com/vladimir.acuna.dev-group/proyectos-aws-gitlab)
> — Mientras GitLab documenta el viaje por servicios AWS,
> este repositorio documenta el dominio de **GitHub Actions como plataforma de ingeniería**.

---

## Por qué este repositorio existe

Cuando comencé a aprender cloud en 2025, creé este repositorio con las dos primeras implementaciones AWS que hice: un sitio en Amplify y el mismo sitio en S3 con un workflow básico de GitHub Actions.

Más adelante construí un ecosistema maduro en GitLab ([proyectos-aws-gitlab](https://gitlab.com/vladimir.acuna.dev-group/proyectos-aws-gitlab)) con 11 casos de estudio progresivos, Terraform, OIDC, FinOps y observabilidad. Naturalmente pensé en eliminar este repositorio de GitHub.

Pero ambos tienen razón de existir por un motivo concreto: **son plataformas distintas con ecosistemas genuinamente diferentes.**

| Dimensión | GitLab (`proyectos-aws-gitlab`) | GitHub (`proyectos-aws`) |
|:---|:---|:---|
| **Enfoque** | Viaje por servicios AWS (A→L) | GitHub Actions como plataforma |
| **CI/CD nativo** | GitLab CI (5 etapas, OIDC incluido) | GitHub Actions (Marketplace, Environments) |
| **IaC** | Terraform en cada caso | Casos progresivos con IaC incremental |
| **Ecosistema único** | GitLab Pages, Variables, Runners | GHCR, Dependabot, Security tab, Codespaces |
| **Complementariedad** | Qué AWS puede hacer | Cómo GitHub puede orquestar AWS |

Este repositorio responde a la pregunta: **¿Qué puede hacer GitHub Actions que no se puede demostrar en GitLab?**

---

## Mapa de la Jornada (11 Casos)

```
NIVEL 1 — FUNDAMENTOS (GitHub Actions básico)
  Caso 01 │ Amplify Hosting         │ ✅ Completado
  Caso 02 │ S3 + Actions Deploy     │ ✅ Completado

NIVEL 2 — SEGURIDAD DE IDENTIDAD (OIDC)
  Caso 03 │ S3 + CloudFront + OIDC  │ 🔜 Q2 2026
  Caso 04 │ Environments + Approvals│ 🔜 Q2 2026

NIVEL 3 — SERVERLESS & TESTING (Workflows avanzados)
  Caso 05 │ Lambda + API Gateway    │ 🔜 Q2-Q3 2026
  Caso 06 │ DynamoDB + Matrix Builds│ 🔜 Q3 2026

NIVEL 4 — PLATAFORMA GITHUB (Ecosistema completo)
  Caso 07 │ Reusable Workflows      │ 🔜 Q3 2026
  Caso 08 │ Containers + GHCR       │ 🔜 Q3 2026

NIVEL 5 — GOBERNANZA & RESILIENCIA (Enterprise patterns)
  Caso 09 │ FinOps + Scheduled Jobs │ 🔜 Q4 2026
  Caso 10 │ Multi-región + DR       │ 🔜 Q4 2026
  Caso 11 │ EKS + GitOps            │ 🔜 Q4 2026
```

---

## Progresión detallada

### Nivel 1 — Fundamentos

#### Caso 01: AWS Amplify Hosting
**Carpeta:** `caso-01-amplify-hosting/`

El primer contacto real con AWS. Amplify Console gestiona el pipeline internamente: detecta el push a GitHub, construye (en este caso sin build) y despliega en URLs con SSL automático por rama.

**Lo que demuestra:** La forma más simple de tener CI/CD en AWS. No requiere configurar nada en GitHub Actions.

**Lo que revela como limitación:** Si Amplify gestiona todo, no tienes control del pipeline desde GitHub. No puedes añadir steps, gates de aprobación, ni integraciones con el ecosistema de Actions.

```
GitHub push → Amplify detecta → Deploy automático
[GitHub Actions no interviene en este caso]
```

---

#### Caso 02: S3 + GitHub Actions Deploy
**Carpeta:** `caso-02-s3-github-actions/`

El primer workflow real de GitHub Actions. Un YAML que escucha cambios en la carpeta del caso y ejecuta `aws s3 sync` con credenciales AWS en secrets.

**Lo que demuestra:** Control explícito del pipeline. El YAML es código versionado, revisable en PR, auditable.

**Lo que revela como deuda técnica:** Credenciales estáticas (`AWS_ACCESS_KEY_ID`) en GitHub Secrets son el patrón antiguo. Son efímeras pero representan un riesgo de exfiltración. OIDC las elimina completamente.

```
GitHub push → Actions workflow → aws s3 sync → S3 bucket
[Credenciales: secrets estáticos ← ⚠️ migrar a OIDC en Caso 03]
```

---

### Nivel 2 — Seguridad de Identidad

#### Caso 03: S3 + CloudFront + OIDC (planificado — Q2 2026)
**Carpeta futura:** `caso-03-cloudfront-oidc/`

**El salto de seguridad más importante del repositorio.** OIDC (OpenID Connect) permite que GitHub Actions asuma un rol IAM sin necesidad de almacenar credenciales. El token se emite por GitHub, AWS lo valida directamente.

```
GitHub push → Actions workflow
    └── GitHub emite JWT OIDC token
        └── AWS STS asume rol IAM (trust policy valida el JWT)
            └── aws s3 sync + CloudFront invalidation
[Sin secretos estáticos en ningún punto]
```

**Nuevas capacidades de GitHub Actions:**
- `id-token: write` permission en el workflow
- `aws-actions/configure-aws-credentials@v4` con `role-to-assume`
- Invalidación de CloudFront como step explícito post-deploy

**Analogía GitLab:** El repositorio de GitLab ya usa OIDC nativamente. Este caso cierra esa brecha en GitHub.

---

#### Caso 04: GitHub Environments con Aprobaciones (planificado — Q2 2026)
**Carpeta futura:** `caso-04-environments-approvals/`

GitHub Environments añaden una capa de gobierno al pipeline: puedes requerir aprobaciones manuales antes de desplegar a producción, definir secrets por entorno y aplicar branch protection rules.

```
Push a dev → Deploy automático a STAGING (sin aprobación)
PR merged a main → Deploy a PROD requiere aprobación manual
    └── Reviewer aprueba en GitHub UI
        └── Deploy a PROD se ejecuta
```

**Capacidades nuevas de GitHub Actions:**
- `environment: production` con `required_reviewers`
- Secrets a nivel de environment (distintos de repository secrets)
- `deployment_status` como trigger de workflows

---

### Nivel 3 — Serverless & Testing

#### Caso 05: Lambda + API Gateway (planificado — Q2-Q3 2026)
**Carpeta futura:** `caso-05-lambda-api-gateway/`

Introduce el primer backend real. Un Lambda en Python/Node.js expuesto via API Gateway, desplegado con SAM desde GitHub Actions.

**Capacidades nuevas de GitHub Actions:**
- `actions/upload-artifact` y `download-artifact` entre jobs
- Workflow con jobs separados: `test → build → deploy`
- `workflow_dispatch` con inputs para seleccionar entorno

---

#### Caso 06: DynamoDB + Matrix Builds (planificado — Q3 2026)
**Carpeta futura:** `caso-06-dynamodb-matrix/`

Persistencia real. Lambda con DynamoDB. El elemento nuevo: matrix strategy para probar el mismo código en múltiples versiones de runtime o múltiples regiones AWS simultáneamente.

```yaml
strategy:
  matrix:
    region: [us-east-1, us-east-2, eu-west-1]
    runtime: [python3.11, python3.12]
```

---

### Nivel 4 — Plataforma GitHub

#### Caso 07: Reusable Workflows + Composite Actions (planificado — Q3 2026)
**Carpeta futura:** `caso-07-reusable-workflows/`

El ecosistema de casos anteriores genera duplicación. Este caso refactoriza: extrae lógica común a reusable workflows (`.github/workflows/`) y composite actions (`.github/actions/`).

```yaml
# En cualquier caso futuro:
jobs:
  deploy:
    uses: ./.github/workflows/deploy-s3-oidc.yml@main
    with:
      bucket: ${{ vars.BUCKET_NAME }}
      environment: production
```

---

#### Caso 08: Containers + GitHub Container Registry (planificado — Q3 2026)
**Carpeta futura:** `caso-08-containers-ghcr/`

Introduce containerización con GitHub Container Registry (GHCR) como registry y ECS Fargate como runtime. El pipeline construye, tagea, publica y despliega la imagen en un solo workflow.

**Ecosistema GitHub único:** GHCR es gratuito para repositorios públicos y está integrado nativamente con el repositorio. No necesitas ECR si el repo ya está en GitHub.

---

### Nivel 5 — Gobernanza & Resiliencia

#### Caso 09: FinOps + Scheduled Workflows (planificado — Q4 2026)
**Carpeta futura:** `caso-09-finops-scheduled/`

Equivalente al stage FinOps del GitLab. Un workflow programado (`cron`) extrae datos de AWS Cost Explorer, genera un reporte Markdown y lo commitea automáticamente al repositorio.

```yaml
on:
  schedule:
    - cron: '0 8 1 * *'  # Primer día del mes, 08:00 UTC
```

---

#### Caso 10: Multi-región + Disaster Recovery (planificado — Q4 2026)
**Carpeta futura:** `caso-10-multiregion-dr/`

Failover entre regiones con Route53 y health checks. El pipeline usa matrix strategy sobre regiones y ejecuta smoke tests post-deploy para validar disponibilidad antes de actualizar DNS.

---

#### Caso 11: EKS + GitOps con GitHub Actions (planificado — Q4 2026)
**Carpeta futura:** `caso-11-eks-gitops/`

El cierre del viaje: GitHub Actions como plataforma GitOps. Cambios en manifiestos Kubernetes (en este repo) disparan reconciliación sobre un cluster EKS. Complementa el Caso K (EKS) del repositorio GitLab.

---

## Relación con el repositorio GitLab

Ambos repositorios documentan el mismo stack AWS pero desde perspectivas complementarias:

```
GitLab (proyectos-aws-gitlab)          GitHub (proyectos-aws)
================================       ================================
Caso A: Amplify hosting            ←→  Caso 01: Amplify + pipeline control
Caso B: S3 + CloudFront            ←→  Casos 02-03: S3, CDN, OIDC
Casos D-F: Lambda, DynamoDB,       ←→  Casos 05-06: Mismo stack,
           API Gateway                            distinto pipeline
Caso H: EventBridge/SQS            ←→  Caso 09: FinOps + scheduled jobs
Casos J-K: ECS, EKS                ←→  Casos 08, 11: Containers, GitOps
Caso L: FinOps                     ←→  Caso 09: Cost reporting automatizado

DIFERENCIA CLAVE:
GitLab → ¿Qué hace cada servicio AWS?
GitHub → ¿Cómo orquesta GitHub Actions ese servicio?
```

---

## Estado de evolución

| Fase | Casos | Estado | Trimestre |
|:---|:---|:---|:---|
| Fundamentos | 01, 02 | ✅ Completados | Q1 2026 |
| Seguridad de Identidad | 03, 04 | 🔜 Planificados | Q2 2026 |
| Serverless & Testing | 05, 06 | 🔜 Planificados | Q2-Q3 2026 |
| Plataforma GitHub | 07, 08 | 🔜 Planificados | Q3 2026 |
| Gobernanza & Resiliencia | 09, 10, 11 | 🔜 Planificados | Q4 2026 |

---

*Este documento es el equivalente de `AWS_CLOUD_JOURNEY.md` del repositorio GitLab,
adaptado al contexto de GitHub Actions como plataforma de ingeniería.*
