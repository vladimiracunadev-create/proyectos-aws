# 🛡️ Caso M: Resiliencia & Failover (Multi-AZ + Multi-Región)

[![Nivel-12](https://img.shields.io/badge/Nivel-12_Staff_SRE-crimson?style=for-the-badge)](.)
[![Status](https://img.shields.io/badge/Status-FUTURO_PLANIFICADO-lightgrey?style=for-the-badge)](.)
[![Fase](https://img.shields.io/badge/Fase_Actual-0_Scaffold-blue?style=for-the-badge)](.)

> **Esto es lo que diferencia un demo de un sistema profesional: la capacidad de detectar fallos y
> conmutar (failover) con runbooks y pruebas documentadas.**
>
> La resiliencia no es opcional en producción. Es el estándar mínimo de cualquier empresa que toma
> en serio la continuidad de su servicio. Este caso demuestra, de forma demostrable con un
> **GameDay futuro**, cómo un sistema en AWS puede sobrevivir a la caída de instancias, zonas de
> disponibilidad completas y hasta regiones enteras.

---

## 🎯 Propósito

Demostrar **continuidad operacional** ante fallos reales:

- Una instancia EC2/ECS/EKS cae → el balanceador detecta el fallo y redirige el tráfico.
- Una Zona de Disponibilidad (AZ) completa pierde conectividad → el tráfico fluye a otra AZ
  dentro de la misma región.
- Una región entera (ej: `us-east-1`) queda inaccesible → Route 53 o Global Accelerator
  conmuta automáticamente hacia la región secundaria (`us-west-2`).

**Audiencia objetivo**: Reclutadores SRE/Cloud/Arquitectura, equipos de Platform Engineering,
ingenieros que necesiten demostrar madurez operativa.

---

## 🔥 Problema Real que Resuelve

| Escenario de Fallo | Sin Resiliencia | Con Caso M |
|---|---|---|
| Instancia EC2/Pod cae | ❌ Downtime hasta reinicio manual | ✅ Auto-healing en segundos |
| AZ `us-east-1a` cae | ❌ Downtime parcial o total | ✅ Tráfico redirigido a `us-east-1b/c` |
| Región `us-east-1` cae | ❌ Downtime total (minutos/horas) | ✅ Failover a `us-west-2` en segundos |
| Despliegue con error | ❌ Afecta 100% del tráfico | ✅ Rolling update; canary posible |

---

## 🏗️ Qué Demuestra

### Nivel A: Alta Disponibilidad Multi-AZ (1 región)

- **ALB (Application Load Balancer)** distribuyendo tráfico entre múltiples AZs.
- **Health checks** automáticos con endpoint `/healthz`.
- **Auto Scaling Group** o **ECS Service desired count ≥ 2** en AZs distintas.
- **Eliminación de SPOF** (Single Point of Failure) a nivel de instancia y AZ.

### Nivel B: Recuperación ante Desastre Multi-Región

- **Región primaria**: `us-east-1` (o la elegida) con arquitectura completa Multi-AZ.
- **Región secundaria**: `us-west-2` en modo **Warm Standby** (mínima capacidad activa).
- **Route 53 Failover Routing** con health checks al endpoint primario.
- **RTO objetivo**: < 60 segundos (failover automático DNS).
- **RPO objetivo**: < 5 minutos (datos replicados o eventual consistency aceptada).

---

## ❌ Qué NO Hace Todavía (Fase 0)

- **No despliega ningún recurso en AWS.** Todo lo que ves aquí es documentación, plantillas
  skeleton y scripts placeholder.
- No hay `terraform apply` ni `aws` CLI apuntando a recursos reales.
- No hay credenciales ni variables secretas requeridas en este momento.
- Los scripts de simulación en `scripts/` son **placeholders no destructivos**.

---

## 🗺️ Roadmap por Fases

### Fase 0 (ACTUAL): Scaffold + Docs + Placeholders

- [x] Estructura de carpetas y archivos creada.
- [x] Documentación de arquitectura, runbook y roadmap.
- [x] Plantillas de Terraform (skeleton, sin `apply`).
- [x] Scripts de simulación (placeholders, no ejecutables aún).
- [x] Integración en README principal y ROADMAP global.

### Fase 1: Multi-AZ en Región Única

- [ ] Desplegar ALB + ECS Fargate (o EC2 ASG) en `us-east-1` con **2 AZs mínimo**.
- [ ] Implementar endpoint `/healthz` en la aplicación (HTTP 200 / HTTP 5xx).
- [ ] Configurar Health Checks en el Target Group (intervalo 15s, threshold 2).
- [ ] Ejecutar `drill-failover.sh` (Fase 1): bajar 1 task ECS y observar el ALB.
- [ ] Verificar **0 downtime** desde el cliente con `check.sh`.
- [ ] Documentar evidencia de resultados en `VISUALIZATION.md`.

### Fase 2: Warm Standby Multi-Región + Route 53 Failover

- [ ] Declarar infraestructura espejo en `us-west-2` (Terraform module reutilizado).
- [ ] Configurar **Route 53 Failover Routing Policy** con Health Check al ALB primario.
- [ ] Establecer TTL bajo en el registro DNS (60 segundos max).
- [ ] Ejecutar `drill-failover.sh` (Fase 2): forzar unhealthy en primario, observar DNS.
- [ ] Ejecutar `drill-failback.sh`: restaurar primario, verificar retorno automático.
- [ ] Documentar **RTO/RPO reales** medidos durante el GameDay.

### Fase 3: Automatización GameDay + Observabilidad + (Opcional) ARC

- [ ] Automatizar GameDay con scripts parametrizados.
- [ ] CloudWatch Dashboards para métricas de failover (latencia, error rate, DNS TTL).
- [ ] Alertas SNS para cambios de estado de Health Check.
- [ ] Evaluar **AWS ARC (Application Recovery Controller)** o **Global Accelerator**
  como alternativa a Route 53 puro para RTO < 30s.
- [ ] Runbook post-mortem automatizado.

---

## 📋 Requisitos (TODOS MARCADOS COMO FUTURO)

> ⚠️ **FUTURO**: Los siguientes requisitos aplican cuando se implemente la Fase 1 o superior.
> En Fase 0 (actual) no se necesita ningún recurso AWS.

- **Cuenta AWS** con permisos para: ALB, ECS/EKS, Route 53, CloudWatch, IAM.
- **Dominio registrado** o **Hosted Zone** en Route 53 (para Fase 2).
- **Terraform >= 1.5** instalado localmente (para `plan` y `validate`).
- **Credenciales AWS** configuradas (OIDC via GitLab CI o `aws configure` local).
- **Región primaria**: `us-east-1` (configurable en `variables.tf`).
- **Región secundaria**: `us-west-2` (configurable en `variables.tf`).
- **Imagen Docker**: disponible en ECR o imagen pública como placeholder.

---

## 🎬 Demo Futura (Pasos con curl/dig)

> ⚠️ **PLACEHOLDER**: Los endpoints son ficticios. Se actualizan cuando la Fase 1/2 esté activa.

```bash
# 1. Verificar endpoint primario
curl -f https://PRIMARY_ALB_DNS/healthz
# → HTTP 200 {"status":"healthy","az":"us-east-1a","region":"us-east-1"}

# 2. Ver registro DNS apuntando al primario
dig +short api.TU_DOMINIO.com

# 3. Simular caída (Fase 2 - ver drill-failover.sh)
./scripts/drill-failover.sh --mode regional

# 4. Observar failover DNS (esperar ~60s = TTL Route 53)
watch -n 5 'dig +short api.TU_DOMINIO.com'
# → El IP cambia de us-east-1 a us-west-2

# 5. Verificar que la app responde desde la región secundaria
curl -f https://SECONDARY_ALB_DNS/healthz
# → HTTP 200 {"status":"healthy","az":"us-west-2a","region":"us-west-2"}

# 6. Failback controlado
./scripts/drill-failback.sh
```

---

## 💰 Riesgos de Costo y Mitigaciones

| Componente | Costo Estimado | Mitigación |
|---|---|---|
| ALB (1 región) | ~$16 USD/mes | Destruir con `terraform destroy` tras validar |
| ALB (2 regiones) | ~$32 USD/mes | Levantar solo durante GameDay (~2h) |
| ECS Fargate (2 tasks) | ~$10-20 USD/mes | Task count = 0 cuando no se usa |
| Route 53 Hosted Zone | $0.50 USD/mes | Costo marginal, aceptable |
| Route 53 Health Checks | $0.75 c/u/mes | Solo 2 health checks (primario + secundario) |
| NAT Gateway (2 AZs) | ~$65 USD/mes | ⚠️ Costo más alto; usar solo en GameDay |
| Global Accelerator | $18 USD/mes + data | Fase 3 opcional; evaluar costo/beneficio |

> **Free Tier Mindset**: Levanta la infraestructura → valida → destruye. Nunca dejes recursos
> en pie sin monitoreo de costos con AWS Budgets (ya configurado en Caso L).

---

## ✅ Definition of Done (Fase 1 — Próximo Sprint)

- [ ] ALB con 2 Target Groups en AZs distintas respondiendo HTTP 200.
- [ ] Health Check configurado: intervalo 15s / threshold unhealthy = 2.
- [ ] ECS Service con `desired_count = 2` en AZs diferentes.
- [ ] `check.sh` valida 0 downtime durante bajar 1 task ECS.
- [ ] Evidencia capturada en `VISUALIZATION.md` (screenshots + curl output).
- [ ] `terraform plan` pasa sin errores en CI (job `case_m_validate`).
- [ ] Documentación actualizada con resultados reales de RTO/RPO.

---

## 🔗 Documentación Complementaria

- ☁️ [Guía Paso a Paso AWS (Fases 0→3)](./AWS_PASO_A_PASO.md)
- 🏗️ [Arquitectura Objetivo](./docs/architecture.md)
- 📋 [Runbook de Failover](./docs/runbook-failover.md)
- 🗺️ [Roadmap Detallado](./docs/roadmap.md)
- 🔧 [Instrucciones IaC](./infra/README.md)
- ⬅️ [Regresar al Roadmap Principal](../README.md)

---

> **Preparado por Vladimir Acuña — Staff Platform Engineer / SRE.**
> *Este caso es demostrable con un GameDay futuro. La estructura está lista; solo falta apretar
> el gatillo cuando el momento (y el presupuesto) lo amerite.*
