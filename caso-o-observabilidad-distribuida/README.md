# 🔭 Caso O: Observabilidad Distribuida

[![Nivel-14](https://img.shields.io/badge/Nivel-14_Observabilidad_Distribuida-purple?style=for-the-badge)]()
[![Status](https://img.shields.io/badge/Status-Proyectado-lightgrey?style=for-the-badge)]()
[![Prerequisito](https://img.shields.io/badge/Prerequisito-Caso_H-orange?style=for-the-badge)]()

Expansión del Caso H a escenarios reales multi-servicio: trazas X-Ray correlacionadas entre múltiples Lambdas en cadena, SLOs definidos como código, CloudWatch Synthetics simulando usuarios reales y alertas basadas en error budget.

---

## Objetivo

Demostrar observabilidad de nivel productivo en una arquitectura distribuida:
- Trazar una petición completa a través de 3+ servicios Lambda encadenados
- Definir SLOs (Service Level Objectives) con alertas sobre el error budget
- Detectar degradación antes que el usuario con Synthetics canaries
- Correlacionar logs, métricas y trazas desde un único panel

---

## Stack planificado

| Componente | Tecnología | Propósito |
|---|---|---|
| Trazas distribuidas | AWS X-Ray + Trace IDs propagados | Correlacionar peticiones entre Lambdas |
| Métricas y SLOs | CloudWatch Metrics + Alarms | Error budget, availability target |
| Canaries | CloudWatch Synthetics | Simular usuarios reales en endpoints críticos |
| Logs estructurados | Lambda Powertools Logger | Correlación log-trace por request ID |
| Dashboard | CloudWatch Dashboard IaC (SAM) | Vista unificada métricas + trazas + canaries |
| Alertas | CloudWatch Alarms + SNS | Notificación cuando se quema el error budget |

---

## Diferencia con Caso H

| Aspecto | Caso H | Caso O |
|---|---|---|
| Servicios observados | 1 Lambda con endpoints | 3+ Lambdas en cadena |
| Trazas | X-Ray en un servicio | X-Ray propagado entre servicios (Trace ID) |
| SLOs | No definidos | Availability + latency p99 como código |
| Canaries | No | CloudWatch Synthetics simulando usuarios |
| Complejidad | 3/10 | 6/10 |

---

## Fases planificadas

### Fase 0 — Scaffold (actual)
- [x] README y documentación inicial
- [x] Carpeta del caso creada

### Fase 1 — Trazas multi-servicio
- [ ] 3 Lambdas en cadena: API Gateway → Lambda A → Lambda B → Lambda C
- [ ] X-Ray SDK en todas con propagación de Trace ID
- [ ] Service Map visible en CloudWatch

### Fase 2 — SLOs como código
- [ ] Availability target: 99.9% (permite ~43 min downtime/mes)
- [ ] Latency p99 < 1000ms
- [ ] CloudWatch Alarms disparando cuando se quema el 10% del error budget

### Fase 3 — Synthetics y dashboard unificado
- [ ] Canary que ejecuta el flujo completo cada 5 minutos
- [ ] Dashboard SAM: métricas + canary status + service map + top errores
- [ ] Alerta integrada a canal externo (SNS → email o webhook)

---

## Costo estimado

**< $5 USD por lab** — mismo modelo que Caso H:
- CloudWatch Dashboard: ~$3/mes (destruir post-lab)
- CloudWatch Synthetics canary: ~$0.0012 por ejecución (5 min = 288/día = ~$0.35/mes)
- X-Ray: free tier 100K trazas/mes — costo $0 para labs
- Lambda: free tier — $0

---

## Prerequisitos técnicos

- Caso H completado (CloudWatch Dashboard IaC + X-Ray básico)
- Caso M recomendado (infraestructura distribuida real para trazar)

---

## Por qué este caso importa

La observabilidad distribuida es el estándar en arquitecturas de microservicios. Correlacionar una petición a través de múltiples servicios, definir SLOs medibles y detectar degradación antes que los usuarios diferencia un sistema monitoreado de uno observado.

---

## Vínculos

- ⬅️ **[Regresar al README principal](../README.md)**
- 📍 **[Estado y Roadmap](../docs/ESTADO_Y_ROADMAP.md)**
- 🔗 **[Prerequisito: Caso H](../caso-h-observability/README.md)**
- 🔗 **[Prerequisito recomendado: Caso M](../caso-m-resiliencia-failover/README.md)**
