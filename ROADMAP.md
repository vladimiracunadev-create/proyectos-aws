# 🗺️ Roadmap: Cloud Portfolio (AWS Monorepo)

Este roadmap define la evolución técnica del ecosistema, priorizando la **profesionalización del CI/CD**, **FinOps**, **Observabilidad** y **Seguridad**.

---

## 🏗️ Fase 1: Cimientos y Automatización (Q1 2026)

### 1) Entornos y Aislamiento (CI/CD)
- [x] **Amplify Multi-branch**: Despliegue automático para `main` y `dev`.
- [x] **S3 Sync**: Sincronización desde `main` activada por GitHub Actions.
- [ ] **Dual Environment (S3)**: Implementar despliegue paralelo a un bucket de `staging` desde la rama `dev`.
- [ ] **Inyectores de Entorno**: Etiquetas visuales en el DOM ("DEV" / "PROD") basadas en la rama de despliegue.

### 2) Experiencia del Desarrollador (DX)
- [x] **Hub CLI**: Scripts PowerShell y Bash para simplificar comandos comunes.
- [x] **Documentación como Código**: Wiki automatizada y READMEs técnicos.
- [ ] **Doctor Checks**: Ampliar validaciones de entorno (versiones de Node, AWS CLI, Docker).

---

## 🛡️ Fase 2: Seguridad y Resiliencia (Q2 2026)

### 3) Hardening de Infraestructura
- [x] **GitHub OIDC**: Eliminación de credenciales estáticas en Actions.
- [ ] **CloudFront Integration**: Añadir CDN delante de los buckets S3 para mejorar latencia y seguridad (WAF).
- [ ] **IAM Least Privilege**: Auditoría y restricción de políticas de los roles de CI.

### 4) Observabilidad y Calidad
- [ ] **Smoke Tests Post-deploy**: Pruebas automatizadas de salud tras cada despliegue.
- [ ] **Security Matrix**: Dashboard de vulnerabilidades (SAST/Dependencias) consolidado.

---

## 💰 Fase 3: Gobernanza y Escalamiento (Q3-Q4 2026)

### 5) FinOps (Gobernanza de Costos)
- [ ] **AWS Budgets**: Implementación de alarmas de costo por subproyecto.
- [ ] **Cost Breakdown**: Añadir sección en la documentación con el coste estimado por "Demo".

### 6) Nuevas Arquitecturas
- [ ] **Serverless API Layer**: Introducción de AWS Lambda (Node.js/Python) para demos dinámicas.
- [ ] **Event-Driven Patterns**: Uso de EventBridge o SQS para orquestar flujos entre demos.

---

## 📌 Gestión del Proyecto
- **Etiquetas**: `ci/cd`, `infra`, `security`, `finops`, `dx`.
- **Estrategia**: Todo cambio debe originarse en `dev` y pasar por revisión (PR) antes de llegar a `main`.
