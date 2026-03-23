# FinOps & Análisis de Costos

Desglose real de costos por caso. El objetivo de este documento es doble:
demostrar transparencia sobre el costo de operar cada arquitectura,
y servir de referencia para tomar decisiones de diseño basadas en economía real.

> Última actualización: 2026-03-22
> Cuenta AWS: Free Tier activa hasta 2027-01 (aprox.)
> Moneda: USD

---

## Resumen ejecutivo

| Caso | Servicio principal | Costo mensual estimado | Free Tier cubre |
|:---:|:---|:---:|:---|
| 01 | AWS Amplify | ~$0.00 | Sí (1000 min build/mes, 15 GB serve) |
| 02 | Amazon S3 | ~$0.001 | Sí (5 GB storage, 20K GET, 2K PUT) |
| 03 | S3 + CloudFront | ~$0.02 | Parcial (CloudFront 1TB/mes gratis 1er año) |
| 04 | S3 + CloudFront + Envs | ~$0.02 | Mismo que Caso 03 |
| 05 | Lambda + API Gateway | ~$0.00 | Sí (1M req Lambda/mes, 1M req APIGW/mes) |
| 06 | DynamoDB + Lambda | ~$0.00–$0.05 | Sí (25 GB DynamoDB, 25 WCU/RCU) |
| 07 | Multi-servicio | ~$0.02 | Sí |
| 08 | ECS Fargate | ~$5–15 | No — Fargate no tiene Free Tier significativo |
| 09 | Cost Explorer | ~$0.01 | No — $0.01/1000 API calls |
| 10 | Multi-región | ~$0.05–0.20 | Parcial |
| 11 | EKS | ~$72/mes | No — EKS cobra $0.10/hora por cluster |

**Total estimado (casos 01-09, excluyendo ECS/EKS):** < $0.50/mes

---

## Detalle por caso

### Caso 01: AWS Amplify Hosting

| Componente | Precio | Uso estimado | Costo/mes |
|:---|:---:|:---:|:---:|
| Build minutes | $0.01/min | ~5 min/deploy × 20 deploys | $1.00 → **$0** (Free Tier: 1000 min) |
| Data served | $0.15/GB | ~0.1 GB/mes | **$0** (Free Tier: 15 GB) |
| Requests | $0.0000002/req | ~500 req/mes | **$0** |

**Costo real Q1 2026:** $0.00

**Nota:** El Free Tier de Amplify cubre perfectamente un portafolio personal con tráfico bajo-medio.
Al superar los 1000 minutos de build o 15 GB de datos servidos, el costo sube marginalmente.

---

### Caso 02: Amazon S3 Static Hosting

| Componente | Precio | Uso estimado | Costo/mes |
|:---|:---:|:---:|:---:|
| Storage | $0.023/GB | ~0.01 GB (site) | **$0** (Free Tier: 5 GB) |
| GET requests | $0.0004/1000 | ~200/mes | **$0** (Free Tier: 20K) |
| PUT/COPY/POST | $0.005/1000 | ~50 (deploys) | **$0** (Free Tier: 2K) |
| Data transfer OUT | $0.09/GB | ~0.05 GB/mes | **$0** (Free Tier: 100 GB) |

**Costo real Q1 2026:** ~$0.001/mes (prácticamente $0)

**Nota:** S3 con tráfico mínimo es casi gratuito. El costo sube al agregar CloudFront
(Caso 03) y al superar el Free Tier de data transfer.

---

### Caso 03: S3 + CloudFront + OIDC (proyectado)

| Componente | Precio | Uso estimado | Costo/mes |
|:---|:---:|:---:|:---:|
| S3 (igual caso 02) | — | — | ~$0.001 |
| CloudFront HTTP req | $0.0075/10K | ~1K req/mes | ~$0.001 |
| CloudFront data OUT | $0.085/GB (1er TB) | ~0.05 GB/mes | ~$0.004 |
| **CloudFront Free Tier** | 1TB gratis/mes (12 meses) | — | **$0 primer año** |

**Costo proyectado:** $0 (primer año Free Tier) → ~$0.01/mes después

---

### Caso 05: Lambda + API Gateway (proyectado)

| Componente | Precio | Uso estimado | Costo/mes |
|:---|:---:|:---:|:---:|
| Lambda invocaciones | $0.0000002/req | ~10K/mes | ~$0.002 |
| Lambda duration | $0.0000166667/GB-s | ~10K × 128MB × 0.1s | ~$0.002 |
| API Gateway | $3.50/M req | ~10K/mes | ~$0.035 |
| **Lambda Free Tier** | 1M req + 400K GB-s/mes | — | **$0** |
| **APIGW Free Tier** | 1M req/mes (12 meses) | — | **$0 primer año** |

**Costo proyectado:** $0 (Free Tier) → ~$0.04/mes después

---

### Caso 08: ECS Fargate (proyectado — sin Free Tier)

| Componente | Precio | Uso estimado | Costo/mes |
|:---|:---:|:---:|:---:|
| vCPU | $0.04048/hora | 0.25 vCPU × 24h × 30d | ~$7.29 |
| Memory | $0.004445/hora | 0.5 GB × 24h × 30d | ~$1.60 |
| Data transfer | $0.09/GB | ~0.1 GB/mes | ~$0.01 |

**Costo proyectado:** ~$8.90/mes (task corriendo 24/7)

**Estrategia de ahorro:** Apagar el task cuando no se usa. Con `ecs update-service --desired-count 0`
el costo cae a $0 hasta el próximo demo. El pipeline puede incluir un step de apagado post-validación.

---

### Caso 11: EKS (proyectado — costo más alto)

| Componente | Precio | Uso estimado | Costo/mes |
|:---|:---:|:---:|:---:|
| EKS Control Plane | $0.10/hora | 1 cluster × 24h × 30d | **$72.00** |
| EC2 worker nodes | ~$0.017/hora (t3.small) | 2 nodos × 24h × 30d | ~$24.48 |
| EBS storage | $0.10/GB-mes | ~10 GB | ~$1.00 |

**Costo proyectado:** ~$97.50/mes si corre 24/7

**Estrategia FinOps:** El cluster EKS solo vive durante la demo. Se crea con Terraform al inicio
y se destruye al finalizar. Costo real: ~$1-3 por sesión de demo de 30 min.

---

## Estrategia general de costos (GitHub Actions)

### Minutos de Actions (GitHub Free)

GitHub Free ofrece **2000 minutos/mes** para repositorios públicos (ilimitado) y privados.

| Workflow | Duración estimada | Frecuencia | Minutos/mes |
|:---|:---:|:---:|:---:|
| `despliegue.yml` | ~1 min | ~10/mes | ~10 min |
| `security-scan.yml` | ~3 min | ~20/mes | ~60 min |
| `wiki-sync.yml` | ~1 min | ~5/mes | ~5 min |

**Total GitHub Actions:** ~75 min/mes → **$0** (muy por debajo del Free Tier)

---

## Comparativa: GitHub vs GitLab (mismo stack)

| Elemento | GitHub Actions | GitLab CI |
|:---|:---|:---|
| Minutos CI gratuitos (público) | Ilimitado | 400 min/mes |
| Container Registry | GHCR gratuito (público) | GitLab Registry 10 GB gratis |
| Environments | GitHub Environments (free) | Environments (free) |
| OIDC con AWS | Soportado | Soportado |
| Scheduled jobs | Soportado (`schedule:`) | Soportado |
| Self-hosted runners | Soportado | Soportado |
| Costo AWS de los casos | Idéntico (mismos servicios) | Idéntico |

**Conclusión:** Para repositorios públicos, ambas plataformas son esencialmente gratuitas.
La diferencia está en el ecosistema y las integraciones nativas, no en el costo.

---

## Proyección anual (todos los casos activos)

| Escenario | Casos activos | Costo AWS estimado |
|:---|:---|:---:|
| Q2 2026 (casos 01-04) | Amplify + S3 + CloudFront | ~$0/mes |
| Q3 2026 (casos 01-08) | + Lambda + DynamoDB + Fargate | ~$10/mes |
| Q4 2026 (casos 01-11) | + EKS (solo demos) | ~$15-20/mes |

**Nota:** EKS y Fargate solo corren durante demos activas, no de forma permanente.

---

*Este documento se actualizará con datos reales al completar cada caso.
El Caso 09 automatizará la actualización vía Cost Explorer + scheduled workflow.*
