# 💰 FinOps: Costos Reales por Caso Completado

> **Autor:** Vladimir Acuna
> **Version:** 1.0
> **Ultima actualizacion:** 18 de marzo de 2026
> **Alcance:** 11 casos completados (A, B, C, D, E, F, G, H, J, K, L)

---

## Por qué este documento existe

AWS cobra por uso. No por intención, no por tener la cuenta abierta (salvo excepciones como EKS), sino por consumo real de recursos. Entender ese modelo es parte de la madurez técnica.

Este repositorio fue construido para aprender. Por eso cada caso tiene una estrategia de costo asociada: algunos se pueden dejar activos permanentemente sin gasto, otros requieren destruir la infraestructura al terminar la práctica. No saberlo no es un error de cloud, es un error de planificación.

Este documento responde tres preguntas por cada caso:
1. ¿Qué servicios cobran?
2. ¿Cuánto cuesta si lo dejas activo?
3. ¿Cuál es la estrategia de control recomendada?

---

## Conceptos base del modelo de precios en AWS

Antes de revisar cada caso, conviene tener claro el lenguaje:

| Concepto | Qué significa | Ejemplo |
|---|---|---|
| **Free Tier** | Capa gratuita: AWS regala cierta cantidad mensual de cada servicio | 1 millón de invocaciones Lambda/mes gratis para siempre |
| **Always Free** | Sin límite de tiempo, siempre gratuito hasta cierto umbral | DynamoDB: 25GB + 25 WCU/RCU siempre gratis |
| **12 months free** | Solo los primeros 12 meses desde la creación de la cuenta | EC2 t2.micro, 750 horas/mes |
| **Pay-per-use** | Pagas solo lo que consumes, sin cargo por tener el servicio disponible | Lambda, EventBridge, SQS, SNS |
| **Provisioned** | Pagas por tener el recurso reservado, lo uses o no | EKS control plane ($0.10/hora siempre), NAT Gateway ($0.045/hora siempre) |
| **On-demand** | Pagas por hora de uso real, puedes parar y no pagar | EC2, RDS, Fargate (cuando el task corre) |

**Regla práctica:** si un servicio tiene un precio "por hora" o "por mes" fijo, corre el riesgo de generar costo aunque no reciba tráfico. Si el precio es "por request" o "por GB procesado", difícilmente cobra en laboratorios de bajo volumen.

---

## Resumen ejecutivo de costos

| Caso | Servicios con costo potencial | Costo lab activo | Estrategia | Destruir al terminar |
|---|---|---|---|---|
| **A** — Amplify | Amplify Hosting, CloudFront | ~$0 | Mantener activo | No |
| **B** — S3 GitLab | S3 Website | ~$0 | Mantener activo | No |
| **C** — Terraform CloudFront | S3, CloudFront, DynamoDB state | ~$0 | Mantener activo | No |
| **D** — Serverless Basic | Lambda, API GW, DynamoDB | ~$0 | Mantener activo | No |
| **E** — DynamoDB Pro | Lambda, API GW, DynamoDB GSI | ~$0 | Mantener activo | No |
| **F** — Security Cognito | Cognito, Lambda; WAF si activo | $0 sin WAF / $5-7 con WAF | Mantener sin WAF | No |
| **G** — Event Driven | EventBridge, SQS, SNS, Lambda | ~$0 | Mantener activo | No |
| **H** — Observability | CloudWatch Dashboard, X-Ray | $3/mes si stack activo | Destruir al terminar lab | Sí (si no se usa) |
| **J** — ECS Fargate | ALB, Fargate, ECR | $25-30/mes | Deploy → evidencia → destroy | Sí, inmediato |
| **K** — EKS | EKS control plane, NAT GW, Fargate | $100-120/mes | Deploy → validar → destroy | Sí, inmediato |
| **L** — FinOps | Budgets, IAM, S3 | ~$0 | Mantener activo | No |

---

## Análisis detallado por caso

---

### Caso A — AWS Amplify

**Servicios activos:** Amplify Hosting, CloudFront (incluido), SSL/HTTPS (incluido)

| Servicio | Modelo | Free Tier | Costo si se supera |
|---|---|---|---|
| Amplify Hosting — build minutos | Pay-per-use | 1,000 minutos/mes gratis | $0.01/minuto |
| Amplify Hosting — almacenamiento | Pay-per-use | 5 GB/mes gratis | $0.023/GB |
| Amplify Hosting — transferencia | Pay-per-use | 15 GB/mes gratis | $0.15/GB |

**Costo real en laboratorio:** $0.00

Un portfolio estático con Amplify rara vez supera 1GB de almacenamiento o 1GB de tráfico mensual. El free tier de Amplify Hosting es generoso y permanente.

**Estrategia:** Dejar activo. El caso tiene URL pública y sirve como demo en vivo para reclutadores.

---

### Caso B — S3 + GitLab CI

**Servicios activos:** S3 Website Hosting, transferencia de datos de salida

| Servicio | Modelo | Free Tier | Costo si se supera |
|---|---|---|---|
| S3 — almacenamiento | Pay-per-use | 5 GB/mes gratis (12 meses) | $0.023/GB/mes |
| S3 — GET requests | Pay-per-use | 20,000 GETs gratis | $0.0004/1,000 |
| Transferencia de salida | Pay-per-use | 1 GB/mes siempre gratis | $0.09/GB |

**Costo real en laboratorio:** $0.00

Un sitio estático pequeño con tráfico de portfolio no supera el free tier. Si la cuenta tiene más de 12 meses, el almacenamiento pasa a costar ~$0.001/mes para un sitio de 50MB. Despreciable.

**Estrategia:** Dejar activo.

**Punto de atención:** Si la cuenta tiene más de 12 meses y se usa mucho S3 en otros proyectos, verificar que el free tier de 5GB siga disponible. La consola de Free Tier muestra el uso acumulado.

---

### Caso C — Terraform + CloudFront + S3

**Servicios activos:** S3 privado (origen), CloudFront (CDN), DynamoDB (state lock de Terraform)

| Servicio | Modelo | Free Tier | Costo si se supera |
|---|---|---|---|
| CloudFront — transferencia | Pay-per-use | 1 TB/mes gratis (12 meses) | $0.0085/GB (NA) |
| CloudFront — requests HTTPS | Pay-per-use | 10M requests/mes gratis (12 meses) | $0.01/10,000 |
| S3 — almacenamiento | Pay-per-use | 5 GB gratis (12 meses) | $0.023/GB |
| DynamoDB — state lock | Pay-per-use | 25 WCU + 25 RCU + 25 GB siempre gratis | $0 para lock de Terraform |

**Costo real en laboratorio:** $0.00 (dentro del free tier)

**Nota técnica:** El bucket de estado de Terraform y la tabla DynamoDB para locking son de uso mínimo. El lock ocurre solo durante `terraform apply/destroy` y dura segundos. Costo negligible incluso fuera del free tier.

**Estrategia:** Dejar activo. La URL de CloudFront sirve como demo con HTTPS real, sin costo.

---

### Caso D — Serverless Basic (Lambda + API Gateway + DynamoDB)

**Servicios activos:** AWS Lambda, API Gateway HTTP, DynamoDB PAY_PER_REQUEST

| Servicio | Modelo | Free Tier (Always Free) | Costo si se supera |
|---|---|---|---|
| Lambda — invocaciones | Pay-per-use | 1,000,000/mes siempre gratis | $0.20/millón |
| Lambda — duración | Pay-per-use | 400,000 GB-s/mes siempre gratis | $0.0000166667/GB-s |
| API Gateway HTTP | Pay-per-use | 1,000,000/mes gratis (12 meses), luego $1.00/millón | $1.00/millón |
| DynamoDB — lectura | Pay-per-use | 25 RCU siempre gratis + on-demand más allá | $0.25/millón read units |
| DynamoDB — escritura | Pay-per-use | 25 WCU siempre gratis + on-demand más allá | $1.25/millón write units |
| DynamoDB — almacenamiento | Pay-per-use | 25 GB siempre gratis | $0.25/GB/mes |

**Costo real en laboratorio:** $0.00

Un portfolio con algunas decenas de visitas al día y un backend de aprendizaje está extremadamente lejos de superar el millón de invocaciones mensuales. Lambda y DynamoDB son los servicios más "free" del catálogo AWS para workloads de laboratorio.

**Estrategia:** Dejar activo. El backend es serverless real: escala a cero automáticamente.

---

### Caso E — DynamoDB Single Table + GSI

**Servicios activos:** Lambda, API Gateway, DynamoDB con 2 GSI

| Servicio | Diferencia vs Caso D | Consideración |
|---|---|---|
| DynamoDB GSI1 (status) | Cada GSI tiene su propia capacidad | Lee del mismo pool del free tier de la tabla base |
| DynamoDB GSI2 (product) | Igual que GSI1 | Segundo GSI comparte el free tier |
| TransactWriteItems | Consume 2x WCU por item en transacción | Para laboratorio: negligible |

**Costo real en laboratorio:** $0.00

Los GSI en DynamoDB on-demand no tienen costo base; se cobra por las lecturas que los usan. En un laboratorio con pocas queries, esto cae completamente en el free tier.

**Estrategia:** Dejar activo.

**Concepto clave para entender el costo de GSI:** Un GSI no es una tabla separada en términos de costo fijo. Es una vista proyectada que consume capacidad cuando se escribe a la tabla base (replicación del GSI) y cuando se lee desde el GSI. Para workloads de laboratorio, esto es $0.

---

### Caso F — Security First (Cognito + JWT Authorizer + WAF)

**Servicios activos:** Cognito User Pool, API Gateway HTTP con JWT Authorizer, Lambda, y opcionalmente WAF

| Servicio | Modelo | Free Tier | Costo si se supera |
|---|---|---|---|
| Cognito User Pool — MAU | Pay-per-use | 50,000 Monthly Active Users siempre gratis | $0.0055/MAU para los siguientes 50K |
| JWT Authorizer (API GW) | Incluido en API GW | Gratis — no hay costo adicional por usar JWT Authorizer | — |
| WAF WebACL | Provisioned | **Sin free tier: $5.00/mes por WebACL activo** | + $1.00/millón de requests |
| WAF — Managed Rules | Por regla activada | $1.00/mes por grupo de reglas activo | $1.00/millón de requests |

**Costo real:**
- **Sin WAF (DeployWAF=false, default):** $0.00
- **Con WAF activo:** $5 (WebACL) + $2 (2 grupos de reglas) = ~$7/mes base

**Punto crítico del WAF:** El WAF es el único servicio en este caso con costo fijo provisioned. El template SAM tiene `DeployWAF=false` por defecto precisamente por esto. Si se activa el WAF para probar, destruir el stack al terminar.

**Estrategia:** Mantener activo sin WAF. Activar WAF solo para demos específicos y destruir al terminar.

**Comando para verificar si WAF está activo:**
```bash
aws wafv2 list-web-acls --scope REGIONAL --region us-east-2
```

---

### Caso G — Event Driven (EventBridge + SQS + SNS)

**Servicios activos:** API Gateway, Lambda (Publisher + Consumer), EventBridge custom bus, SQS (cola + DLQ), SNS

| Servicio | Modelo | Free Tier (Always Free) | Costo si se supera |
|---|---|---|---|
| EventBridge — custom events | Pay-per-use | 1,000,000 events/mes gratis | $1.00/millón de eventos |
| SQS — requests | Pay-per-use | 1,000,000 requests/mes siempre gratis | $0.40/millón |
| SNS — notificaciones | Pay-per-use | 1,000,000 publishes/mes siempre gratis | $0.50/millón |
| Lambda | Pay-per-use | 1,000,000 invocaciones/mes siempre gratis | $0.20/millón |

**Costo real en laboratorio:** $0.00

Este caso es el más "barato de entender" en términos de costos. Todos los servicios son pay-per-use con free tier generoso y permanente.

**Estrategia:** Dejar activo. El Event Bus y las colas existen pero no cobran si no se usan.

**Concepto clave:** En arquitecturas event-driven, el costo escala con el volumen de negocio real, no con la existencia de la infraestructura. Eso es una ventaja sobre arquitecturas basadas en servidores 24/7.

---

### Caso H — Observability (CloudWatch + X-Ray + Dashboard IaC)

**Servicios activos:** Lambda, API Gateway, CloudWatch (métricas custom + logs + alarmas + dashboard), X-Ray

| Servicio | Modelo | Free Tier | Costo si se supera |
|---|---|---|---|
| CloudWatch — métricas custom | Pay-per-use | 10 métricas/mes siempre gratis | $0.30/métrica/mes |
| CloudWatch Logs — ingesta | Pay-per-use | 5 GB/mes siempre gratis | $0.50/GB |
| CloudWatch Logs — almacenamiento | Pay-per-use | 5 GB/mes siempre gratis | $0.03/GB/mes |
| CloudWatch Alarms | Pay-per-use | 10 alarmas siempre gratis | $0.10/alarma/mes |
| **CloudWatch Dashboard** | **Provisioned** | **Sin free tier: $3.00/dashboard/mes** | — |
| X-Ray — trazas | Pay-per-use | 100,000 trazas/mes siempre gratis | $5.00/millón |

**Costo real:**
- **Con stack activo permanente:** ~$3-4/mes (principalmente el dashboard)
- **Con stack destruido después del lab:** $0.00

**El dashboard es el costo clave.** Cada `AWS::CloudWatch::Dashboard` en el template SAM genera un costo fijo de $3/mes. Para este caso, el dashboard se crea con IaC y se destruye con el stack — eso es parte del diseño. Si se deja el stack activo continuamente, es el único costo real.

**Estrategia:** Destruir el stack cuando no se use activamente. Redeployar para demos específicos.

```bash
# Destruir (eliminar el dashboard y detener el costo)
sam delete --stack-name caso-h-observability --region us-east-2 --no-prompts

# Redesplegar cuando se necesite
sam deploy --stack-name caso-h-observability
```

---

### Caso J — Contenedores ECS Fargate + ALB

**Servicios activos:** ECR (registry), ECS Fargate (tasks), ALB (Application Load Balancer)

| Servicio | Modelo | Free Tier | Costo activo |
|---|---|---|---|
| ECR — almacenamiento | Pay-per-use | 500 MB/mes siempre gratis | $0.10/GB/mes |
| Fargate — vCPU | **Provisioned** | **Sin free tier** | $0.04048/vCPU/hora |
| Fargate — memoria | **Provisioned** | **Sin free tier** | $0.004445/GB/hora |
| ALB — base | **Provisioned** | **Sin free tier** | $0.008/hora = ~$5.76/mes |
| ALB — LCU | Pay-per-use | — | $0.008/LCU/hora |

**Cálculo detallado con task de 0.25 vCPU + 0.5 GB (24/7 por 30 días):**
- Fargate vCPU: 0.04048 × 0.25 × 720 = **$7.29/mes**
- Fargate memoria: 0.004445 × 0.5 × 720 = **$1.60/mes**
- ALB base: 0.008 × 720 = **$5.76/mes**
- ALB LCU (tráfico mínimo): ~**$1-2/mes**
- ECR: 500MB gratis → **$0**

**Total con stack activo 24/7:** ~**$16-17/mes**

**Con task más realista (0.5 vCPU + 1 GB):**
- ~$25-30/mes

**Estrategia: Deploy → captura de evidencia → destroy inmediato.**

```bash
cd caso-j-containers-ecs/terraform
terraform destroy -auto-approve   # DESTRUYE ALB + ECS + ECR tasks
```

**El ALB es el riesgo principal.** No importa si hay tráfico o no: cuesta ~$5.76/mes solo por existir. El ECS Fargate task también cobra mientras esté en estado RUNNING.

---

### Caso K — Kubernetes en EKS

**Servicios activos:** EKS Control Plane, Fargate nodes, NAT Gateway, VPC (subnets, routing)

| Servicio | Modelo | Free Tier | Costo activo |
|---|---|---|---|
| EKS Control Plane | **Provisioned** | **Sin free tier** | **$0.10/hora = $72/mes** |
| NAT Gateway — base | **Provisioned** | **Sin free tier** | **$0.045/hora = $32.40/mes** |
| NAT Gateway — tráfico | Pay-per-use | — | $0.045/GB procesado |
| Fargate pods | Provisioned | Sin free tier | $0.04048 vCPU/hora + $0.004445 GB/hora |
| EBS (si se usan PVC) | Provisioned | — | $0.10/GB/mes |

**Cálculo con cluster mínimo activo 24/7:**
- EKS Control Plane: **$72/mes** (fijo, no hay forma de reducirlo)
- NAT Gateway: **$32.40/mes** (fijo, más tráfico)
- Fargate pods (2 nodos básicos): **~$10-15/mes**

**Total con cluster activo 24/7:** ~**$115-120/mes**

**Este es el caso más caro del repositorio.** El control plane de EKS ($0.10/hora) no tiene free tier y no puede ser "pausado" — o está activo y cobra, o se destruye.

**Estrategia: Deploy → validar funcionamiento → destroy en minutos.**

```bash
cd caso-k-kubernetes-eks/terraform
terraform destroy -auto-approve   # 🚨 OBLIGATORIO al terminar el lab
```

**Por qué se documentó como caso completado si está destruido:** Porque el aprendizaje es el proceso de construcción y validación, no el tiempo de vida del recurso. La evidencia queda en `VISUALIZATION.md`, el código en el repo, y el conocimiento en quien lo construyó.

---

### Caso L — FinOps & Governance

**Servicios activos:** AWS Budgets, IAM (OIDC), S3 Hosting, Cost Explorer

| Servicio | Modelo | Free Tier | Costo activo |
|---|---|---|---|
| AWS Budgets | Pay-per-use | 2 primeros Budgets siempre gratis | $0.02/budget/día adicional |
| IAM / OIDC | Sin costo | Siempre gratis | $0 |
| Cost Explorer | Sin costo base | Gratis para reportes estándar | $0.01/API request avanzada |
| S3 — hosting sitio | Pay-per-use | 5 GB gratis (12 meses) | $0.023/GB/mes |

**Costo real:** $0.00

El Caso L es el caso de gobernanza: instala los controles (budgets, OIDC, políticas IAM) que protegen de los costos de los casos más caros. Irónicamente, el caso de control de costos no tiene costos significativos.

**Estrategia:** Mantener activo permanentemente. Los budgets y OIDC son infraestructura de protección, no recursos temporales.

---

## Tabla de riesgo financiero por tipo de recurso

Esta tabla aplica a cualquier caso presente o futuro:

| Recurso | Riesgo | Costo aprox. | Señal de alerta |
|---|---|---|---|
| EKS Cluster activo | 🔴 CRÍTICO | $72/mes solo control plane | Aparece en billing como `AmazonEKS` |
| NAT Gateway activo | 🔴 CRÍTICO | $32/mes + tráfico | Aparece como `NatGateway-Hours` |
| ALB activo (sin tráfico) | 🔴 ALTO | $5-16/mes | Aparece como `LoadBalancerUsage` |
| EC2 running | 🔴 ALTO | $8-100+/mes según tipo | Aparece como `BoxUsage` |
| WAF WebACL | 🟠 MEDIO | $5/mes base | Aparece como `WebACL` en WAF billing |
| CloudWatch Dashboard | 🟡 BAJO | $3/dashboard/mes | Aparece como `DashboardsUsageHour` |
| RDS activo | 🟠 MEDIO | $12-50+/mes | Aparece como `InstanceUsage:db.*` |
| EBS volumen suelto | 🟡 BAJO | $0.10/GB/mes | Aparece como `EBS:VolumeUsage` |
| Elastic IP sin usar | 🟡 BAJO | $3.60/mes | Aparece como `ElasticIP:IdleAddress` |
| Lambda | 🟢 ÍNFIMO | $0 para labs | Millón de requests gratis/mes |
| DynamoDB on-demand | 🟢 ÍNFIMO | $0 para labs | 25 WCU/RCU + 25 GB siempre gratis |
| SQS, SNS, EventBridge | 🟢 ÍNFIMO | $0 para labs | Millón de mensajes gratis/mes |
| S3 estático | 🟢 ÍNFIMO | $0 para labs | 5 GB gratis, tráfico mínimo |
| Cognito | 🟢 ÍNFIMO | $0 para labs | 50,000 MAU siempre gratis |

---

## Estrategia de auditoría de costos

### Verificación rápida antes de cerrar sesión

```bash
# Recursos con costo fijo que deben estar destruidos
aws ec2 describe-instances --filters Name=instance-state-name,Values=running \
  --query 'Reservations[*].Instances[*].[InstanceId,InstanceType]' --output table

aws elbv2 describe-load-balancers \
  --query 'LoadBalancers[*].[LoadBalancerName,State.Code]' --output table

aws eks list-clusters --output table

aws ec2 describe-nat-gateways --filter Name=state,Values=available \
  --query 'NatGateways[*].[NatGatewayId,State]' --output table

aws wafv2 list-web-acls --scope REGIONAL --region us-east-2 \
  --query 'WebACLs[*].[Name,ARN]' --output table
```

### Verificación mensual (primer día de cada mes)

1. Revisar AWS Cost Explorer: filtrar por servicio, ver qué cobró
2. Revisar las alertas de Budgets (Caso L las configuró)
3. Ejecutar `make finops-check` del repositorio

### Presupuesto objetivo

Para este repositorio de aprendizaje, el presupuesto mensual razonable es:
- **Meta:** $0-5 USD/mes en operación normal
- **Pico aceptable:** $20-30 USD/mes si se está practicando activamente con J o K
- **Señal de alarma:** Cualquier mes > $10 sin estar activamente usando J o K

---

## Proyección de costos para casos futuros

| Caso | Estado | Costo estimado lab | Nota |
|---|---|---|---|
| **M** — Resiliencia Multi-AZ | Fase 0 completa | $12-15 USD/lab activo | ALB + Fargate + Route 53 |
| **M** — Resiliencia Multi-Region | Proyectado | $25-40 USD/lab activo | 2 regiones × recursos |
| **I** — GenAI Bedrock | Proyectado | $1-5 USD/lab | Pay-per-token; sin RAG |
| **I** — con OpenSearch Serverless | Proyectado | $350+/mes | Mínimo 4 OCUs → evitar |

---

## Para el GitLab Pages del repositorio

Este documento es la fuente de verdad para la calculadora interactiva de costos disponible en:
`/apps/cost-calculator/index.html`

Los valores de la calculadora provienen de los precios de esta tabla. Si AWS actualiza precios, actualizar primero este documento y luego sincronizar los valores en el HTML.

---

## Referencias oficiales de precios

- [Lambda Pricing](https://aws.amazon.com/lambda/pricing/)
- [API Gateway HTTP API Pricing](https://aws.amazon.com/api-gateway/pricing/)
- [DynamoDB Pricing](https://aws.amazon.com/dynamodb/pricing/)
- [CloudFront Pricing](https://aws.amazon.com/cloudfront/pricing/)
- [ECS Fargate Pricing](https://aws.amazon.com/fargate/pricing/)
- [EKS Pricing](https://aws.amazon.com/eks/pricing/)
- [ALB Pricing](https://aws.amazon.com/elasticloadbalancing/pricing/)
- [Cognito Pricing](https://aws.amazon.com/cognito/pricing/)
- [WAF Pricing](https://aws.amazon.com/waf/pricing/)
- [CloudWatch Pricing](https://aws.amazon.com/cloudwatch/pricing/)
- [AWS Free Tier — tabla completa](https://aws.amazon.com/free/)
- [AWS Pricing Calculator](https://calculator.aws/pricing/2/home)
