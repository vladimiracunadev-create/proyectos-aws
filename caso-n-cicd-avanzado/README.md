# 🔄 Caso N: CI/CD Avanzado con GitLab

[![Nivel-13](https://img.shields.io/badge/Nivel-13_DevOps_Avanzado-blue?style=for-the-badge)]()
[![Status](https://img.shields.io/badge/Status-Proyectado-lightgrey?style=for-the-badge)]()
[![Prerequisito](https://img.shields.io/badge/Prerequisito-Caso_L-orange?style=for-the-badge)]()

Cierre del ciclo DevOps del monorepo: pipelines multi-ambiente con protection rules, rollback automatizado y revisiones de PR como gates de despliegue. Sin costo adicional de AWS — usa infraestructura GitLab pura.

---

## Objetivo

Demostrar un pipeline GitLab CI/CD de nivel production-ready con:
- Ambientes separados (dev / staging / prod) con estado propio
- Aprobación manual obligatoria antes de desplegar a producción
- Rollback automático si el health check post-deploy falla
- Revisión de PR como gate: el merge a `main` solo ocurre si staging pasó

---

## Stack planificado

| Componente | Tecnología | Propósito |
|---|---|---|
| Pipelines | GitLab CI/CD | Orquestación multi-stage |
| Ambientes | GitLab Environments | Estado por ambiente (dev/staging/prod) |
| Protection rules | GitLab Deployment approvals | Gate manual antes de prod |
| Rollback | GitLab CI + scripts bash | Revertir si health check falla |
| Secretos | GitLab CI/CD Variables (masked) | Credenciales por ambiente |

---

## Fases planificadas

### Fase 0 — Scaffold (actual)
- [x] README y documentación inicial
- [x] Carpeta del caso creada

### Fase 1 — Pipeline básico multi-stage
- [ ] `.gitlab-ci.yml` con stages: build → test → deploy-dev → deploy-staging → deploy-prod
- [ ] Ambiente `dev` con deploy automático en cada push a rama
- [ ] Ambiente `staging` con deploy automático en merge a `main`

### Fase 2 — Protection rules y aprobaciones
- [ ] Ambiente `prod` protegido con aprobación manual requerida
- [ ] Notificación al aprobador vía webhook
- [ ] Log de quién aprobó y cuándo

### Fase 3 — Rollback automático
- [ ] Health check post-deploy: si falla en 2 minutos → trigger rollback
- [ ] Rollback: re-deploy del artefacto anterior
- [ ] Notificación de rollback con diff entre versiones

---

## Costo estimado

**$0 USD** — este caso usa exclusivamente GitLab CI/CD runners compartidos y environments. No levanta recursos AWS adicionales.

---

## Prerequisitos técnicos

- Caso L completado (OIDC configurado — credenciales efímeras en CI)
- Al menos un caso serverless activo para usar como target de despliegue (recomendado: Caso D o E)

---

## Por qué este caso importa

Los pipelines multi-ambiente con aprobaciones y rollback son el estándar mínimo en equipos de ingeniería serios. Saber configurarlos demuestra madurez DevOps más allá del "funciona en mi máquina".

---

## Vínculos

- ⬅️ **[Regresar al README principal](../README.md)**
- 📍 **[Estado y Roadmap](../docs/ESTADO_Y_ROADMAP.md)**
- 🔗 **[Prerequisito: Caso L](../caso-l-finops-optimization/README.md)**
