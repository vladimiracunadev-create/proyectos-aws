# GitLab → AWS (web estática) — Plantilla profesional

[![Deployed](https://img.shields.io/badge/deployed-Amplify-brightgreen.svg)](https://main.d1uybq9oui7h8c.amplifyapp.com/)
[![Pipeline](https://gitlab.com/vladimir.acuna.dev-group/proyectos-aws-gitlab/badges/main/pipeline.svg)](https://gitlab.com/vladimir.acuna.dev-group/proyectos-aws-gitlab/-/pipelines)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Changelog](https://img.shields.io/badge/changelog-Unreleased-yellow.svg)](CHANGELOG.md)

**Temas:** `aws` `gitlab` `static-site` `amplify` `s3` `cloudfront`

**¿Quieres contribuir?** Lee `CONTRIBUTING.md` y `CODE_OF_CONDUCT.md`.

---

## Descripción

Plantilla para desplegar una web estática desde GitLab hacia AWS. Incluye dos enfoques bien documentados para distintos niveles de control y automatización:

- `caso-a-amplify/` — Conexión rápida con **AWS Amplify** para despliegue automático y sencillo.
- `caso-b-gitlab-s3/` — **GitLab CI/CD** despliega a **Amazon S3** (y **CloudFront opcional**) para mayor control.

---

## Índice

- [Estado del proyecto](#estado-del-proyecto)
- [Casos de uso](#casos-de-uso)
- [Quick start](#quick-start)
- [Desarrollo y pruebas](#desarrollo-y-pruebas)
- [CI / Despliegue](#ci--despliegue)
- [Contribuir](#contribuir)
- [Licencia](#licencia)
- [Changelog](#changelog)
- [Contacto](#contacto)

---

## Estado del proyecto

- **Estatus:** Activo (se aceptan contribuciones)
- **CI:** Pipeline en GitLab (ver badge arriba)

### Demos

- **Demo (Caso A — Amplify):** https://main.d1uybq9oui7h8c.amplifyapp.com/ (deployed 2026-01-13)
- **Demo (Caso B — GitLab CI → S3):** https://vladimir-caso-b-site-2026.s3.us-east-2.amazonaws.com/index.html (deployed 2026-01-13)

> Nota: Si deseas URL con HTTPS + dominio propio y mejor caché, habilita CloudFront (opcional) en el Caso B.

---

## Casos de uso

- **Caso A — Amplify:** ideal si quieres conectar y desplegar en minutos.
- **Caso B — GitLab CI → S3 (CloudFront opcional):** ideal si necesitas control fino de publicación, versionado de artefactos, caché e invalidación (si usas CloudFront), y políticas IAM mínimas.

---

## Quick start

1. Clona el repositorio:

```bash
git clone https://gitlab.com/vladimir.acuna.dev-group/proyectos-aws-gitlab.git
cd proyectos-aws-gitlab


