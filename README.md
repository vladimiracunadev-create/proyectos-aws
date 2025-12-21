# 🚀 Cloud Portfolio: Proyectos AWS (Monorepo)

Este repositorio es un **Monorepo** que agrupa arquitecturas y despliegues reales en Amazon Web Services.  
El objetivo es documentar la implementación de soluciones cloud, desde hosting estático hasta infraestructura como código, aplicando un flujo de trabajo profesional (dev → PR → main + CI/CD).

---

## ✅ Cambios Profesionales en 3 Niveles (Local → GitHub → AWS)

Este repositorio permite realizar actualizaciones de forma **ordenada y profesional** en los **tres niveles** del ciclo de despliegue:

1. **Local (VS Code):** actualización de archivos y pruebas rápidas.
2. **GitHub (Control de versiones):** commits en rama `dev`, validación y **Pull Request** hacia `main`.
3. **AWS (Publicación automática):**
   - **Amplify** despliega por rama (`main` / `dev`) con CI/CD.
   - **S3 + GitHub Actions** sincroniza el contenido del bucket automáticamente.

**Resultado:** cambios visibles en los entornos correspondientes sin depender de subir ZIP manualmente, con trazabilidad y buenas prácticas (PR + despliegue automático).

---

## 🌐 Demos en Vivo (se abren en otra pestaña)

### 1️⃣ AWS S3 + GitHub Actions (Despliegue Automatizado)
*Despliegue de sitio estático con automatización completa cada vez que se detectan cambios en la rama `main`.*
- **Estado:** ✅ Operativo  
- **Tecnologías:** S3, IAM, GitHub Actions (YAML)  
- **Carpeta:** `aws-s3-scrum-mi-sitio-1/`  
- 🔗 <a href="https://mi-pagina-scrum-123.s3.us-east-2.amazonaws.com/index.html" target="_blank" rel="noopener noreferrer">Ver Demo en S3</a>

### 2️⃣ AWS Amplify - Continuous Deployment
*Hosting optimizado con manejo de ramas (`main`/`dev`) y certificado SSL automático.*
- **Estado:** ✅ Operativo  
- **Tecnologías:** AWS Amplify Console  
- **Carpeta:** `aws-amplify-mi-sitio-1/`  
- 🔗 <a href="https://main.d3r1wuymolxagh.amplifyapp.com/" target="_blank" rel="noopener noreferrer">Demo Rama Main</a>  
- 🔗 <a href="https://dev.d20m8tc0banvg.amplifyapp.com/" target="_blank" rel="noopener noreferrer">Demo Rama Dev</a>  

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

