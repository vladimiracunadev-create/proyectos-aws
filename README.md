# GitLab → AWS Monorepo (DevOps Training Suite) ☁️ 🚀

[![Infrastructure-AWS](https://img.shields.io/badge/infrastructure-AWS-orange?style=for-the-badge&logo=amazon-aws)]()
[![Pipeline-GitLab](https://img.shields.io/badge/pipeline-GitLab_CI-6C4DE6?style=for-the-badge&logo=gitlab)](https://gitlab.com/vladimir.acuna.dev-group/proyectos-aws-gitlab/-/pipelines)
[![IaC-Terraform](https://img.shields.io/badge/IaC-Terraform-844FBA?style=for-the-badge&logo=terraform)]()
[![Container-Docker](https://img.shields.io/badge/Container-Docker-2496ED?style=for-the-badge&logo=docker)]()
[![Orchestrator-K8s](https://img.shields.io/badge/Orchestrator-K8s-326CE5?style=for-the-badge&logo=kubernetes)]()

Este monorepo es una suite educativa avanzada diseñada para modernizar y automatizar el flujo de despliegue en la nube. Desde el alojamiento estático hasta la orquestación industrial de contenedores en AWS, exploramos cómo construir infraestructuras seguras, escalables y profesionales.

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
- 🕒 **[Historial de Cambios](./CHANGELOG.md)**: Registro detallado de versiones y mejoras.
- 📑 **[Wiki del Proyecto](../../wikis/home)**: Base de conocimientos colaborativa en GitLab.

---

## 🗺️ Roadmap de Aprendizaje (Casos de Estudio)

Cada carpeta representa un hito en la evolución de un Ingeniero Cloud. Aquí el detalle de cada módulo:

### 🟢 Nivel 1: Automatización y Hosting Estático

#### [📂 Caso A: AWS Amplify](./caso-a-amplify/) `Nivel 0` `COMPLETADO`
*   **Stack**: AWS Amplify + GitLab Auto-Mirroring.
*   **Enfoque**: **Integración Continua nativa.** Ideal para prototipos rápidos. Aprende cómo AWS gestiona automáticamente el escalado, SSL y CDN.
*   👉 [Ver Demo en Vivo](https://main.d1uybq9oui7h8c.amplifyapp.com/)

#### [📂 Caso B: S3 + GitLab CI](./caso-b-gitlab-s3/) `Nivel 1` `COMPLETADO`
*   **Stack**: GitLab Runners + AWS CLI + S3 Website Hosting.
*   **Enfoque**: **Pipelines Artesanales.** Entiende qué pasa "bajo el capó". Aprendes sobre políticas de bucket, sincronización manual y gestión de secretos.
*   👉 [Ver Demo en Vivo](http://vladimir-caso-b-site-2026.s3-website.us-east-2.amazonaws.com/)

### 🔵 Nivel 2: Profesionalización e Infraestructura como Código (IaC)

#### [📂 Caso C: Terraform + CloudFront](./caso-c-terraform-s3/) `Nivel 2` `COMPLETADO`
*   **Stack**: Terraform + S3 (OAC) + CloudFront + Remote State.
*   **Enfoque**: **Infraestructura como Código (IaC).** Elimina el error humano. Aprende a centralizar el estado en la nube y proteger recursos con **Origin Access Control**.
*   👉 [Ver Demo en Vivo](https://d3otfpeykrm536.cloudfront.net/)

#### [📂 Caso D: Serverless Basic (SAM)](./caso-d-serverless-basic/) `Nivel 3` `COMPLETADO`
*   **Stack**: API Gateway + AWS Lambda + DynamoDB.
*   **Enfoque**: **Lógica Backend y Persistencia.** Añade vida a tus apps. Escalamiento a cero costos cuando no hay uso y potencia reactiva bajo demanda.
*   👉 [Demo Portafolio](https://staging.d3oq987bpa7ls7.amplifyapp.com/) / [API Endpoint](https://tc78a6xibg.execute-api.us-east-2.amazonaws.com)

### 🟠 Nivel 3: Gestión de Aplicaciones y Datos (Senior)

#### [📂 Caso E: Persistence Pro](./caso-e-dynamodb-persistence/) `Nivel 4` `PROYECTADO`
*   **Stack**: DynamoDB (Single Table Design) + SQS.
*   **Enfoque**: **Modelado de Datos Senior.** Domina los índices (GSI/LSI) y la persistencia asíncrona para aplicaciones de alto rendimiento.

#### [📂 Caso F: Security First](./caso-f-security-cognito/) `Nivel 5` `PROYECTADO`
*   **Stack**: AWS Cognito + WAF + IAM Roles.
*   **Enfoque**: **Seguridad Perimetral.** Implementa autenticación de usuarios y protección contra ataques web (DDoS/SQLi).

#### [📂 Caso G: Event Driven](./caso-g-event-driven/) `Nivel 6` `PROYECTADO`
*   **Stack**: EventBridge + Step Functions.
*   **Enfoque**: **Arquitecturas Reactivas.** Desacoplamiento total de servicios mediante el paso de mensajes y orquestación de flujos.

#### [📂 Caso H: Observability & Health](./caso-h-observability/) `Nivel 7` `NUEVO`
*   **Stack**: CloudWatch + X-Ray + GitLab Observability.
*   **Enfoque**: **Monitoreo Proactivo.** Trazabilidad distribuida para encontrar fallos antes que el usuario y tableros de salud integrados en GitLab.

#### [📂 Caso I: GenAI Bedrock](./caso-i-genai-bedrock/) `Nivel 8` `PROYECTADO`
*   **Stack**: Amazon Bedrock + LangChain + Lambda.
*   **Enfoque**: **Inteligencia Artificial Propia.** Integración de modelos LLM en tu infraestructura de forma privada y segura.

### 🔴 Nivel 4: Contenedores y Escalamiento Grado Industrial

#### [📂 Caso J: Dockerización de Microservicios](./caso-j-containers-ecs/) `Nivel 9` `NUEVO`
*   **Stack**: Docker + ECS Fargate + ECR.
*   **Enfoque**: **Portabilidad e Isolation.** Empaquetado industrial de apps para que corran igual en local y en la nube. Gestión de registros de imágenes.

#### [📂 Caso K: Kubernetes en AWS (EKS)](./caso-k-kubernetes-eks/) `Nivel 10` `NUEVO`
*   **Stack**: AWS EKS + YAML + GitLab Kubernetes Agent.
*   **Enfoque**: **Orquestación Real en AWS.** Kubernetes directo en la nube conectado con GitLab. Gestiona flotas de contenedores, auto-sanación y balanceo masivo.

### 🟣 Nivel 5: Gobernanza, Integraciones y Optimizaciones

#### [📂 Caso L: FinOps & Governance](./caso-l-finops-optimization/) `Nivel 11` `NUEVO`
*   **Stack**: AWS Budgets + GitLab Integraciones + IAM Governance.
*   **Enfoque**: **Excelencia Operativa.** Integración profunda de GitLab con AWS, control de costos y políticas de gobernanza corporativa.

---

## 🤝 Comunidad y Contribución
¡Este proyecto está abierto a mejora continua! Revisa nuestras **[Normas de Conducta](./docs/CODE_OF_CONDUCT.md)** y la **[Guía de Contribución](./CONTRIBUTING.md)**.

---
> **Construido con ❤️ por Vladimir Acuña — Optimizado para Ingeniería Cloud Senior.**
