# Roadmap (Cloud Portfolio: AWS Monorepo)

Este roadmap refleja el estado actual del proyecto y las proximas prioridades para completar la suite educativa de AWS.

---

## Estado Actual (Completado)

### Casos implementados y desplegados

- [x] **Caso A**: AWS Amplify con deploy automatico por ramas (`main`/`dev`)
- [x] **Caso B**: S3 + GitLab CI/CD con sincronizacion automatizada
- [x] **Caso C**: Terraform + CloudFront con OAC (Origin Access Control)
- [x] **Caso D**: Serverless API con Lambda, API Gateway y DynamoDB
- [x] **Caso E**: Persistence Pro con Single Table Design, GSIs, landing publica y validacion real en AWS
- [x] **Caso F**: Security First con Cognito User Pool, JWT Authorizer y WAF opcional
- [x] **Caso G**: Event Driven con EventBridge + SQS + DLQ + SNS + landing publica
- [x] **Caso H**: Observability con CloudWatch Dashboard IaC + X-Ray + Alarmas
- [x] **Caso J**: Docker Dashboard Premium con ECS Fargate, ECR y Load Balancer
- [x] **Caso K**: Orquestacion real con AWS EKS, Load Balancer L7 y Self-Healing
- [x] **Caso L**: FinOps & Governance con AWS Budgets, OIDC y S3 Hosting Seguro

### Infraestructura y herramientas

- [x] Pipelines GitLab CI/CD con stages de seguridad, plan y deploy
- [x] Makefile unificado para comandos comunes
- [x] DevContainers para entorno reproducible
- [x] Auditoria de seguridad con `tfsec` y `detect-secrets`
- [x] Pre-commit hooks para prevencion de secretos
- [x] Terraform Remote State en S3 (`us-east-2`)
- [x] Documentacion completa con guias paso a paso

---

## Proximos hitos (Corto plazo)

### 1. Mejoras de calidad y observabilidad

- [x] **Testing automatizado**: 60+ tests unitarios para Lambdas (D, E, F, G, H) — completado
- [ ] **Monitoreo CloudWatch**: Dashboards basicos para casos A-E y J
- [ ] **Alertas**: Configuracion de alarmas para errores y costos
- [ ] **Lighthouse CI**: Validacion de performance para frontends

### 2. Documentacion y wikis

- [ ] **Wiki GitLab**: Expandir troubleshooting y guias operativas
- [ ] **Video walkthrough**: Grabacion de demos en vivo
- [x] **Diagramas de arquitectura**: Completados para todos los casos implementados
- [ ] **Guias de migracion**: Replicar los casos en otras cuentas AWS

---

## Evolucion por casos

### 3. Persistencia y datos (Caso E ya resuelto)

- [x] **DynamoDB Persistence Pro**: Single Table Design con GSIs y API serverless
- [x] **Landing publica**: UI basica para crear y consultar ordenes en vivo
- [x] **Validacion en AWS**: Stack desplegado y endpoints comprobados en `us-east-2`
- [x] **Streams y eventos**: Integracion aterrizada en el Caso G con EventBridge + SQS + DLQ
- [ ] **Backup y restore**: Politicas de retencion y restauracion puntual

### 4. Seguridad y autenticacion (Caso F)

- [x] **AWS Cognito**: User Pool con Pre-Signup trigger y `USER_PASSWORD_AUTH`
- [x] **JWT Authorizer**: Validacion nativa en API Gateway HTTP API (sin codigo Lambda)
- [x] **WAF opcional**: `AWSManagedRulesCommonRuleSet` + `AWSManagedRulesSQLiRuleSet` con `DeployWAF` param
- [x] **Landing interactiva**: Flujo de 3 pasos: registro → login → perfil protegido
- [ ] **IAM Roles avanzados**: Politicas granulares por caso
- [ ] **Secrets Manager**: Migracion desde variables enmascaradas

### 5. Arquitectura event-driven (Caso G)

- [x] **Scaffold del caso**: Estructura del modulo, SAM template, Lambdas base y documentacion completa
- [x] **EventBridge**: Bus de eventos entre servicios
- [ ] **Step Functions**: Orquestacion de workflows
- [x] **SNS/SQS**: Patrones pub/sub y cola de mensajes
- [x] **Dead Letter Queues**: Manejo de errores

---

## Largo plazo (Innovacion)

### 6. Observabilidad completa (Caso H) ✅ COMPLETADO

- [x] **X-Ray**: Trazabilidad distribuida con `Tracing: Active` en todas las Lambdas
- [x] **Custom Metrics**: KPIs de negocio publicados desde Lambda a CloudWatch namespace `CasoH`
- [x] **CloudWatch Dashboard IaC**: Dashboard definido en SAM template (se crea/destruye con el stack)
- [x] **CloudWatch Alarms**: Errores Lambda y latencia p99 configuradas declarativamente
- [ ] **CloudWatch Logs Insights**: Queries avanzadas sobre logs estructurados
- [ ] **GitLab Observability**: Integracion de metricas de pipeline

### 7. IA generativa (Caso I)

- [ ] **Amazon Bedrock**: Integracion de LLMs
- [ ] **LangChain**: Orquestacion de prompts
- [ ] **RAG**: Retrieval-Augmented Generation con datos propios
- [ ] **Lambda con IA**: Endpoints inteligentes

### 8. Orquestacion con Kubernetes (Caso K) ✅ COMPLETADO

- [x] **AWS EKS**: Cluster EKS v1.32 con Auto Mode desplegado y validado
- [x] **Helm Charts**: Gestion de aplicaciones
- [x] **ALB Ingress Controller**: Balanceo de carga L7
- [x] **Self-Healing**: Pruebas de resiliencia documentadas
- [ ] **GitLab Kubernetes Agent**: CI/CD integrado (mejora futura)
- [ ] **Service Mesh**: Istio para observabilidad (mejora futura)

### 9. Resiliencia y failover (Caso M) `FUTURO / PLANIFICADO`

> **Importancia**: Esto es lo que diferencia un demo de un sistema profesional. Los roles SRE,
> Cloud Architect y Platform Engineer exigen demostrar continuidad operacional.

- [x] **Fase 0**: Scaffold, documentacion, plantillas IaC y scripts placeholder
- [ ] **Fase 1**: ALB Multi-AZ + ECS con `desired_count >= 2` + endpoint `/healthz` + GameDay
- [ ] **Fase 2**: Warm Standby en `us-west-2` + Route 53 Failover Routing (RTO < 120s)
- [ ] **Fase 3**: Automatizacion GameDay + CloudWatch Dashboards + opcion de Global Accelerator
- [ ] [Ver carpeta del Caso M](./caso-m-resiliencia-failover/README.md)

### 10. CI/CD avanzado con GitLab (Caso N) `PROYECTADO`

- [ ] **Pipelines multi-stage**: stages dev → staging → prod con environments de GitLab
- [ ] **Deployment protection rules**: aprobacion manual antes de pasar a prod
- [ ] **Rollback automatizado**: revertir despliegue si el health check falla post-deploy
- [ ] **Revisiones de PR como gates**: el merge a main solo se permite si el pipeline de staging pasa
- [ ] **Prerequisito**: todos los casos anteriores completados

### 11. Observabilidad distribuida (Caso O) `PROYECTADO`

- [ ] **Trazas X-Ray multi-servicio**: correlacion de trazas entre multiples Lambdas en cadena
- [ ] **CloudWatch Synthetics**: canaries que simulan usuarios reales en endpoints criticos
- [ ] **SLOs definidos**: error budget, availability target, alertas basadas en SLO
- [ ] **Integracion externa de alertas**: webhook a canal externo cuando se quema el error budget
- [ ] **Prerequisito**: Caso H completado; Caso M recomendado para infraestructura distribuida

---

## Mejoras continuas

### Seguridad

- [x] **OIDC con GitLab**: Implementado en Caso L — credenciales efimeras en CI/CD
- [ ] **Policy as Code**: OPA (Open Policy Agent)
- [ ] **Compliance**: AWS Config para auditoria continua
- [ ] **Vulnerability Scanning**: Trivy para imagenes Docker

### Automatizacion

- [ ] **Terraform modules**: Reutilizacion entre casos
- [ ] **Custom GitLab CI templates**: Estandarizacion de pipelines
- [ ] **GitHub Actions Sync**: Para proyectos open source
- [ ] **Renovate Bot**: Actualizacion automatica de dependencias

### Performance

- [ ] **CloudFront optimizations**: Compresion y cache policies
- [ ] **Lambda Layers**: Compartir dependencias
- [ ] **RDS Read Replicas**: Para casos futuros con bases de datos
- [ ] **ElastiCache**: Para casos con alta lectura

---

## Como se gestiona

- **Issues etiquetados**: `enhancement`, `bug`, `documentation`, `security`, `performance`
- **Milestones**: Por caso de estudio (E, F, G, H, I, K, L, M)
- **Board Kanban**: Backlog -> In Progress -> Review -> Done
- **Releases**: Semantic Versioning en `CHANGELOG.md`

---

## Objetivos de aprendizaje

Al completar todos los casos, se habran dominado:

1. **Infraestructura**: Terraform, SAM, CloudFormation, Kubernetes
2. **Servicios AWS**: 15+ servicios integrados
3. **CI/CD**: GitLab Pipelines, automation y testing
4. **Seguridad**: IAM, OIDC, WAF, Secrets y Encryption
5. **Observabilidad**: CloudWatch, X-Ray y metricas personalizadas
6. **Arquitectura**: Serverless, Event-Driven, Microservicios y Orquestacion
7. **FinOps**: Optimizacion de costos, budgets y governance

---

_Ultima actualizacion: 2026-03-18_
