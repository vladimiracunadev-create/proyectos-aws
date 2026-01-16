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

## 🎓 ¿Eres nuevo?
**[👉 Empieza leyendo el MANUAL DE APRENDIZAJE para Novatos](./MANUAL_DE_APRENDIZAJE.md)**
Entiende qué significa cada archivo y tecnología de este proyecto con explicaciones sencillas.

---

## 🗺️ Roadmap de Aprendizaje

Cada carpeta en este repositorio representa un "Caso de Estudio" que añade complejidad y profesionalismo sobre el anterior.

### Nivel 1: Conceptos Básicos
- **[📂 caso-a-amplify](./caso-a-amplify/)** (Nivel 0) `DEPLOYED`
    - *Stack*: AWS Amplify (ClickOps).
    - *Objetivo*: Despliegue en 5 minutos, conexión automática con GitLab.
    - *Live Demo*: [👉 Ver Sitio en Vivo](https://main.d1uybq9oui7h8c.amplifyapp.com/)
- **[📂 caso-b-gitlab-s3](./caso-b-gitlab-s3/)** (Nivel 1) `DEPLOYED`
    - *Stack*: S3 + GitLab CI.
    - *Objetivo*: Entender qué pasa "por debajo". Pipelines manuales, buckets, sync.
    - *Live Demo*: [👉 Ver Sitio en Vivo](http://vladimir-caso-b-site-2026.s3-website.us-east-2.amazonaws.com/)

### Nivel 2: Profesionalización (IaC & Serverless)
- **[📂 caso-c-terraform-s3](./caso-c-terraform-s3/)** (Nivel 2) `DEPLOYED`
    - *Stack*: **Terraform** + S3 + CloudFront.
    - *Objetivo*: Infraestructura como Código (IaC). Cero configuración manual.
    - *Live Demo*: [👉 Ver Sitio en Vivo](https://d3otfpeykrm536.cloudfront.net/)
- **[📂 caso-d-serverless-basic](./caso-d-serverless-basic/)** (Nivel 3) `DEPLOYED`
    - *Stack*: Lambda + API Gateway + DynamoDB.
    - *Objetivo*: Añadir lógica dinámica backend sin servidores (Serverless).
    - *Live Demo (Frontend)*: [👉 Portafolio](https://staging.d3oq987bpa7ls7.amplifyapp.com/)
    - *Live Demo (Backend)*: [👉 API Endpoint](https://tc78a6xibg.execute-api.us-east-2.amazonaws.com)

### Nivel 3: Arquitectura Empresarial
- **[📂 caso-e-dynamodb-persistence](./caso-e-dynamodb-persistence/)** (Nivel 4) `PROYECTADO`
    - *Stack*: DynamoDB + Lambda (CRUD Completo).
    - *Objetivo*: Modelo de Datos Avanzado. Operaciones complejas, índices y diseño de tabla única.
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


