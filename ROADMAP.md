
---

## `ROADMAP.md` (con hitos + epics claros)

```md
# 🗺️ Roadmap (Cloud Portfolio: AWS Monorepo)

Este roadmap prioriza **profesionalización del CI/CD**, separación clara de entornos, IaC, observabilidad y seguridad.

---

## ✅ Estado actual
- [x] S3 + GitHub Actions (deploy automático a `main`)
- [x] Amplify con ramas `main` / `dev` (deploy por rama)
- [x] PR flow `dev` → `main` funcionando

---

## 🎯 Próximos hitos (corto plazo)

### 1) Entornos bien definidos (DEV/PROD)
- [ ] S3: desplegar también desde `dev` a un entorno DEV
  - Opción A: **2 buckets** (prod/dev)
  - Opción B: **1 bucket** con prefijos `/prod` y `/dev`
- [ ] Indicador visual “ENV: DEV/PROD” en las demos
- [ ] Checklist de validación post-deploy (Amplify + S3)

### 2) Seguridad y buenas prácticas
- [ ] IAM least privilege para GitHub Actions (policy mínima)
- [ ] Templates de Issues / PR
- [ ] Reglas de rama (proteger `main`, requerir PR)

---

## 🚀 Mediano plazo

### 3) CloudFront + performance (opcional pero pro)
- [ ] CloudFront delante de S3
- [ ] Invalidation automatizada al desplegar (si aplica)
- [ ] Headers de cache control/documentación

### 4) IaC (Terraform)
- [ ] Terraform para S3 website + policies + (opcional) CloudFront
- [ ] Terraform para recursos de laboratorio (con módulos)

---

## 🧱 Largo plazo

### 5) Serverless API (aws-lambda-api-1)
- [ ] API mínima (Hello/healthcheck + logging)
- [ ] Deploy (SAM o Terraform)
- [ ] Integración con front demo

### 6) Observabilidad y costos
- [ ] CloudWatch logs/metrics básicos
- [ ] Presupuesto y alertas (AWS Budgets)
- [ ] Documentar costos estimados

---

## 📌 Cómo se gestiona
- Issues etiquetados: `ci`, `infra`, `security`, `docs`, `feature`, `bug`
- Board (Kanban): Backlog → In Progress → Review → Done
