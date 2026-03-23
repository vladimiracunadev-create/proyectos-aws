# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo. El formato se basa en [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [5.0.0] - 2026-03-22 (Actual)

### Added
- **Proyección de 11 casos**: Arquitectura evolutiva completa desde Amplify hasta multi-región con FinOps, cubriendo Q1–Q4 2026.
- **Carpetas placeholder casos 03–11**: `caso-03-cloudfront-oidc/` hasta `caso-11-multi-region-finops/`, cada una con README completo (badges, tablas AWS+Actions, diagrama de flujo, cobertura de certificaciones, navegación).
- **`GITHUB_ACTIONS_JOURNEY.md`**: Narrativa central del repositorio — por qué coexiste con el repo GitLab y cómo se complementan.
- **`docs/CASOS_COMPLETADOS.md`**: Checklists de validación con comandos de verificación para casos en producción.
- **`docs/FINOPS_COSTOS.md`**: Desglose real de costos por caso, cobertura Free Tier, comparativa GitHub vs GitLab.
- **`docs/CERT_COVERAGE.md`**: Mapa de dominios DVA-C02, SAA-C03, SOA-C02 por caso.
- **`docs/INSTALL.md`**: Guía de inicio rápido con 3 opciones (solo leer, desarrollo local, demo K8s).
- **`.github/ISSUE_TEMPLATE/`**: Templates estructurados para bug reports y feature requests (formularios YAML).
- **`.github/pull_request_template.md`**: Checklist completo (calidad, docs, seguridad, certificaciones, FinOps).
- **`.github/CODEOWNERS`**: Revisores obligatorios por área (workflows, seguridad, infra, casos en producción).
- **`.github/dependabot.yml`**: Actualizaciones automáticas semanales para github-actions, mensuales para Docker.
- **`.github/workflows/release.yml`**: Workflow que crea GitHub Releases automáticamente al pushear tags `v*.*.*`.

### Changed
- **Renombrado de carpetas** (preservando historial git): `aws-amplify-mi-sitio-1/` → `caso-01-amplify-hosting/`, `aws-s3-scrum-mi-sitio-1/` → `caso-02-s3-github-actions/`.
- **`README.md`**: Reescrito completamente con badges shields.io, tabla de 11 casos con fases y estado, diagrama Mermaid, sección de complementariedad con GitLab.
- **`ROADMAP.md`**: Reescrito con definición de Q al inicio, badges por caso, criterios de éxito, tabla de cobertura de certificaciones por fase.
- **`amplify.yml`**: Actualizado `appRoot` a `caso-01-amplify-hosting`.
- **`.github/workflows/despliegue.yml`**: Actualizado nombre, path y sync command para `caso-02-s3-github-actions`.
- **`docs/wiki/CI-CD-Architecture.md`**: Reescrito para corregir corrupción de encoding UTF-8 (emojis renderizados como `ðŸ—ï¸`).
- **`docs/wiki/Tooling-Guide.md`**: Corregidos caracteres `â–¸` corruptos y nomenclatura de carpetas.

### Fixed
- **`docs/RECRUITER.md`**: Corregido enlace roto `aws-amplify-mi-sitio-1/AWS_PASO_A_PASO.md` → `caso-01-amplify-hosting/README.md`.
- **`FILE_ARCHITECTURE.md`**: Actualizadas referencias a nuevos nombres de casos.
- **`docs/TOOLING.md`**: Actualizadas referencias a nomenclatura nueva.
- **`docs/CI_CD_ENGINEERING_DEEP_DIVE.md`**: Actualizadas referencias a nomenclatura nueva.
- **`docs/QUICK_REFERENCE.md`**: Actualizadas referencias a nomenclatura nueva.

---

## [4.2.0] - 2026-02-23

### Added
- **Expansión de Documentación**: Creación de `SYSTEM_SPECS.md`, `FILE_ARCHITECTURE.md`, `CHANGELOG.md`, `GLOSSARY.md` y `ENVIRONMENT_SETUP.md`.
- **Diagramas de Arquitectura**: Integración de Mermaid en `docs/RECRUITER.md`.
- **Estándar Industrial**: Documentación de secciones de Observabilidad y FinOps en los README de subproyectos.

### Changed
- **Refactorización Premium**: Mejora estética y técnica de `ROADMAP.md`, `CONTRIBUTING.md` y `SECURITY.md`.

### Fixed
- **Resiliencia CI/CD**: Se configuró `continue-on-error` en el escaneo de dependencias para evitar bloqueos por falta de configuración en el Grafo de Dependencias de GitHub.

---

## [4.1.0] - 2026-02-23

### Added
- **READMEs de Proyectos**: Documentación específica para `caso-01-amplify-hosting` y `caso-02-s3-github-actions`.
- **Guías Paso a Paso**: Creación de `README.md por caso` para ambos flujos de despliegue.

---

## [4.0.0] - 2026-02-22

### Added
- **PWA Capabilities**: Service Workers, Manifiestos y páginas offline en ambos portafolios.
- **Optimización de Activos**: Nueva estructura de carpetas para PDFs e iconos SVG unificados.
- **Branching Sync**: Implementación de flujo de trabajo coordinado entre las ramas `main` y `dev`.

---

## [1.0.0] - Archivo Histórico
- Lanzamiento inicial del monorepo con despliegue básico a S3 y Amplify.
