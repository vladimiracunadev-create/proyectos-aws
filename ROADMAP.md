# Roadmap — GitHub Actions Journey (AWS Monorepo)

Evolución trimestral de los 11 casos. Cada caso introduce un servicio AWS nuevo
**y** una capacidad de GitHub Actions que no existía en el caso anterior.

> Estado global: **2/11 casos completados** — Fase 1 terminada.

---

## Fase 1 — Fundamentos (Q1 2026) ✅

### Caso 01: AWS Amplify Hosting
- [x] Sitio PWA completo desplegado en Amplify Console
- [x] Multi-branch deploy: `main` y `dev` con URLs independientes
- [x] SSL automático (ACM), CDN de Amplify
- [x] Service Worker, Web App Manifest, offline fallback
- [x] i18n en 6 idiomas (ES, EN, FR, IT, PT, ZH)
- [x] Static JSON API (`/api/v1/`)
- [x] 30+ PDFs × 6 idiomas (Python reportlab)
- [x] Three.js 3D experience

**Capacidad GitHub Actions demostrada:** Deploy delegado a Amplify (trigger por push sin workflow YAML).

---

### Caso 02: S3 + GitHub Actions Deploy
- [x] S3 Static Website Hosting activo
- [x] Workflow `despliegue.yml` con `paths` filter
- [x] `workflow_dispatch` para deploy manual
- [x] `aws s3 sync --delete` (limpieza automática del bucket)

**Capacidad GitHub Actions demostrada:** Primer workflow YAML real. Pipeline controlado desde GitHub, no desde AWS.

---

## Fase 2 — Seguridad de Identidad (Q2 2026) 🔜

### Caso 03: S3 + CloudFront + OIDC
**Carpeta:** `caso-03-cloudfront-oidc/`

**Objetivo:** Eliminar credenciales estáticas del pipeline. Introducir CDN sobre S3.

- [ ] Configurar OIDC trust policy en el rol IAM (`sts:AssumeRoleWithWebIdentity`)
- [ ] Reemplazar `AWS_ACCESS_KEY_ID` por `id-token: write` + `role-to-assume`
- [ ] Crear distribución CloudFront sobre el bucket S3
- [ ] Añadir step de invalidación de caché post-deploy (`aws cloudfront create-invalidation`)
- [ ] Documentar en `caso-03-cloudfront-oidc/README.md`

**Capacidad GitHub Actions demostrada:** OIDC federation, workflow sin secrets de larga duración.

**Criterio de éxito:** El workflow no tiene ningún secret de AWS. El token es emitido por GitHub y validado por AWS STS en tiempo de ejecución.

---

### Caso 04: GitHub Environments con Aprobaciones
**Carpeta:** `caso-04-environments-approvals/`

**Objetivo:** Gobierno del pipeline. Staging despliega automático; producción requiere aprobación manual.

- [ ] Configurar entornos `staging` y `production` en GitHub Settings
- [ ] `required_reviewers` en el environment `production`
- [ ] Secrets por entorno (distintos buckets staging vs prod)
- [ ] Etiqueta visual en el DOM: "ENV: STAGING" / "ENV: PRODUCTION"
- [ ] Documentar diferencia entre repository secrets y environment secrets

**Capacidad GitHub Actions demostrada:** `environment:` keyword, deployment gates, secrets por scope.

**Criterio de éxito:** Un push a `main` despliega automáticamente a staging. Para llegar a prod, un reviewer debe aprobar en la UI de GitHub.

---

## Fase 3 — Serverless & Testing (Q2-Q3 2026) 🔜

### Caso 05: Lambda + API Gateway
**Carpeta:** `caso-05-lambda-api-gateway/`

**Objetivo:** Primer backend real. Pipeline multi-job con tests antes del deploy.

- [ ] Lambda Python/Node.js expuesta via API Gateway (SAM)
- [ ] Workflow con 3 jobs: `test` → `build` → `deploy`
- [ ] `needs:` entre jobs (secuenciación explícita)
- [ ] `actions/upload-artifact` / `download-artifact` para pasar el artefacto SAM entre jobs
- [ ] `workflow_dispatch` con `inputs` para elegir entorno

**Capacidad GitHub Actions demostrada:** Multi-job workflows, artifacts, job dependencies.

**Criterio de éxito:** El deploy nunca ocurre si los tests fallan. El artefacto de build es el mismo que pasa a producción.

---

### Caso 06: DynamoDB + Matrix Builds
**Carpeta:** `caso-06-dynamodb-matrix/`

**Objetivo:** Persistencia real. Probar la misma Lambda en múltiples runtimes y regiones simultáneamente.

- [ ] Lambda con acceso a DynamoDB (CRUD básico)
- [ ] Matrix strategy: runtimes `[python3.11, python3.12]`
- [ ] Matrix strategy: regiones `[us-east-1, us-east-2]`
- [ ] `fail-fast: false` para no cancelar toda la matrix ante un fallo
- [ ] Reporte de resultados por matrix cell

**Capacidad GitHub Actions demostrada:** `strategy.matrix`, `fail-fast`, parallel jobs.

**Criterio de éxito:** El pipeline ejecuta 4 combinaciones en paralelo y reporta cuáles pasaron y cuáles fallaron individualmente.

---

## Fase 4 — Plataforma GitHub (Q3 2026) 🔜

### Caso 07: Reusable Workflows + Composite Actions
**Carpeta:** `caso-07-reusable-workflows/`

**Objetivo:** Eliminar duplicación entre casos. Extraer patrones comunes a librerías internas.

- [ ] Reusable workflow: `.github/workflows/deploy-s3-oidc.yml` (callable)
- [ ] Composite action: `.github/actions/setup-aws-oidc/action.yml`
- [ ] Refactorizar casos 03-06 para usar los reusables
- [ ] Demostrar llamada con `uses: ./.github/workflows/deploy-s3-oidc.yml@main`
- [ ] Documentar diferencia: reusable workflow vs composite action vs regular step

**Capacidad GitHub Actions demostrada:** `workflow_call`, composite actions, DRY en pipelines.

---

### Caso 08: Containers + GitHub Container Registry (GHCR)
**Carpeta:** `caso-08-containers-ghcr/`

**Objetivo:** Containerizar una aplicación, publicarla en GHCR y desplegarla en ECS Fargate.

- [ ] Dockerfile para la app del Caso 05 (Lambda → container)
- [ ] Build y push a GHCR (`ghcr.io/vladimiracunadev-create/...`)
- [ ] Deploy a ECS Fargate (task definition actualizada via Actions)
- [ ] Multi-platform build: `linux/amd64` + `linux/arm64`
- [ ] Semantic versioning automático de la imagen (tag por SHA + semver)

**Capacidad GitHub Actions demostrada:** GHCR nativo, `docker/build-push-action`, multi-platform.

**Criterio de éxito:** La imagen publicada en GHCR está disponible públicamente con las mismas credenciales del repositorio. Sin ECR externo.

---

## Fase 5 — Gobernanza & Resiliencia (Q4 2026) 🔜

### Caso 09: FinOps + Scheduled Workflows
**Carpeta:** `caso-09-finops-scheduled/`

**Objetivo:** Visibilidad de costos automatizada. Workflow programado que extrae datos de Cost Explorer y los versiona en el repositorio.

- [ ] Workflow `cron: '0 8 1 * *'` (primer día del mes)
- [ ] Script Python que llama a `ce:GetCostAndUsage` via OIDC
- [ ] Genera `docs/FINOPS_COSTOS.md` con datos reales y lo commitea
- [ ] Badge de costo mensual en README
- [ ] AWS Budgets con alertas a email/Slack

**Capacidad GitHub Actions demostrada:** `schedule` trigger, workflow que commitea al repo, integración con herramientas de reporting.

---

### Caso 10: Multi-región + Disaster Recovery
**Carpeta:** `caso-10-multiregion-dr/`

**Objetivo:** Alta disponibilidad geográfica. Failover automático con Route53 y smoke tests validando cada región antes de actualizar DNS.

- [ ] Deploy paralelo a `us-east-1` y `eu-west-1` via matrix
- [ ] Smoke tests post-deploy por región (curl + assertions)
- [ ] Route53 health checks + failover routing policy
- [ ] Rollback automático si los smoke tests fallan

**Capacidad GitHub Actions demostrada:** Matrix + smoke tests + rollback condicional.

---

### Caso 11: EKS + GitOps con GitHub Actions
**Carpeta:** `caso-11-eks-gitops/`

**Objetivo:** GitOps sobre Kubernetes. Cambios en manifiestos K8s en este repositorio disparan reconciliación sobre EKS.

- [ ] Cluster EKS vía Terraform (reutiliza el Caso K del repo GitLab)
- [ ] Manifiestos K8s en `caso-11-eks-gitops/k8s/`
- [ ] GitHub Actions como controlador GitOps (en lugar de ArgoCD)
- [ ] `kubectl apply` autenticado con OIDC (no kubeconfig estático)
- [ ] Progresive delivery: canary deploy manual con `workflow_dispatch`

**Capacidad GitHub Actions demostrada:** GitOps pattern, K8s nativo desde Actions, OIDC para K8s API.

---

## Resumen de capacidades por fase

| Fase | Casos | Capacidades GitHub Actions |
|:---|:---|:---|
| Fundamentos | 01-02 | Trigger básico, S3 sync, paths filter |
| Identidad | 03-04 | OIDC, Environments, required reviewers |
| Serverless | 05-06 | Multi-job, artifacts, matrix strategy |
| Plataforma | 07-08 | Reusable workflows, GHCR, composite actions |
| Gobernanza | 09-11 | Scheduled, GitOps, multi-region, rollback |

---

## Gestión

- Todo cambio parte de `dev` → PR → `main`
- Cada caso nuevo necesita: carpeta propia + README + workflow actualizado
- Criterios de éxito definidos antes de empezar cada caso
- Costos documentados en `docs/FINOPS_COSTOS.md` al completar cada caso
