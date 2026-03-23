# Caso 07 — Reusable Workflows + Composite Actions

![Estado](https://img.shields.io/badge/estado-📋%20Planificado-lightgrey?style=flat-square)
![Trimestre](https://img.shields.io/badge/trimestre-Q3%202026-blue?style=flat-square)
![AWS](https://img.shields.io/badge/AWS-Múltiples%20servicios-FF9900?style=flat-square&logo=amazonaws&logoColor=white)
![Actions](https://img.shields.io/badge/GitHub_Actions-Reusable%20·%20Composite-2088FF?style=flat-square&logo=githubactions&logoColor=white)

---

## 🎯 Objetivo

Eliminar duplicación entre casos. Extraer la lógica común de deploy a una
**librería interna de GitHub Actions** reutilizable por todos los casos futuros.

---

## 🔑 Lo que introduce

### En GitHub Actions
| Capacidad nueva | Descripción |
|:---|:---|
| `workflow_call` | Convierte un workflow en una función llamable desde otros workflows |
| Composite Action | Agrupa steps repetidos en una acción reutilizable (`.github/actions/`) |
| `inputs` y `outputs` | Tipado y validación de parámetros entre caller y callee |
| `secrets: inherit` | Pasa secrets del caller al reusable workflow de forma segura |

---

## 🏗️ Estructura objetivo

```
.github/
├── workflows/
│   ├── deploy-s3-oidc.yml        ← Reusable: deploy a S3 con OIDC
│   ├── deploy-lambda-sam.yml     ← Reusable: deploy Lambda con SAM
│   └── smoke-test.yml            ← Reusable: smoke tests post-deploy
└── actions/
    ├── setup-aws-oidc/
    │   └── action.yml            ← Composite: configura OIDC en 1 step
    └── notify-deploy/
        └── action.yml            ← Composite: notificación post-deploy
```

### Uso desde cualquier caso futuro

```yaml
# En caso-08, caso-09, caso-10...
jobs:
  deploy:
    uses: ./.github/workflows/deploy-s3-oidc.yml@main
    with:
      bucket: ${{ vars.BUCKET_PROD }}
      environment: production
    secrets: inherit
```

---

## 📜 Certificaciones relevantes

![DVA-C02](https://img.shields.io/badge/DVA--C02-Deployment%2024%25-FF6B6B?style=flat-square)
![SOA-C02](https://img.shields.io/badge/SOA--C02-Automation%2018%25-45B7D1?style=flat-square)

| Certificación | Temas que cubre este caso |
|:---|:---|
| **DVA-C02** | CI/CD pipelines reutilizables, modularización de infraestructura |
| **SOA-C02** | Automatización de operaciones, estandarización de deploys |

---

## ⬅️ Anterior · Siguiente ➡️

| | Caso |
|:---|:---|
| ⬅️ Anterior | [Caso 06 — DynamoDB + Matrix](../caso-06-dynamodb-matrix/README.md) |
| ➡️ Siguiente | [Caso 08 — Containers + GHCR](../caso-08-containers-ghcr/README.md) |
