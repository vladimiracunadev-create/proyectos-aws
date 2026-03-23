# Caso 03 — Guia paso a paso: S3 + CloudFront + OIDC

> Estado: Implementacion proyectada — Q2 2026.
> Los pasos siguientes representan el plan tecnico detallado para cuando se ejecute este caso.
> Tiempo estimado: 45-60 minutos.

---

## Por que este caso es critico

El Caso 02 usa `AWS_ACCESS_KEY_ID` como secret estatico en GitHub. Si esa clave se filtra
(log expuesto, commit accidental), un atacante tiene acceso permanente hasta rotacion manual.

Con OIDC no hay secreto que filtrar: GitHub emite un JWT que dura milisegundos,
AWS STS lo valida y devuelve credenciales que expiran en 15 minutos.

---

## Prerrequisitos

| Requisito | Verificacion |
|:---|:---|
| Caso 02 funcionando | S3 bucket activo con despliegue via Actions |
| Cuenta AWS con permisos IAM | `aws sts get-caller-identity` |
| AWS CLI 2.x | `aws --version` |
| Acceso a Settings del repo GitHub | Rol Owner o Admin |

---

## Paso 1 — Crear el OIDC Provider en IAM

AWS necesita confiar en los tokens JWT que emite GitHub Actions.

```bash
aws iam create-open-id-connect-provider \
  --url https://token.actions.githubusercontent.com \
  --client-id-list sts.amazonaws.com \
  --thumbprint-list 6938fd4d98bab03faadb97b34396831e3780aea1
```

Verificar que el provider existe:

```bash
aws iam list-open-id-connect-providers
# Debe mostrar: arn:aws:iam::<ACCOUNT_ID>:oidc-provider/token.actions.githubusercontent.com
```

---

## Paso 2 — Crear el IAM Role con trust policy

La trust policy restringe que solo este repositorio y esta rama puedan asumir el rol.

```bash
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
REPO="vladimiracunadev-create/proyectos-aws"

aws iam create-role \
  --role-name GitHubActions-CloudFront-Deploy \
  --assume-role-policy-document "{
    \"Version\": \"2012-10-17\",
    \"Statement\": [
      {
        \"Effect\": \"Allow\",
        \"Principal\": {
          \"Federated\": \"arn:aws:iam::${ACCOUNT_ID}:oidc-provider/token.actions.githubusercontent.com\"
        },
        \"Action\": \"sts:AssumeRoleWithWebIdentity\",
        \"Condition\": {
          \"StringEquals\": {
            \"token.actions.githubusercontent.com:aud\": \"sts.amazonaws.com\"
          },
          \"StringLike\": {
            \"token.actions.githubusercontent.com:sub\": \"repo:${REPO}:ref:refs/heads/main\"
          }
        }
      }
    ]
  }"
```

Adjuntar politica de permisos S3 y CloudFront:

```bash
aws iam put-role-policy \
  --role-name GitHubActions-CloudFront-Deploy \
  --policy-name S3CloudFrontDeploy \
  --policy-document "{
    \"Version\": \"2012-10-17\",
    \"Statement\": [
      {
        \"Effect\": \"Allow\",
        \"Action\": [\"s3:PutObject\", \"s3:DeleteObject\", \"s3:ListBucket\"],
        \"Resource\": [
          \"arn:aws:s3:::caso-03-bucket\",
          \"arn:aws:s3:::caso-03-bucket/*\"
        ]
      },
      {
        \"Effect\": \"Allow\",
        \"Action\": \"cloudfront:CreateInvalidation\",
        \"Resource\": \"arn:aws:cloudfront::${ACCOUNT_ID}:distribution/*\"
      }
    ]
  }"
```

---

## Paso 3 — Crear bucket S3 privado

A diferencia del Caso 02, este bucket no tiene acceso publico — CloudFront lo sirve via OAC.

```bash
aws s3api create-bucket \
  --bucket caso-03-cloudfront-oidc \
  --region us-east-1

# Bloquear acceso publico directo
aws s3api put-public-access-block \
  --bucket caso-03-cloudfront-oidc \
  --public-access-block-configuration \
    "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"
```

---

## Paso 4 — Crear distribucion CloudFront con OAC

OAC (Origin Access Control) permite que solo CloudFront lea el bucket, sin exponer S3 al publico.

```bash
# Crear OAC
aws cloudfront create-origin-access-control \
  --origin-access-control-config '{
    "Name": "caso-03-oac",
    "OriginAccessControlOriginType": "s3",
    "SigningBehavior": "always",
    "SigningProtocol": "sigv4"
  }'
```

Crear la distribucion (guardar el DistributionId de la respuesta):

```bash
aws cloudfront create-distribution \
  --distribution-config '{
    "Origins": {
      "Quantity": 1,
      "Items": [{
        "Id": "S3-caso-03",
        "DomainName": "caso-03-cloudfront-oidc.s3.us-east-1.amazonaws.com",
        "OriginAccessControlId": "<OAC_ID>",
        "S3OriginConfig": {"OriginAccessIdentity": ""}
      }]
    },
    "DefaultCacheBehavior": {
      "TargetOriginId": "S3-caso-03",
      "ViewerProtocolPolicy": "redirect-to-https",
      "CachePolicyId": "658327ea-f89d-4fab-a63d-7e88639e58f6",
      "AllowedMethods": {"Quantity": 2, "Items": ["GET","HEAD"]}
    },
    "DefaultRootObject": "index.html",
    "Enabled": true,
    "Comment": "caso-03-cloudfront-oidc"
  }'
```

Politica de bucket para que CloudFront acceda via OAC:

```bash
aws s3api put-bucket-policy \
  --bucket caso-03-cloudfront-oidc \
  --policy "{
    \"Version\": \"2012-10-17\",
    \"Statement\": [{
      \"Effect\": \"Allow\",
      \"Principal\": {\"Service\": \"cloudfront.amazonaws.com\"},
      \"Action\": \"s3:GetObject\",
      \"Resource\": \"arn:aws:s3:::caso-03-cloudfront-oidc/*\",
      \"Condition\": {
        \"StringEquals\": {
          \"AWS:SourceArn\": \"arn:aws:cloudfront::${ACCOUNT_ID}:distribution/<DISTRIBUTION_ID>\"
        }
      }
    }]
  }"
```

---

## Paso 5 — Actualizar el workflow de GitHub Actions

Reemplazar las credenciales estaticas del Caso 02 con OIDC:

```yaml
name: Caso 03 — CloudFront + OIDC Deploy

on:
  push:
    branches: [main]
    paths:
      - 'caso-03-cloudfront-oidc/**'

permissions:
  id-token: write    # habilita emision del JWT OIDC
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Configurar credenciales AWS via OIDC
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::<ACCOUNT_ID>:role/GitHubActions-CloudFront-Deploy
          aws-region: us-east-1

      - name: Sincronizar con S3
        run: aws s3 sync ./caso-03-cloudfront-oidc s3://caso-03-cloudfront-oidc --delete

      - name: Invalidar cache CloudFront
        run: |
          aws cloudfront create-invalidation \
            --distribution-id <DISTRIBUTION_ID> \
            --paths "/*"
```

Eliminar los secrets estaticos del repo (ya no son necesarios):

1. GitHub -> Settings -> Secrets -> Actions
2. Borrar `AWS_ACCESS_KEY_ID` y `AWS_SECRET_ACCESS_KEY`

---

## Paso 6 — Verificacion

Verificar que el JWT se genera y el rol se asume correctamente (visible en los logs del workflow):

```text
Run aws-actions/configure-aws-credentials@v4
  Assuming role with OIDC...
  Assumed role: arn:aws:iam::<ACCOUNT_ID>:role/GitHubActions-CloudFront-Deploy
```

Verificar el sitio via CloudFront:

```bash
CLOUDFRONT_URL=$(aws cloudfront list-distributions \
  --query "DistributionList.Items[?Comment=='caso-03-cloudfront-oidc'].DomainName" \
  --output text)

curl -I https://${CLOUDFRONT_URL}
# HTTP/2 200
# server: CloudFront
# x-cache: Hit from cloudfront
```

---

## Errores comunes y soluciones

### Error: `InvalidIdentityToken`

```text
An error occurred (InvalidIdentityToken) when calling the AssumeRoleWithWebIdentity operation
```

Causa: El thumbprint del OIDC provider no coincide o el audience es incorrecto.

Solucion: Verificar que el OIDC Provider tiene `sts.amazonaws.com` como audience y
el thumbprint correcto para `token.actions.githubusercontent.com`.

---

### Error: `AccessDenied` al crear invalidacion CloudFront

Causa: El rol IAM no tiene permiso `cloudfront:CreateInvalidation`.

Solucion: Verificar la inline policy del rol con:

```bash
aws iam get-role-policy \
  --role-name GitHubActions-CloudFront-Deploy \
  --policy-name S3CloudFrontDeploy
```

---

### La trust policy bloquea el workflow

Causa: La condicion `StringLike` en el `sub` claim es demasiado restrictiva.

Solucion: Durante desarrollo, relajar la condicion a `repo:owner/repo:*`
y luego volver a restringir a la rama especifica en produccion.

---

## Diferencia con el Caso 02

| Aspecto | Caso 02 | Caso 03 |
|:---|:---|:---|
| Autenticacion AWS | Credenciales estaticas (secrets) | OIDC (sin secrets) |
| Riesgo si se filtra | Acceso permanente hasta rotar | Sin impacto (token ya expiro) |
| HTTPS | Solo HTTP (S3 endpoint) | HTTPS con certificado ACM |
| CDN | Sin CDN | CloudFront global |
| Tiempo de credencial | Permanente hasta rotacion | 15 minutos |

---

## Siguiente paso

-> [Caso 04 — Environments + Approvals](../caso-04-environments-approvals/AWS_PASO_A_PASO.md): gobierno humano sobre el pipeline.
