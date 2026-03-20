# Caso H: Observability & Health (CloudWatch + X-Ray)

[![Nivel-7](https://img.shields.io/badge/Nivel-7_Operaciones-blue?style=for-the-badge)]()
[![Status](https://img.shields.io/badge/Status-Completado-success?style=for-the-badge)]()
[![Stack](https://img.shields.io/badge/Stack-SAM_Lambda_CloudWatch_XRay-orange?style=for-the-badge)]()

> **"No puedes mejorar lo que no puedes medir."**
> Este caso convierte la infraestructura en una **caja de cristal**: cada invocacion,
> cada error y cada milisegundo de latencia queda registrado, trazado y alertado.

---

## Estado real

- El caso implementa observabilidad completa sobre un stack SAM autocontenido.
- **AWS X-Ray** activo en la Lambda del caso: service map, traces y detalle por invocacion.
- **CloudWatch Dashboard** definido como IaC (se crea y destruye con el stack).
- **CloudWatch Alarms**: error rate y latencia p99 configuradas.
- **Metricas custom** en namespace `CasoH` publicadas desde Lambda.
- Stack name: `caso-h-observability` | Region: `us-east-2`
- Infraestructura de evidencia estatica: el dashboard se levanta solo en ventanas de laboratorio por su costo fijo.
- **[Reporte de Visualizacion y Resultados](./VISUALIZATION.md)**
- URL temporal del ultimo laboratorio validado: `https://z7evf8mrzf.execute-api.us-east-2.amazonaws.com/`

---

## Objetivo

Demostrar los tres pilares de la observabilidad en AWS:

1. **Metricas** (CloudWatch): latencia, invocaciones, errores y metricas de negocio.
2. **Logs** (CloudWatch Logs): captura estructurada con contexto operacional.
3. **Trazas** (X-Ray): correlacion entre entrada HTTP, Lambda y salida de telemetria.

---

## Stack

- **Entrada**: API Gateway HTTP API
- **Logica**: AWS Lambda `HealthDashboardFunction` (Python 3.12)
- **Tracing**: AWS X-Ray (activo por SAM Globals)
- **Metricas**: Amazon CloudWatch (namespace `CasoH`, metricas custom)
- **Dashboard**: `AWS::CloudWatch::Dashboard` inline en CloudFormation
- **Alarmas**: `AWS::CloudWatch::Alarm` sobre errores y duracion Lambda
- **IaC**: AWS SAM / CloudFormation

---

## Estructura del caso

```text
caso-h-observability/
|-- README.md
|-- AWS_PASO_A_PASO.md
|-- VISUALIZATION.md
|-- index.html
|-- img/
|-- backend/
|   |-- template.yaml
|   |-- events/
|   |   `-- health-check.json
|   `-- src/
|       `-- app.py
`-- docs/
    `-- architecture.md
```

---

## Endpoints

| Ruta | Metodo | Descripcion |
|---|---|---|
| `/` | GET | Landing interactiva que explica el caso y dispara acciones de demo |
| `/health` | GET | Vista HTML en navegador / JSON con `?format=json` |
| `/metrics` | POST | Publica la metrica custom `HealthChecks` en CloudWatch |

---

## Que aprende un reclutador de este caso

- Que sabes activar X-Ray en Lambdas con cero codigo adicional en el handler.
- Que defines observabilidad **como codigo** y no como configuracion manual.
- Que distingues metricas tecnicas (errores, latencia) de metricas de negocio.
- Que entiendes el trade-off FinOps de un dashboard con costo fijo.

---

## Documentacion complementaria

- [Arquitectura (Mermaid)](./docs/architecture.md)
- [Guia Paso a Paso AWS](./AWS_PASO_A_PASO.md)
- [Reporte de Visualizacion y Resultados](./VISUALIZATION.md)
- [Roadmap Principal](../README.md)
- [Analisis de Casos PROYECTADO](../docs/PROYECTADOS_ANALISIS.md)
