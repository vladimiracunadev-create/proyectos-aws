# 🏗️ Arquitectura: Caso K — Kubernetes en AWS (EKS)

> **Stack**: AWS EKS + kubectl + YAML Manifests + Terraform + GitLab K8s Agent
> **Nivel**: 10 — Orquestación Enterprise

---

## 🎯 Visión General

El Caso K es el nivel más complejo de orquestación de contenedores: **Kubernetes gestionado
en AWS**. EKS (Elastic Kubernetes Service) entrega el plano de control managed, y tú gestionas
los worker nodes y los manifests YAML.

¿Por qué Kubernetes sobre ECS? Cuando necesitas: scheduling avanzado, self-healing declarativo,
portable multi-cloud, Helm para apps complejas, o tu empresa ya tiene skills de K8s.

---

## 📐 Diagrama 1: Arquitectura EKS Completa

```mermaid
graph TB
    subgraph Internet
        User["🌍 Usuario"]
    end

    subgraph K8s_Ingress["🌐 Ingress Layer (AWS)"]
        LB["☁️ AWS Load Balancer\n(L7 — ALB Ingress Controller)\nCreado automáticamente por\naws-load-balancer-controller"]
    end

    subgraph EKS_Cluster["☸️ AWS EKS Cluster (us-east-1)"]
        subgraph ControlPlane["🧠 Control Plane (Managed by AWS)"]
            API["kube-apiserver"]
            ETCD["etcd"]
            Scheduler["Scheduler"]
        end

        subgraph NodeGroup["🖥️ Node Group (EC2 — Managed)"]
            subgraph Node1["Worker Node 1 (us-east-1a)"]
                Pod1["🐳 Pod: app-v1\n(ReplicaSet)"]
                Pod2["🐳 Pod: app-v1\n(ReplicaSet)"]
            end
            subgraph Node2["Worker Node 2 (us-east-1b)"]
                Pod3["🐳 Pod: app-v1\n(ReplicaSet)"]
                Kubelet["kubelet\nkube-proxy"]
            end
        end

        subgraph K8sObjects["📋 Kubernetes Objects"]
            Deployment["Deployment\nreplicas: 3\nrollingUpdate: maxSurge 1"]
            Service["Service\ntype: ClusterIP\nport: 3000"]
            Ingress["Ingress\nalb.ingress.k8s.aws/..."]
            HPA["HPA\nminReplicas: 2\nmaxReplicas: 10\ntarget: CPU 70%"]
        end
    end

    User -->|"HTTP"| LB
    LB --> Pod1
    LB --> Pod2
    LB --> Pod3
    ControlPlane --> NodeGroup
    Deployment --> Pod1
    Deployment --> Pod2
    Deployment --> Pod3
    Service --> Deployment
    Ingress --> LB
    HPA --> Deployment

    style LB fill:#FF9900,color:#fff
    style ControlPlane fill:#326CE5,color:#fff
    style Pod1 fill:#2496ED,color:#fff
    style Pod2 fill:#2496ED,color:#fff
    style Pod3 fill:#2496ED,color:#fff
    style HPA fill:#E74C3C,color:#fff
```

---

## 📐 Diagrama 2: Self-Healing Automático (K8s vs. ECS)

```mermaid
sequenceDiagram
    participant K8s as ☸️ Kubernetes Scheduler
    participant Node as 🖥️ Worker Node
    participant Pod as 🐳 Pod (App)
    participant LB as ⚖️ Load Balancer

    Note over K8s,Pod: Estado deseado: replicas=3, running=3

    Pod->>Pod: 💥 Crash (OOM / error)
    Pod->>K8s: Pod status: Failed
    K8s->>LB: Endpoint removed (Pod no listo)
    LB->>LB: Deja de enviar tráfico al Pod

    K8s->>Node: Crear nuevo Pod (ReplicaSet controller)
    Node->>Pod: Nuevo Pod arranca
    Pod->>Pod: Readiness probe: GET /healthz

    alt Readiness OK
        Pod->>K8s: Running & Ready
        K8s->>LB: Endpoint added
        Note over K8s,LB: ✅ Restaurado en ~30s sin intervención manual
    else Readiness falla (crash loop)
        Pod->>K8s: CrashLoopBackoff
        K8s->>K8s: Backoff exponencial (1s, 2s, 4s, 8s...)
        Note over K8s: Alerta en CloudWatch / GitLab Observability
    end
```

---

## 📐 Diagrama 3: Deploy GitLab → EKS (GitLab Kubernetes Agent)

```mermaid
graph LR
    subgraph GitLab_CI["🦊 GitLab CI Pipeline"]
        Build["Stage: build\ndocker build + push ECR"]
        Deploy["Stage: deploy\nkubectl set image\ndeployment/app app=ECR:SHA"]
    end

    subgraph AgentK8s["🔗 GitLab Kubernetes Agent"]
        Agent["kas (GitLab Agent)\ncorre como Pod en EKS\nconexión WebSocket a GitLab\nsin exponer API Server"]
    end

    subgraph EKS["☸️ EKS"]
        API_K8s["kube-apiserver\n(privado, no expuesto)"]
        Rollout["Rolling Update\nnueva imagen en todos los Pods"]
    end

    Build --> Deploy
    Deploy -->|"kubectl via kas tunnel"| Agent
    Agent -->|"forwarding sobre WebSocket"| API_K8s
    API_K8s --> Rollout

    style Agent fill:#6C4DE6,color:#fff
    style API_K8s fill:#326CE5,color:#fff
    style Rollout fill:#27AE60,color:#fff
```

---

## 📐 Diagrama 4: Horizontal Pod Autoscaler (HPA)

```mermaid
graph TB
    subgraph Metrics["📊 Metrics Server"]
        CPU["CPU utilización\npor Pod (%)"]
    end

    subgraph HPA["⚡ HPA Controller"]
        Check["Cada 15s:\ncurrent_replicas × (currentCPU / targetCPU)"]
        Decision{"CPU > 70%?"}
    end

    subgraph Deployment["📋 Deployment"]
        Pods_2["replicas: 2 (mínimo)"]
        Pods_5["replicas: 5 (scale up)"]
        Pods_10["replicas: 10 (máximo)"]
    end

    CPU --> Check
    Check --> Decision
    Decision -->|"Sí: Scale Up"| Pods_5
    Decision -->|"No: mantener / Scale Down"| Pods_2
    Pods_5 -->|"CPU sigue alta"| Pods_10

    style Decision fill:#E74C3C,color:#fff
    style Pods_5 fill:#F39C12,color:#fff
    style Pods_10 fill:#E74C3C,color:#fff
    style Pods_2 fill:#27AE60,color:#fff
```

---

## 🔧 Componentes y Roles

| Componente | Servicio | Función | vs. ECS Fargate |
|---|---|---|---|
| **Control Plane** | EKS | kube-apiserver gestionado por AWS | ECS: plano de control nativo AWS |
| **Worker Nodes** | EC2 (Managed Node Group) | Corren los Pods | Fargate: sin gestión de EC2 |
| **Scheduling** | kube-scheduler | Ubica Pods según recursos/affinity | ECS: scheduling más simple |
| **Ingress** | AWS LBC (ALB) | L7 routing con anotaciones K8s | ECS: ALB via Terraform |
| **Self-Healing** | ReplicaSet + K8s Controllers | Reinicia Pods caídos automáticamente | ECS: también lo hace |
| **Escalamiento** | HPA + Cluster Autoscaler | Pods y Nodes escalan automáticamente | ECS: Service auto scaling |

---

## 💰 Nota de Costos (Importante)

> EKS cobra **$0.10 USD/hora** (~$72/mes) solo por el plano de control,
> más los EC2 de los worker nodes, NAT Gateway y LB.
>
> Estrategia: **Deploy → Validar → `terraform destroy`** inmediatamente.
> Ver [VISUALIZATION.md](../VISUALIZATION.md) para resultados sin mantener el cluster activo.

---

## 🔗 Referencias

- [README del Caso K](../README.md)
- [Guía Paso a Paso AWS](../AWS_PASO_A_PASO.md)
- [Reporte de Resultados](../VISUALIZATION.md)
