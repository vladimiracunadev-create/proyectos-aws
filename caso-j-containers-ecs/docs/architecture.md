# 🏗️ Arquitectura: Caso J — Dockerización con ECS Fargate + ECR

> **Stack**: Docker + ECS Fargate + ECR + ALB + Terraform
> **Nivel**: 9 — Contenedores en Producción

---

## 🎯 Visión General

El Caso J representa el salto de "código en mi máquina" a **contenedores industriales en AWS**.
ECS Fargate elimina la gestión de servidores (EC2): tú defines cuántos recursos necesita tu
contenedor, AWS se encarga de dónde y cómo correrlo.

El patrón `ECR → ECS Fargate → ALB` es el estándar de facto en empresas que migran de
on-premise a AWS sin querer gestionar Kubernetes directamente.

---

## 📐 Diagrama 1: Arquitectura Completa ECS Fargate

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#2496ED', 'secondaryColor': '#FF9900', 'tertiaryColor': '#f4f4f4', 'fontsize': '16px' }}}%%
graph TB
    subgraph Dev["💻 Developer"]
        Code["📝 Código fuente\n+ Dockerfile"]
        Build["🐳 docker build\ntag & push"]
    end

    subgraph ECR["🗄️ AWS ECR\n(Registry)"]
        direction TB
        Repo["📦 Repo: caso-j-app\nTag: latest / SHA"]
        Scan["🔍 Vulnerability Scan\n(Trivy / Inspector)"]
    end

    subgraph ECS["☁️ AWS ECS Fargate"]
        direction TB
        Cluster["🏗️ ECS Cluster\n(Control Plane)"]
        Service["⚙️ ECS Service\ndesired_count: 2\nrolling update"]
        Task1["🐳 Task 1\nFargate (AZ-a)\nvCPU / RAM"]
        Task2["🐳 Task 2\nFargate (AZ-b)\nvCPU / RAM"]
    end

    subgraph Networking["🌐 Network (IaC)"]
        direction TB
        ALB["⚖️ Load Balancer\nPublic-facing\nListener: 80"]
        TG["🎯 Target Group\nHealth Check: /"]
        VPC["🌐 VPC Custom\nPublic + Private\nMulti-AZ"]
    end

    User["🌍 Usuario"] -->|"HTTP"| ALB
    ALB --> TG
    TG --> Task1
    TG --> Task2
    Code --> Build
    Build -->|"push"| Repo
    Repo --> Scan
    Repo -->|"pull"| Task1
    Repo -->|"pull"| Task2
    Cluster --> Service
    Service --> Task1
    Service --> Task2
    Task1 --- VPC
    Task2 --- VPC

    style ALB fill:#FF9900,color:#fff,stroke:#e68a00,stroke-width:2px
    style Task1 fill:#2496ED,color:#fff
    style Task2 fill:#2496ED,color:#fff
    style Repo fill:#E74C3C,color:#fff,stroke:#c0392b,stroke-width:2px
    style VPC fill:#16A085,color:#fff
```

---

## 📐 Diagrama 2: Pipeline CI/CD Docker → ECR → ECS

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'fontsize': '16px' }}}%%
sequenceDiagram
    participant Dev as 💻 Dev
    participant GitLab as 🦊 GitLab CI
    participant ECR as 🗄️ ECR
    participant ECS as ☁️ ECS

    Dev->>GitLab: git push main
    GitLab->>GitLab: Stage: test (lint, unit tests)
    GitLab->>GitLab: Stage: build\ndocker build -t app:$SHA .
    GitLab->>ECR: docker push caso-j-app:$SHA
    ECR->>ECR: Scan de vulnerabilidades

    GitLab->>ECS: aws ecs update-service\n--force-new-deployment
    ECS->>ECS: Rolling Update iniciado
    Note over ECS: Nueva Task v2 arranca (health check OK)
    Note over ECS: ALB drains Task v1 (draining 30s)
    Note over ECS: Task v1 detenida

    ECS-->>GitLab: Deploy exitoso (desired=2, running=2)
    GitLab-->>Dev: Pipeline green ✅
```

---

## 📐 Diagrama 3: Rolling Update (Zero Downtime Deploy)

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#27AE60', 'fontsize': '16px' }}}%%
graph TB
    subgraph Antes["Estado Inicial — v1"]
        direction TB
        T1v1["🐳 Task 1 v1\nHealthy ✅"]
        T2v1["🐳 Task 2 v1\nHealthy ✅"]
        ALB1["⚖️ ALB → v1"]
    end

    subgraph Durante["Durante Rolling Update"]
        direction TB
        T1v2["🔵 Task 1 v2\nStarting... ⏳"]
        T2v1b["🐳 Task 2 v1\nHealthy ✅ (draining)"]
        ALB2["⚖️ ALB → v2 (new)\n& v1 (drain)"]
    end

    subgraph Despues["Estado Final — v2"]
        direction TB
        T1v2b["🔵 Task 1 v2\nHealthy ✅"]
        T2v2["🔵 Task 2 v2\nHealthy ✅"]
        ALB3["⚖️ ALB → v2"]
    end

    Antes --> Durante
    Durante --> Despues

    style T1v2 fill:#F39C12,color:#fff
    style T1v2b fill:#27AE60,color:#fff
    style T2v2 fill:#27AE60,color:#fff
```

---

## 📐 Diagrama 4: VPC y Modelo de Red (Terraform)

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#16A085', 'fontsize': '16px' }}}%%
graph TB
    subgraph VPC["🌐 VPC: 10.0.0.0/16"]
        direction TB
        subgraph AZ_A["📍 AZ-a"]
            PubA["Public Subnet\n(ALB)"]
            PrivA["Private Subnet\n(ECS Tasks)"]
        end
        subgraph AZ_B["📍 AZ-b"]
            PubB["Public Subnet\n(ALB)"]
            PrivB["Private Subnet\n(ECS Tasks)"]
        end
        IGW["🌐 Internet Gateway"]
        NAT["🚀 NAT Gateway\n(Outbound only)"]
    end

    Internet["🌍 Internet"] -->IGW
    IGW --> PubA
    IGW --> PubB
    PubA --> NAT
    NAT --> PrivA
    NAT --> PrivB

    style VPC fill:#f9f9f9,stroke:#333
    style PubA fill:#27AE60,color:#fff
    style PubB fill:#27AE60,color:#fff
    style PrivA fill:#2980B9,color:#fff
    style PrivB fill:#2980B9,color:#fff
    style NAT fill:#E74C3C,color:#fff
```

---

## 🔧 Componentes y Roles

| Componente | Servicio | Función | Diferencia con Serverless |
|---|---|---|---|
| **Registry** | ECR | Almacena imágenes Docker privadas | Lambda usa código directo, no imagen |
| **Orquestador** | ECS | Decide dónde corren los contenedores | Lambda es auto-orquestado |
| **Cómputo** | Fargate | Corre contenedores sin gestionar EC2 | Lambda: runtime managed |
| **LB** | ALB | Distribuye tráfico a tasks saludables | API GW en serverless |
| **IaC** | Terraform | VPC + ECS + ECR + ALB declarativo | SAM para serverless |

---

## 🔗 Referencias

- [README del Caso J](../README.md)
- [Guía Paso a Paso AWS](../AWS_PASO_A_PASO.md)
- [Reporte de Resultados](../VISUALIZATION.md)
