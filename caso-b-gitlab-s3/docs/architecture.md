# 🏗️ Arquitectura: Caso B — S3 + GitLab CI (Pipeline Artesanal)

> **Stack**: GitLab Runners + AWS CLI + S3 Website Hosting
> **Nivel**: 1 — Pipelines Manuales y Control Total

---

## 🎯 Visión General

El Caso B expone **todo lo que Amplify oculta**: la sincronización manual de archivos a S3,
la gestión de políticas de bucket, y la configuración de hosting estático paso a paso.
Es el puente entre "magia automática" y "entiendo lo que pasa bajo el capó".

El patrón GitLab CI → AWS CLI → S3 es el fundamento de decenas de pipelines empresariales.

---

## 📐 Diagrama 1: Pipeline GitLab → S3

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#6C4DE6', 'secondaryColor': '#569A31', 'tertiaryColor': '#f4f4f4', 'fontsize': '16px' }}}%%
graph TB
    subgraph Dev["💻 Desarrollador"]
        Commit["📝 git commit + push\na rama main"]
    end

    subgraph Pipeline["🦊 GitLab CI Pipeline (.gitlab-ci.yml)"]
        direction TB
        Stage_Test["🧪 Stage: test\nlint + validaciones"]
        Stage_Deploy["🚀 Stage: deploy\n(solo en main)"]

        subgraph Job_Deploy["🛠️ Job: deploy_case_b"]
            direction TB
            AWSCLI["🐳 Image: aws-cli:latest"]
            GetCreds["🔑 Leer variables CI/CD:\nAWS_ACCESS_KEY_ID\nAWS_SECRET_ACCESS_KEY\nS3_BUCKET"]
            Sync["📤 aws s3 sync caso-b-gitlab-s3/\ns3://BUCKET/ --delete\n--exclude '*.md'"]
        end

        Stage_Test --> Stage_Deploy
        Stage_Deploy --> Job_Deploy
        AWSCLI --> GetCreds --> Sync
    end

    subgraph AWS["☁️ AWS Infraestructura"]
        direction TB
        S3["🪣 S3 Bucket\nWebsite Hosting habilitado\nÍndice: index.html\nError: index.html"]
        Policy["📋 Bucket Policy\nGetObject público\npara s3-website"]
        URL["🌐 Endpoint HTTP\nhttp://bucket.s3-website.us-east-2.amazonaws.com"]
    end

    Commit --> Pipeline
    Sync --> S3
    S3 --- Policy
    S3 --> URL

    style Commit fill:#6C4DE6,color:#fff
    style AWSCLI fill:#FF9900,color:#fff
    style S3 fill:#569A31,color:#fff,stroke:#3d6e22,stroke-width:2px
    style URL fill:#2496ED,color:#fff
```

---

## 📐 Diagrama 2: Flujo de Request del Usuario Final

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'fontsize': '16px' }}}%%
sequenceDiagram
    participant U as 🌍 Usuario
    participant DNS as 🔍 DNS
    participant S3W as 🌐 S3 Website Endpoint
    participant S3 as 🪣 S3 Bucket

    U->>DNS: Resuelve bucket.s3-website.us-east-2.amazonaws.com
    DNS-->>U: IP del endpoint S3 Website

    U->>S3W: GET http://bucket.s3-website.us-east-2.amazonaws.com/
    S3W->>S3: GET objeto /index.html
    S3-->>S3W: 200 OK + HTML

    S3W-->>U: 200 OK + HTML
    U->>S3W: GET /styles.css, /app.js
    S3W->>S3: GET /styles.css, /app.js
    S3-->>U: 200 OK + assets

    Note over U,S3: Sin HTTPS (HTTP puro en S3 Website Endpoint)
    Note over U,S3: Para HTTPS: agregar CloudFront (ver Caso C)
```

---

## 📐 Diagrama 3: Gestión de Secretos en GitLab CI

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#E74C3C', 'fontsize': '16px' }}}%%
graph TB
    subgraph GitLab_Settings["⚙️ GitLab Settings"]
        direction TB
        V1["🔑 AWS_ACCESS_KEY_ID\n(Masked, Protected)"]
        V2["🔑 AWS_SECRET_ACCESS_KEY\n(Masked, Protected)"]
        V3["🪣 S3_BUCKET\n(Plain text)"]
    end

    subgraph Runner["🏃 GitLab Runner (Job)"]
        direction TB
        Env["Variables disponibles\ncomo ENV vars en el job"]
        CLI["📤 aws s3 sync ...\nusa $AWS_ACCESS_KEY_ID\nautomáticamente"]
    end

    subgraph IAM["🔐 AWS IAM"]
        User["👤 IAM User\ncon permisos S3\ns3:PutObject\ns3:DeleteObject\ns3:ListBucket"]
    end

    V1 --> Env
    V2 --> Env
    V3 --> Env
    Env --> CLI
    CLI -->|"Autentica via"| IAM

    Note1["⚠️ Caso B usa IAM keys permanentes.\nCaso L mejora esto con OIDC (sin keys)."]

    style V2 fill:#E74C3C,color:#fff
    style IAM fill:#FF9900,color:#fff,stroke:#e68a00,stroke-width:2px
    style Note1 fill:#FFF3CD,color:#333,stroke:#F0AD4E
```

---

## 🔧 Componentes y Roles

| Componente | Servicio | Función | Diferencia con Caso A |
|---|---|---|---|
| **Pipeline** | GitLab CI | Orquesta el deploy manualmente | En Caso A Amplify lo hace automático |
| **CLI** | AWS CLI | Sincroniza archivos con `aws s3 sync` | En Caso A oculto dentro de Amplify |
| **Storage** | S3 | Almacena y sirve el sitio web estático | Igual, pero configuras tú todo |
| **Hosting** | S3 Website Endpoint | HTTP (sin HTTPS nativo) | Caso A usa CloudFront automático con HTTPS |
| **Secretos** | Variables GitLab CI | IAM keys permanentes (masked) | Caso L mejora con OIDC |

---

## ⚠️ Limitaciones Conocidas de Este Patrón

| Limitación | Impacto | Solución |
|---|---|---|
| Sin HTTPS | El endpoint S3 es HTTP puro | Agregar CloudFront (ver Caso C) |
| IAM keys permanentes | Riesgo de filtración si se exponen | Migrar a OIDC (ver Caso L) |
| Sin CDN | Latencia varía según región del usuario | Agregar CloudFront (ver Caso C) |
| Sin caché | S3 sirve directo cada request | Headers de caché en `aws s3 sync` |

---

## 🔗 Referencias

- [README del Caso B](../README.md)
- [Guía Paso a Paso AWS](../AWS_PASO_A_PASO.md)
- [Siguiente nivel → Caso C (CloudFront + Terraform)](../../caso-c-terraform-s3/docs/architecture.md)
