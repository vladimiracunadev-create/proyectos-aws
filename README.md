# GitLab → AWS (Monorepo Educativo) ☁️

[![Deployed](https://img.shields.io/badge/deployed-AWS-orange.svg)]()
[![Pipeline](https://gitlab.com/vladimir.acuna.dev-group/proyectos-aws-gitlab/badges/main/pipeline.svg)](https://gitlab.com/vladimir.acuna.dev-group/proyectos-aws-gitlab/-/pipelines)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Style](https://img.shields.io/badge/code_style-prettier-ff69b4.svg)](https://prettier.io)
[![Antigravity](https://img.shields.io/badge/built_with-Antigravity-8A2BE2.svg)]()

**Repositorio Maestro de Aprendizaje AWS**
Este proyecto es una guía evolutiva paso a paso para dominar el despliegue de aplicaciones en AWS, desde sitios estáticos simples hasta arquitecturas avanzadas con contenedores y seguridad.

> **Nota:** Este proyecto se trabaja íntegramente con **Antigravity**.

---

## 🗺️ Roadmap de Aprendizaje

Cada carpeta en este repositorio representa un "Caso de Estudio" que añade complejidad y profesionalismo sobre el anterior.

### Nivel 1: Conceptos Básicos
- **[📂 caso-a-amplify](./caso-a-amplify/)** (Nivel 0)
    - *Stack*: AWS Amplify (ClickOps).
    - *Objetivo*: Despliegue en 5 minutos, conexión automática con GitLab.
- **[📂 caso-b-gitlab-s3](./caso-b-gitlab-s3/)** (Nivel 1)
    - *Stack*: S3 + GitLab CI.
    - *Objetivo*: Entender qué pasa "por debajo". Pipelines manuales, buckets, sync.

### Nivel 2: Profesionalización (IaC & Serverless)
- **[📂 caso-c-terraform-s3](./caso-c-terraform-s3/)** (Nivel 2) `NUEVO`
    - *Stack*: **Terraform** + S3 + CloudFront.
    - *Objetivo*: Infraestructura como Código (IaC). Cero configuración manual.
- **[📂 caso-d-serverless-basic](./caso-d-serverless-basic/)** (Nivel 3) `PROYECTADO`
    - *Stack*: Lambda + API Gateway.
    - *Objetivo*: Añadir lógica dinámica backend sin servidores (Serverless).

### Nivel 3: Arquitectura Empresarial
- **[📂 caso-e-dynamodb-persistence](./caso-e-dynamodb-persistence/)** (Nivel 4) `PROYECTADO`
    - *Stack*: DynamoDB + Lambda.
    - *Objetivo*: Persistencia de datos NoSQL. Aplicaciones reales con estado.
- **[📂 caso-f-security-cognito](./caso-f-security-cognito/)** (Nivel 5) `PROYECTADO`
    - *Stack*: Cognito + WAF.
    - *Objetivo*: Autenticación de usuarios y seguridad perimetral.
- **[📂 caso-g-containers-ecs](./caso-g-containers-ecs/)** (Nivel 6) `PROYECTADO`
    - *Stack*: Docker + ECS Fargate.
    - *Objetivo*: Microservicios en contenedores para cargas de trabajo complejas.

---

## 🛠️ Desarrollo

Este es un monorepo gestionado con herramientas estándar de Node.js.

### Requisitos
- Node.js 18+
- Terraform (para Caso C en adelante)
- AWS CLI configurado

### Comandos Globales
```bash
npm install     # Instalar herramientas de calidad (Linter, Prettier)
npm run lint    # Revisar código en todos los casos
npm run format  # Formatear código automáticamente
```

### Reglas de Contribución
Usamos **Conventional Commits**. Tus mensajes de commit deben seguir el formato:
- `feat(caso-c): added main.tf`
- `fix(root): updated readme`
- `docs(caso-a): improved instructions`

---

## 📜 Licencia
Este proyecto está bajo la Licencia MIT. Úsalo libremente para aprender y enseñar.


