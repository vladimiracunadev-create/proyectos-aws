# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.
El formato seguirá [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) y este proyecto utiliza [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.7.0] - 2026-03-17

### Added

- **Skill `repo-status-analysis`** (`skills/repo-status-analysis/SKILL.md`): Nuevo skill para radiografia del repositorio. Genera o actualiza `docs/ESTADO_Y_ROADMAP.md` con barra de estado, diagramas Mermaid de progresion de casos, mapa de documentacion global, sistema de skills, gaps criticos y tabla de mejoras priorizadas. Se invoca con `/repo-status-analysis`.
- **`docs/ESTADO_Y_ROADMAP.md`**: Documento de estado permanente generado por `repo-status-analysis`. Incluye 5 diagramas Mermaid, analisis de los 11 casos completados, gaps identificados (H sin VISUALIZATION.md, M en Fase 0, Wiki desincronizada), 10 mejoras futuras priorizadas y proxima sesion recomendada. Enlazado desde README principal en nueva seccion "Estado y Hoja de Ruta".
- **`docs/FINOPS_COSTOS.md`**: Analisis detallado de costos para los 11 casos completados. Estrategia free tier, costos provisioned, tabla de riesgo financiero y proyeccion de casos futuros (M, I).
- **`docs/CONCEPTOS_NUBE.md`**: Puente conceptual entre IT tradicional y terminologia AWS. Mapeo de conceptos conocidos (servidores, redes, DNS, seguridad) hacia servicios AWS con ejemplos de cada caso construido.
- **`apps/cost-calculator/index.html`**: Calculadora interactiva de costos en GitLab Pages. Sliders por caso, precios reales 2026, desglose por servicio. Disponible en el portal de GitLab Pages.

### Changed

- **`docs/SKILLS.md`**: Actualizado de 10 a 11 skills. Agrega `repo-status-analysis` en nueva categoria "Estado y mejoras del repositorio", tabla de decision rapida y arbol de ubicacion.
- **`docs/ESTADO_Y_ROADMAP.md`**: Barra de estado actualizada a "11 skills / 95%" para reflejar el skill nuevo. Diagrama de skills y subgrafo actualizados.
- **`skills/README.md`**: Contador actualizado a 11 skills. Fila `repo-status-analysis` agregada a la tabla de situaciones.
- **`README.md`**: Nueva seccion "Estado y Hoja de Ruta" con link directo a `docs/ESTADO_Y_ROADMAP.md`.

---

## [3.6.0] - 2026-03-17

### Added

- **Caso F (Security First — Cognito + JWT + WAF)**: Implementacion completa del modulo de seguridad perimetral.
    - `AWS::Cognito::UserPool` con Pre-Signup Lambda trigger para auto-confirmacion en demo (sin email verification).
    - `AWS::Cognito::UserPoolClient` con `USER_PASSWORD_AUTH` y sin secreto de cliente.
    - `AWS::Serverless::HttpApi` con JWT Authorizer nativo de Cognito (valida firma RS256 sin codigo Lambda).
    - Endpoints: `POST /auth/register`, `POST /auth/login`, `GET /profile` (protegido), `GET /health`, `GET /`.
    - WAF opcional con `DeployWAF=false` por defecto (`AWSManagedRulesCommonRuleSet` + `AWSManagedRulesSQLiRuleSet`).
    - Landing page interactiva con flujo de 3 pasos: registrar → login → perfil protegido.
    - 35+ tests unitarios con `unittest.mock.patch` (sin moto, sin credenciales AWS).
    - Smoke test `scripts/smoke/smoke_caso_f.sh` cubriendo registro, login y perfil con JWT real.
    - `AWS_PASO_A_PASO.md` con comandos verificados, troubleshooting y notas de costo.
    - `docs/architecture.md` con diagramas Mermaid del flujo de capas (WAF → API GW → Cognito → Lambda).

### Changed

- **`.gitlab-ci.yml`**: Nuevo job `test_caso_f` (`python:3.12-slim`, scoped a `caso-f-security-cognito/**/*`).
- **`Makefile`**: Nuevos targets `test-f` y `smoke-f`. Target `test` ahora incluye `test-f`.
- **`package.json`**: Nuevo script `test:f`. Script `test` actualizado para incluir Caso F.

---

## [3.5.0] - 2026-03-17

### Added

- **Caso H (Observability)**: Implementacion completa del modulo de observabilidad como codigo.
    - CloudWatch Dashboard IaC (`AWS::CloudWatch::Dashboard`) con widgets de invocaciones, errores, duracion y logs.
    - X-Ray tracing activo en Lambda (`Tracing: Active`).
    - Alarmas CloudWatch para errores Lambda y duracion p99 (`>3000ms`).
    - Landing page con metricas custom via `POST /metrics` → `cloudwatch.put_metric_data`.
    - 14 tests unitarios con `unittest.mock.patch` para `cloudwatch`.
    - Smoke test `scripts/smoke/smoke_caso_h.sh`.

- **Testing automatizado (Casos D, E, G, H)**: Infraestructura completa de tests unitarios.
    - `pytest` para los 4 casos Lambda existentes (D, E, G, H): 60+ tests en total.
    - `conftest.py` en cada caso para resolver el `sys.path` hacia `src/`.
    - Jobs CI `test_caso_d/e/g/h` en `.gitlab-ci.yml` con `python:3.12-slim` y `pip install pytest boto3`.
    - Smoke tests bash para los 4 casos (`scripts/smoke/smoke_caso_d/e/g/h.sh`).
    - Targets `test`, `test-d/e/g/h`, `smoke-d/e/g/h` en `Makefile`.
    - Scripts `test:d/e/g/h` en `package.json`.

- **README.md**: Nueva seccion "Mapa de Relaciones entre Casos" con diagrama Mermaid de dependencias tecnicas (A→M) y tabla de justificaciones.

### Fixed

- **Caso H (`index.html:141`)**: Error HTMLHint `spec-char-escape` — `p99 > 3000ms` corregido a `p99 &gt; 3000ms`. Bloqueaba el job `lint` del pipeline.
- **CI jobs test_caso_d/e/g/h**: `pip install pytest` cambiado a `pip install pytest boto3` — las Lambdas importan boto3 a nivel de modulo y fallaban con `ModuleNotFoundError` incluso en tests unitarios.

---

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

### Added

- **Arquitectura Maestra Unificada**: Reescritura profunda de **[ARCHITECTURE.md](./docs/ARCHITECTURE.md)**, consolidando diagramas y lógica de los 8 casos de estudio (A-M) en una única visión global coherente y profesional.
- **Documentación Global (Integridad)**: Actualización masiva de documentos clave para reflejar el estado actual del proyecto.
    - **[ARCHITECTURE.md](./docs/ARCHITECTURE.md)**: Integración del **Caso M** en diagramas Mermaid y documentación del patrón **Professional Tier (Job Splitting)**.
    - **[SECURITY_CHECKLIST.md](./docs/SECURITY_CHECKLIST.md)**: Actualizado con políticas de Shift-Left Security y gestión de ignores en `tfsec`.
    - **[IMPLEMENTATION_SUMMARY.md](./docs/IMPLEMENTATION_SUMMARY.md)**: Nuevas métricas (7 casos completados, 40+ security checks).
    - **[TOOLING.md](./docs/TOOLING.md)**: Documentación de la estrategia de Job Splitting para despliegues.

### Changed

- **`.gitlab-ci.yml`**: Nuevo job `invalidate_cloudfront_c` (stage: `deploy`) con `needs: [deploy_case_c]`. Invalida `/*` en CloudFront después de cada deploy exitoso de Terraform.
- **`caso-c-terraform-s3/main.tf`**: Eliminado `null_resource.cloudfront_invalidation`. Añadidos comentarios `#tfsec:ignore` con justificación técnica en cada hallazgo.
- **`caso-c-terraform-s3/versions.tf`**: Eliminado proveedor `hashicorp/null` (no requerido tras eliminar `null_resource`).

---

## [3.4.0] - 2026-03-12

### Added

- **Caso G (Event Driven)**: Finalizacion del modulo de arquitectura asincrona.
    - Despliegue real en AWS de `API Gateway + Lambda + EventBridge + SQS + DLQ + SNS`.
    - Landing publica en la raiz `/` para explicar el caso y probar el flujo desde la propia API.
    - Guia `AWS_PASO_A_PASO.md` con outputs reales, validacion y troubleshooting del consumidor.
    - Documentacion de arquitectura Mermaid para contrato de eventos, flujo principal y ruta de error.

### Fixed

- **Caso G - Lambda consumidora**: Corregido parseo del campo `detail` cuando EventBridge entrega el mensaje a SQS ya materializado como objeto.
    - **Causa raiz**: el consumidor asumia que `detail` llegaba siempre como string JSON.
    - **Solucion**: compatibilidad con `detail` como string u objeto antes de procesar el mensaje.

### Changed

- **Documentacion global**: Sincronizados `README.md`, `ROADMAP.md`, `docs/ARCHITECTURE.md`, `docs/BEGINNERS_GUIDE.md`, `docs/QUICK_REFERENCE.md`, `docs/RECRUITER.md`, `docs/TECHNICAL_SPECS.md`, `docs/FILE_STRUCTURE.md`, `wiki/home.md` y referencias del Caso E para reflejar que `Caso G` ya esta `COMPLETADO (VALIDADO)`.
- **Caso G - Health endpoint**: `/health` ahora es legible para humanos en navegador y sigue disponible como JSON para herramientas con `?format=json`.

---

## [3.2.5] - 2026-02-23
### Added
- **Arquitecturas (Deep Expansion)**: Mejora radical de la documentación técnica.
    - Inclusión de diagramas **Mermaid** detallados en todos los casos de estudio (A-L).
    - Estandarización de badges y enlaces `🏗️ Arquitectura (Mermaid)` en los READMEs de cada carpeta.
- **Caso M (Resiliencia & Failover)**: Inicialización del **Nivel 12**. 
    - **Fase 0** (Scaffold + Docs) completada: Runbook de failover, roadmap multiregión y plantillas IaC iniciales.

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
_Ultima actualización: 2026-03-05_
