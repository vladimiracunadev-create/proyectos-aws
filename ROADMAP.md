# 🗺️ Roadmap — GitHub Actions Journey

> **Q = Quarter (trimestre calendario)**
> Q1 = Enero–Marzo · Q2 = Abril–Junio · Q3 = Julio–Septiembre · Q4 = Octubre–Diciembre
> Ejemplo: **Q2 2026** = Abril a Junio de 2026.

Evolución de los 11 casos. Cada caso introduce un servicio AWS nuevo **y** una capacidad
de GitHub Actions que no existía en el caso anterior.

![Progreso](https://img.shields.io/badge/progreso-2%20de%2011%20casos-brightgreen?style=flat-square)
![Fase actual](https://img.shields.io/badge/fase%20actual-Fase%201%20completada%20✅-success?style=flat-square)
![Próximo](https://img.shields.io/badge/próximo-Caso%2003%20OIDC-orange?style=flat-square)

---

## ✅ Fase 1 — Fundamentos (Q1 2026 · Completada)

### 🟢 Caso 01: AWS Amplify Hosting
![AWS](https://img.shields.io/badge/AWS-Amplify-FF9900?style=flat-square&logo=amazonaws)
![DVA](https://img.shields.io/badge/DVA--C02-Deployment-FF6B6B?style=flat-square)

- [x] Sitio PWA completo desplegado en Amplify Console
- [x] Multi-branch: `main` y `dev` con URLs independientes y SSL automático
- [x] Service Worker · Web App Manifest · offline fallback
- [x] i18n en 6 idiomas (ES · EN · FR · IT · PT · ZH)
- [x] Static JSON API (`/api/v1/`) · 30+ PDFs · Three.js 3D experience

**GitHub Actions:** Deploy delegado a Amplify — pipeline sin YAML propio.

---

### 🟢 Caso 02: S3 + GitHub Actions Deploy
![AWS](https://img.shields.io/badge/AWS-S3-FF9900?style=flat-square&logo=amazonaws)
![DVA](https://img.shields.io/badge/DVA--C02-Deployment-FF6B6B?style=flat-square)

- [x] S3 Static Website Hosting activo en us-east-2
- [x] Workflow `despliegue.yml` con `paths` filter (monorepo-aware)
- [x] `workflow_dispatch` para deploy manual desde GitHub UI
- [x] `aws s3 sync --delete` (limpieza automática del bucket)

**GitHub Actions:** Primer YAML real. `paths`, `workflow_dispatch`, secrets de repositorio.

---

## 🔐 Fase 2 — Seguridad de Identidad (Q2 2026 · Abril–Junio)

### 🟡 Caso 03: S3 + CloudFront + OIDC
![AWS](https://img.shields.io/badge/AWS-CloudFront%20·%20IAM-FF9900?style=flat-square&logo=amazonaws)
![DVA](https://img.shields.io/badge/DVA--C02-Security%2026%25-FF6B6B?style=flat-square)
![SAA](https://img.shields.io/badge/SAA--C03-Secure%20Arch%2030%25-4ECDC4?style=flat-square)
![SOA](https://img.shields.io/badge/SOA--C02-Security%2016%25-45B7D1?style=flat-square)

- [ ] Configurar OIDC Trust Policy en rol IAM
- [ ] Reemplazar `AWS_ACCESS_KEY_ID` → `id-token: write` + `role-to-assume`
- [ ] Crear distribución CloudFront sobre S3
- [ ] Step de invalidación de caché post-deploy

**GitHub Actions:** OIDC federation — cero secrets estáticos.
**Criterio de éxito:** El workflow no tiene ningún secret de AWS almacenado.

---

### 🟡 Caso 04: GitHub Environments + Aprobaciones
![AWS](https://img.shields.io/badge/AWS-S3%20·%20CloudFront-FF9900?style=flat-square&logo=amazonaws)
![DVA](https://img.shields.io/badge/DVA--C02-Deployment%2024%25-FF6B6B?style=flat-square)
![SOA](https://img.shields.io/badge/SOA--C02-Deployment%2018%25-45B7D1?style=flat-square)

- [ ] Environments `staging` (auto) y `production` (requiere aprobación)
- [ ] `required_reviewers` en production environment
- [ ] Secrets por entorno (buckets distintos)
- [ ] Banner visual DOM: "STAGING" / "PRODUCTION"

**GitHub Actions:** `environment:`, deployment gates, secrets por scope.
**Criterio de éxito:** Staging es automático; prod espera aprobación en GitHub UI.

---

## ⚡ Fase 3 — Serverless & Testing (Q2–Q3 2026 · Mayo–Septiembre)

### 🟡 Caso 05: Lambda + API Gateway
![AWS](https://img.shields.io/badge/AWS-Lambda%20·%20API%20GW%20·%20SAM-FF9900?style=flat-square&logo=amazonaws)
![DVA](https://img.shields.io/badge/DVA--C02-Development%2032%25-FF6B6B?style=flat-square)
![SAA](https://img.shields.io/badge/SAA--C03-High%20Perf%2024%25-4ECDC4?style=flat-square)

- [ ] Lambda Python/Node.js + API Gateway (SAM template)
- [ ] Pipeline: job `test` → job `build` → job `deploy` (con `needs:`)
- [ ] `upload-artifact` / `download-artifact` entre jobs
- [ ] `workflow_dispatch` con `inputs` para elegir entorno

**GitHub Actions:** Multi-job, artifacts, job sequencing.
**Criterio de éxito:** Deploy no ocurre si tests fallan. El artefacto de build es idéntico al de prod.

---

### 🟡 Caso 06: DynamoDB + Matrix Builds
![AWS](https://img.shields.io/badge/AWS-DynamoDB%20·%20Lambda-FF9900?style=flat-square&logo=amazonaws)
![DVA](https://img.shields.io/badge/DVA--C02-Development%2032%25-FF6B6B?style=flat-square)
![SAA](https://img.shields.io/badge/SAA--C03-Resilient%2026%25-4ECDC4?style=flat-square)

- [ ] Lambda con CRUD sobre DynamoDB (política IAM mínima)
- [ ] Matrix: `runtime: [python3.11, python3.12]` × `region: [us-east-1, us-east-2]`
- [ ] `fail-fast: false` — fallo en una celda no cancela las demás

**GitHub Actions:** `strategy.matrix`, parallel jobs, `fail-fast`.
**Criterio de éxito:** 4 combinaciones ejecutadas en paralelo con reporte individual.

---

## 🏗️ Fase 4 — Plataforma GitHub (Q3 2026 · Julio–Septiembre)

### 🟡 Caso 07: Reusable Workflows + Composite Actions
![DVA](https://img.shields.io/badge/DVA--C02-Deployment%2024%25-FF6B6B?style=flat-square)
![SOA](https://img.shields.io/badge/SOA--C02-Automation%2018%25-45B7D1?style=flat-square)

- [ ] Reusable workflow: `.github/workflows/deploy-s3-oidc.yml` (callable)
- [ ] Composite action: `.github/actions/setup-aws-oidc/action.yml`
- [ ] Refactorizar casos 03-06 para consumir los reusables
- [ ] Documentar: reusable workflow vs composite action vs step inline

**GitHub Actions:** `workflow_call`, composite actions, DRY en pipelines.

---

### 🟡 Caso 08: Containers + GHCR
![AWS](https://img.shields.io/badge/AWS-ECS%20Fargate-FF9900?style=flat-square&logo=amazonaws)
![Docker](https://img.shields.io/badge/Docker-GHCR-2496ED?style=flat-square&logo=docker)
![DVA](https://img.shields.io/badge/DVA--C02-Deployment%2024%25-FF6B6B?style=flat-square)
![SAA](https://img.shields.io/badge/SAA--C03-High%20Perf%2024%25-4ECDC4?style=flat-square)

- [ ] Build multi-platform (`linux/amd64` + `linux/arm64`) con buildx
- [ ] Push a `ghcr.io/vladimiracunadev-create/caso-08` (sin ECR externo)
- [ ] Deploy a ECS Fargate con task definition actualizada
- [ ] Semantic tagging automático (SHA + semver)

**GitHub Actions:** GHCR nativo, `docker/build-push-action`, multi-platform.

---

## 🏛️ Fase 5 — Gobernanza & Resiliencia (Q4 2026 · Octubre–Diciembre)

### 🟡 Caso 09: FinOps + Scheduled Workflows
![AWS](https://img.shields.io/badge/AWS-Cost%20Explorer%20·%20Budgets-FF9900?style=flat-square&logo=amazonaws)
![SAA](https://img.shields.io/badge/SAA--C03-Cost%20Opt%2020%25-4ECDC4?style=flat-square)
![SOA](https://img.shields.io/badge/SOA--C02-Cost%2012%25-45B7D1?style=flat-square)

- [ ] Cron `0 8 1 * *` — primer día del mes, 08:00 UTC
- [ ] Script Python: `ce.get_cost_and_usage()` via OIDC
- [ ] Auto-commit de `docs/FINOPS_COSTOS.md` con datos reales
- [ ] AWS Budgets con alerta a email

**GitHub Actions:** `schedule` trigger, workflow que commitea, `GITHUB_TOKEN` para push.

---

### 🟡 Caso 10: Multi-región + Disaster Recovery
![AWS](https://img.shields.io/badge/AWS-Route53%20·%20CloudFront-FF9900?style=flat-square&logo=amazonaws)
![SAA](https://img.shields.io/badge/SAA--C03-Resilient%2026%25-4ECDC4?style=flat-square)
![SOA](https://img.shields.io/badge/SOA--C02-Reliability%2016%25-45B7D1?style=flat-square)

- [ ] Deploy paralelo a `us-east-1` y `eu-west-1` via matrix
- [ ] Smoke tests por región post-deploy
- [ ] Route53 failover routing con health checks
- [ ] Rollback automático si smoke tests fallan

**GitHub Actions:** Matrix regions + conditional rollback.

---

### 🟡 Caso 11: EKS + GitOps
![AWS](https://img.shields.io/badge/AWS-EKS%20·%20IRSA-FF9900?style=flat-square&logo=amazonaws)
![K8s](https://img.shields.io/badge/Kubernetes-1.32-326CE5?style=flat-square&logo=kubernetes)
![SAA](https://img.shields.io/badge/SAA--C03-Resilient%2026%25-4ECDC4?style=flat-square)
![DVA](https://img.shields.io/badge/DVA--C02-Deployment%2024%25-FF6B6B?style=flat-square)

- [ ] Cluster EKS via Terraform (reutiliza Caso K del repo GitLab)
- [ ] Manifiestos K8s en `caso-11-eks-gitops/k8s/`
- [ ] GitHub Actions como controlador GitOps (sin ArgoCD)
- [ ] OIDC para K8s API (IRSA — IAM Roles for Service Accounts)

**GitHub Actions:** GitOps pattern, K8s nativo desde Actions, IRSA.

---

## 📊 Cobertura de certificaciones por fase

| Fase | Casos | ![DVA](https://img.shields.io/badge/DVA--C02-FF6B6B?style=flat-square) | ![SAA](https://img.shields.io/badge/SAA--C03-4ECDC4?style=flat-square) | ![SOA](https://img.shields.io/badge/SOA--C02-45B7D1?style=flat-square) |
|:---|:---|:---:|:---:|:---:|
| Fundamentos | 01, 02 | Deployment | — | Deployment |
| Identidad | 03, 04 | Security | Secure Arch | Security |
| Serverless | 05, 06 | Development | High Perf | Deployment |
| Plataforma | 07, 08 | Deployment | High Perf | Automation |
| Gobernanza | 09, 10, 11 | Deployment | Cost · Resilient | Cost · Reliability |

> 📋 Detalle completo: [docs/CERT_COVERAGE.md](docs/CERT_COVERAGE.md)

---

## 📌 Reglas de gestión

- Todo cambio parte de `dev` → PR → `main`
- Cada caso nuevo: carpeta propia + README con badges + workflow actualizado + criterio de éxito
- Costos reales documentados en `docs/FINOPS_COSTOS.md` al completar cada caso
- Etiquetas de issues: `ci/cd` · `infra` · `security` · `finops` · `dx` · `certification`
