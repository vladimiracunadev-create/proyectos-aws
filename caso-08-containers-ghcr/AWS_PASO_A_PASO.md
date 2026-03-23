# Caso 08 — Guia paso a paso: Containers + GitHub Container Registry

> Estado: Implementacion proyectada — Q3 2026.
> Tiempo estimado: 90 minutos.

---

## Que resuelve este caso

Containeriza la aplicacion del Caso 05, publica la imagen en GHCR (gratuito para
repos publicos) y la despliega en ECS Fargate. Introduce build multi-platform
para soportar tanto arquitecturas amd64 como arm64.

---

## Prerrequisitos

| Requisito | Verificacion |
|:---|:---|
| Docker Desktop instalado | `docker --version` |
| Caso 05 funcionando | Lambda con handler Python/Node |
| Permisos ECS e IAM en el rol | Ver seccion de permisos |
| VPC con subnets publicas | `aws ec2 describe-vpcs` |

---

## Paso 1 — Crear el Dockerfile

```dockerfile
# Dockerfile
FROM public.ecr.aws/lambda/python:3.12

COPY src/ ${LAMBDA_TASK_ROOT}/
COPY requirements.txt .
RUN pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

CMD ["handler.lambda_handler"]
```

Para una app web standalone (sin Lambda):

```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/ .

EXPOSE 8080
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

---

## Paso 2 — Configurar permisos GHCR

GHCR usa el `GITHUB_TOKEN` nativo, sin secrets adicionales.
Solo se necesita que el token tenga permiso de escritura en packages:

```yaml
permissions:
  contents: read
  packages: write    # permite push a ghcr.io
```

Para hacer visible la imagen del paquete (si el repo es publico):

1. GitHub -> paquete -> Package settings -> Change visibility -> Public

---

## Paso 3 — Crear el cluster ECS Fargate

```bash
# Crear cluster
aws ecs create-cluster \
  --cluster-name caso-08-cluster \
  --capacity-providers FARGATE \
  --region us-east-1

# Crear IAM role para las tasks
aws iam create-role \
  --role-name ecsTaskExecutionRole-caso08 \
  --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Principal": {"Service": "ecs-tasks.amazonaws.com"},
      "Action": "sts:AssumeRole"
    }]
  }'

aws iam attach-role-policy \
  --role-name ecsTaskExecutionRole-caso08 \
  --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy
```

---

## Paso 4 — Task Definition inicial

```bash
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

aws ecs register-task-definition \
  --family caso-08-task \
  --network-mode awsvpc \
  --requires-compatibilities FARGATE \
  --cpu 256 \
  --memory 512 \
  --execution-role-arn arn:aws:iam::${ACCOUNT_ID}:role/ecsTaskExecutionRole-caso08 \
  --container-definitions "[{
    \"name\": \"caso-08-container\",
    \"image\": \"ghcr.io/vladimiracunadev-create/caso-08:latest\",
    \"portMappings\": [{\"containerPort\": 8080, \"protocol\": \"tcp\"}],
    \"logConfiguration\": {
      \"logDriver\": \"awslogs\",
      \"options\": {
        \"awslogs-group\": \"/ecs/caso-08\",
        \"awslogs-region\": \"us-east-1\",
        \"awslogs-stream-prefix\": \"ecs\"
      }
    }
  }]"
```

---

## Paso 5 — Workflow con build multi-platform

```yaml
name: Caso 08 — Containers + GHCR

on:
  push:
    branches: [main]
    paths:
      - 'caso-08-containers-ghcr/**'

permissions:
  contents: read
  packages: write
  id-token: write

jobs:
  build-push:
    name: Build y Push imagen
    runs-on: ubuntu-latest
    outputs:
      image-tag: ${{ steps.meta.outputs.tags }}
      image-digest: ${{ steps.build.outputs.digest }}
    steps:
      - uses: actions/checkout@v4

      - name: Setup QEMU (cross-platform)
        uses: docker/setup-qemu-action@v3

      - name: Setup Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login a GHCR
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Metadata (tags automaticos)
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ghcr.io/${{ github.repository }}/caso-08
          tags: |
            type=sha,prefix=sha-
            type=raw,value=latest,enable=${{ github.ref == 'refs/heads/main' }}

      - name: Build y Push multi-platform
        id: build
        uses: docker/build-push-action@v5
        with:
          context: caso-08-containers-ghcr/
          platforms: linux/amd64,linux/arm64
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  deploy-ecs:
    name: Deploy a ECS Fargate
    runs-on: ubuntu-latest
    needs: build-push
    environment: production
    steps:
      - uses: actions/checkout@v4

      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ vars.AWS_ROLE_ARN }}
          aws-region: us-east-1

      - name: Actualizar Task Definition con nueva imagen
        run: |
          IMAGE="ghcr.io/${{ github.repository }}/caso-08:sha-${{ github.sha }}"
          TASK_DEF=$(aws ecs describe-task-definition --task-definition caso-08-task)
          NEW_TASK_DEF=$(echo $TASK_DEF | python3 -c "
          import json,sys
          td = json.load(sys.stdin)['taskDefinition']
          td['containerDefinitions'][0]['image'] = '$IMAGE'
          for k in ['taskDefinitionArn','revision','status','requiresAttributes',
                    'compatibilities','registeredAt','registeredBy']:
              td.pop(k, None)
          print(json.dumps(td))
          ")
          aws ecs register-task-definition --cli-input-json "$NEW_TASK_DEF"

      - name: Rolling update del servicio
        run: |
          aws ecs update-service \
            --cluster caso-08-cluster \
            --service caso-08-service \
            --task-definition caso-08-task \
            --force-new-deployment

      - name: Esperar a que el deploy complete
        run: |
          aws ecs wait services-stable \
            --cluster caso-08-cluster \
            --services caso-08-service
```

---

## Paso 6 — Verificacion

```bash
# Ver el estado del servicio ECS
aws ecs describe-services \
  --cluster caso-08-cluster \
  --services caso-08-service \
  --query "services[0].{Status:status,Running:runningCount,Desired:desiredCount}"

# Verificar la imagen activa en el task
aws ecs describe-tasks \
  --cluster caso-08-cluster \
  --tasks $(aws ecs list-tasks --cluster caso-08-cluster --query "taskArns[0]" --output text) \
  --query "tasks[0].containers[0].image"

# Probar el endpoint via ALB
curl -I https://<ALB_DNS>/
# HTTP/1.1 200 OK
```

---

## Errores comunes y soluciones

### `pull access denied` para la imagen GHCR

Causa: ECS no tiene credenciales para leer imagenes de GHCR (privadas por defecto).

Solucion: Hacer la imagen publica (GitHub -> Package -> Settings -> Visibility: Public)
o configurar un secret en AWS Secrets Manager con el token de GitHub y referenciar
`repositoryCredentials` en la Task Definition.

---

### El build multi-platform tarda mucho

Causa: La emulacion QEMU para arm64 en runners amd64 es lenta.

Solucion: Usar cache de buildx con `cache-from/cache-to: type=gha` (ya incluido).
En builds de produccion, considerar un runner arm64 nativo.

---

## Siguiente paso

-> [Caso 09 — FinOps + Scheduled](../caso-09-finops-scheduled/AWS_PASO_A_PASO.md): visibilidad automatica de costos.
