# Caso 05 — Lambda + API Gateway

![Estado](https://img.shields.io/badge/estado-📋%20Planificado-lightgrey?style=flat-square)
![Trimestre](https://img.shields.io/badge/trimestre-Q2--Q3%202026-blue?style=flat-square)
![AWS](https://img.shields.io/badge/AWS-Lambda%20·%20API%20Gateway%20·%20SAM-FF9900?style=flat-square&logo=amazonaws&logoColor=white)
![Actions](https://img.shields.io/badge/GitHub_Actions-Multi--job%20·%20Artifacts-2088FF?style=flat-square&logo=githubactions&logoColor=white)

---

## 🎯 Objetivo

Primer backend real. Introduce el patrón **test → build → deploy** con jobs
encadenados y artefactos compartidos entre ellos.

---

## 🔑 Lo que introduce

### En AWS

| Servicio | Para qué |
|:---|:---|
| **AWS Lambda** | Función serverless Python/Node.js |
| **API Gateway** | Endpoint HTTP público que invoca la Lambda |
| **AWS SAM** | Framework de despliegue serverless (IaC declarativo) |

### En GitHub Actions

| Capacidad nueva | Descripción |
|:---|:---|
| `needs:` | Secuenciación explícita de jobs (test debe pasar antes de build) |
| `actions/upload-artifact` | El job `build` sube el paquete SAM compilado |
| `actions/download-artifact` | El job `deploy` descarga y usa ese mismo paquete |
| `workflow_dispatch` con `inputs` | Deploy manual con selección de entorno como parámetro |

---

## 🏗️ Arquitectura proyectada

```mermaid
flowchart TB
    DEV[Dev Local\ngit push] --> GH[(GitHub)]

    GH --> J1[Job: test\npytest o jest]
    J1 -->|needs: test OK| J2[Job: build\nsam build]
    J2 -->|upload-artifact| ART[Actions Artifact\npackage.zip]
    ART -->|download-artifact| J3[Job: deploy\nneeds: build]

    J3 -->|sam deploy| CF[CloudFormation\nStack]
    CF --> LAMBDA[AWS Lambda\nPython o Node.js]
    CF --> APIGW[API Gateway\nHTTP endpoint]

    APIGW --> CLIENT[Cliente API]
```

## 🔄 Flujo multi-job (objetivo)

```text
workflow trigger (push o dispatch)
  │
  ├── job: test (pytest)
  │     └── ✅ tests pasan
  │
  ├── job: build (needs: test)
  │     └── sam build → artefacto .zip
  │         └── upload-artifact → guardado en Actions
  │
  └── job: deploy (needs: build)
        └── download-artifact
            └── sam deploy --no-confirm-changeset
                └── Lambda + API Gateway actualizados
```

> **Principio clave:** El artefacto que se prueba es el mismo que llega a producción.
> No hay "build de prod" diferente al "build de tests".

---

## 📋 Implementación proyectada — pasos clave

> Guia detallada con comandos exactos, errores comunes y verificaciones: **[AWS_PASO_A_PASO.md](./AWS_PASO_A_PASO.md)**

1. **Escribir la Lambda** → función Python/Node.js con handler estándar + `requirements.txt` o `package.json`
2. **Crear `template.yaml` SAM** → define `AWS::Serverless::Function` + `AWS::Serverless::Api`
3. **Job `test`** → `pytest` o `jest` sobre la función — el job de build solo se ejecuta si pasan
4. **Job `build`** → `sam build` compila el paquete → `actions/upload-artifact` guarda el `.zip`
5. **Job `deploy`** → `actions/download-artifact` descarga el paquete → `sam deploy --no-confirm-changeset --capabilities CAPABILITY_IAM`
6. **Verificar** → CloudFormation crea el stack automáticamente · API Gateway genera la URL del endpoint

> **Principio clave:** El artefacto que se prueba en el job `test` es el mismo `.zip` que llega a producción. No hay re-build en producción.

---

## 📜 Certificaciones relevantes

![DVA-C02](https://img.shields.io/badge/DVA--C02-Development%2032%25-FF6B6B?style=flat-square)
![SAA-C03](https://img.shields.io/badge/SAA--C03-High%20Performance%2024%25-4ECDC4?style=flat-square)
![SOA-C02](https://img.shields.io/badge/SOA--C02-Deployment%2018%25-45B7D1?style=flat-square)

| Certificación | Temas que cubre este caso |
|:---|:---|
| **DVA-C02** | Lambda lifecycle, API Gateway types, SAM templates, packaging |
| **SAA-C03** | Serverless vs EC2 trade-offs, API Gateway REST vs HTTP |
| **SOA-C02** | Automated deployment pipelines, artifact management |

---

## ⬅️ Anterior · Siguiente ➡️

| | Caso |
|:---|:---|
| ⬅️ Anterior | [Caso 04 — Environments](../caso-04-environments-approvals/README.md) |
| ➡️ Siguiente | [Caso 06 — DynamoDB + Matrix](../caso-06-dynamodb-matrix/README.md) |
