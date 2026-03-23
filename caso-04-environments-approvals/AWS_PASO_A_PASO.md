# Caso 04 — Guia paso a paso: GitHub Environments + Aprobaciones

> Estado: Implementacion proyectada — Q2 2026.
> Tiempo estimado: 30 minutos.

---

## Que resuelve este caso

El Caso 03 asegura la identidad (OIDC). Este caso asegura el gobierno:
staging se despliega automaticamente, pero produccion requiere que una persona
apruebe el deploy en GitHub antes de que continue.

---

## Prerrequisitos

| Requisito | Verificacion |
|:---|:---|
| Caso 03 funcionando con OIDC | Workflow desplegando sin credenciales estaticas |
| Dos buckets S3 | staging y produccion separados |
| Acceso Owner al repositorio | Necesario para crear Environments |

---

## Paso 1 — Crear los GitHub Environments

1. GitHub -> Settings -> Environments -> New environment
2. Crear **staging** sin protection rules (despliega automatico)
3. Crear **production** con protection rule:
   - Activar "Required reviewers"
   - Añadir tu usuario (o equipo) como revisor requerido
   - Opcional: activar "Prevent self-review" si hay equipo

---

## Paso 2 — Configurar secrets por entorno

Cada entorno tiene su propio bucket S3 independiente.

En el entorno **staging**:

```text
Settings -> Environments -> staging -> Add secret
BUCKET_NAME = caso-04-staging
```

En el entorno **production**:

```text
Settings -> Environments -> production -> Add secret
BUCKET_NAME = caso-04-production
```

Los secrets del entorno sobreescriben los secrets del repositorio cuando el job
usa `environment: <nombre>`.

---

## Paso 3 — Crear los buckets S3

```bash
# Bucket de staging
aws s3api create-bucket \
  --bucket caso-04-staging \
  --region us-east-1

# Bucket de produccion
aws s3api create-bucket \
  --bucket caso-04-production \
  --region us-east-1

# Habilitar Static Website Hosting en ambos
for BUCKET in caso-04-staging caso-04-production; do
  aws s3api put-bucket-website \
    --bucket $BUCKET \
    --website-configuration '{"IndexDocument":{"Suffix":"index.html"}}'
done
```

---

## Paso 4 — Workflow con gates de aprobacion

```yaml
name: Caso 04 — Deploy con Environments

on:
  push:
    branches: [main, dev]
    paths:
      - 'caso-04-environments-approvals/**'

permissions:
  id-token: write
  contents: read

jobs:
  deploy-staging:
    name: Deploy a Staging
    runs-on: ubuntu-latest
    environment: staging         # sin protection rules: continua automaticamente
    steps:
      - uses: actions/checkout@v4
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ vars.AWS_ROLE_ARN }}
          aws-region: us-east-1
      - run: aws s3 sync ./caso-04-environments-approvals s3://${{ secrets.BUCKET_NAME }} --delete

  deploy-production:
    name: Deploy a Produccion
    runs-on: ubuntu-latest
    needs: deploy-staging        # solo corre si staging fue exitoso
    environment: production      # PAUSA aqui hasta que el revisor apruebe
    steps:
      - uses: actions/checkout@v4
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ vars.AWS_ROLE_ARN }}
          aws-region: us-east-1
      - run: aws s3 sync ./caso-04-environments-approvals s3://${{ secrets.BUCKET_NAME }} --delete
```

---

## Paso 5 — Flujo de aprobacion en GitHub UI

Cuando el job `deploy-production` llega al gate:

1. GitHub envia notificacion por email al revisor configurado
2. El revisor ve en la pestaña Actions un banner: "Waiting for review"
3. El revisor hace clic en "Review pending deployments"
4. Selecciona el entorno `production`
5. Escribe un comentario opcional y hace clic en "Approve and deploy"
6. El workflow continua y despliega a produccion

Si el revisor rechaza, el workflow termina sin desplegar a produccion.

---

## Paso 6 — Verificacion

Verificar que staging se despliega automaticamente al hacer push a `dev`:

```bash
git checkout dev
touch caso-04-environments-approvals/test.txt
git add -A && git commit -m "test: trigger staging deploy"
git push origin dev
# En GitHub Actions: el job deploy-staging corre sin intervencion
# El job deploy-production queda en espera de aprobacion
```

Verificar la separacion de entornos:

```bash
# El bucket staging tiene el contenido nuevo
aws s3 ls s3://caso-04-staging/

# El bucket produccion aun tiene el contenido anterior (sin aprobacion)
aws s3 ls s3://caso-04-production/
```

---

## Errores comunes y soluciones

### El job de produccion no pide aprobacion

Causa: El environment `production` no tiene "Required reviewers" configurado.

Solucion: Settings -> Environments -> production -> Environment protection rules ->
activar "Required reviewers" y añadir al menos un usuario.

---

### El revisor no recibe la notificacion

Causa: Las notificaciones de GitHub Actions pueden ir a spam o estar desactivadas.

Solucion: Settings del usuario -> Notifications -> Actions -> activar notificaciones
de "Required reviews" para el repositorio.

---

### `secrets.BUCKET_NAME` devuelve vacio

Causa: El secret esta definido en el repositorio pero no en el entorno especifico.

Diferencia importante: los secrets de repositorio y los secrets de entorno son distintos.
Un secret definido en Settings -> Secrets -> Actions (nivel repositorio) NO es el mismo
que uno definido en Settings -> Environments -> staging -> Secrets.

---

## Siguiente paso

-> [Caso 05 — Lambda + API Gateway](../caso-05-lambda-api-gateway/AWS_PASO_A_PASO.md): primer backend real con pipeline multi-job.
