# 📂 Estructura de Archivos del Sistema

> **Objetivo**: Este documento es el **mapa completo** del repositorio. Explica cada archivo y directorio con su propósito, importancia y relación con el sistema. Úsalo como referencia rápida cuando no sepas dónde buscar algo.

---

## 🌳 Vista General del Árbol

```
proyectos-aws-gitlab/
├── .devcontainer/          # Entorno de desarrollo reproducible
├── .github/                # Automatización GitHub (Issues, PRs, Dependabot)
├── .gitlab/                # Templates de GitLab (Issues, MRs)
├── apps/                   # Aplicaciones auxiliares (Android/iOS)
├── assets/                 # Recursos estáticos (CSS, JS, íconos)
├── caso-a-amplify/         # Caso A: AWS Amplify
├── caso-b-gitlab-s3/       # Caso B: S3 + GitLab CI
├── caso-c-terraform-s3/    # Caso C: Terraform + CloudFront
├── caso-d-serverless-basic/# Caso D: Lambda + API Gateway
├── caso-e-dynamodb-*/      # Caso E: DynamoDB Persistence
├── caso-f-security-*/      # Caso F: Cognito (Proyectado)
├── caso-g-event-driven/    # Caso G: EventBridge (Validado en AWS)
├── caso-h-observability/   # Caso H: CloudWatch (Proyectado)
├── caso-i-genai-bedrock/   # Caso I: Bedrock (Proyectado)
├── caso-j-containers-ecs/  # Caso J: Docker + ECS Fargate
├── caso-k-kubernetes-eks/  # Caso K: Kubernetes EKS
├── caso-l-finops-*/        # Caso L: FinOps & Governance
├── docs/                   # 📚 Documentación técnica completa
├── scripts/                # 🛠️ Scripts de auditoría y mantenimiento
├── wiki/                   # Wiki sincronizada con GitLab
├── .gitlab-ci.yml          # Pipeline principal de CI/CD
├── Makefile                # Automatización centralizada
├── README.md               # Punto de entrada del proyecto
├── index.html              # Portal PWA interactivo
├── package.json            # Dependencias y scripts Node.js
└── llms.txt                # Contexto para IAs
```

---

## ⚙️ Archivos Raíz — Configuración y Orquestación

Estos archivos controlan **cómo se construye, valida y despliega** todo el proyecto.

| Archivo | Importancia | Descripción |
|---------|:-----------:|-------------|
| **`Makefile`** | 🔴 Crítica | Centro de automatización. Contiene ~20 comandos (`make help`, `make deploy-b`, `make finops-check`, `make case-k-deploy`, etc.). Es el primer punto de contacto para cualquier operación. |
| **`.gitlab-ci.yml`** | 🔴 Crítica | Pipeline CI/CD principal. Define jobs de seguridad (`secret_detection`, `dependency_scan`, `scan_infrastructure`), calidad (`lint`) y despliegue modular para los Casos B, C, L y M. Implementa un flujo profesional de **Plan -> Apply -> Invalidate** para CloudFront. |
| **`README.md`** | 🔴 Crítica | Punto de entrada. Contiene la visión general, Quick Start, enlaces a toda la documentación y el catálogo de los 12 casos de estudio con demos en vivo. |
| **`index.html`** | 🟠 Alta | Portal web interactivo (PWA) con diseño Glassmorphism. Dashboard para navegar la documentación visualmente. |
| **`package.json`** | 🟠 Alta | Define las dependencias de desarrollo (ESLint, Prettier, HTMLHint, Stylelint, Commitlint, Husky) y los scripts de linting (`npm run lint`, `npm run format`). |
| **`package-lock.json`** | 🟠 Alta | Lockfile de dependencias. Garantiza instalaciones reproducibles en CI/CD. **No editar manualmente.** |
| **`.eslintrc.js`** | 🟡 Media | Configuración de ESLint. Define reglas de calidad para JavaScript (entorno browser+node, ES2021). |
| **`.prettierrc`** | 🟡 Media | Configuración de Prettier. Define el estilo de formateo (tabs, comillas, ancho de línea). |
| **`.pre-commit-config.yaml`** | 🟡 Media | Hooks pre-commit. Ejecuta validaciones automáticas antes de cada commit (trailing whitespace, YAML, etc.). |
| **`commitlint.config.js`** | 🟡 Media | Valida que los mensajes de commit sigan la convención de [Conventional Commits](https://www.conventionalcommits.org/). |
| **`.gitignore`** | 🟡 Media | Define qué archivos excluir del control de versiones (node_modules, .terraform, tfstate, etc.). |
| **`amplify.yml`** | 🟡 Media | Configuración de build para AWS Amplify (Caso A). Define las fases de build y los artefactos. |
| **`deploy.sh`** | 🟡 Media | Script de despliegue para el Caso L. Autentica vía OIDC y sincroniza con S3. |
| **`generate_finops_data.py`** | 🟡 Media | Generador de datos FinOps. Consulta AWS Cost Explorer y produce `costs.json` para el dashboard del Caso L. |
| **`sw.js`** | 🟢 Baja | Service Worker para la PWA. Habilita caché offline y mejora la experiencia de usuario. |
| **`manifest.json`** | 🟢 Baja | Manifiesto PWA. Define nombre, íconos y colores para la instalación en dispositivos. |
| **`s3_policy_temp.json`** | 🟢 Baja | Template temporal de política S3 para el Caso B. |
| **`trust_policy_temp.json`** | 🟢 Baja | Template temporal de política de confianza IAM para OIDC. |
| **`llms.txt`** | 🟢 Baja | Archivo de contexto para Modelos de Lenguaje (LLMs). Ayuda a IAs a entender la estructura del proyecto. |
| **`CHANGELOG.md`** | 🟢 Baja | Historial de versiones. Registra cada cambio con fecha, tipo y descripción. |
| **`ROADMAP.md`** | 🟢 Baja | Plan de desarrollo futuro. Hitos pendientes y dirección estratégica. |
| **`CONTRIBUTING.md`** | 🟢 Baja | Guía de contribución. Cómo proponer cambios, estándares de código y flujo de PRs. |
| **`LICENSE`** | 🟢 Baja | Licencia MIT. Permite uso libre con atribución. |
| **`NOTICE`** | 🟢 Baja | Avisos legales y atribuciones de terceros. |

---

## 📚 Directorio `docs/` — Base de Conocimiento

La inteligencia documentada del proyecto. Cada archivo tiene un rol específico:

| Archivo | Propósito | ¿Para quién? |
|---------|-----------|:------------:|
| **`ARCHITECTURE.md`** | Diagramas Mermaid de arquitectura, patrones identificados (Modular Monolith, 12-Factor, IaC, CI/CD), stack tecnológico completo. | Desarrolladores |
| **`FINOPS_MANUAL.md`** | 💰 **Manual de FinOps**. Semáforo de riesgo financiero (🔴🟡🟢), workflow de toma de decisiones para eliminar recursos costosos, guía de interpretación de auditoría. | Todos |
| **`FILE_STRUCTURE.md`** | 📂 **(Este archivo)**. Mapa completo del repositorio con importancia y descripción de cada archivo. | Todos |
| **`BEGINNERS_GUIDE.md`** | Glosario de términos Cloud/DevOps, conceptos fundamentales, flujo de aprendizaje recomendado. | Principiantes |
| **`COMPLETED_CASES_GUIDE.md`** | Explicación simple de todos los casos ya completados, qué resuelve cada uno y cómo empezar a leerlos. | Todos |
| **`INSTALL.md`** | Guía de instalación: Docker (DevContainers) vs instalación manual nativa. Requisitos previos. | Nuevos usuarios |
| **`QUICK_REFERENCE.md`** | Cheatsheet. Comandos esenciales de `make`, `terraform`, `docker`, `kubectl` y `aws cli`. | Todos |
| **`RECRUITER.md`** | Tour ejecutivo. Resumen del valor de negocio, habilidades demostradas, métricas del proyecto. | Reclutadores |
| **`TECHNICAL_SPECS.md`** | Requisitos de hardware y software específicos para cada caso de estudio. | DevOps |
| **`TOOLING.md`** | Explicación de cada herramienta (Docker, Terraform, AWS CLI, tfsec, gitleaks), por qué se eligió y cómo se integra. | Desarrolladores |
| **`IMPLEMENTATION_SUMMARY.md`** | Resumen ejecutivo del estado de implementación de cada caso, métricas de cobertura y observabilidad. | Todos |
| **`SECURITY_CHECKLIST.md`** | ✅ Lista de verificación de seguridad completa: IAM, redes, cifrado, secretos, auditoría. | DevSecOps |
| **`IAM_SECURITY.md`** | Profundización en IAM: principio de mínimo privilegio, roles, políticas de confianza, OIDC. | DevSecOps |
| **`CODE_OF_CONDUCT.md`** | Normas de conducta de la comunidad. | Colaboradores |
| **`CONTRIBUTING.md`** | Copia local de la guía de contribución (también existe en root). | Colaboradores |
| **`killed.md`** | 🔐 Registro de secretos comprometidos y rotados. Documenta cuándo se filtraron y qué acciones se tomaron. | Seguridad |
| **`LICENSE`** | Copia local de la licencia MIT. | Legal |

---

## 🛠️ Directorio `scripts/` — Herramientas de Auditoría

Scripts ejecutables para mantenimiento y control de costos.

| Archivo | Descripción |
|---------|-------------|
| **`aws-resource-audit.sh`** | Script **Bash** (Linux/Mac). Escanea recursos activos en `us-east-1`, `us-east-2` y `sa-east-1`. Detecta EC2, NAT Gateways, EKS, ALBs, RDS, EBS sueltos y EIPs no asociadas. Se ejecuta con `make finops-check`. |
| **`aws-resource-audit.ps1`** | Script **PowerShell** (Windows). Versión equivalente del script de auditoría para entornos Windows. Misma cobertura de regiones y recursos. |

> 💡 Ambos scripts se invocan automáticamente desde el `Makefile` según el sistema operativo detectado.

---

## 🔧 Directorios de Plataforma

### `.devcontainer/` — Entorno Reproducible
| Archivo | Descripción |
|---------|-------------|
| `devcontainer.json` | Configuración de VS Code Dev Containers. Define la imagen Docker, extensiones y configuraciones para que el entorno sea idéntico en cualquier máquina. |
| `Dockerfile` | Imagen Docker personalizada con todas las herramientas preinstaladas (Terraform, AWS CLI, Node.js, Python, kubectl). |

### `.github/` — Automatización GitHub
| Archivo | Descripción |
|---------|-------------|
| `SECURITY.md` | Política de reporte de vulnerabilidades de seguridad. |
| `dependabot.yml` | Configuración de Dependabot para actualización automática de dependencias npm. |
| `PULL_REQUEST_TEMPLATE.md` | Template para Pull Requests con checklist de verificación. |
| `ISSUE_TEMPLATE/` | Templates para reportar bugs y solicitar features. |

### `.gitlab/` — Automatización GitLab
| Directorio | Descripción |
|------------|-------------|
| `issue_templates/` | Templates para Issues de GitLab. |
| `merge_request_templates/` | Templates para Merge Requests de GitLab. |

### `apps/` — Aplicaciones Auxiliares
| Directorio | Descripción |
|------------|-------------|
| `android/` | Placeholder para la versión Android de la PWA. |
| `ios/` | Placeholder para la versión iOS de la PWA. |

### `assets/` — Recursos Estáticos
| Directorio | Descripción |
|------------|-------------|
| `css/` | Hojas de estilo globales para el portal web. |
| `js/` | Scripts JavaScript compartidos (navegación, theme, etc.). |
| `icons/` | Íconos y favicons para la PWA. |

### `wiki/` — Wiki GitLab
| Archivo | Descripción |
|---------|-------------|
| `home.md` | Página principal de la Wiki de GitLab. Replica la estructura de documentación con enlaces absolutos a GitLab. Se sincroniza automáticamente con la Wiki del proyecto. |

---

## 📦 Casos de Estudio — Estructura Interna

Cada directorio `caso-X-*` es un **proyecto autocontenido**. Aquí la anatomía de cada uno:

### Caso A: `caso-a-amplify/` — AWS Amplify `Nivel 0`
| Archivo | Descripción |
|---------|-------------|
| `index.html` | Dashboard HTML principal de la aplicación web. |
| `styles.css` | Estilos de la aplicación. |
| `app.js` | Lógica JavaScript del dashboard. |
| `amplify.yml` | Configuración de build de Amplify. |
| `AWS_PASO_A_PASO.md` | Guía paso a paso para desplegar en AWS Amplify. |
| `assets/` | Imágenes y recursos del caso. |

### Caso B: `caso-b-gitlab-s3/` — S3 + GitLab CI `Nivel 1`
| Archivo | Descripción |
|---------|-------------|
| `index.html` | Dashboard web del caso. |
| `app.js` | Lógica JavaScript. |
| `.gitlab-ci.yml` | Pipeline CI/CD específico del caso (sync a S3). |
| `AWS_PASO_A_PASO.md` | Guía de creación del bucket S3 y configuración de hosting. |
| `assets/` | Recursos estáticos. |

### Caso C: `caso-c-terraform-s3/` — Terraform + CloudFront `Nivel 2`
| Archivo | Descripción |
|---------|-------------|
| `main.tf` | **Infraestructura principal**. Define S3, CloudFront, OAC y políticas. |
| `variables.tf` | Variables parametrizables de Terraform. |
| `outputs.tf` | Outputs (URL de CloudFront, ARN del bucket). |
| `versions.tf` | Restricciones de versión de Terraform y providers. |
| `.terraform.lock.hcl` | Lockfile de providers Terraform. |
| `website/` | Código fuente del sitio web desplegado. |
| `AWS_PASO_A_PASO.md` | Guía de despliegue con Terraform. |

### Caso D: `caso-d-serverless-basic/` — Serverless `Nivel 3`
| Archivo/Dir | Descripción |
|-------------|-------------|
| `backend/` | Código Lambda (Python/Node) y template SAM/CloudFormation. |
| `frontend/` | Aplicación web que consume la API. |
| `amplify.yml` | Configuración de build del frontend en Amplify. |
| `AWS_PASO_A_PASO.md` | Guía de despliegue de API Gateway + Lambda + DynamoDB. |

### Caso E: `caso-e-dynamodb-persistence/` — DynamoDB `Nivel 4` `COMPLETADO (VALIDADO)`
| Archivo/Dir | Descripción |
|-------------|-------------|
| `backend/template.yaml` | Infraestructura SAM para HTTP API, Lambda y tabla DynamoDB con GSIs. |
| `backend/src/app.py` | API Python que crea órdenes y resuelve consultas por cliente, estado y producto. |
| `backend/events/` | Eventos JSON de prueba para `sam local invoke`. |
| `frontend/` | Cliente HTML/JS local para crear órdenes y probar los patrones de acceso. |
| `docs/architecture.md` | Diagramas Mermaid del Single Table Design, la landing y los flujos de consulta. |
| `AWS_PASO_A_PASO.md` | Guía detallada para desplegar, probar y destruir el caso. |

### Caso G: `caso-g-event-driven/` — Event Driven `Nivel 6` `COMPLETADO (VALIDADO)`
| Archivo/Dir | Descripción |
|-------------|-------------|
| `backend/template.yaml` | Infraestructura SAM para HTTP API, EventBridge custom bus, SQS, DLQ, SNS y Lambdas. |
| `backend/src/app.py` | Lambda publicadora para `GET /`, `GET /health`, `POST /events/orders` y Lambda consumidora para mensajes SQS. |
| `backend/events/publish-order.json` | Evento de prueba para `sam local invoke`. |
| `index.html` | Landing local complementaria para publicar eventos y probar el endpoint del caso. |
| `docs/architecture.md` | Diagramas Mermaid del flujo asincrono, DLQ y contrato del evento. |
| `AWS_PASO_A_PASO.md` | Guia detallada para desplegar, validar, inspeccionar y destruir el caso. |

### Caso J: `caso-j-containers-ecs/` — Docker + ECS `Nivel 9`
| Archivo | Descripción |
|---------|-------------|
| `Dockerfile` | **Imagen Docker** de la API Node.js. Multi-stage build optimizado. |
| `docker-compose.yml` | Orquestación local para desarrollo. |
| `.dockerignore` | Archivos excluidos de la imagen Docker. |
| `server.js` | Código fuente del servidor Express.js. |
| `ecs-fargate-stack.yml` | CloudFormation stack para ECS Fargate (alternativa a Terraform). |
| `terraform/` | **IaC completa**: VPC, subnets, ALB, ECS cluster, task definitions, ECR. |
| `public/` | Assets estáticos servidos por la API. |
| `VISUALIZATION.md` | Reporte de screenshots y resultados del despliegue. |

### Caso K: `caso-k-kubernetes-eks/` — Kubernetes `Nivel 10`
| Archivo | Descripción |
|---------|-------------|
| `deployment.yaml` | **Manifiesto K8s**: Deployment + Service + LoadBalancer. |
| `app/` | Código fuente de la aplicación containerizada. |
| `terraform/` | IaC para el cluster EKS (VPC, subnets, node groups). |
| `VISUALIZATION.md` | Reporte de screenshots y resultados del cluster. |

### Caso L: `caso-l-finops-optimization/` — FinOps `Nivel 11`
| Archivo/Dir | Descripción |
|-------------|-------------|
| `app/` | Aplicación web del dashboard de costos (HTML/JS). |
| `img/` | Screenshots y evidencias del caso. |
| `AWS_PASO_A_PASO.md` | Guía exhaustiva: AWS Budgets, OIDC con GitLab, IAM Governance, S3+CloudFront. |

---

## 🔗 Navegación Rápida

| Necesitas... | Ve a... |
|:-------------|:--------|
| Empezar desde cero | [`README.md`](../README.md) |
| Instalar el entorno | [`docs/INSTALL.md`](./INSTALL.md) |
| Comandos rápidos | [`docs/QUICK_REFERENCE.md`](./QUICK_REFERENCE.md) |
| Auditar costos AWS | [`docs/FINOPS_MANUAL.md`](./FINOPS_MANUAL.md) |
| Entender la arquitectura | [`docs/ARCHITECTURE.md`](./ARCHITECTURE.md) |
| Revisar seguridad | [`docs/SECURITY_CHECKLIST.md`](./SECURITY_CHECKLIST.md) |
| Presentar a un reclutador | [`docs/RECRUITER.md`](./RECRUITER.md) |

---

> **Última actualización:** 2026-03-11
> **Mantenido por:** Vladimir Acuña
