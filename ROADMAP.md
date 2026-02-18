# 🗺️ Roadmap (Cloud Portfolio: AWS Monorepo)

Este roadmap refleja el estado actual del proyecto y las próximas prioridades para completar la suite educativa de AWS.

---

## ✅ Estado Actual (Completado)

### Casos Implementados y Desplegados

- [x] **Caso A**: AWS Amplify con deploy automático por ramas (`main`/`dev`)
- [x] **Caso B**: S3 + GitLab CI/CD con sincronización automatizada
- [x] **Caso C**: Terraform + CloudFront con OAC (Origin Access Control)
- [x] **Caso D**: Serverless API con Lambda, API Gateway y DynamoDB
- [x] **Caso J**: Docker Dashboard Premium con ECS Fargate, ECR y Load Balancer
- [x] **Caso K**: Orquestación Real con AWS EKS, Load Balancer L7 y Self-Healing
- [x] **Caso L**: FinOps & Governance con AWS Budgets, OIDC y S3 Hosting Seguro

### Infraestructura y Herramientas

- [x] Pipelines GitLab CI/CD con stages de seguridad, plan y deploy
- [x] Makefile unificado para comandos comunes
- [x] DevContainers para entorno reproducible
- [x] Auditoría de seguridad con `tfsec` y `detect-secrets`
- [x] Pre-commit hooks para prevención de secretos
- [x] Terraform Remote State en S3 (región us-east-2)
- [x] Documentación completa con guías paso a paso

---

## 🎯 Próximos Hitos (Corto Plazo)

### 1. Mejoras de Calidad y Observabilidad

- [ ] **Testing Automatizado**: Tests unitarios para Lambdas y scripts
- [ ] **Monitoreo CloudWatch**: Dashboards básicos para casos A-D y J
- [ ] **Alertas**: Configuración de alarmas para errores y costos
- [ ] **Lighthouse CI**: Validación de performance para frontends

### 2. Documentación y Wikis

- [ ] **Wiki GitLab**: Expandir contenido técnico y troubleshooting
- [ ] **Video Walkthrough**: Grabación de demos en vivo
- [x] **Diagramas de Arquitectura**: Completar para todos los casos (Flujos ECS/ECR incluidos)
- [ ] **Guías de Migración**: Documentar cómo replicar en otras cuentas AWS

---

## 🚀 Mediano Plazo (Casos Planificados)

### 3. Persistencia y Datos (Caso E)

- [ ] **DynamoDB Persistence Pro**: Single Table Design con GSI/LSI
- [ ] **Streams y Replicación**: Setup de triggers y eventos
- [ ] **Backup y Restore**: Políticas de retención
- [ ] **Integración con SQS**: Procesamiento asíncrono

### 4. Seguridad y Autenticación (Caso F)

- [ ] **AWS Cognito**: User pools y autenticación
- [ ] **WAF**: Protección contra ataques web (DDoS, SQLi)
- [ ] **IAM Roles avanzados**: Políticas granulares por caso
- [ ] **Secrets Manager**: Migración desde variables enmascaradas

### 5. Arquitectura Event-Driven (Caso G)

- [ ] **EventBridge**: Bus de eventos entre servicios
- [ ] **Step Functions**: Orquestación de workflows
- [ ] **SNS/SQS**: Patrones pub/sub y cola de mensajes
- [ ] **Dead Letter Queues**: Manejo de errores

---

## 🧱 Largo Plazo (Innovación)

### 6. Observabilidad Completa (Caso H)

- [ ] **X-Ray**: Trazabilidad distribuida
- [ ] **CloudWatch Logs Insights**: Queries avanzadas
- [ ] **GitLab Observability**: Integración de métricas
- [ ] **Custom Metrics**: KPIs de negocio

### 7. IA Generativa (Caso I)

- [ ] **Amazon Bedrock**: Integración de LLMs
- [ ] **LangChain**: Orquestación de prompts
- [ ] **RAG**: Retrieval-Augmented Generation con datos propios
- [ ] **Lambda con IA**: Endpoints inteligentes

### 8. Orquestación con Kubernetes (Caso K)

- [ ] **AWS EKS**: Cluster en producción
- [ ] **Helm Charts**: Gestión de aplicaciones
- [ ] **GitLab Kubernetes Agent**: CI/CD integrado
- [ ] **Auto-scaling**: HPA y Cluster Autoscaler
- [ ] **Service Mesh**: Istio para observabilidad



---

## 🔧 Mejoras Continuas

### Seguridad

- [ ] **OIDC con GitLab**: Eliminar IAM keys permanentes
- [ ] **Policy as Code**: OPA (Open Policy Agent)
- [ ] **Compliance**: AWS Config para auditoría continua
- [ ] **Vulnerability Scanning**: Trivy para imágenes Docker

### Automatización

- [ ] **Terraform Modules**: Reutilización entre casos
- [ ] **Custom GitLab CI Templates**: Estandarización de pipelines
- [ ] **GitHub Actions Sync**: Para proyectos open source
- [ ] **Renovate Bot**: Actualización automática de dependencias

### Performance

- [ ] **CloudFront optimizations**: Compresión y cache policies
- [ ] **Lambda Layers**: Compartir dependencias
- [ ] **RDS Read Replicas**: Para casos futuros con bases de datos
- [ ] **ElastiCache**: Para casos con alta lectura

---

## 📌 Cómo se Gestiona

- **Issues etiquetados**: `enhancement`, `bug`, `documentation`, `security`, `performance`
- **Milestones**: Por caso de estudio (E, F, G, H, I, K, L)
- **Board Kanban**: Backlog → In Progress → Review → Done
- **Releases**: Semantic Versioning en CHANGELOG.md

---

## 🎓 Objetivos de Aprendizaje

Al completar todos los casos, se habrán dominado:

1. **Infraestructura**: Terraform, SAM, CloudFormation, Kubernetes
2. **Servicios AWS**: 15+ servicios integrados
3. **CI/CD**: GitLab Pipelines, automation, testing
4. **Seguridad**: IAM, OIDC, WAF, Secrets, Encryption
5. **Observabilidad**: CloudWatch, X-Ray, métricas personalizadas
6. **Arquitectura**: Serverless, Event-Driven, Microservicios, Orquestación
7. **FinOps**: Optimización de costos, budgets, governance

---

_Última actualización: 2026-02-16_
