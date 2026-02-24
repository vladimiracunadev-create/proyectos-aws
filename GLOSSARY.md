# 📖 Glosario Técnico

Este glosario define los términos y conceptos clave utilizados en este ecosistema para asegurar una comprensión uniforme entre desarrolladores y reclutadores.

---

## ☁️ Infraestructura y Nube (AWS)

- **Amplify Console**: Servicio de AWS para el despliegue continuo de aplicaciones web modernas (SPA/SSR).
- **S3 (Simple Storage Service)**: Servicio de almacenamiento de objetos, utilizado aquí para Hosting Estático.
- **OIDC (OpenID Connect)**: Protocolo de identidad que permite a GitHub Actions obtener credenciales temporales de AWS sin llaves estáticas.
- **Drift (Deriva)**: Cuando la infraestructura real en la nube difiere de lo definido en el código (IaC).

---

## 🤖 DevOps y CI/CD

- **SAST (Static Application Security Testing)**: Análisis del código fuente antes de la ejecución para encontrar vulnerabilidades.
- **Secret Scanning**: Proceso automático de búsqueda de llaves API o tokens en el historial de Git (TruffleHog/detect-secrets).
- **Inmutabilidad**: Concepto donde los despliegues no se modifican una vez realizados; se crea una nueva versión (ej. Blue/Green).
- **Drift Detection**: El proceso de monitorear si la configuración de AWS ha cambiado manualmente fuera de los flujos de automatización.

---

## 📈 Negocio y Gobernanza

- **FinOps**: Práctica de gestión financiera en la nube para optimizar costos y maximizar el valor de negocio.
- **DX (Developer Experience)**: El sentimiento y la eficiencia de un desarrollador al interactuar con el sistema, herramientas y documentación.
- **SDLC (Software Development Life Cycle)**: El proceso completo de planificación, creación, prueba y despliegue del software.

---

## 📱 Web & PWA

- **Service Worker**: Script que corre en segundo plano en el navegador, permitiendo funcionalidades offline y caché inteligente.
- **SPA (Single Page Application)**: Aplicación web que carga una sola página y actualiza el contenido dinámicamente.
- **Glassmorphism**: Estilo de diseño basado en transparencias y desenfoques, utilizado en este portafolio.

---
*Para términos específicos de arquitectura local, consulta [FILE_ARCHITECTURE.md](./FILE_ARCHITECTURE.md).*
