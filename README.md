# 🚀 Cloud Portfolio: Proyectos AWS (Monorepo)

Monorepo con **arquitecturas y despliegues reales en AWS**, enfocado en demostrar prácticas modernas de **CI/CD**, manejo de **entornos por rama**, y documentación de **infraestructura cloud**.

> Objetivo: mostrar implementación **real y trazable** (Local → GitHub → AWS), con enfoque de portafolio profesional.

---

## 🌐 Demos en Vivo (abren en otra pestaña)

### 1️⃣ AWS S3 + GitHub Actions (Despliegue Automatizado)
*Sitio estático desplegado automáticamente al detectar cambios en `main` dentro de la carpeta del proyecto.*
- **Estado:** ✅ Operativo  
- **Tecnologías:** S3, IAM, GitHub Actions (YAML)  
- **Carpeta:** `aws-s3-scrum-mi-sitio-1/`  
- 🔗 <a href="https://mi-pagina-scrum-123.s3.us-east-2.amazonaws.com/index.html" target="_blank" rel="noopener noreferrer">Ver Demo en S3</a>

### 2️⃣ AWS Amplify - Continuous Deployment
*Hosting con despliegue por rama (`main` / `dev`) y SSL automático.*
- **Estado:** ✅ Operativo  
- **Tecnologías:** AWS Amplify Console  
- **Carpeta:** `aws-amplify-mi-sitio-1/`  
- 🔗 <a href="https://main.d3r1wuymolxagh.amplifyapp.com/" target="_blank" rel="noopener noreferrer">Demo Rama Main</a>  
- 🔗 <a href="https://dev.d20m8tc0banvg.amplifyapp.com/" target="_blank" rel="noopener noreferrer">Demo Rama Dev</a>  

---

## ✅ Cambios Profesionales en 3 Niveles (Local → GitHub → AWS)

Este repo permite actualizar de manera **profesional y trazable**:

1. **Local (VS Code):** editas y validas cambios.
2. **GitHub:** trabajas en `dev`, haces commits y creas **Pull Request** a `main`.
3. **AWS:**
   - **Amplify** despliega automáticamente por rama (`dev` / `main`).
   - **S3 + GitHub Actions** mantiene el bucket sincronizado (según workflow configurado).

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
