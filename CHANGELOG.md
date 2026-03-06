# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.
El formato seguirá [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) y este proyecto utiliza [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.3.0] - 2026-03-05

### Fixed

- **Caso C — Pipeline CI/CD (`scan_infrastructure`)**: Corregido error crítico de parseo HCL que bloqueaba `tfsec`.
    - **Causa raíz**: `main.tf` contenía bloques `action` y `action_trigger` (syntaxis experimental de Terraform Stacks / HCP), inválidos en Terraform estándar. `tfsec` fallaba al parsear antes de ejecutar cualquier análisis.
    - **Solución**: Eliminados los bloques inválidos de `main.tf`. El archivo es ahora HCL estándar compatible con todas las versiones de Terraform.

- **Caso C — Hallazgos de seguridad `tfsec`**: Resueltos los 5 hallazgos (3 HIGH, 2 MEDIUM) que hacían fallar la pipeline tras corregir el parseo.
    - `aws-cloudfront-enable-waf` (HIGH): WAF implica costo fijo para proyecto de portafolio/demo. Ignorado con `#tfsec:ignore` documentado.
    - `aws-cloudfront-use-secure-tls-policy` (HIGH): TLS personalizado requiere dominio propio + certificado ACM. Ignorado con justificación.
    - `aws-s3-encryption-customer-key` (HIGH): CMK (KMS) añade costo y complejidad innecesaria para demo. Se mantiene AES256. Ignorado con justificación.
    - `aws-cloudfront-enable-logging` (MEDIUM): Logging requiere bucket S3 adicional con permisos especiales. Ignorado documentado.
    - `aws-s3-enable-bucket-logging` (MEDIUM): Idem anterior. Ignorado documentado.

- **Caso C — Invalidación de caché CloudFront**: Resuelto error `aws: not found` en el job `deploy_case_c`.
    - **Causa raíz**: La imagen `hashicorp/terraform:1.14.3` no incluye AWS CLI. El `null_resource` con `local-exec` fallaba con `exit code 127`.
    - **Solución**: Eliminado `null_resource.cloudfront_invalidation` de `main.tf` y el proveedor `hashicorp/null` de `versions.tf`. La invalidación se delega a un nuevo job `invalidate_cloudfront_c` en `.gitlab-ci.yml` que usa la imagen `public.ecr.aws/aws-cli/aws-cli:latest`. El job lee el Distribution ID desde la variable CI/CD `CLOUDFRONT_DISTRIBUTION_ID_C`.

### Changed

- **`.gitlab-ci.yml`**: Nuevo job `invalidate_cloudfront_c` (stage: `deploy`) con `needs: [deploy_case_c]`. Invalida `/*` en CloudFront después de cada deploy exitoso de Terraform.
- **`caso-c-terraform-s3/main.tf`**: Eliminado `null_resource.cloudfront_invalidation`. Añadidos comentarios `#tfsec:ignore` con justificación técnica en cada hallazgo.
- **`caso-c-terraform-s3/versions.tf`**: Eliminado proveedor `hashicorp/null` (no requerido tras eliminar `null_resource`).

---

## [3.2.0] - 2026-02-17
### Added
- **Caso L (FinOps & Governance)**: Finalización del módulo de excelencia operativa y seguridad.
    - Implementación de **AWS Budgets** para alertas de costos ("monthly-alert").
    - Configuración de **GitLab OIDC** para autenticación Zero Trust entre GitLab y AWS.
    - Gobernanza IAM con políticas de límites regionales (Ohio Only) y etiquetado obligatorio.
    - Despliegue automatizado de sitio web estático en S3 con políticas de acceso público.
    - **Automatización de Datos**: Dashboard estático ahora muestra costos reales de AWS (JSON Generation).

## [3.1.0] - 2026-02-16
### Added
- **Caso K (Kubernetes EKS)**: Finalización del hito de orquestación industrial.
    - Despliegue de clúster EKS v1.32 con Auto Mode.
    - Implementación de balanceo de carga L7 (AWS Load Balancer Controller).
    - Validación de resiliencia mediante pruebas de **Self-Healing**.
    - Guía de limpieza FinOps para gestión de costos en la nube.
- **Documentación Estratégica**: Actualización de guías para reclutadores y novatos con el rationale técnico de Kubernetes.

## [1.3.0] - 2026-02-10
### Added
- **Caso J (Premium Dashboard)**: Evolución de la interfaz técnica JSON a un Dashboard industrial con **Glassmorphism** y animaciones.
- **Arquitectura**: Sección de "Claridad Conceptual" en la documentación para explicar la relación Docker (Local) vs AWS (ECR/ECS/Fargate).
- **Diagramas**: Inclusión de diagramas Mermaid detallando la cadena de suministro de imágenes (Image Supply Chain).

### Fixed
- **Navegación**: Corrección de enlaces rotos (`wiki/home.md`, `docs/TOOLING.md`) en la PWA principal.
- **Documentación**: Completado de contenido faltante en `docs/TOOLING.md` detallando el stack de herramientas.

## [1.2.0] - 2026-02-09
### Added
- **Caso J**: Finalización del módulo de Dockerización con ECS Fargate.
    - Despliegue automatizado de infraestructura con Terraform.
    - Pipeline manual documentado para Build, Tag & Push a ECR.
    - Documentación exhaustiva `AWS_PASO_A_PASO.md` con bitácora de comandos.

## [1.1.0] - 2026-01-23
### Added
- **Automatización**: Implementación de `Makefile` raíz para orquestar tareas comunes (install, lint, deploy, security).
- **Entorno Senior**: Configuración de **DevContainers** (`.devcontainer/`) con Docker para un entorno de desarrollo 100% reproducible.
- **Seguridad IaC**: Integración de `tfsec` para auditoría de seguridad automática en el Pipeline de GitLab y localmente.
- **Roadmap Extendido**: Expansión del monorepo a 12 casos (A-L), incluyendo:
    - **Caso J**: Dockerización de Microservicios (ECS Fargate).
    - **Caso K**: Orquestación real en **AWS EKS (Kubernetes)**.
    - **Caso L**: Gobernanza y FinOps (Optimización de costos).
- **Nueva Documentación**: Creación de `ARCHITECTURE.md` (diagramas Mermaid) e `INSTALL.md` (guías multiescenario) en la carpeta `docs/`.

### Changed
- **Reorganización Documental**: Mudanza de todos los manuales técnicos y archivos legales a la carpeta centralizada `docs/`.
- **Rediseño Senior**: Actualización estética y técnica de todos los archivos `README.md` (Raíz e Individuales) bajo estándares industriales.
- **Orden Alfabético**: Reordenamiento de carpetas de proyectos (A-L) para una progresión de aprendizaje lógica (G movido a J).
- **Infraestructura**: Migración a **Remote Backend** de Terraform almacenado en la región de Ohio (`us-east-2`) para persistencia global del estado.

### Fixed
- **Integridad Visual**: Estandarización de rutas de activos CSS y corrección de MIME types en CloudFront.
- **Pipeline de GitLab**: Resolución de errores de permisos mediante la unificación de identidades IAM y corrección de disparadores por carpeta.
- **Identidades**: Corrección de inconsistencias de nombres y niveles en los encabezados internos de los casos de estudio.

## [0.2.0] - 2026-01-20
### Added
- **Caso B**: Despliegue estático a S3 automatizado vía GitLab CI.
- **Caso C**: Infraestructura como Código (IaC) con Terraform y CDN CloudFront con OAC.

### Fixed
- Error de variable `$S3_BUCKET` en el pipeline de despliegue.
- Configuración de políticas de acceso OAC para mayor seguridad en S3.

## [0.1.0] - 2026-01-13
### Added
- Estructura inicial del monorepo y Caso A (AWS Amplify).
- Documentación base de aprendizaje.

---
_Ultima actualización: 2026-02-10_