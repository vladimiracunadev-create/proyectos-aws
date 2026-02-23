# 🏉 AWS S3 Scrum Portfolio

Portafolio profesional optimizado para despliegue estático en **AWS S3** utilizando **GitHub Actions** para la automatización total. Este proyecto demuestra una arquitectura de CI/CD moderna aprovechando **OIDC** para mayor seguridad.

## ✨ Características

- **Arquitectura Estática:** Servido directamente desde un bucket S3 para máximo rendimiento y bajo costo.
- **CI/CD Automatizado:** Sincronización inteligente con `aws s3 sync`.
- **PWA Integrada:** Manifiesto y modo offline completo.
- **Multilingüe:** Interfaz conmutable entre Español e Inglés.
- **Seguridad:** Despliegue sin credenciales estáticas (Keyless) mediante GitHub OIDC.

## 🛠️ Stack Tecnológico

- **Frontend:** HTML5 semántico, CSS3 avanzado y JavaScript (Vanilla).
- **Automatización:** GitHub Actions (YAML).
- **Infraestructura:** AWS S3 (Hosting), AWS IAM (OIDC).

## 📂 Estructura

- `index.html`: Estructura principal optimizada para SEO.
- `styles.css`: Estilos modernos con variables y diseño responsivo.
- `app.js`: Lógica de interacción y traducción.
- `assets/`: Recursos multimedia y documentos estratégicos.
- `service-worker.js`: Estrategias de caché para PWA.

## 🚀 Despliegue

Este proyecto se despliega automáticamente en el bucket S3 configurado al realizar un push a la rama `main`. El flujo está definido en `.github/workflows/despliegue.yml` en la raíz del monorepo.

Para configurar la infraestructura en AWS, lee [AWS_PASO_A_PASO.md](./AWS_PASO_A_PASO.md).
