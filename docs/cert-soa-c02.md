# ⚙️ Certificacion AWS SOA-C02 — SysOps Administrator Associate

> **Cobertura actual del repositorio:** 40%
> **Costo del examen:** ~$300 USD
> **Duracion del examen:** 180 minutos — incluye un lab practico (exam lab) de 20 minutos en consola AWS real
> **Validez:** 3 años
> **Recomendacion:** Tercera certificacion a largo plazo. Requiere completar Caso M (resiliencia) y Caso O (observabilidad distribuida) para alcanzar el 70%+. La SAA-C03 es prerequisito logico.

---

## Que evalua este examen

La SOA-C02 es la mas operacional de las tres. Evalua la administracion de infraestructura AWS: monitoreo, alertas, automatizacion de operaciones, resiliencia, parchado de sistemas, cumplimiento y redes. Incluye un **exam lab real en consola AWS** — el unico entre las tres asociadas.

---

## Dominios y cobertura por caso

### Dominio 1 — Monitoreo, logging y remediacion (20% del examen)

| Tema requerido | Cubierto por | Estado |
|---|---|---|
| CloudWatch Metrics, Alarms, Dashboards | Caso H | ✅ |
| CloudWatch Logs Insights (queries) | Caso H (documentado) | ✅ parcial |
| X-Ray trazas y service maps | Caso H | ✅ |
| EventBridge rules y targets | Caso G | ✅ |
| Systems Manager (SSM) — Run Command, Patch Manager | No cubierto | ❌ estudiar |
| AWS Config — reglas de cumplimiento | No cubierto | ❌ estudiar |
| CloudTrail — auditoria de API calls | No implementado | ❌ estudiar |
| Health Dashboard y Service Health | No cubierto | ⚠️ conceptual |

**Cobertura del dominio: 45%**
**Gap critico:** Systems Manager y AWS Config — pilares operacionales ausentes en el repo.

---

### Dominio 2 — Continuidad de negocio y resiliencia (16% del examen)

| Tema requerido | Cubierto por | Estado |
|---|---|---|
| Multi-AZ con ALB y auto recovery | Caso J | ✅ |
| Route 53 health checks y failover | Caso M (Fase 0 — pendiente) | 🔄 |
| Backup y restore con AWS Backup | No cubierto | ❌ estudiar |
| RDS snapshots automaticos | No aplica en repo | ❌ estudiar separado |
| S3 Replication entre regiones | No implementado | ❌ estudiar |
| ECS health checks y task replacement | Caso J | ✅ parcial |
| DynamoDB Point-in-Time Recovery | Caso E (mencionado) | ⚠️ conceptual |

**Cobertura del dominio: 30%**
**Gap critico:** AWS Backup, RDS snapshots y S3 replication — temas clasicos del examen.

---

### Dominio 3 — Despliegue, provisionamiento y automatizacion (18% del examen)

| Tema requerido | Cubierto por | Estado |
|---|---|---|
| CloudFormation — stacks, change sets, drift | SAM genera CF — todos los casos | ✅ |
| SAM — despliegue automatizado | Casos D, E, F, G, H | ✅ |
| Systems Manager — State Manager, Automation | No cubierto | ❌ estudiar |
| OpsWorks | No cubierto | ❌ solo conceptual |
| Service Catalog | No cubierto | ❌ conceptual |
| EC2 Image Builder | No cubierto | ❌ estudiar |
| Terraform IaC para AWS | Casos C, J, K, L | ✅ (no evaluado en examen pero equivalente) |
| GitLab CI/CD para despliegue automatizado | Todos los casos | ✅ practica real |

**Cobertura del dominio: 40%**

---

### Dominio 4 — Seguridad y cumplimiento (16% del examen)

| Tema requerido | Cubierto por | Estado |
|---|---|---|
| IAM — roles, politicas, boundaries | Caso L + todos los casos | ✅ |
| AWS Organizations y SCPs | No cubierto | ❌ estudiar |
| AWS Config — reglas y remediacion automatica | No cubierto | ❌ estudiar |
| GuardDuty — deteccion de amenazas | No cubierto | ⚠️ conceptual |
| Security Hub — dashboard de cumplimiento | No cubierto | ⚠️ conceptual |
| WAF y Shield | Caso F | ✅ |
| Certificate Manager (ACM) | Caso J (ALB con HTTPS) | ✅ |
| CloudTrail — integridad de logs | No implementado | ❌ estudiar |

**Cobertura del dominio: 35%**

---

### Dominio 5 — Redes y entrega de contenido (18% del examen)

| Tema requerido | Cubierto por | Estado |
|---|---|---|
| VPC — subnets publicas/privadas, NAT Gateway | Caso J y K (ECS/EKS en VPC) | ✅ |
| Security Groups y NACLs | Casos J, K | ✅ |
| CloudFront — distribuciones, behaviors, OAI | Caso C | ✅ |
| Route 53 — tipos de records, routing policies | Caso M (pendiente) | 🔄 |
| ALB y NLB — listeners, target groups | Caso J | ✅ |
| VPC Peering y Transit Gateway | No cubierto | ❌ estudiar |
| PrivateLink y VPC Endpoints | No cubierto | ❌ estudiar |
| Direct Connect vs VPN | No cubierto | ❌ conceptual |

**Cobertura del dominio: 45%**

---

### Dominio 6 — Optimizacion de costo y rendimiento (12% del examen)

| Tema requerido | Cubierto por | Estado |
|---|---|---|
| Trusted Advisor | No cubierto | ⚠️ conceptual |
| Compute Optimizer | No cubierto | ⚠️ conceptual |
| Cost Explorer y Budgets | Caso L | ✅ |
| S3 storage classes y lifecycle | Caso B, C | ✅ parcial |
| Auto Scaling — target tracking, step scaling | Caso J (ECS scaling) | ✅ parcial |
| Lambda — provisioned concurrency vs reserved | Mencionado en H | ⚠️ conceptual |

**Cobertura del dominio: 40%**

---

## Resumen visual de cobertura

```
Dominio 1 — Monitoreo y logging (20%):      ████░░░░░░  45%
Dominio 2 — Continuidad / resiliencia (16%): ███░░░░░░░  30%
Dominio 3 — Despliegue y automatizacion (18%):████░░░░░░  40%
Dominio 4 — Seguridad y cumplimiento (16%):  ███░░░░░░░  35%
Dominio 5 — Redes y contenido (18%):         ████░░░░░░  45%
Dominio 6 — Costo y rendimiento (12%):       ████░░░░░░  40%

COBERTURA TOTAL ESTIMADA:                    ████░░░░░░  40%
```

---

## Como mejorar la cobertura con casos futuros

| Caso futuro | Dominios que cubre | Cobertura esperada tras completarlo |
|---|---|---|
| Caso M — Resiliencia Multi-AZ + Route 53 | Dom 2 + Dom 5 | +15% → 55% total |
| Caso O — Observabilidad distribuida | Dom 1 + Dom 4 | +10% → 65% total |
| Lab independiente: Systems Manager | Dom 1 + Dom 3 | +8% → 73% total |
| Lab independiente: AWS Config + CloudTrail | Dom 1 + Dom 4 | +5% → 78% total |

---

## Temas criticos que requieren estudio externo al repo

| Tema | Frecuencia en examen | Accion |
|---|---|---|
| Systems Manager (Run Command, Patch Manager, Session Manager) | Muy alta | Lab dedicado 4 horas |
| AWS Config (reglas managed + custom, remediacion) | Alta | Lab dedicado 2 horas |
| CloudTrail (integridad, log file validation, integracion con CloudWatch) | Alta | Lab dedicado 1 hora |
| AWS Backup (vault, backup plans, restore) | Media | Lab dedicado 2 horas |
| GuardDuty (hallazgos, tipos de amenazas) | Media | Conceptual + demo |
| VPC Endpoints y PrivateLink | Media | Lab con S3 VPC endpoint |
| Transit Gateway | Baja-Media | Solo conceptual |
| EC2 Image Builder | Baja | Solo conceptual |

---

## Nota sobre el Exam Lab

La SOA-C02 incluye un **lab practico de 20 minutos** donde ejecutas tareas reales en una consola AWS sandbox. Tareas tipicas:
- Crear una alarma de CloudWatch para una metrica de Lambda
- Configurar un S3 lifecycle policy
- Asociar un Security Group a una instancia EC2
- Habilitar CloudTrail en una region

El trabajo en este repositorio con consola y CLI te prepara bien para este lab.

---

## Plan de estudio recomendado

```
Prerequisito:  Completar SAA-C03 primero
Semana 1-2:   Completar Caso M (Route 53 failover real)
Semana 3:     Systems Manager — lab completo (Run Command, Patch Manager)
Semana 4:     AWS Config + CloudTrail — labs dedicados
Semana 5:     AWS Backup + GuardDuty — conceptual + demo
Semana 6:     VPC avanzado (endpoints, peering)
Semana 7:     Simulacro con exam labs (usar Tutorials Dojo SOA-C02)
Semana 8:     Examen
```

---

*Ultima revision: marzo 2026 — basado en guia oficial SOA-C02 de AWS Training and Certification*
