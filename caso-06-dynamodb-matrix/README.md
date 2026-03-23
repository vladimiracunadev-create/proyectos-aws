# Caso 06 — DynamoDB + Matrix Builds

![Estado](https://img.shields.io/badge/estado-📋%20Planificado-lightgrey?style=flat-square)
![Trimestre](https://img.shields.io/badge/trimestre-Q3%202026-blue?style=flat-square)
![AWS](https://img.shields.io/badge/AWS-DynamoDB%20·%20Lambda-FF9900?style=flat-square&logo=amazonaws&logoColor=white)
![Actions](https://img.shields.io/badge/GitHub_Actions-Matrix%20Strategy-2088FF?style=flat-square&logo=githubactions&logoColor=white)

---

## 🎯 Objetivo

Añadir persistencia real (DynamoDB) y demostrar **matrix strategy**:
el mismo código probado en múltiples runtimes y regiones en paralelo.

---

## 🔑 Lo que introduce

### En AWS
| Servicio | Para qué |
|:---|:---|
| **DynamoDB** | Base de datos NoSQL serverless (CRUD real desde Lambda) |
| **DynamoDB Streams** | Eventos de cambio para futuros casos event-driven |
| **IAM** | Política mínima necesaria para que Lambda acceda a DynamoDB |

### En GitHub Actions
| Capacidad nueva | Descripción |
|:---|:---|
| `strategy.matrix` | Define combinaciones: runtimes × regiones |
| `fail-fast: false` | Una celda que falla no cancela las demás |
| Matrix output en summary | Tabla de resultados por combinación en el workflow summary |

---

## 🔄 Matrix en acción (objetivo)

```yaml
strategy:
  fail-fast: false
  matrix:
    runtime: [python3.11, python3.12]
    region:  [us-east-1, us-east-2]

# Resultado: 4 jobs en paralelo
# python3.11 × us-east-1   ✅
# python3.11 × us-east-2   ✅
# python3.12 × us-east-1   ✅
# python3.12 × us-east-2   ✅
```

---

## 🗄️ Modelo de datos DynamoDB

```json
{
  "PK":        "USER#vladimir",
  "SK":        "PROJECT#caso-06",
  "title":     "DynamoDB Matrix Demo",
  "status":    "active",
  "createdAt": "2026-Q3"
}
```

---

## 📜 Certificaciones relevantes

![DVA-C02](https://img.shields.io/badge/DVA--C02-Development%2032%25-FF6B6B?style=flat-square)
![SAA-C03](https://img.shields.io/badge/SAA--C03-Resilient%20Arch%2026%25-4ECDC4?style=flat-square)

| Certificación | Temas que cubre este caso |
|:---|:---|
| **DVA-C02** | DynamoDB data modeling, partition keys, capacity modes, Streams |
| **SAA-C03** | DynamoDB vs RDS trade-offs, single-table design, global tables |
| **SOA-C02** | DynamoDB monitoring (CloudWatch), backup & point-in-time recovery |

---

## ⬅️ Anterior · Siguiente ➡️

| | Caso |
|:---|:---|
| ⬅️ Anterior | [Caso 05 — Lambda + API GW](../caso-05-lambda-api-gateway/README.md) |
| ➡️ Siguiente | [Caso 07 — Reusable Workflows](../caso-07-reusable-workflows/README.md) |
