# 🌐 AWS Amplify Portfolio

Este subproyecto contiene el portafolio profesional de Vladimir Acuña, diseñado para ser desplegado de forma continua utilizando **AWS Amplify Console**. Es una Single Page Application (SPA) con capacidades de **PWA (Progressive Web App)**.

## ✨ Características Industriales

- **📈 Observabilidad:** Integración de Google Analytics y logs de build en Amplify Console para monitoreo de salud.
- **💰 FinOps Ready:** Configurado para monitoreo a través de AWS Budgets a nivel de aplicación.
- **🛡️ Resiliencia PWA:** Service Workers con estrategias de caché agresivas para garantizar disponibilidad offline.
- **🚀 CI/CD Atómico:** Despliegues inmutables con rollback instantáneo en caso de fallos.

## 🛠️ Stack Tecnológico

- **Frontend:** Vanilla HTML5, CSS3 y JavaScript moderno.
- **PWA:** Web Manifest y Service Workers personalizados.
- **Infraestructura:** AWS Amplify (Hosting, CI/CD, SSL).

## 📂 Estructura

- `index.html`: Punto de entrada principal con estructura semántica.
- `styles.css`: Sistema de diseño basado en variables y flexbox/grid.
- `app.js`: Lógica de la interfaz, cambio de idiomas y vistas.
- `pwa.js`: Gestión del ciclo de vida de la PWA.
- `assets/`: Activos visuales y documentos PDF (CV, portafolio).

## 🚀 Despliegue

Este proyecto se despliega automáticamente en AWS Amplify al realizar un push a las ramas `main` (producción) o `dev` (staging).

Para más detalles sobre la configuración en AWS, consulta [AWS_PASO_A_PASO.md](./AWS_PASO_A_PASO.md).
