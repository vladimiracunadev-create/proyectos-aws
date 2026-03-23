# Cobertura de Certificaciones AWS

Mapeo de los 11 casos de este repositorio con los dominios de las certificaciones AWS más relevantes.
Este documento es complementario al del [repositorio GitLab](https://gitlab.com/vladimir.acuna.dev-group/proyectos-aws-gitlab),
que cubre el mismo mapeo desde la perspectiva de los servicios AWS.

---

## AWS Certified Developer – Associate (DVA-C02)

Relevancia: **Alta** — Este repositorio está especialmente alineado con DVA-C02
porque enfatiza pipelines CI/CD, Lambda, API Gateway y DynamoDB.

| Dominio DVA-C02 | Peso | Casos que lo cubren |
|:---|:---:|:---|
| Development with AWS Services | 32% | Casos 05, 06 (Lambda, DynamoDB, API GW) |
| Security | 26% | Casos 03, 04 (OIDC, IAM, Environments) |
| Deployment | 24% | Casos 01, 02, 03, 04, 07 (Amplify, S3, GitHub Actions) |
| Troubleshooting & Optimization | 18% | Transversal (security-scan, smoke tests, FinOps) |

### Temas DVA-C02 cubiertos por caso

| Caso | Temas |
|:---|:---|
| 01 | Amplify deployment, branch strategies, SSL/CDN |
| 02 | S3 static hosting, IAM access keys (patrón a reemplazar), `aws s3 sync` |
| 03 | OIDC Federation, CloudFront invalidation, IAM roles vs users |
| 04 | Deployment environments, approval gates, secrets management |
| 05 | Lambda functions, API Gateway REST, SAM templates, artifact packaging |
| 06 | DynamoDB CRUD, Lambda + DynamoDB permissions, parallel testing |
| 07 | Reusable deployment patterns, DRY pipelines |
| 08 | Container images, ECS task definitions, ECR/GHCR |
| 09 | Scheduled automation, Cost Explorer API, programmatic reporting |
| 10 | Multi-region architecture, Route53 health checks, DR patterns |
| 11 | EKS workloads, K8s manifests, GitOps workflows |

---

## AWS Certified Solutions Architect – Associate (SAA-C03)

Relevancia: **Media** — SAA-C03 es más amplio; este repo cubre principalmente
los dominios de deployment, seguridad y resiliencia.

| Dominio SAA-C03 | Peso | Casos relevantes |
|:---|:---:|:---|
| Design Secure Architectures | 30% | Casos 03, 04 (OIDC, IAM least privilege) |
| Design Resilient Architectures | 26% | Casos 10, 11 (multi-región, DR, EKS) |
| Design High-Performing Architectures | 24% | Casos 03 (CloudFront), 08 (Fargate) |
| Design Cost-Optimized Architectures | 20% | Caso 09 (FinOps, Cost Explorer) |

### Temas SAA-C03 cubiertos

| Área SAA-C03 | Cubierta por |
|:---|:---|
| S3 storage classes y hosting | Casos 02, 03 |
| CloudFront distributions | Caso 03 |
| IAM roles, policies, OIDC | Caso 03 |
| Amplify vs S3 vs CloudFront (cuándo usar cada uno) | Casos 01-03 |
| ECS Fargate vs EC2 | Caso 08 |
| EKS arquitectura básica | Caso 11 |
| Route53 failover routing | Caso 10 |
| AWS Budgets y Cost Explorer | Caso 09 |
| DynamoDB capacity modes | Caso 06 |
| API Gateway types (REST vs HTTP vs WebSocket) | Caso 05 |

---

## AWS Certified SysOps Administrator – Associate (SOA-C02)

Relevancia: **Media-Alta** — SOA-C02 cubre monitoring, automación y operaciones,
que son la columna vertebral de los workflows de GitHub Actions.

| Dominio SOA-C02 | Peso | Casos relevantes |
|:---|:---:|:---|
| Monitoring, Logging & Remediation | 20% | Caso 09 (Cost Explorer), transversal (security-scan) |
| Reliability & Business Continuity | 16% | Caso 10 (DR, multi-región) |
| Deployment, Provisioning & Automation | 18% | Todos los casos |
| Security & Compliance | 16% | Casos 03, 04 |
| Networking & Content Delivery | 18% | Casos 03, 10 (CloudFront, Route53) |
| Cost & Performance Optimization | 12% | Caso 09 |

---

## GitHub Actions — Habilidades adicionales (no AWS cert)

Aunque no forma parte de las certificaciones AWS, el dominio de GitHub Actions
es una habilidad diferenciadora en roles DevOps/Platform Engineering.

| Habilidad GitHub Actions | Caso donde se demuestra |
|:---|:---|
| Workflow triggers (push, PR, schedule, dispatch) | 02, 09 |
| `paths` filter en monorepos | 02 |
| Secrets y variables (repository vs environment) | 02, 04 |
| OIDC federation con AWS | 03 |
| Multi-job workflows con `needs:` | 05 |
| Artifacts entre jobs | 05 |
| Matrix strategy | 06 |
| Reusable workflows (`workflow_call`) | 07 |
| Composite actions | 07 |
| GitHub Container Registry (GHCR) | 08 |
| Scheduled workflows (`cron`) | 09 |
| Self-hosted runners (concepto) | 11 |

---

## Relación con el repositorio GitLab

El repositorio [proyectos-aws-gitlab](https://gitlab.com/vladimir.acuna.dev-group/proyectos-aws-gitlab)
cubre los mismos dominios de certificación pero desde la perspectiva del **qué** (qué hace cada servicio AWS).
Este repositorio los cubre desde el **cómo** (cómo se orquesta con GitHub Actions).

Juntos, los dos repositorios ofrecen cobertura práctica de:

- **DVA-C02:** ~75% de los temas prácticos cubiertos con deployments reales
- **SAA-C03:** ~50% de los temas de arquitectura cubiertos
- **SOA-C02:** ~60% de los temas de operaciones y automatización cubiertos

---

*Nota: La cobertura indicada es referencial. Los exámenes de certificación
cubren muchos más temas y servicios que los incluidos en estos repositorios.*
