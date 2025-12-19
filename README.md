# 🚀 Cloud Portfolio: Proyectos AWS (Monorepo)

Este repositorio es un **Monorepo** que agrupa arquitecturas y despliegues reales en Amazon Web Services. El objetivo es documentar la implementación de soluciones cloud, desde hosting estático hasta infraestructura como código.

---

## 🌐 Demos en Vivo

### 1️⃣ AWS S3 + GitHub Actions (Despliegue Automatizado)
*Despliegue de sitio estático con automatización completa cada vez que se detectan cambios en la rama main.*
- **Estado:** ✅ Operativo
- **Tecnologías:** S3, IAM, GitHub Actions (YAML)
- **Carpeta:** `aws-s3-scrum-mi-sitio-1/`
- **🔗 [Ver Demo en S3](https://mi-pagina-scrum-123.s3.us-east-2.amazonaws.com/index.html)**

### 2️⃣ AWS Amplify - Continuous Deployment
*Hosting optimizado con manejo de ramas (main/dev) y certificado SSL automático.*
- **Estado:** ✅ Operativo
- **Tecnologías:** AWS Amplify Console
- **Carpeta:** `aws-amplify-mi-sitio-1/`
- **🔗 [Demo Rama Main](https://main.d3r1wuymolxagh.amplifyapp.com/)**
- **🔗 [Demo Rama Dev](https://dev.d20m8tc0banvg.amplifyapp.com/)**

---

## 🛠️ Estructura del Proyecto

```text
.
├── .github/workflows/          # Automatización (GitHub Actions)
├── aws-s3-scrum-mi-sitio-1/    # Sitio 1: S3 + CI/CD
├── aws-amplify-mi-sitio-1/     # Sitio 2: Amplify CI/CD
├── aws-lambda-api-1/           # (En desarrollo) Serverless API
├── aws-ec2-docker-lab/         # (Pendiente) Contenedores
└── infra-terraform/            # (Pendiente) IaC

## ⚙️ Pipeline de Automatización (DevOps)

Este repositorio utiliza **CI/CD (Integración y Despliegue Continuo)** para eliminar la carga manual de subir archivos a la nube.

### Flujo de Trabajo:
1. **Detección de Cambios:** El flujo se activa automáticamente cada vez que se hace un `git push` a la rama `main`, pero solo si hay cambios dentro de la carpeta del proyecto.
2. **Entorno Seguro:** Se levanta un contenedor temporal con **Ubuntu Latest** en los servidores de GitHub.
3. **Autenticación:** El proceso utiliza **GitHub Secrets** para manejar las llaves de acceso de AWS (`Access Key ID` y `Secret Access Key`) de forma cifrada y segura.
4. **Sincronización Inteligente:** Se utiliza el comando `aws s3 sync` con el parámetro `--delete`. Esto garantiza que el Bucket de S3 sea un espejo exacto del repositorio (si borras un archivo en Git, se borra en S3).

**Beneficio:** Reducción de errores humanos y despliegue inmediato en menos de 1 minuto.
