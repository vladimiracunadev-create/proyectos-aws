# 🚀 Cloud Portfolio: Proyectos AWS (Monorepo)

**Monorepo de portafolio con despliegues reales en AWS** para demostrar prácticas modernas de **CI/CD**, separación de **entornos por rama**, y documentación clara de infraestructura.

**TL;DR (30s):**
- ✅ CI/CD real: cambios en Git → despliegue automático (S3 + GitHub Actions / Amplify por ramas)
- ✅ Trabajo profesional con `dev → PR → main` y trazabilidad completa
- ✅ Enfoque de portafolio: documentación + demos + estructura lista para crecer

---

## 🌐 Demos en Vivo

### 1) AWS S3 + GitHub Actions (Deploy Automatizado)
- **Estado:** ✅ Operativo  
- **Stack:** S3, IAM, GitHub Actions (YAML)  
- **Carpeta:** `aws-s3-scrum-mi-sitio-1/`  
- **Demo:** https://mi-pagina-scrum-123.s3.us-east-2.amazonaws.com/index.html

### 2) AWS Amplify – Continuous Deployment por Rama
- **Estado:** ✅ Operativo  
- **Stack:** AWS Amplify Console, SSL automático  
- **Carpeta:** `aws-amplify-mi-sitio-1/`  
- **Demo Main:** https://main.d3r1wuymolxagh.amplifyapp.com/  
- **Demo Dev:**  https://dev.d20m8tc0banvg.amplifyapp.com/

---

## 🧭 Flujo Profesional (Local → GitHub → AWS)

1. **Local (VS Code):** editas, pruebas y validas cambios.
2. **GitHub:** trabajas en `dev`, haces commits y creas **Pull Request** a `main`.
3. **AWS:**
   - **Amplify** despliega automáticamente por rama (`dev` / `main`).
   - **S3 + GitHub Actions** sincroniza el bucket desde `main` según workflow.

---

## 🏗️ Arquitectura (alto nivel)

```mermaid
flowchart LR
  A[Dev local] --> B[GitHub repo]
  B -->|PR dev → main| C[Branch main]
  C --> D[GitHub Actions]
  D --> E[(S3 Bucket)]
  B --> F[Amplify Console]
  F --> G[Deploy main]
  F --> H[Deploy dev]

