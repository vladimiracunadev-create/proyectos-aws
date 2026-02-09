# Guía de Despliegue: Docker + ECS Fargate + ECR (Stack Industrial)

Esta guía detalla paso a paso cómo desplegar la aplicación contenedorizada en AWS utilizando CloudFormation.

## Prerrequisitos

1.  **AWS CLI** instalado y configurado (`aws configure`).
2.  **Docker** instalado y corriendo.
3.  Permisos en AWS para crear VPC, ECR, ECS e IAM Roles.

---

## Estrategia de Despliegue

Utilizaremos una estrategia de **"Infraestructura Primero"** para asegurar la consistencia:

1.  Desplegar Infraestructura (Redes + Repo + Cluster) sin tareas activas.
2.  Construir y subir la imagen Docker al repo creado.
3.  Actualizar el Servicio para desplegar la aplicación.

---

## 1. Despliegue de Infraestructura Base

Ejecuta el siguiente comando para crear la infraestructura. Nótese `ServiceDesiredCount=0` para evitar que ECS intente arrancar tareas sin imagen.

```bash
aws cloudformation deploy \
  --template-file ecs-fargate-stack.yml \
  --stack-name caso-j-stack \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides AppName=caso-j-app Environment=dev ServiceDesiredCount=0
```

*Espera a que termine (aprox. 3-5 minutos).*

Obtén la URI del repositorio ECR creado:

```bash
aws cloudformation describe-stacks \
  --stack-name caso-j-stack \
  --query "Stacks[0].Outputs[?OutputKey=='ECRRepoURI'].OutputValue" \
  --output text
```

*Guarda esta URI, la usaremos como `<ECR_URI>`.*

---

## 2. Construcción y Publicación de Imagen

**Login en ECR:**

```bash
aws ecr get-login-password --region <TU_REGION> | docker login --username AWS --password-stdin <ECR_URI>
```
*(Nota: usa solo el dominio, ej: `123456789012.dkr.ecr.us-east-1.amazonaws.com`)*

**Docker Build & Push:**

```bash
# Construir imagen (usa el Dockerfile multi-stage optimizado)
docker build -t caso-j-app:latest .

# Etiquetar con la URI del repo remoto
docker tag caso-j-app:latest <ECR_URI>:latest

# Subir imagen
docker push <ECR_URI>:latest
```

---

## 3. Activar el Servicio

Ahora que la imagen está en el repositorio, actualizamos el stack para que ECS lance 1 tarea (podrías poner 2 o más para alta disponibilidad).

```bash
aws cloudformation deploy \
  --template-file ecs-fargate-stack.yml \
  --stack-name caso-j-stack \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides AppName=caso-j-app Environment=dev ServiceDesiredCount=1
```

---

## 4. Verificación

Obtén la URL pública del Load Balancer:

```bash
aws cloudformation describe-stacks \
  --stack-name caso-j-stack \
  --query "Stacks[0].Outputs[?OutputKey=='LoadBalancerDNS'].OutputValue" \
  --output text
```

Abre esa URL en tu navegador. Deberías ver el mensaje de éxito de la API.

---

## Paridad Local (Desarrollo)

Para probar exactamente lo mismo en tu máquina:

```bash
docker-compose up --build
```

Esto levantará el contenedor en `http://localhost:3000` simulando el entorno de producción (mismo Dockerfile, límites de recursos simulados).

---

## Limpieza

Para borrar todo y no generar costos:

1.  **Vaciar ECR** (CloudFormation no borra repos con imágenes):
    ```bash
    aws ecr batch-delete-image --repository-name caso-j-app-dev --image-ids imageTag=latest
    ```
2.  **Borrar Stack**:
    ```bash
    aws cloudformation delete-stack --stack-name caso-j-stack
    ```
