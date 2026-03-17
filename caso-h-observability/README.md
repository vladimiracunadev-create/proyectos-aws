# 👁️ Caso H: Observability & Health (CloudWatch + X-Ray)

[![Nivel-7](https://img.shields.io/badge/Nivel-7_Operaciones-blue?style=for-the-badge)]()
[![Status](https://img.shields.io/badge/Status-Completado-success?style=for-the-badge)]()
[![Stack](https://img.shields.io/badge/Stack-SAM_Lambda_CloudWatch_XRay-orange?style=for-the-badge)]()

> **"No puedes mejorar lo que no puedes medir."**
> Este caso convierte la infraestructura en una **caja de cristal**: cada invocación,
> cada error y cada milisegundo de latencia queda registrado, trazado y alertado.

---

## Estado real

- El caso implementa observabilidad completa sobre el stack existente del portafolio.
- **AWS X-Ray** activo en todas las Lambdas: service map, traces y subsegmentos.
- **CloudWatch Dashboard** definido como IaC (se crea y destruye con el stack SAM).
- **CloudWatch Alarms**: error rate y latencia p99 configuradas.
- **Métricas custom** en namespace `CasoH` publicadas desde Lambda.
- Stack name: `caso-h-observability` | Región: `us-east-2`

---

## 🎯 Objetivo

Demostrar los tres pilares de la observabilidad en AWS:

1. **Métricas** (CloudWatch): latencia, invocaciones, errores, métricas de negocio.
2. **Logs** (CloudWatch Logs): captura estructurada con contexto de traza.
3. **Trazas** (X-Ray): correlación distribuida entre API Gateway y Lambda.

---

## 🛠️ Stack

- **Entrada**: API Gateway HTTP API
- **Lógica**: AWS Lambda `HealthDashboardFunction` (Python 3.12)
- **Tracing**: AWS X-Ray (activo por SAM Globals)
- **Métricas**: Amazon CloudWatch (namespace `CasoH`, métricas custom)
- **Dashboard**: `AWS::CloudWatch::Dashboard` inline en CloudFormation
- **Alarmas**: `AWS::CloudWatch::Alarm` sobre errores y duración Lambda
- **IaC**: AWS SAM / CloudFormation

---

## 📁 Estructura del caso

```text
caso-h-observability/
├── README.md
├── AWS_PASO_A_PASO.md
├── index.html
├── backend/
│   ├── template.yaml
│   ├── events/
│   │   └── health-check.json
│   └── src/
│       └── app.py
└── docs/
    └── architecture.md
```

---

## 🔌 Endpoints

| Ruta | Método | Descripción |
|---|---|---|
| `/` | GET | Landing interactiva — explica la observabilidad del caso |
| `/health` | GET | Vista HTML en navegador / JSON con `?format=json` |
| `/metrics` | POST | Publica métrica custom `HealthChecks/Count` en CloudWatch |

---

## 🏗️ Qué aprende un reclutador de este caso

- Que sabes activar X-Ray en Lambdas con cero código extra (SAM Globals).
- Que defines observabilidad **como código** (dashboard y alarmas en CloudFormation).
- Que distingues métricas técnicas (errores, latencia) de métricas de negocio.
- Que tienes criterio para no depender de dashboards manuales en la consola.

---

## 🔗 Documentación complementaria

- 🏗️ [Arquitectura (Mermaid)](./docs/architecture.md)
- ☁️ [Guía Paso a Paso AWS](./AWS_PASO_A_PASO.md)
- ⬅️ [Roadmap Principal](../README.md)
- 📊 [Análisis de Casos PROYECTADO](../docs/PROYECTADOS_ANALISIS.md)
