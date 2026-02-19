# 📂 Estructura de Archivos del Sistema

Este documento proporciona una guía detallada sobre la estructura de archivos y directorios de este repositorio. Entender dónde está cada cosa es crucial para navegar y contribuir eficientemente al proyecto.

---

## 根 (Root)

Archivos y directorios en la raíz del proyecto.

### Archivos de Configuración y Documentación Principal

*   **`Makefile`**: ⚙️ **CRÍTICO**. Es el cerebro de la automatización del proyecto. Contiene comandos abreviados (`make install`, `make deploy`, `make help`) para ejecutar tareas complejas de forma sencilla. Es el punto de entrada recomendado para cualquier operación.
*   **`README.md`**: 📘 El punto de partida. Contiene la visión general del proyecto, los casos de estudio, instrucciones de inicio rápido y enlaces a toda la documentación relevante.
*   **`CHANGELOG.md`**: 🕒 Historial de cambios. Registra todas las modificaciones, nuevas características y correcciones realizadas en cada versión del proyecto.
*   **`ROADMAP.md`**: 🗺️ Hoja de ruta. Detalla los planes futuros, hitos pendientes y la dirección general del desarrollo del proyecto.
*   **`CONTRIBUTING.md`**: 🤝 Guía para colaboradores. Explica cómo proponer cambios, reportar errores y los estándares de código que se deben seguir.
*   **`LICENSE`**: ⚖️ Términos legales. Define bajo qué licencia se distribuye este software (MIT).
*   **`package.json`** y **`package-lock.json`**: 📦 Gestión de dependencias de Node.js. Define las librerías necesarias para el desarrollo frontend y scripts de NPM.
*   **`llms.txt`**: 🤖 Archivo de contexto para LLMs (Modelos de Lenguaje Grande), ayudando a la IA a entender mejor el proyecto.

### Directorios Principales

*   **`.github/`**: Automatización para GitHub. Contiene flujos de trabajo (Workflows) de GitHub Actions.
*   **`.gitlab/`**: Automatización para GitLab. Contiene plantillas y configuraciones específicas para los pipelines de GitLab CI/CD.
*   **`docs/`**: 📚 **Base de Conocimiento**. Contiene toda la documentación técnica detallada, manuales, guías de seguridad y especificaciones.
    *   *Ver sección detallada de `docs/` más abajo.*
*   **`scripts/`**: 🛠️ Herramientas y utilidades. Scripts en Bash, Python o PowerShell para tareas de mantenimiento, auditoría (como el script de FinOps) y despliegue.
*   **`wiki/`**: Documentación estilo Wiki, sincronizada con la Wiki de GitLab.
*   **`apps/`**: Código fuente de aplicaciones auxiliares o microservicios que no pertenecen a un caso específico.
*   **`assets/`**: Recursos estáticos como imágenes, diagramas y logotipos usados en la documentación y el portal web.

---

## 📚 Directorio `docs/`

Aquí reside la inteligencia del proyecto. Cada archivo tiene un propósito específico:

*   **`ARCHITECTURE.md`**: 🏗️ Visión técnica profunda. Diagramas de arquitectura, decisiones de diseño y stack tecnológico.
*   **`FINOPS_MANUAL.md`**: 💰 **IMPORTANTE**. Manual de FinOps. Explica cómo auditar costos, interpretar el semáforo de riesgo financiero y limpiar recursos para evitar cobros inesperados.
*   **`FILE_STRUCTURE.md`**: 📂 (Este archivo). Mapa de navegación del repositorio.
*   **`BEGINNERS_GUIDE.md`**: 🎓 Para novatos. Glosario de términos Cloud y DevOps, y conceptos fundamentales.
*   **`INSTALL.md`**: 🚀 Guía de instalación detallada. Pasos para configurar el entorno de desarrollo local (Docker vs Nativo).
*   **`QUICK_REFERENCE.md`**: ⚡ "Cheatsheet". Comandos rápidos y atajos para el día a día.
*   **`RECRUITER.md`**: 👔 Para reclutadores. Resumen ejecutivo del valor de negocio y habilidades demostradas en el proyecto.
*   **`SECURITY_CHECKLIST.md`**: ✅ Auditoría de seguridad. Lista de validación para asegurar que los despliegues cumplen con estándares de seguridad.
*   **`IAM_SECURITY.md`**: 🛡️ Profundización en IAM. Políticas, roles y mejores prácticas de gestión de identidad en AWS.
*   **`TECHNICAL_SPECS.md`**: 🛠️ Requisitos técnicos. Hardware y software necesario para ejecutar el proyecto.
*   **`TOOLING.md`**: 🔧 Explicación de las herramientas usadas (Terraform, Docker, AWS CLI, etc.) y por qué se eligieron.
*   **`IMPLEMENTATION_SUMMARY.md`**: Resumen del estado de implementación de los diferentes módulos.

---

## 📂 Directorios de Casos de Estudio (`caso-X-...`)

El núcleo educativo del monorepo. Cada directorio (`caso-a`, `caso-b`, etc.) es un proyecto autocontenido que enseña una habilidad específica de AWS/DevOps.

*   **Estructura típica de un caso**:
    *   `README.md`: Explicación específica del caso.
    *   `AWS_PASO_A_PASO.md`: Guía detallada para reproducir el caso manualmente en la consola de AWS.
    *   `main.tf` / `template.yaml`: Código de Infraestructura (Terraform o CloudFormation/SAM).
    *   Código Fuente: Archivos HTML, JS, Python, etc., de la aplicación de ejemplo.

---

> **Nota**: Mantener esta estructura limpia y ordenada es vital para la escalabilidad del proyecto. Si añades nuevos archivos, asegúrate de documentarlos aquí.
