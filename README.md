# GitLab → AWS Monorepo (DevOps Training Suite) ☁️ 🚀

[![Infrastructure-AWS](https://img.shields.io/badge/infrastructure-AWS-orange?style=for-the-badge&logo=amazon-aws)]()
[![Pipeline-GitLab](https://img.shields.io/badge/pipeline-GitLab_CI-6C4DE6?style=for-the-badge&logo=gitlab)](https://gitlab.com/vladimir.acuna.dev-group/proyectos-aws-gitlab/-/pipelines)
[![IaC-Terraform](https://img.shields.io/badge/IaC-Terraform-844FBA?style=for-the-badge&logo=terraform)]()
[![Container-Docker](https://img.shields.io/badge/Container-Docker-2496ED?style=for-the-badge&logo=docker)]()
[![Orchestrator-K8s](https://img.shields.io/badge/Orchestrator-K8s-326CE5?style=for-the-badge&logo=kubernetes)]()

Este monorepo es una suite educativa avanzada diseñada para modernizar y automatizar el flujo de despliegue en la nube. Desde el alojamiento estático hasta la orquestación industrial de contenedores, exploramos cómo construir infraestructuras seguras, escalables y auditables.

---

## ⚡ Inicio Inmediato (Quick Start)

Este proyecto incluye un **Makefile** para simplificar tus tareas. No necesitas memorizar comandos largos.

```bash
# 1. Instalar todo lo necesario
make install

# 2. Verificar calidad y seguridad
make lint
make tf-security

# 3. Ver todos los comandos disponibles
make help
```

---

## 📖 Documentación Avanzada
Hemos organizado la base de conocimientos para que sea fácil de navegar:

- 🏗️ **[Arquitectura](./docs/ARCHITECTURE.md)**: Visión técnica, diagramas Mermaid y stack.
- 🚀 **[Guía de Instalación](./docs/INSTALL.md)**: Docker (DevContainers) vs Manual.
- 🛠️ **[Especificaciones Técnicas](./docs/TECHNICAL_SPECS.md)**: Requerimientos de hardware y software.
- 🛡️ **[Seguridad IAM](./docs/IAM_SECURITY.md)**: Políticas de acceso y privilegios mínimos.
- 📘 **[Guía para Principiantes](./docs/BEGINNERS_GUIDE.md)**: Glosario y conceptos básicos.

---

## 🗺️ Roadmap de Aprendizaje (Casos de Estudio)

Cada carpeta en este repositorio representa un hito en la evolución de un Ingeniero Cloud. A continuación, el detalle de cada módulo:

### 🟢 Nivel 1: Cimientos y Automatización Básica

#### [📂 Caso A: AWS Amplify](./caso-a-amplify/) `Nivel 0`
*   **Stack**: AWS Amplify + GitLab Mirroring.
*   **Enfoque**: **Integración Continua nativa.** Ideal para prototipos rápidos. Aprende cómo AWS gestiona automáticamente el escalado, SSL y CDN sin configurar servidores.
*   👉 **[Ver Demo en Vivo](https://main.d1uybq9oui7h8c.amplifyapp.com/)**

#### [📂 Caso B: S3 + GitLab CI](./caso-b-gitlab-s3/) `Nivel 1`
*   **Stack**: GitLab Runners AWS CLI + S3 Website Hosting.
*   **Enfoque**: **Pipelines artesanales.** Entiende cómo funcionan los procesos por debajo. Aprendes sobre buckets públicos vs privados, sincronización de archivos (`aws s3 sync`) y gestión de secretos en GitLab.
*   👉 **[Ver Demo en Vivo](http://vladimir-caso-b-site-2026.s3-website.us-east-2.amazonaws.com/)**

### 🔵 Nivel 2: Profesionalización e Infraestructura como Código (IaC)

#### [📂 Caso C: Terraform + CloudFront](./caso-c-terraform-s3/) `Nivel 2`
*   **Stack**: Terraform + S3 (OAC) + CloudFront + Remote Backend.
*   **Enfoque**: **Infraestructura como Código Profesional.** Elimina el ClickOps. Aprende a compartir el estado de la infraestructura entre el PC y la nube, y a proteger tus recursos con **Origin Access Control**.
*   👉 **[Ver Demo en Vivo](https://d3otfpeykrm536.cloudfront.net/)**

#### [📂 Caso D: Serverless Basic (SAM)](./caso-d-serverless-basic/) `Nivel 3`
*   **Stack**: API Gateway + AWS Lambda (Python/JS) + DynamoDB.
*   **Enfoque**: **Lógica Backend y Persistencia.** Añade vida a tus aplicaciones. Aprende a usar el modelo de aplicaciones serverless para manejar datos sin servidores encendidos 24/7.
*   👉 **[Demo Portafolio](https://staging.d3oq987bpa7ls7.amplifyapp.com/)** / **[Endpoint de API](https://tc78a6xibg.execute-api.us-east-2.amazonaws.com)**

### 🟠 Nivel 3: Contenedores y Escalamiento Industrial

#### [📂 Caso G: Dockerización (Microservicios)](./caso-g-containers-ecs/) `Nivel 4`
*   **Stack**: Docker + Node.js Express API.
*   **Enfoque**: **Portabilidad Total.** Aprende a empaquetar tus aplicaciones con todas sus dependencias. El estándar para despliegues modernos que deben funcionar igual en cualquier máquina o nube.

#### [📂 Caso K: Kubernetes (EKS/Local)](./caso-k-kubernetes-eks/) `Nivel 5`
*   **Stack**: K8s Manifests + Services + Deployments.
*   **Enfoque**: **Orquestación de Flotas.** Si Docker es el contenedor, Kubernetes es el Capitán. Aprende a gestionar alta disponibilidad, auto-recuperación y balanceo de carga masivo.

---

## 🤝 Comunidad y Contribución
¡Este proyecto está abierto a mejora continua! Revisa nuestras **[Normas de Conducta](./docs/CODE_OF_CONDUCT.md)** y la **[Guía de Contribución](./docs/CONTRIBUTING.md)**.

---
> **Construido con ❤️ por Vladimir Acuña — Optimizado para Ingeniería Cloud Senior.**
