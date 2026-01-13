# GitLab → AWS (web estática) — Plantilla profesional

[![Pipeline](https://gitlab.com/vladimir.acuna.dev-group/proyectos-aws-gitlab/badges/main/pipeline.svg)](https://gitlab.com/vladimir.acuna.dev-group/proyectos-aws-gitlab/-/pipelines)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Changelog](https://img.shields.io/badge/changelog-Unreleased-yellow.svg)](CHANGELOG.md)

Descripción
-----------
Plantilla para desplegar una web estática desde GitLab hacia AWS. Incluye dos enfoques bien documentados para distintos niveles de control y automatización:

- `caso-a-amplify/` — Conexión rápida con **AWS Amplify** para despliegue automático y sencillo.
- `caso-b-gitlab-s3/` — Pipelines de **GitLab CI/CD** que despliegan a **Amazon S3 + CloudFront** para mayor control.

Índice
------
- [Estado del proyecto](#estado-del-proyecto)
- [Casos de uso](#casos-de-uso)
- [Quick start](#quick-start)
- [Desarrollo y pruebas](#desarrollo-y-pruebas)
- [Contribuir](#contribuir)
- [Licencia](#licencia)
- [Contacto](#contacto)

Estado del proyecto
-------------------
- Estatus: Activo (se aceptan contribuciones)
- CI: Pipeline en GitLab (ver badge arriba)

Casos de uso
------------
- Caso A — Amplify: ideal si quieres conectar y desplegar en minutos.
- Caso B — GitLab CI → S3: ideal si necesitas control fino de caching, invalidación de CloudFront y políticas IAM.

Quick start
-----------
1. Clona el repositorio:

```bash
git clone https://gitlab.com/vladimir.acuna.dev-group/proyectos-aws-gitlab.git
cd proyectos-aws-gitlab
```

2. Elige un caso y sigue las instrucciones en la carpeta correspondiente:

- `caso-a-amplify/README.md`
- `caso-b-gitlab-s3/README.md`

Desarrollo y pruebas
--------------------
- Estructura mínima: HTML/CSS/JS estático en cada carpeta `caso-*`.
- Para pruebas locales: abre `index.html` en el navegador o usa un servidor estático (por ejemplo `npx http-server`).

Contribuir
----------
Gracias por considerar contribuir. Lee `CONTRIBUTING.md` para pautas de ramas, commits y PRs. También hay plantillas de issues y MR para agilizar la colaboración.

Licencia
--------
Este proyecto está bajo la licencia MIT — ver `LICENSE`.

Changelog
---------
Revisa `CHANGELOG.md` para ver el historial de cambios y la versión actual.

Contacto
--------
Para preguntas, abre un **issue** o contacta al responsable del repositorio.

---

Notas internas
--------------
- Mantén las credenciales fuera del repositorio. Usa variables protegidas en GitLab CI.
- No reutilices recursos de otros proyectos (buckets, usuarios IAM).

