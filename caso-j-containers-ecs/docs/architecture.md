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
graph TB
    subgraph Dev["💻 Developer"]
        Code["Código fuente\n+ Dockerfile"]
        Build["docker build\ndocker tag\ndocker push"]
    end

    subgraph ECR["🗄️ AWS ECR\n(Elastic Container Registry)"]
        Repo["Repositorio ECR\nImagen: caso-j-app:latest\nImagen: caso-j-app:v1.2.3"]
        Scan["Vulnerability Scan\n(Trivy / ECR native)"]
    end

    subgraph ECS["☁️ AWS ECS Fargate"]
        Cluster["ECS Cluster\n(plano de control)"]
        Service["ECS Service\ndesired_count: 2\ndeployment: rolling update"]
        Task1["🐳 Task 1\nFargate (serverless)\nvCPU: 0.5, RAM: 1GB\nus-east-1a"]
        Task2["🐳 Task 2\nFargate (serverless)\nvCPU: 0.5, RAM: 1GB\nus-east-1b"]
    end

    subgraph Networking["🌐 Network (Terraform)"]
        ALB["⚖️ Application Load Balancer\nPublic-facing\nHTTP:80 → Target Group"]
        TG["Target Group\nHealth Check: /\nInterval: 30s"]
        VPC["VPC Custom\nPublic + Private Subnets\n2 AZs"]
    end

    User["🌍 Usuario"] -->|"HTTP"| ALB
    ALB --> TG
    TG --> Task1
    TG --> Task2
    Code --> Build
    Build -->|"push"| Repo
    Repo --> Scan
    Repo -->|"pull en deploy"| Task1
    Repo -->|"pull en deploy"| Task2
    Cluster --> Service
    Service --> Task1
    Service --> Task2
    Task1 --- VPC
    Task2 --- VPC

    style ALB fill:#FF9900,color:#fff
    style Task1 fill:#2496ED,color:#fff
    style Task2 fill:#2496ED,color:#fff
    style Repo fill:#E74C3C,color:#fff
    style VPC fill:#16A085,color:#fff
```

---

## 📐 Diagrama 2: Pipeline CI/CD Docker → ECR → ECS

```mermaid
sequenceDiagram
    participant Dev as 💻 Dev
    participant GitLab as 🦊 GitLab CI
    participant ECR as 🗄️ ECR
    participant ECS as ☁️ ECS

    Dev->>GitLab: git push main
    GitLab->>GitLab: Stage: test (lint, unit tests)
    GitLab->>GitLab: Stage: build\ndocker build -t app:$CI_COMMIT_SHA .
    GitLab->>ECR: docker push caso-j-app:$CI_COMMIT_SHA
    ECR->>ECR: Scan de vulnerabilidades

    GitLab->>ECS: aws ecs update-service\n--force-new-deployment\n--image caso-j-app:$SHA

    ECS->>ECS: Rolling Update iniciado
    Note over ECS: Nueva Task v2 arranca (health check OK)
    Note over ECS: ALB drains Task v1 (connection draining 30s)
    Note over ECS: Task v1 detenida

    ECS-->>GitLab: Deploy exitoso (desired=2, running=2)
    GitLab-->>Dev: Pipeline green ✅
```

---

## 📐 Diagrama 3: Rolling Update (Zero Downtime Deploy)

```mermaid
graph LR
    subgraph Antes["Estado Inicial — v1"]
        T1v1["🐳 Task 1 v1\nHealthy ✅"]
        T2v1["🐳 Task 2 v1\nHealthy ✅"]
        ALB1["⚖️ ALB\nenvía tráfico a v1"]
    end

    subgraph Durante["Durante Rolling Update"]
        T1v2["🐳 Task 1 v2\nStarting... ⏳"]
        T2v1b["🐳 Task 2 v1\nHealthy ✅ (draining)"]
        ALB2["⚖️ ALB\nenvía solo a v2 (cuando healthy)\ny v1 (mientras draining)"]
    end

    subgraph Despues["Estado Final — v2"]
        T1v2b["🐳 Task 1 v2\nHealthy ✅"]
        T2v2["🐳 Task 2 v2\nHealthy ✅"]
        ALB3["⚖️ ALB\nenvía tráfico a v2"]
    end

    Antes -->|"deploy"| Durante
    Durante -->|"v1 drenado"| Despues

    style T1v2 fill:#F39C12,color:#fff
    style T1v2b fill:#27AE60,color:#fff
    style T2v2 fill:#27AE60,color:#fff
```

---

## 📐 Diagrama 4: VPC y Modelo de Red (Terraform)

```mermaid
graph TB
    subgraph VPC["🌐 VPC: 10.0.0.0/16"]
        subgraph AZ_A["📍 us-east-1a"]
            PubA["Public Subnet\n10.0.1.0/24\n(ALB)"]
            PrivA["Private Subnet\n10.0.10.0/24\n(ECS Tasks)"]
        end
        subgraph AZ_B["📍 us-east-1b"]
            PubB["Public Subnet\n10.0.2.0/24\n(ALB)"]
            PrivB["Private Subnet\n10.0.20.0/24\n(ECS Tasks)"]
        end
        IGW["🌐 Internet Gateway"]
        NAT["NAT Gateway\n(para pull de imágenes ECR\ndesde subnets privadas)"]
    end

    Internet["🌍 Internet"] -->IGW
    IGW --> PubA
    IGW --> PubB
    PubA -->|"SNAT"| NAT
    NAT --> PrivA
    NAT --> PrivB

    style VPC fill:#EBF5FB,color:#333
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
