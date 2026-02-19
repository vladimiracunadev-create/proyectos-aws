# 🛠️ Tooling & Herramientas

Este proyecto utiliza un conjunto de herramientas estándar para garantizar la calidad, seguridad y despliegue consistente de la infraestructura y aplicaciones.

---

## 🚀 Core Tools

### 1. GNU Make
Centralizamos la ejecución de comandos en el `Makefile`. Esto permite tener una interfaz unificada para todas las tareas.

**Comandos Principales:**
- `make help`: Muestra la ayuda con todos los comandos disponibles.
- `make install`: Instala dependencias del proyecto.
- `make lint`: Ejecuta verificaciones de calidad de código.
- `make format`: Formatea el código automáticamente.

### 2. Node.js & NPM
Utilizado para el ecosistema de frontend y herramientas de desarrollo.
- **Versión**: LTS recomedada.
- **Configuración**: `package.json` define los scripts y dependencias.

---

## ☁️ Infraestructura como Código (IaC)

### 3. Terraform
Gestionamos la infraestructura de AWS de manera declarativa.
- **Directorios**: `caso-c-terraform-s3`, `caso-j-containers-ecs/terraform`, etc.
- **Workflow estándar**: `terraform init` -> `terraform plan` -> `terraform apply`.

**Comandos Make:**
- `make tf-init`, `make tf-plan`, `make tf-apply` (para Caso C).
- `make case-j-init`, `make case-j-plan`, `make case-j-apply` (para Caso J).

### 4. AWS CLI
Interfaz de línea de comandos para interactuar con los servicios de AWS.
- Debe estar configurado con `aws configure` antes de ejecutar despliegues.

---

## 🐳 Contenedores

### 5. Docker
Utilizado para empaquetar aplicaciones y garantizar portabilidad.
- **Caso J**: Se usa Docker para construir la imagen de la API y desplegarla en ECS Fargate.
- **Comandos**: `make docker-build`, `make docker-login`, `make docker-push`.

---

## 🛡️ Calidad y Seguridad

### 6. Linters & Formatters
- **ESLint**: Para análisis estático de código JavaScript.
- **Prettier**: Para formateo consistente de código.
- **HTMLHint**: Para validar archivos HTML.
- **Markdownlint**: Para asegurar la consistencia en la documentación.

### 7. Seguridad
- **tfsec**: Escaneo estático de seguridad para código Terraform (`make tf-security`).
- **gitleaks**: Detección de secretos en el código.
- **npm audit**: Auditoría de vulnerabilidades en dependencias.

---

## 📈 Gestión de Almacenamiento (CI/CD)

Para optimizar el uso de cuotas en GitLab SaaS, implementamos una estrategia de **Limpieza Proactiva**:

1.  **Expiración de Artefactos**: Los artefactos generados (como el portal `public/` o planes de Terraform) se configuran con `expire_in: 1 day`. Esto evita acumular gigabytes de archivos históricos innecesarios.
2.  **Optimización de Caché**: Usamos claves de caché dinámicas (`node_modules`) con políticas `pull-push` para minimizar la redundancia de datos entre ejecuciones.
3.  **Monitoreo**: Se recomienda revisar periódicamente **Usage Quotas** en GitLab para identificar artefactos huérfanos o crecimientos inesperados.

---

## 💻 Scripts Operativos
Este monorepo incluye herramientas personalizadas para el mantenimiento diario:

### 8. Auditoría de Costos (FinOps)
Herramienta Cross-Platform (PowerShell/Bash) para escanear recursos activos en múltiples regiones.
- **Comando**: `make finops-check`
- **Ubicación**: `scripts/aws-resource-audit.ps1` (Windows) y `scripts/aws-resource-audit.sh` (Linux/Mac).
- **Cobertura**: EC2, RDS, EKS, ECS, NAT Gateways, ALBs.

---

## 📦 Estructura del Proyecto

El proyecto sigue una estructura de monorepo donde cada "Caso" (A, B, C...) tiene su propio directorio, pero comparten herramientas comunes en la raíz.
