# Caso 02 — Guía paso a paso: S3 + GitHub Actions Deploy

Guía completa para reproducir el pipeline de despliegue a S3 controlado por
GitHub Actions desde cero, con todos los comandos exactos y los errores comunes documentados.

> **Tiempo estimado:** 20–30 minutos. Deploys posteriores: ~45 segundos automáticos.

---

## Prerrequisitos

| Requisito | Verificación |
|:---|:---|
| Cuenta AWS activa con permisos IAM | `aws sts get-caller-identity` |
| AWS CLI instalada | `aws --version` → debe ser 2.x |
| Repositorio GitHub con el código | Este mismo repo |
| Acceso a `Settings` del repo en GitHub | Rol de Owner o Admin |

---

## Paso 1 — Crear el bucket S3

### 1.1 Crear el bucket

```bash
aws s3api create-bucket \
  --bucket mi-pagina-scrum-123 \
  --region us-east-2 \
  --create-bucket-configuration LocationConstraint=us-east-2
```

> **Importante:** Los nombres de bucket son globales en AWS — si `mi-pagina-scrum-123`
> ya existe, elige otro nombre y actualiza el workflow.

Respuesta esperada:

```json
{
    "Location": "http://mi-pagina-scrum-123.s3.amazonaws.com/"
}
```

### 1.2 Habilitar Static Website Hosting

```bash
aws s3api put-bucket-website \
  --bucket mi-pagina-scrum-123 \
  --website-configuration '{
    "IndexDocument": {"Suffix": "index.html"},
    "ErrorDocument": {"Key": "index.html"}
  }'
```

### 1.3 Desactivar el bloqueo de acceso público

S3 bloquea el acceso público por defecto. Para un sitio estático público:

```bash
aws s3api put-public-access-block \
  --bucket mi-pagina-scrum-123 \
  --public-access-block-configuration \
    "BlockPublicAcls=false,IgnorePublicAcls=false,BlockPublicPolicy=false,RestrictPublicBuckets=false"
```

### 1.4 Añadir política de lectura pública

```bash
aws s3api put-bucket-policy \
  --bucket mi-pagina-scrum-123 \
  --policy '{
    "Version": "2012-10-17",
    "Statement": [
      {
        "Sid": "PublicReadGetObject",
        "Effect": "Allow",
        "Principal": "*",
        "Action": "s3:GetObject",
        "Resource": "arn:aws:s3:::mi-pagina-scrum-123/*"
      }
    ]
  }'
```

### 1.5 Verificar la URL del sitio

```bash
# La URL del endpoint estático sigue el patrón:
# http://<bucket>.s3-website.<region>.amazonaws.com
echo "http://mi-pagina-scrum-123.s3-website.us-east-2.amazonaws.com"

# Verificar que el bucket responde (aún sin archivos → 404 esperado)
curl -I http://mi-pagina-scrum-123.s3-website.us-east-2.amazonaws.com
# HTTP/1.1 404 Not Found  ← correcto, aún no hay archivos
```

---

## Paso 2 — Crear usuario IAM con permisos mínimos

### 2.1 Crear la política IAM

La política otorga solo lo necesario para que el workflow sincronice archivos:

```bash
aws iam create-policy \
  --policy-name GitHubActions-S3-Deploy-caso02 \
  --policy-document '{
    "Version": "2012-10-17",
    "Statement": [
      {
        "Sid": "S3SyncPermissions",
        "Effect": "Allow",
        "Action": [
          "s3:PutObject",
          "s3:DeleteObject",
          "s3:GetObject",
          "s3:ListBucket"
        ],
        "Resource": [
          "arn:aws:s3:::mi-pagina-scrum-123",
          "arn:aws:s3:::mi-pagina-scrum-123/*"
        ]
      }
    ]
  }'
```

Anotar el `PolicyArn` de la respuesta — lo necesitas en el siguiente paso.

### 2.2 Crear el usuario IAM

```bash
aws iam create-user --user-name github-actions-caso02
```

### 2.3 Adjuntar la política al usuario

```bash
aws iam attach-user-policy \
  --user-name github-actions-caso02 \
  --policy-arn arn:aws:iam::<TU_ACCOUNT_ID>:policy/GitHubActions-S3-Deploy-caso02
```

### 2.4 Crear las credenciales de acceso

```bash
aws iam create-access-key --user-name github-actions-caso02
```

Respuesta (guardar estos valores — no se pueden recuperar después):

```json
{
    "AccessKey": {
        "UserName": "github-actions-caso02",
        "AccessKeyId": "AKIAIOSFODNN7EXAMPLE",
        "Status": "Active",
        "SecretAccessKey": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
        "CreateDate": "2026-03-22T..."
    }
}
```

> **Seguridad:** Estas credenciales estáticas son la **deuda técnica** de este caso.
> El Caso 03 las elimina completamente con OIDC — nunca hay un secret que rotar o filtrar.

---

## Paso 3 — Configurar secrets en GitHub

1. Abrir el repositorio en GitHub → **Settings** → **Secrets and variables** → **Actions**
2. Clic **"New repository secret"**

Crear los dos secrets:

| Nombre | Valor |
|:---|:---|
| `AWS_ACCESS_KEY_ID` | El `AccessKeyId` del paso anterior |
| `AWS_SECRET_ACCESS_KEY` | El `SecretAccessKey` del paso anterior |

> **No añadir** `AWS_REGION` como secret — es un valor público que va directamente en el YAML.

---

## Paso 4 — El workflow de GitHub Actions

El workflow ya existe en `.github/workflows/despliegue.yml`. Este es su contenido anotado:

```yaml
name: Caso 02 — S3 Deploy
on:
  push:
    branches: [main]
    paths:
      # Solo se activa si cambian archivos en esta carpeta
      # Cambios en caso-01 o docs/ no disparan este workflow
      - 'caso-02-s3-github-actions/**'
  workflow_dispatch:    # Permite ejecución manual desde GitHub UI

jobs:
  deploy:
    runs-on: ubuntu-latest   # Runner gratuito de GitHub
    steps:
      - name: Checkout código
        uses: actions/checkout@v4

      - name: Sincronizar con AWS S3
        run: |
          aws s3 sync ./caso-02-s3-github-actions s3://mi-pagina-scrum-123 --delete
          # --delete: borra en S3 los archivos que ya no están en el repo
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          AWS_REGION: 'us-east-2'
          # aws CLI preinstalada en ubuntu-latest — no requiere setup adicional
```

> **Por qué `paths` filter:** Sin él, cualquier push al repo (cambios en caso-01, docs, etc.)
> dispararía el deploy innecesariamente. Con `paths`, el workflow solo corre cuando hay
> cambios relevantes.

---

## Paso 5 — Primer deploy

### 5.1 Disparar el workflow

```bash
# Hacer un cambio mínimo en la carpeta del caso
touch caso-02-s3-github-actions/.deploy-trigger
git add caso-02-s3-github-actions/.deploy-trigger
git commit -m "chore: trigger primer deploy caso-02"
git push origin main
```

### 5.2 Monitorear la ejecución

1. GitHub → repositorio → pestaña **"Actions"**
2. Ver el workflow "Caso 02 — S3 Deploy" ejecutándose
3. Clic para ver los logs en tiempo real

Log esperado del step `aws s3 sync`:

```text
upload: caso-02-s3-github-actions/index.html to s3://mi-pagina-scrum-123/index.html
upload: caso-02-s3-github-actions/styles.css to s3://mi-pagina-scrum-123/styles.css
upload: caso-02-s3-github-actions/app.js to s3://mi-pagina-scrum-123/app.js
...
```

### 5.3 Verificar el sitio en S3

```bash
# Verificar que los archivos están en el bucket
aws s3 ls s3://mi-pagina-scrum-123/ --recursive --human-readable | head -20

# Verificar que el sitio responde
curl -I http://mi-pagina-scrum-123.s3-website.us-east-2.amazonaws.com
# HTTP/1.1 200 OK  ← sitio disponible
```

---

## Paso 6 — Verificación completa

### Verificar que el `paths` filter funciona

```bash
# Cambio en otro caso — NO debe disparar el workflow de caso-02
echo "<!-- test -->" >> caso-01-amplify-hosting/index.html
git add -A && git commit -m "test: cambio en caso-01 no debe afectar caso-02"
git push origin main

# En GitHub Actions: el workflow de caso-02 NO debe aparecer como ejecutado
```

### Verificar el `--delete` flag

```bash
# Crear un archivo "basura" en S3 directamente
aws s3 cp /dev/null s3://mi-pagina-scrum-123/archivo-basura.txt

# Verificar que está en S3
aws s3 ls s3://mi-pagina-scrum-123/ | grep archivo-basura

# Disparar el workflow → debe BORRAR archivo-basura.txt (no está en el repo)
touch caso-02-s3-github-actions/index.html  # modificar un archivo del caso
git add -A && git commit -m "test: verificar --delete en s3 sync"
git push origin main

# Después del deploy, verificar que fue borrado
aws s3 ls s3://mi-pagina-scrum-123/ | grep archivo-basura
# No debe aparecer
```

### Verificar el deploy manual (`workflow_dispatch`)

1. GitHub → **Actions** → workflow "Caso 02 — S3 Deploy"
2. Clic **"Run workflow"** → seleccionar rama `main` → **"Run workflow"**
3. Útil para hotfixes sin necesitar hacer un commit nuevo

---

## Errores comunes y soluciones

### Error: `Unable to locate credentials`

```text
An error occurred (NoCredentialsError) when calling the ListObjectsV2 operation:
Unable to locate credentials
```

**Causa:** Los secrets `AWS_ACCESS_KEY_ID` o `AWS_SECRET_ACCESS_KEY` no están configurados
o tienen un nombre incorrecto.

**Verificación:**

- GitHub → Settings → Secrets → Actions → confirmar que los dos secrets existen
- El nombre debe ser exactamente `AWS_ACCESS_KEY_ID` (mayúsculas, sin espacios)

---

### Error: `Access Denied` al hacer sync

```text
upload failed: caso-02-s3-github-actions/index.html to s3://mi-pagina-scrum-123/index.html
An error occurred (AccessDenied) when calling the PutObject operation: Access Denied
```

**Causa:** El usuario IAM no tiene `s3:PutObject` sobre el bucket.

**Verificación:**

```bash
# Ver las políticas del usuario
aws iam list-attached-user-policies --user-name github-actions-caso02

# Simular el permiso (policy simulator)
aws iam simulate-principal-policy \
  --policy-source-arn arn:aws:iam::<ACCOUNT_ID>:user/github-actions-caso02 \
  --action-names s3:PutObject \
  --resource-arns "arn:aws:s3:::mi-pagina-scrum-123/*"
```

---

### Error: El workflow no se dispara al hacer push

**Causa:** El archivo modificado no está dentro de `caso-02-s3-github-actions/**`.

**Verificación:**

```bash
# Confirmar que el commit modifica archivos en la carpeta correcta
git diff --name-only HEAD~1 HEAD

# Los archivos deben empezar con:
# caso-02-s3-github-actions/...
```

---

### El sitio responde HTTP pero no HTTPS

**Esta es una limitación conocida y documentada del Caso 02.** S3 Static Website
Hosting solo sirve HTTP. HTTPS requiere CloudFront frente al bucket, que se implementa
en el **Caso 03**.

---

### Los PDFs no se sirven correctamente (Content-Type incorrecto)

```bash
# Forzar el Content-Type correcto al sincronizar
aws s3 sync ./caso-02-s3-github-actions s3://mi-pagina-scrum-123 \
  --delete \
  --exclude "*.pdf"

aws s3 sync ./caso-02-s3-github-actions s3://mi-pagina-scrum-123 \
  --exclude "*" \
  --include "*.pdf" \
  --content-type "application/pdf"
```

Añadir estos dos steps separados en el workflow si los PDFs muestran el header
`Content-Type: application/octet-stream`.

---

## Monitoreo post-deploy

### Ver métricas del bucket en CloudWatch

```bash
# Solicitudes al bucket en las últimas 24h
aws cloudwatch get-metric-statistics \
  --namespace AWS/S3 \
  --metric-name NumberOfObjects \
  --dimensions Name=BucketName,Value=mi-pagina-scrum-123 \
              Name=StorageType,Value=AllStorageTypes \
  --start-time $(date -u -d '24 hours ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 86400 \
  --statistics Average
```

### Ver logs de acceso (si están habilitados)

```bash
# Habilitar access logs (opcional, genera costo mínimo)
aws s3api put-bucket-logging \
  --bucket mi-pagina-scrum-123 \
  --bucket-logging-status '{
    "LoggingEnabled": {
      "TargetBucket": "mi-pagina-scrum-123-logs",
      "TargetPrefix": "access-logs/"
    }
  }'
```

---

## Costos reales de este caso

| Recurso | Uso típico (portafolio personal) | Costo |
|:---|:---|:---|
| **S3 Storage** | ~50 MB (PDFs + assets) | ~$0.001/mes |
| **S3 Requests** | ~1000 GET/mes | ~$0.0004/mes |
| **S3 Transfer** | ~1 GB salida/mes (Free Tier: 100 GB) | $0.00 |
| **GitHub Actions** | ~5 min/deploy × 10 deploys/mes (Free Tier: 2000 min) | $0.00 |
| **Total estimado** | | **< $0.01 / mes** |

---

## Comparativa con el Caso 01

| Aspecto | Caso 01 (Amplify) | Caso 02 (S3 + Actions) |
|:---|:---|:---|
| **Visibilidad del pipeline** | Solo en Amplify Console | En GitHub Actions (versionado) |
| **HTTPS** | Automático (CloudFront incluido) | ⚠️ Solo HTTP hasta Caso 03 |
| **CDN** | CloudFront incluido | ⚠️ Sin CDN hasta Caso 03 |
| **Steps personalizables** | No (caja negra) | Sí (YAML completo) |
| **Costo por deploy** | $0 (Free Tier) | ~$0.0001 |
| **Control de credenciales** | No aplica | ⚠️ Credenciales estáticas → Caso 03 |

---

## Deuda técnica identificada

Las credenciales estáticas (`AWS_ACCESS_KEY_ID`) representan un riesgo:

- Si se filtran en un log o commit accidental, un atacante tiene acceso **permanente**
  hasta que rotes manualmente la clave
- Requieren rotación periódica manual
- No hay trazabilidad detallada de qué deploy usó qué clave

**Solución:** [Caso 03 — CloudFront + OIDC](../caso-03-cloudfront-oidc/README.md) elimina
estas credenciales completamente. El token OIDC dura ~15 segundos y es válido solo para
este repositorio y esta rama.

---

## Siguiente paso

➡️ [Caso 03 — CloudFront + OIDC](../caso-03-cloudfront-oidc/README.md): eliminar las credenciales estáticas y añadir CDN real.
