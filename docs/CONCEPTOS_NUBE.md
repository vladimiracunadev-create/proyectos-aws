# De IT Tradicional a la Nube — Guía de Conceptos

> **Para quién es esto**: tienes base de IT (servidores, redes, bases de datos, seguridad).
> Ya sabes cómo funciona la infraestructura. Este documento traduce esos conceptos al lenguaje AWS
> y explica qué producto concreto usamos en cada caso de este repositorio.

---

## Cómo leer este documento

Cada sección sigue el mismo patrón:

```
Concepto IT que ya conoces
  └─ Equivalente en la nube
      └─ Nombre exacto del servicio AWS
          └─ Cómo lo usamos en este repositorio
```

Al final de cada sección hay una retroalimentación: qué aprendiste al construir ese caso.

---

## 1. Servidor de aplicaciones

### Lo que conoces
Un servidor físico o VM con un proceso corriendo 24/7 esperando peticiones HTTP.
Si no llega nadie, igual consume CPU y RAM. Si llegan 10.000 usuarios a la vez, se satura.

### En la nube: función como servicio
El código se despliega como una **función** que solo corre cuando llega una petición.
No hay servidor que mantener. Si no hay tráfico, el costo es cero.

| Concepto IT | AWS | Usado en |
|---|---|---|
| Proceso servidor web | **AWS Lambda** | Casos D, E, F, G, H |
| Código empaquetado en container | **AWS ECS Fargate** | Caso J |
| Orquestador de containers | **AWS EKS** | Caso K |

**AWS Lambda** en detalle:
- Es una función Python (o Node, Java, etc.) que recibe un `event` y devuelve una respuesta
- Se invoca bajo demanda: si nadie llama, no existe
- Límite de ejecución: 15 minutos máximo por invocación
- El "tamaño" se configura en MB de RAM (128 MB a 10 GB)

**ECS Fargate** en detalle:
- Es un container Docker que AWS corre por ti sin que gestiones el servidor subyacente
- Diferencia clave con Lambda: el container puede tener estado, correr indefinidamente, y escuchar en un puerto TCP
- Pagas por segundo de ejecución del container

**Retroalimentación — Casos D, E, F, G, H:**
Construiste 5 APIs serverless diferentes. Cada una hace algo distinto, pero todas comparten la misma idea: el código corre solo cuando alguien lo llama. Cuando destruyes el stack, el código desaparece junto con la infraestructura. Eso es imposible en IT tradicional.

---

## 2. Balanceador de carga

### Lo que conoces
Un equipo (F5, HAProxy, nginx) que recibe peticiones y las distribuye entre varios servidores.
Detecta servidores caídos y deja de enviarles tráfico.

### En la nube

| Concepto IT | AWS | Usado en |
|---|---|---|
| Load Balancer HTTP/S | **Application Load Balancer (ALB)** | Casos J, K, M |
| Punto de entrada de API | **API Gateway** | Casos D, E, F, G, H |

**API Gateway** es la pieza más usada en este repositorio. No es exactamente un load balancer — es más una "puerta de API" que:
- Recibe peticiones HTTP y las enruta a la Lambda correcta
- Aplica autenticación antes de pasar la petición (JWT Authorizer en Caso F)
- Genera logs y métricas automáticamente
- Maneja CORS, throttling y quotas sin código

**ALB** es el load balancer clásico de AWS, usado cuando tienes containers o EC2 en lugar de Lambdas.

**Retroalimentación — Caso F:**
El JWT Authorizer de API Gateway hace algo que en IT tradicional habrías puesto en el load balancer o en un reverse proxy nginx: valida el token antes de que el código de negocio siquiera arranque. Si el token es inválido, Lambda nunca corre — costo cero.

---

## 3. Base de datos

### Lo que conoces
MySQL, PostgreSQL, Oracle. Tablas normalizadas, JOINs, transacciones ACID.

### En la nube

| Concepto IT | AWS | Usado en |
|---|---|---|
| Base de datos relacional | **Amazon RDS** | No usado en este repo |
| Base de datos NoSQL clave-valor | **Amazon DynamoDB** | Casos D, E, F (implícito), G |
| Cache distribuido | **Amazon ElastiCache** | No usado en este repo |

**DynamoDB** es la base de datos más usada en este repositorio. Las diferencias clave con SQL:

```
SQL tradicional            │ DynamoDB
──────────────────────────────────────────────────────
Diseñas tablas primero     │ Diseñas por consultas primero
Múltiples tablas + JOINs   │ Una sola tabla, todo junto
Schema fijo                │ Schema flexible por ítem
Índices secundarios = lento│ GSI = lectura rápida por otro campo
SELECT con WHERE libre     │ Solo puedes leer por pk/sk o GSI
```

**Retroalimentación — Caso E (el más importante de DynamoDB):**
Modelaste una tabla con `pk/sk` que almacena órdenes, clientes y auditoría en el mismo lugar. Creaste GSIs para leer por estado y por producto sin hacer scans. Esto es el cambio de mentalidad más importante del repositorio: en NoSQL no preguntas "qué tablas necesito" sino "qué consultas debe responder la aplicación".

---

## 4. Almacenamiento de archivos

### Lo que conoces
NAS, SAN, sistema de archivos compartido (NFS, CIFS), o disco local del servidor.

### En la nube

| Concepto IT | AWS | Usado en |
|---|---|---|
| Almacenamiento de objetos (archivos, imágenes, backups) | **Amazon S3** | Casos A, B, C, L |
| Disco de una VM | **Amazon EBS** | No usado directamente |
| Sistema de archivos compartido | **Amazon EFS** | No usado en este repo |

**S3** (Simple Storage Service) es fundamental:
- No es un sistema de archivos — es un almacén de objetos
- Cada objeto tiene una URL única
- Puede servir como hosting de sitio estático (Casos A, B)
- Puede ser origen privado de un CDN (Caso C)
- Escala ilimitado, durabilidad 99.999999999% (11 nueves)

**Retroalimentación — Casos A, B, C:**
Tres formas de publicar un sitio estático, cada una más profesional:
- **A**: Amplify lo hace todo automático
- **B**: tú sincronizas manualmente con `aws s3 sync`
- **C**: S3 privado + CloudFront encima — nadie puede acceder directo al bucket, todo pasa por el CDN

---

## 5. CDN / Caché de contenido

### Lo que conoces
Akamai, Cloudflare, Varnish. Ponen una capa de caché delante del origen para servir contenido desde el punto geográfico más cercano al usuario.

### En la nube

| Concepto IT | AWS | Usado en |
|---|---|---|
| CDN global | **Amazon CloudFront** | Caso C |
| Acelerador global (TCP/UDP) | **AWS Global Accelerator** | Previsto en Caso M |

**CloudFront** distribuye contenido desde más de 400 puntos de presencia globales.
En el Caso C lo usamos con **OAC (Origin Access Control)**: solo CloudFront puede leer el bucket S3 — ningún usuario puede ir directo al origen.

---

## 6. DNS

### Lo que conoces
BIND, Windows DNS. Resuelve nombres a IPs. Registros A, CNAME, MX, TTL.

### En la nube

| Concepto IT | AWS | Usado en |
|---|---|---|
| Servidor DNS | **Amazon Route 53** | Caso M (Fase 0 completada, Fase 1 planificada) |

**Route 53** hace todo lo que hace un DNS tradicional, más:
- **Failover Routing**: si el servidor primario falla, redirige automáticamente al secundario
- **Health Checks**: monitorea URLs y activa el failover si detecta caída
- **Latency Routing**: envía al usuario al servidor más cercano geográficamente

**Retroalimentación — Caso M (Fase 0 completada):**
El esqueleto ya existe. Cuando se active, Route 53 será el punto de control del failover entre regiones.

---

## 7. Firewall / Control de acceso de red

### Lo que conoces
Firewall perimetral (Cisco, Fortinet), reglas de entrada/salida, segmentación de red.

### En la nube

| Concepto IT | AWS | Usado en |
|---|---|---|
| Firewall de aplicación web (WAF) | **AWS WAF** | Caso F (opcional) |
| Firewall de red virtual | **Security Groups** | Todos los casos con VPC |
| Red privada virtual | **Amazon VPC** | Casos J, K |
| Reglas de red por subred | **Network ACL** | Gestionado por AWS en serverless |

**AWS WAF** en el Caso F:
- Se pone delante de API Gateway
- Bloquea SQLi, XSS y otros ataques conocidos con reglas administradas por AWS
- Es opcional en el demo (parámetro `DeployWAF=false`) porque tiene costo fijo de $5/mes

**Security Groups** son el firewall básico de AWS: reglas de entrada/salida por puerto e IP para EC2, RDS, ECS, etc.

---

## 8. Gestión de identidades y accesos

### Lo que conoces
Active Directory, LDAP, grupos de usuarios, políticas de contraseña, control de acceso por roles.

### En la nube hay dos capas distintas:

#### Capa 1: Quién puede usar los servicios AWS (operadores, pipelines, servidores)

| Concepto IT | AWS | Usado en |
|---|---|---|
| Usuario de sistema con permisos | **IAM User / Role** | Todos los casos |
| Cuenta de servicio para una app | **IAM Role** | Lambda, ECS, GitLab CI |
| Política de permisos | **IAM Policy** | Todos los casos |

**IAM** es la pieza más crítica de AWS. Cada Lambda, cada pipeline de GitLab, cada recurso necesita un rol con permisos mínimos.

**OIDC** (usado en Caso L): en lugar de crear un usuario IAM con credenciales permanentes para GitLab CI, GitLab se autentica con un token de corta duración. AWS verifica el token y entrega credenciales temporales. Es la forma moderna — sin secretos almacenados.

#### Capa 2: Quién puede usar la aplicación (usuarios finales)

| Concepto IT | AWS | Usado en |
|---|---|---|
| Directorio de usuarios de aplicación | **Amazon Cognito User Pool** | Caso F |
| Login OAuth2 / SSO | **Cognito Identity Provider** | Extensión de Caso F |

**Cognito User Pool** es como tener un Active Directory solo para los usuarios de tu app:
- Gestiona registro, confirmación de email, cambio de contraseña, MFA
- Emite tokens JWT (access token, ID token, refresh token) según estándar OAuth2
- API Gateway puede validar esos tokens nativamente, sin que tu Lambda haga nada

**Retroalimentación — Caso F:**
Separaste las dos capas. IAM controla "qué puede hacer la Lambda en AWS". Cognito controla "quién puede llamar a la Lambda". Son dos preguntas diferentes con dos herramientas diferentes.

---

## 9. Mensajería y colas

### Lo que conoces
MQ (ActiveMQ, RabbitMQ), colas de mensajes, patrones pub/sub, sistemas de eventos.

### En la nube

| Concepto IT | AWS | Usado en |
|---|---|---|
| Cola de mensajes | **Amazon SQS** | Caso G |
| Cola de mensajes fallidos | **SQS Dead Letter Queue (DLQ)** | Caso G |
| Bus de eventos (pub/sub) | **Amazon EventBridge** | Caso G |
| Notificaciones push (fan-out) | **Amazon SNS** | Caso G |

**Flujo del Caso G:**

```
[Cliente] → API Gateway → Lambda productora
                               ↓
                          EventBridge  ← publica el hecho de negocio
                               ↓
                            SQS Queue  ← amortigua carga
                               ↓
                          Lambda consumidora
                               ↓
                             SNS       ← notifica resultado

Si la Lambda consumidora falla 3 veces:
                            → DLQ      ← mensaje aislado para análisis
```

**Retroalimentación — Caso G:**
En IT tradicional harías todo esto en la misma transacción síncrona. En cloud, separas la entrada (API acepta rápido) del procesamiento (Lambda procesa cuando puede). El sistema tolera picos sin caerse y los errores quedan en la DLQ sin perder mensajes.

---

## 10. Monitoreo y observabilidad

### Lo que conoces
Nagios, Zabbix, Grafana, Prometheus. Métricas de CPU/RAM, logs del sistema, alertas por email.

### En la nube

| Concepto IT | AWS | Usado en |
|---|---|---|
| Sistema de métricas | **Amazon CloudWatch Metrics** | Caso H |
| Sistema de logs centralizados | **CloudWatch Logs** | Casos D, E, F, G, H |
| Alertas | **CloudWatch Alarms** | Caso H |
| Dashboard | **CloudWatch Dashboard** | Caso H |
| Trazas distribuidas | **AWS X-Ray** | Caso H |

**Tres pilares de la observabilidad** (y su equivalente AWS):

```
Métricas  → CloudWatch Metrics   (qué tan rápido, cuántos errores, qué carga)
Logs      → CloudWatch Logs      (qué pasó exactamente en cada ejecución)
Trazas    → X-Ray                (cómo viajó una petición por todos los servicios)
```

**Diferencia clave con IT tradicional:**
En Caso H, el dashboard y las alarmas están en el SAM template — son código. Si destruyes el stack, desaparecen. Si lo redespliegas, vuelven exactamente igual. En IT tradicional, el Nagios configurado a mano no vive en el repositorio.

**Retroalimentación — Caso H:**
Publicaste métricas custom desde Lambda (métricas de negocio: cuántas peticiones exitosas, no solo CPU). Eso es la diferencia entre "el servidor está vivo" y "la aplicación está funcionando correctamente".

---

## 11. CI/CD (Integración y Despliegue Continuo)

### Lo que conoces
Jenkins, TeamCity, scripts de deploy manual, FTP al servidor, copias de seguridad antes de subir.

### En la nube

| Concepto IT | AWS | Usado en |
|---|---|---|
| Pipeline de CI/CD | **GitLab CI/CD** | Todos los casos |
| Despliegue de infraestructura | **Terraform** | Casos C, J, K, L |
| Despliegue serverless | **AWS SAM** | Casos D, E, F, G, H |
| Repositorio de imágenes Docker | **Amazon ECR** | Casos J, K |

**SAM (Serverless Application Model)** es la herramienta para desplegar Lambdas + API Gateway + DynamoDB de una sola vez. Un `sam deploy` crea todo el stack. Un `sam delete` borra todo limpiamente.

**Terraform** es para infraestructura más "fija": buckets S3, distribuciones CloudFront, clusters EKS, redes VPC.

---

## 12. Infraestructura como Código (IaC)

### Lo que conoces
Scripts bash de instalación, playbooks de Ansible, imágenes de VM clonadas.

### En la nube

| Concepto IT | AWS | Usado en |
|---|---|---|
| Definición declarativa de infraestructura | **Terraform** | Casos C, J, K, L |
| IaC nativo de AWS | **CloudFormation** | Base de SAM |
| IaC para serverless | **AWS SAM** | Casos D, E, F, G, H |

**Declarativo vs imperativo:**
- Bash: "ejecuta estos comandos en este orden"
- Terraform/SAM: "quiero que el estado final sea este" — AWS se encarga del orden

**Retroalimentación — Caso C:**
Fue el primer caso donde la infraestructura vivió en archivos versionados. Si alguien borra el bucket por error, `terraform apply` lo recrea exactamente igual. Eso no era posible con configuración manual.

---

## 13. Contenedores

### Lo que conoces
Virtualización (VMware, Hyper-V), VMs con sistema operativo completo.

### En la nube

| Concepto IT | AWS | Usado en |
|---|---|---|
| Imagen de container | **Docker Image** | Caso J, K |
| Registro de imágenes | **Amazon ECR** | Casos J, K |
| Ejecutor de containers sin VM | **ECS Fargate** | Caso J |
| Orquestador de containers | **EKS (Kubernetes)** | Caso K |

**VM vs Container:**
```
VM:        SO completo + kernel + app  → GB de imagen, minutos de arranque
Container: solo la app + dependencias  → MB de imagen, segundos de arranque
```

**Fargate vs EKS:**
- **Fargate**: AWS gestiona dónde corren los containers. Tú solo dices "corre este container con estos recursos"
- **EKS**: tú gestionas el cluster Kubernetes. Más control, más complejidad, más costo base

**Retroalimentación — Casos J y K:**
Hiciste el mismo recorrido que con serverless: primero la versión más gestionada (Fargate), luego la versión más controlable (EKS). La conclusión fue la misma que con Lambda vs ECS: más control = más responsabilidad operativa.

---

## 14. FinOps — Costos como parte de la arquitectura

### Lo que conoces
Presupuesto de TI anual, licencias de software, contratos de mantenimiento de hardware.

### En la nube el costo es variable y se genera por uso:

| Recurso peligroso | Costo aprox | Qué hacer |
|---|---|---|
| **NAT Gateway** | ~$32/mes por AZ | Destruir siempre con `terraform destroy` |
| **EKS Cluster** | ~$72/mes | Destruir al terminar el laboratorio |
| **ALB** | ~$16/mes | Destruir si no hay tráfico real |
| **Lambda** | ~$0 (free tier) | No hay riesgo en demos |
| **DynamoDB on-demand** | ~$0 (free tier) | No hay riesgo en demos |
| **S3** | ~$0.023/GB | Despreciable en demos |
| **Cognito** | ~$0 (10K MAUs gratis) | No hay riesgo en demos |
| **X-Ray** | ~$0 (100K trazas gratis) | No hay riesgo en demos |

**Retroalimentación — Caso L:**
Implementaste AWS Budgets para recibir alertas antes de superar el presupuesto. También configuraste OIDC para eliminar credenciales permanentes en GitLab CI. Esas dos cosas son señales de madurez operativa: controlar el riesgo financiero y el riesgo de seguridad.

---

## Mapa completo: casos del repositorio y qué aprendiste en cada uno

```
Nivel 1 — Publicar y automatizar
  Caso A → Amplify      = CDN + hosting automático sin configurar nada
  Caso B → S3 + CI      = Entender qué hace Amplify "bajo el capó"
  Caso C → Terraform    = Infraestructura como código por primera vez

Nivel 2 — Backend y datos
  Caso D → Lambda + API Gateway + DynamoDB  = Backend sin servidor
  Caso E → DynamoDB Single Table Design     = Modelado NoSQL real
  Caso F → Cognito + JWT + WAF              = Seguridad perimetral
  Caso G → EventBridge + SQS + DLQ         = Arquitectura asíncrona

Nivel 3 — Observabilidad
  Caso H → CloudWatch + X-Ray              = Ver lo que pasa por dentro

Nivel 4 — Contenedores
  Caso J → Docker + ECS Fargate            = Apps empaquetadas en containers
  Caso K → Kubernetes EKS                  = Orquestación a nivel plataforma

Nivel 5 — Gobernanza
  Caso L → FinOps + OIDC + IAM             = Controlar costo, identidad y acceso

Nivel 6 — Resiliencia (Fase 0 completada)
  Caso M → Route 53 Failover + Multi-AZ    = El sistema sobrevive a fallos

Nivel 7 — CI/CD avanzado (proyectado)
  Caso N → GitLab Environments + Protection Rules = Entrega controlada y verificada

Nivel 8 — Observabilidad distribuida (proyectado)
  Caso O → X-Ray multi-servicio + Synthetics + SLOs = Ver el sistema completo
```

---

## Las preguntas que cambian entre IT tradicional y cloud

| En IT tradicional te preguntas... | En cloud te preguntas... |
|---|---|
| ¿Qué servidor necesito? | ¿Qué servicio administrado resuelve esto? |
| ¿Cuánta RAM y CPU? | ¿Qué límite de concurrencia y memoria para Lambda? |
| ¿Dónde guardo los logs? | ¿A qué CloudWatch Log Group van estos logs? |
| ¿Cómo hago backup? | ¿TTL en DynamoDB o política de retención de S3? |
| ¿El servidor está vivo? | ¿El /health devuelve 200 y las métricas están dentro del rango? |
| ¿Dónde está la tabla de usuarios? | ¿Cognito User Pool o DynamoDB con rol IAM? |
| ¿Quién tiene acceso al servidor? | ¿Qué IAM Role tiene permiso sobre qué recurso? |
| ¿El firewall está bloqueando? | ¿Security Group, WAF, o JWT Authorizer rechaza la petición? |

---

## Glosario de siglas que aparecen en este repositorio

| Sigla | Significado | En una frase |
|---|---|---|
| **IAM** | Identity and Access Management | Controla quién puede hacer qué en AWS |
| **VPC** | Virtual Private Cloud | Red privada virtual dentro de AWS |
| **ALB** | Application Load Balancer | Distribuye tráfico HTTP/S entre instancias |
| **ECR** | Elastic Container Registry | Docker Hub privado de AWS |
| **ECS** | Elastic Container Service | Ejecutor de containers administrado |
| **EKS** | Elastic Kubernetes Service | Kubernetes gestionado por AWS |
| **SAM** | Serverless Application Model | Herramienta de despliegue serverless |
| **IaC** | Infrastructure as Code | Infraestructura definida en archivos de texto |
| **CDN** | Content Delivery Network | Red de distribución de contenido global |
| **OAC** | Origin Access Control | Protege S3 para que solo CloudFront acceda |
| **JWT** | JSON Web Token | Token firmado que prueba identidad |
| **GSI** | Global Secondary Index | Índice de DynamoDB para leer por otro campo |
| **DLQ** | Dead Letter Queue | Cola de mensajes que fallaron |
| **OIDC** | OpenID Connect | Protocolo de autenticación sin contraseñas permanentes |
| **STS** | Security Token Service | Emite credenciales temporales en AWS |
| **WAF** | Web Application Firewall | Filtra peticiones HTTP maliciosas |
| **TTL** | Time To Live | Tiempo de vida antes de que AWS borre el registro |
| **RTO** | Recovery Time Objective | Tiempo máximo aceptable de recuperación ante fallo |
| **RPO** | Recovery Point Objective | Pérdida máxima aceptable de datos ante fallo |
| **MAU** | Monthly Active User | Usuarios activos al mes (unidad de facturación Cognito) |
| **p99** | Percentil 99 | El 99% de las peticiones es más rápido que este valor |

---

_Mantenido por: Vladimir Acuña_
_Última actualización: 2026-03-18_
