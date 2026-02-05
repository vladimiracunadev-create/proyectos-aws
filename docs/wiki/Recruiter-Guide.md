# 👨‍💼 Guía para Reclutadores / Empresas

Este repositorio no es solo una colección de archivos; es un **ecosistema de ingeniería** diseñado para demostrar cómo manejo entornos de producción reales, seguridad y escalabilidad.

## 🌟 Valor de Negocio

1. **Reducción de Riesgos:** Implementación de pipelines de seguridad (SAST, Secret Scanning) que previenen fugas de datos antes de que lleguen a producción.
2. **Time-to-Market (TTM):** Flujo de trabajo `dev -> PR -> main` automatizado, permitiendo despliegues continuos y confiables en AWS S3 y Amplify.
3. **Eficiencia de Costos:** Uso de servicios Serverless (S3, Amplify) y orquestación ligera con Kubernetes para optimizar recursos.

## 🛠️ Destacados Técnicos

### 1. CI/CD y Automatización Profesional
- **GitHub Actions:** Workflows complejos que incluyen validación de sintaxis, escaneo de secretos con TruffleHog y despliegues automáticos.
- **Makefile & Hub CLI:** Capa de abstracción que estandariza las operaciones del desarrollador, facilitando el onboarding de nuevos miembros.

### 2. Seguridad por Diseño (Security by Design)
- **Zero Trust Local:** Uso de pre-commit hooks para evitar que secretos sigan el flujo hacia el servidor.
- **Identidad Moderna:** Configuración de AWS OIDC para eliminar el uso de IAM Access Keys permanentes en la nube.
- **K8S Hardening:** Manifiestos con `securityContext` restrictivo y `NetworkPolicies` para aislar cargas de trabajo.

### 3. Portabilidad y Contenedores
- **Docker-first:** Todo el tooling está encapsulado para garantizar que "funcione en mi máquina" y en el servidor de la misma forma.

---

## 🧭 Tour de "Casos de Éxito"

- **Despliegue Web Dinámico:** Ver [aws-amplify-mi-sitio-1/](file:///c:/proyectos-aws/aws-amplify-mi-sitio-1)
- **Infraestructura como Código:** Ver configuración en [.github/workflows/](file:///c:/proyectos-aws/.github/workflows)
- **Políticas de Seguridad:** Ver [SECURITY.md](file:///c:/proyectos-aws/SECURITY.md) y [docs/killed.md](file:///c:/proyectos-aws/docs/killed.md)

---
*Este proyecto demuestra no solo que sé codificar, sino que entiendo el ciclo de vida completo de una aplicación profesional.*
