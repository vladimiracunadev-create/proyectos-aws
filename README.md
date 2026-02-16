# GitLab → AWS Monorepo (DevOps Training Suite) ☁️ 🚀

[![Infrastructure-AWS](https://img.shields.io/badge/infrastructure-AWS-orange?style=for-the-badge&logo=amazon-aws)]()
[![Pipeline-GitLab](https://img.shields.io/badge/pipeline-GitLab_CI-6C4DE6?style=for-the-badge&logo=gitlab)](https://gitlab.com/vladimir.acuna.dev-group/proyectos-aws-gitlab/-/pipelines)
[![IaC-Terraform](https://img.shields.io/badge/IaC-Terraform-844FBA?style=for-the-badge&logo=terraform)]()
[![Container-Docker](https://img.shields.io/badge/Container-Docker-2496ED?style=for-the-badge&logo=docker)]()
[![Orchestrator-K8s](https://img.shields.io/badge/Orchestrator-K8s-326CE5?style=for-the-badge&logo=kubernetes)]()

Este monorepo es una suite educativa avanzada diseñada para modernizar y automatizar el flujo de despliegue en la nube. Desde el alojamiento estático hasta la orquestación industrial de contenedores en AWS, exploramos cómo construir infraestructuras seguras, escalables y profesionales.

---

## 🌐 Portal de Documentación (PWA)
¡Nuevo! Hemos lanzado un portal web interactivo para explorar este repositorio con un diseño moderno y premium (**Glassmorphism**).

*   **Acceso Local**: Abre `index.html` usando un servidor local (ej: `npx serve .`).
*   **Experiencia PWA**: Instálalo en tu móvil o escritorio para acceso rápido y soporte offline.
*   **Contraste**: Navega por todas las guías, diagramas y especificaciones de forma dinámica.

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

### 🎯 Inicio Rápido
- 🚀 **[Guía de Instalación](docs/INSTALL.md)**: Docker (DevContainers) vs Manual.
- 📘 **[Guía para Principiantes](docs/BEGINNERS_GUIDE.md)**: Glosario y conceptos básicos.
- ⚡ **[Referencia Rápida](docs/QUICK_REFERENCE.md)**: Comandos esenciales y atajos.

### 🏗️ Arquitectura y Stack
- 🏗️ **[Arquitectura](docs/ARCHITECTURE.md)**: Visión técnica, diagramas Mermaid y stack.
- 🛠️ **[Especificaciones Técnicas](docs/TECHNICAL_SPECS.md)**: Requerimientos de hardware y software.
- 🔧 **[Tooling](docs/TOOLING.md)**: Docker, Kubernetes, Makefile y validaciones.
- 📊 **[Resumen de Implementación](docs/IMPLEMENTATION_SUMMARY.md)**: Overview del tooling y seguridad.

### 🛡️ Seguridad
- 🛡️ **[Seguridad IAM](docs/IAM_SECURITY.md)**: Políticas de acceso y privilegios mínimos.
- ✅ **[Security Checklist](docs/SECURITY_CHECKLIST.md)**: Lista de verificación completa de seguridad.
- 🔐 **[Secretos Comprometidos](docs/killed.md)**: Registro de secretos rotados.

### 👔 Para Reclutadores
- 👨‍💼 **[Guía para Reclutadores](docs/RECRUITER.md)**: Tour ejecutivo y valor de negocio.

### 📚 Otros Recursos
- 🕒 **[Historial de Cambios](CHANGELOG.md)**: Registro detallado de versiones y mejoras.
- 🗺️ **[Roadmap](ROADMAP.md)**: Plan de desarrollo y próximos hitos.
- 📑 **[Wiki del Proyecto](wiki/home.md)**: Base de conocimientos colaborativa en GitLab.
- 🤝 **[Guía de Contribución](CONTRIBUTING.md)**: Cómo contribuir al proyecto.
- 📜 **[Código de Conducta](docs/CODE_OF_CONDUCT.md)**: Normas de la comunidad.
- 📄 **[Licencia](LICENSE)**: Términos de uso bajo licencia MIT.

---

## 💻 Desarrollo Local

Para previsualizar el portal y los entornos web de cada caso de forma consistente:

```powershell
# Usando Makefile (Recomendado)
make serve

# O directamente con Python
python -m http.server 8000
```
Acceso: [http://localhost:8000](http://localhost:8000)

### 📤 Subir Cambios al Repositorio

Para subir tus cambios de forma rápida:

```powershell
# Usando Makefile
make upload

# O directamente con Python
python -c "import os; os.system('git add .'); os.system('git commit -m \"Update\"'); os.system('git push')"
```

---

## 🏗️ Casos de Estudio y Dashboards

Cada carpeta representa un hito en la evolución de un Ingeniero Cloud. Aquí el detalle de cada módulo:

### 🟢 Nivel 1: Automatización y Hosting Estático

#### [📂 Caso A: AWS Amplify](./caso-a-amplify/index.html) `Nivel 0` `COMPLETADO`
*   **Stack**: AWS Amplify + GitLab Auto-Mirroring.
*   **Enfoque**: **Integración Continua nativa.** Ideal para prototipos rápidos. Aprende cómo AWS gestiona automáticamente el escalado, SSL y CDN.
*   ☁️ [Guía Paso a Paso AWS](caso-a-amplify/AWS_PASO_A_PASO.md)
*   👉 [Ver Demo en Vivo](https://main.d1uybq9oui7h8c.amplifyapp.com/)

#### [📂 Caso B: S3 + GitLab CI](./caso-b-gitlab-s3/index.html) `Nivel 1` `COMPLETADO`
*   **Stack**: GitLab Runners + AWS CLI + S3 Website Hosting.
*   **Enfoque**: **Pipelines Artesanales.** Entiende qué pasa "bajo el capó". Aprendes sobre políticas de bucket, sincronización manual y gestión de secretos.
*   ☁️ [Guía Paso a Paso AWS](caso-b-gitlab-s3/AWS_PASO_A_PASO.md)
*   👉 [Ver Demo en Vivo](http://vladimir-caso-b-site-2026.s3-website.us-east-2.amazonaws.com/)

### 🔵 Nivel 2: Profesionalización e Infraestructura como Código (IaC)

#### [📂 Caso C: Terraform + CloudFront](./caso-c-terraform-s3/index.html) `Nivel 2` `COMPLETADO`
*   **Stack**: Terraform + S3 (OAC) + CloudFront + Remote State.
*   **Enfoque**: **Infraestructura como Código (IaC).** Elimina el error humano. Aprende a centralizar el estado en la nube y proteger recursos con **Origin Access Control**.
*   ☁️ [Guía Paso a Paso AWS](caso-c-terraform-s3/AWS_PASO_A_PASO.md)
*   👉 [Ver Demo en Vivo](https://d3otfpeykrm536.cloudfront.net/)

#### [📂 Caso D: Serverless Basic (SAM)](./caso-d-serverless-basic/index.html) `Nivel 3` `COMPLETADO`
*   **Stack**: API Gateway + AWS Lambda + DynamoDB.
*   **Enfoque**: **Lógica Backend y Persistencia.** Añade vida a tus apps. Escalamiento a cero costos cuando no hay uso y potencia reactiva bajo demanda.
*   ☁️ [Guía Paso a Paso AWS](caso-d-serverless-basic/AWS_PASO_A_PASO.md)
*   👉 [Demo Portafolio](https://staging.d3oq987bpa7ls7.amplifyapp.com/) / [API Endpoint](https://tc78a6xibg.execute-api.us-east-2.amazonaws.com)

### 🟠 Nivel 3: Gestión de Aplicaciones y Datos (Senior)

#### [📂 Caso E: Persistence Pro](./caso-e-dynamodb-persistence/index.html) `Nivel 4` `PROYECTADO`
*   **Stack**: DynamoDB (Single Table Design) + SQS.
*   **Enfoque**: **Modelado de Datos Senior.** Domina los índices (GSI/LSI) y la persistencia asíncrona para aplicaciones de alto rendimiento.

#### [📂 Caso F: Security First](./caso-f-security-cognito/index.html) `Nivel 5` `PROYECTADO`
*   **Stack**: AWS Cognito + WAF + IAM Roles.
*   **Enfoque**: **Seguridad Perimetral.** Implementa autenticación de usuarios y protección contra ataques web (DDoS/SQLi).

#### [📂 Caso G: Event Driven](./caso-g-event-driven/index.html) `Nivel 6` `PROYECTADO`
*   **Stack**: EventBridge + Step Functions.
*   **Enfoque**: **Arquitecturas Reactivas.** Desacoplamiento total de servicios mediante el paso de mensajes y orquestación de flujos.

#### [📂 Caso H: Observability & Health](./caso-h-observability/index.html) `Nivel 7` `PROYECTADO`
*   **Stack**: CloudWatch + X-Ray + GitLab Observability.
*   **Enfoque**: **Monitoreo Proactivo.** Trazabilidad distribuida para encontrar fallos antes que el usuario y tableros de salud integrados en GitLab.

#### [📂 Caso I: GenAI Bedrock](./caso-i-genai-bedrock/index.html) `Nivel 8` `PROYECTADO`
*   **Stack**: Amazon Bedrock + LangChain + Lambda.
*   **Enfoque**: **Inteligencia Artificial Propia.** Integración de modelos LLM en tu infraestructura de forma privada y segura.

### 🔴 Nivel 4: Contenedores y Escalamiento Grado Industrial

#### [📂 Caso J: Dockerización de Microservicios](./caso-j-containers-ecs/public/index.html) `Nivel 9` `COMPLETADO`
*   **Stack**: Docker + ECS Fargate + ECR + Terraform.
*   **Enfoque**: **Portabilidad e Isolation.** Empaquetado industrial de apps para que corran igual en local y en la nube. Gestión de registros de imágenes.
*   ☁️ [Guía Paso a Paso AWS](caso-j-containers-ecs/AWS_PASO_A_PASO.md)
*   👉 [Ver Demo en Vivo](http://vladimir-case-j-alb-683413891.us-east-2.elb.amazonaws.com/)

#### [📂 Caso K: Kubernetes en AWS (EKS)](./caso-k-kubernetes-eks/README.md) `Nivel 10` `COMPLETADO (VALIDADO)`
*   **Stack**: AWS EKS + YAML + GitLab Kubernetes Agent.
*   **Enfoque**: **Orquestación Real en AWS.** Kubernetes directo en la nube. Gestiona flotas de contenedores, auto-sanación y balanceo masivo.
*   ☁️ [Guía Paso a Paso AWS](caso-k-kubernetes-eks/AWS_PASO_A_PASO.md)
*   🖼️ [Reporte de Visualización y Resultados](caso-k-kubernetes-eks/VISUALIZATION.md)

### 🟣 Nivel 5: Gobernanza, Integraciones y Optimizaciones

#### [📂 Caso L: FinOps & Governance](./caso-l-finops-optimization/) `Nivel 11` `NUEVO`
*   **Stack**: AWS Budgets + GitLab Integraciones + IAM Governance.
*   **Enfoque**: **Excelencia Operativa.** Integración profunda de GitLab con AWS, control de costos y políticas de gobernanza corporativa.

---

## 🤝 Comunidad y Contribución
¡Este proyecto está abierto a mejora continua! Revisa nuestras **[Normas de Conducta](./docs/CODE_OF_CONDUCT.md)** y la **[Guía de Contribución](./CONTRIBUTING.md)**.

---
> **Construido con ❤️ por Vladimir Acuña — Optimizado para Ingeniería Cloud Senior.**
