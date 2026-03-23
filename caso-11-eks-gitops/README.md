# Caso 11 — EKS + GitOps con GitHub Actions

![Estado](https://img.shields.io/badge/estado-📋%20Planificado-lightgrey?style=flat-square)
![Trimestre](https://img.shields.io/badge/trimestre-Q4%202026-blue?style=flat-square)
![AWS](https://img.shields.io/badge/AWS-EKS%20·%20ECR%20·%20IAM-FF9900?style=flat-square&logo=amazonaws&logoColor=white)
![Actions](https://img.shields.io/badge/GitHub_Actions-GitOps%20·%20K8s-2088FF?style=flat-square&logo=githubactions&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-1.32-326CE5?style=flat-square&logo=kubernetes&logoColor=white)

---

## 🎯 Objetivo

Cierre del viaje. **GitHub Actions como controlador GitOps**: cambios en manifiestos
Kubernetes de este repositorio disparan reconciliación automática sobre un cluster EKS.

---

## 🔑 Lo que introduce

### En AWS
| Servicio | Para qué |
|:---|:---|
| **EKS** (v1.32) | Cluster Kubernetes gestionado por AWS |
| **ECR** | Registry privado para las imágenes del Caso 08 |
| **IRSA** | IAM Roles for Service Accounts (OIDC para pods K8s) |
| **ALB Ingress** | AWS Load Balancer Controller para exponer servicios |

### En GitHub Actions
| Capacidad nueva | Descripción |
|:---|:---|
| `kubectl apply` via OIDC | Autenticación al API de K8s sin kubeconfig estático |
| GitOps pattern | El repo ES la fuente de verdad — lo que está en Git = lo que corre |
| Progressive delivery | `workflow_dispatch` con input de porcentaje de canary |
| Self-hosted runner (concepto) | Runner dentro de la VPC para acceder al cluster privado |

---

## 🔄 Flujo GitOps (objetivo)

```
Cambio en caso-11-eks-gitops/k8s/deployment.yaml
  └── GitHub Actions detecta el cambio
      └── Autentica contra EKS via OIDC (IRSA)
          └── kubectl apply -f k8s/
              └── EKS reconcilia el estado deseado
                  ├── Rolling update (0 downtime por defecto)
                  └── Smoke test post-deploy
                      ├── ✅ Deploy exitoso → merge PR automático
                      └── ❌ Falla → rollback + alerta
```

---

## 📁 Estructura objetivo

```
caso-11-eks-gitops/
├── k8s/
│   ├── namespace.yaml
│   ├── deployment.yaml       ← fuente de verdad del estado del cluster
│   ├── service.yaml
│   ├── ingress.yaml          ← ALB Ingress Controller
│   └── hpa.yaml              ← Horizontal Pod Autoscaler
├── terraform/
│   ├── eks-cluster.tf        ← Cluster + node groups
│   ├── irsa.tf               ← IAM Roles for Service Accounts
│   └── alb-controller.tf     ← AWS Load Balancer Controller
└── README.md                 ← este archivo
```

---

## 🔗 Complementariedad con GitLab

El [Caso K del repositorio GitLab](https://gitlab.com/vladimir.acuna.dev-group/proyectos-aws-gitlab)
también implementa EKS, pero desde la perspectiva del **aprovisionamiento** (Terraform + kubectl).

Este caso lo complementa desde la perspectiva del **flujo GitOps**: cómo GitHub Actions
puede actuar como el sistema de reconciliación, sin ArgoCD ni Flux.

---

## 📜 Certificaciones relevantes

![SAA-C03](https://img.shields.io/badge/SAA--C03-Resilient%20Arch%2026%25-4ECDC4?style=flat-square)
![DVA-C02](https://img.shields.io/badge/DVA--C02-Deployment%2024%25-FF6B6B?style=flat-square)
![SOA-C02](https://img.shields.io/badge/SOA--C02-Provisioning%2018%25-45B7D1?style=flat-square)

| Certificación | Temas que cubre este caso |
|:---|:---|
| **SAA-C03** | EKS architecture, worker node groups, managed node groups vs Fargate |
| **DVA-C02** | Container orchestration, rolling updates, health probes |
| **SOA-C02** | EKS cluster operations, node group scaling, CloudWatch Container Insights |

---

## ⬅️ Anterior · Fin del viaje

| | Caso |
|:---|:---|
| ⬅️ Anterior | [Caso 10 — Multi-región + DR](../caso-10-multiregion-dr/README.md) |
| 🏁 Inicio | [README del repositorio](../README.md) |
| 📖 Narrativa completa | [GitHub Actions Journey](../GITHUB_ACTIONS_JOURNEY.md) |
