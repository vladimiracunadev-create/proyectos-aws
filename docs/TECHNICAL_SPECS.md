# 📋 Especificaciones Técnicas y Requerimientos

Este documento detalla qué necesitas para que este proyecto funcione en cualquier máquina y cómo está configurada la seguridad.

---

## 💻 Requerimientos de Hardware

### Mínimos
- **Sistema Operativo**: Windows 10/11, macOS 11+ o Linux (Ubuntu 20.04+).
- **Procesador**: 2 núcleos (Dual Core).
- **Memoria RAM**: 4 GB.
- **Conectividad**: Acceso a Internet (para descarga de proveedores de AWS y subida de archivos).

### Recomendados (Máximos para este laboratorio)
- **Sistema Operativo**: Linux (Debian/Ubuntu) o macOS.
- **Procesador**: 4 núcleos o más.
- **Memoria RAM**: 8 GB o superior.
- **Espacio en Disco**: 1 GB libre (para `node_modules` y archivos temporales de Terraform).

---

## 🛠️ Requerimientos de Software

Para ejecutar este proyecto, debes tener instalado:

1.  **Git**: Para clonar el repositorio y gestionar versiones.
2.  **Node.js (LTS)**: Versión 18.x o superior.
3.  **AWS CLI**: Configurado con credenciales válidas.
4.  **Terraform**: Versión 1.14.0 o superior.
5.  **Docker Desktop**: Necesario para construir imágenes (Caso J) y el entorno de desarrollo.
6.  **Express.js**: Utilizado como servidor de aplicaciones en el Caso J para servir contenido estático y APIs.
7.  **Kubectl**: Para gestionar el orquestador (Caso K).
7.  **Make**:
    *   **Linux/macOS**: Suele venir preinstalado.
    *   **Windows**: Instalar vía [Chocolatey](https://community.chocolatey.org/packages/make) (`choco install make`) o usar mediante Git Bash/WSL.

---

## 🔑 Características de los Accesos (IAM)

El usuario que ejecute este proyecto (ya sea tú en tu PC o GitLab en el pipeline) debe tener **al menos** estos permisos en AWS:

### 1. S3 Management
- `s3:CreateBucket`
- `s3:ListBucket`
- `s3:PutObject`
- `s3:GetObject`
- `s3:DeleteObject`
- `s3:PutBucketPolicy`

### 2. CloudFront Management (Caso C)
- `cloudfront:CreateDistribution`
- `cloudfront:UpdateDistribution`
- `cloudfront:CreateOriginAccessControl`
- `cloudfront:CreateInvalidation`

### 3. Terraform State
- Acceso de lectura/escritura al bucket de estado global: `vladimir-terraform-state-2026`.

---

## 🚀 Portabilidad (Instalación en otra máquina)

Para levantar este proyecto en una máquina nueva, sigue estos pasos desde la terminal:

```bash
# 1. Clonar el repositorio
git clone <url-del-repo>
cd proyectos-aws-gitlab

# 2. Instalar herramientas de calidad y dependencias
make install

# 3. Configurar tus credenciales de AWS
aws configure

# 4. Inicializar infraestructura
make tf-init

# 5. Ejecutar análisis de calidad
make lint
```

Con una sola herramienta (`make`), puedes gestionar todo el ciclo de vida sin recordar comandos largos.
