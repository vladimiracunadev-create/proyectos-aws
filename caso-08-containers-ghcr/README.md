# Caso 08 — Containers + GitHub Container Registry (GHCR)

![Estado](https://img.shields.io/badge/estado-📋%20Planificado-lightgrey?style=flat-square)
![Trimestre](https://img.shields.io/badge/trimestre-Q3%202026-blue?style=flat-square)
![AWS](https://img.shields.io/badge/AWS-ECS%20Fargate%20·%20ECR-FF9900?style=flat-square&logo=amazonaws&logoColor=white)
![Actions](https://img.shields.io/badge/GitHub_Actions-GHCR%20·%20Docker%20Build-2088FF?style=flat-square&logo=githubactions&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Multi--platform-2496ED?style=flat-square&logo=docker&logoColor=white)

---

## 🎯 Objetivo

Containerizar la aplicación del Caso 05, publicarla en **GitHub Container Registry**
(GHCR — gratuito para repos públicos) y desplegarla en **ECS Fargate**.

---

## 🔑 Lo que introduce

### En AWS
| Servicio | Para qué |
|:---|:---|
| **ECS Fargate** | Runtime de containers sin gestionar servidores |
| **ECR** (alternativo a GHCR) | Registry privado de AWS si se prefiere sobre GHCR |
| **VPC / Subnets** | Networking básico para el task Fargate |
| **ALB** | Application Load Balancer frente al servicio ECS |

### En GitHub Actions
| Capacidad nueva | Descripción |
|:---|:---|
| `docker/build-push-action` | Build y push de imagen en un step |
| `docker/metadata-action` | Genera tags automáticos (SHA, semver, latest) |
| Multi-platform build | `linux/amd64` + `linux/arm64` en paralelo con buildx |
| GHCR login | `docker/login-action` con `GITHUB_TOKEN` — sin secrets extra |

---

## 🔄 Flujo (objetivo)

```
Push a main (cambios en caso-08/**)
  │
  ├── Build multi-platform image
  │     ├── linux/amd64
  │     └── linux/arm64
  │
  ├── Push a ghcr.io/vladimiracunadev-create/caso-08:sha-abc123
  │
  └── Update ECS task definition → new image tag
        └── ECS rolling update (0 downtime)
```

---

## 💡 GHCR vs ECR

| | GHCR | ECR |
|:---|:---|:---|
| **Costo** | Gratis (repo público) | $0.10/GB/mes |
| **Auth** | `GITHUB_TOKEN` | IAM (OIDC) |
| **Integración** | Nativa con GitHub | Nativa con AWS |
| **Cuándo usar** | Repo público, imagen pública | Imagen privada, mejor latencia en AWS |

---

## 📜 Certificaciones relevantes

![DVA-C02](https://img.shields.io/badge/DVA--C02-Deployment%2024%25-FF6B6B?style=flat-square)
![SAA-C03](https://img.shields.io/badge/SAA--C03-High%20Perf%2024%25-4ECDC4?style=flat-square)

| Certificación | Temas que cubre este caso |
|:---|:---|
| **DVA-C02** | ECS task definitions, container lifecycle, ECR image management |
| **SAA-C03** | ECS Fargate vs EC2 launch type, ALB target groups, VPC networking |
| **SOA-C02** | Container monitoring con CloudWatch Container Insights |

---

## ⬅️ Anterior · Siguiente ➡️

| | Caso |
|:---|:---|
| ⬅️ Anterior | [Caso 07 — Reusable Workflows](../caso-07-reusable-workflows/README.md) |
| ➡️ Siguiente | [Caso 09 — FinOps + Scheduled](../caso-09-finops-scheduled/README.md) |
