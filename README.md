# GitLab → AWS Monorepo (DevOps Training Suite) ☁️ 🚀

[![Infrastructure-AWS](https://img.shields.io/badge/infrastructure-AWS-orange?style=for-the-badge&logo=amazon-aws)]()
[![Pipeline-GitLab](https://img.shields.io/badge/pipeline-GitLab_CI-6C4DE6?style=for-the-badge&logo=gitlab)](https://gitlab.com/vladimir.acuna.dev-group/proyectos-aws-gitlab/-/pipelines)
[![IaC-Terraform](https://img.shields.io/badge/IaC-Terraform-844FBA?style=for-the-badge&logo=terraform)]()
[![Container-Docker](https://img.shields.io/badge/Container-Docker-2496ED?style=for-the-badge&logo=docker)]()
[![Orchestrator-K8s](https://img.shields.io/badge/Orchestrator-K8s-326CE5?style=for-the-badge&logo=kubernetes)]()

Este monorepo es una suite educativa avanzada diseñada para modernizar y automatizar el flujo de despliegue en la nube. Desde el alojamiento estático hasta la orquestación industrial de contenedores.

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

| Caso | Nivel | Stack | Objetivo y Demo |
| :--- | :--- | :--- | :--- |
| **[Caso A](./caso-a-amplify/)** | 🐣 | Amplify | **ClickOps y Velocidad.** Despliegue en 5 min. <br> 👉 [Ver Demo](https://main.d1uybq9oui7h8c.amplifyapp.com/) |
| **[Caso B](./caso-b-gitlab-s3/)** | 🛠️ | S3 + GitLab | **Automatización básica.** Entender pipelines y buckets. <br> 👉 [Ver Demo](http://vladimir-caso-b-site-2026.s3-website.us-east-2.amazonaws.com/) |
| **[Caso C](./caso-c-terraform-s3/)** | 🏗️ | Terraform | **Infraestructura como Código (IaC).** Profesionalización. <br> 👉 [Ver Demo](https://d3otfpeykrm536.cloudfront.net/) |
| **[Caso D](./caso-d-serverless-basic/)** | ⚡ | SAM / Lambda | **Lógica Serverless dinámica.** Backend sin servidores. <br> 👉 [Portafolio](https://staging.d3oq987bpa7ls7.amplifyapp.com/) / [API](https://tc78a6xibg.execute-api.us-east-2.amazonaws.com) |
| **[Caso G](./caso-g-containers-ecs/)** | 🐳 | Docker | **Empaquetado industrial.** Microservicios escalables. <br> *(Infra proyectada)* |
| **[Caso K](./caso-k-kubernetes-eks/)** | ☸️ | Kubernetes | **Orquestación y Alta Disponibilidad.** Flotas de apps. <br> *(Infra proyectada)* |

---

## 🤝 Comunidad y Contribución
¡Este proyecto está abierto a mejora continua! Revisa nuestras **[Normas de Conducta](./docs/CODE_OF_CONDUCT.md)** y la **[Guía de Contribución](./docs/CONTRIBUTING.md)**.

---
> **Construido con ❤️ por Vladimir Acuña — Optimizado para Ingeniería Cloud Senior.**
