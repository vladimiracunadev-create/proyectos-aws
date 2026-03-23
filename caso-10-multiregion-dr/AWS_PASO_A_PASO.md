# Caso 10 — Guia paso a paso: Multi-region + Disaster Recovery

> Estado: Implementacion proyectada — Q4 2026.
> Tiempo estimado: 90 minutos.

---

## Que resuelve este caso

Deploy paralelo a dos regiones AWS (us-east-1 y eu-west-1) con validacion
de salud por region antes de actualizar el DNS con Route53. Si los smoke
tests fallan, el workflow hace rollback del DNS automaticamente.

---

## Prerrequisitos

| Requisito | Verificacion |
|:---|:---|
| Dominio en Route53 | `aws route53 list-hosted-zones` |
| Permisos Route53 y S3 multi-region | Ver paso 1 |
| Caso 03 funcionando en us-east-1 | Bucket S3 + CloudFront activos |

---

## Paso 1 — Permisos IAM adicionales para el rol

```json
{
  "Effect": "Allow",
  "Action": [
    "route53:ChangeResourceRecordSets",
    "route53:GetHostedZone",
    "route53:ListResourceRecordSets",
    "route53:GetChange"
  ],
  "Resource": [
    "arn:aws:route53:::hostedzone/<HOSTED_ZONE_ID>",
    "arn:aws:route53:::change/*"
  ]
}
```

---

## Paso 2 — Crear buckets S3 en ambas regiones

```bash
# Bucket en us-east-1 (ya existe del caso anterior, reusar o crear nuevo)
aws s3api create-bucket \
  --bucket caso-10-us-east-1 \
  --region us-east-1

# Bucket en eu-west-1
aws s3api create-bucket \
  --bucket caso-10-eu-west-1 \
  --region eu-west-1 \
  --create-bucket-configuration LocationConstraint=eu-west-1

# Bloquear acceso publico en ambos (se sirven via CloudFront)
for BUCKET in caso-10-us-east-1 caso-10-eu-west-1; do
  aws s3api put-public-access-block \
    --bucket $BUCKET \
    --public-access-block-configuration \
      "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"
done
```

---

## Paso 3 — Configurar Route53 con Failover Routing

```bash
HOSTED_ZONE_ID="<TU_HOSTED_ZONE_ID>"
CDN_US="<CLOUDFRONT_US_DOMAIN>"
CDN_EU="<CLOUDFRONT_EU_DOMAIN>"

# Health Check para us-east-1
aws route53 create-health-check \
  --caller-reference "caso-10-hc-us-$(date +%s)" \
  --health-check-config "{
    \"Type\": \"HTTPS\",
    \"FullyQualifiedDomainName\": \"${CDN_US}\",
    \"RequestInterval\": 30,
    \"FailureThreshold\": 3
  }"

# Record PRIMARY (us-east-1)
aws route53 change-resource-record-sets \
  --hosted-zone-id $HOSTED_ZONE_ID \
  --change-batch "{
    \"Changes\": [{
      \"Action\": \"UPSERT\",
      \"ResourceRecordSet\": {
        \"Name\": \"caso-10.tudominio.com\",
        \"Type\": \"CNAME\",
        \"SetIdentifier\": \"primary-us-east-1\",
        \"Failover\": \"PRIMARY\",
        \"HealthCheckId\": \"<HC_ID_US>\",
        \"TTL\": 60,
        \"ResourceRecords\": [{\"Value\": \"${CDN_US}\"}]
      }
    }]
  }"

# Record SECONDARY (eu-west-1) - sin health check, siempre disponible como fallback
aws route53 change-resource-record-sets \
  --hosted-zone-id $HOSTED_ZONE_ID \
  --change-batch "{
    \"Changes\": [{
      \"Action\": \"UPSERT\",
      \"ResourceRecordSet\": {
        \"Name\": \"caso-10.tudominio.com\",
        \"Type\": \"CNAME\",
        \"SetIdentifier\": \"secondary-eu-west-1\",
        \"Failover\": \"SECONDARY\",
        \"TTL\": 60,
        \"ResourceRecords\": [{\"Value\": \"${CDN_EU}\"}]
      }
    }]
  }"
```

---

## Paso 4 — Workflow con matrix de regiones

```yaml
name: Caso 10 — Multi-region Deploy

on:
  push:
    branches: [main]
    paths:
      - 'caso-10-multiregion-dr/**'

permissions:
  id-token: write
  contents: read

jobs:
  deploy:
    name: Deploy ${{ matrix.region }}
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        region: [us-east-1, eu-west-1]
        include:
          - region: us-east-1
            bucket: caso-10-us-east-1
            cdn-id: ${{ vars.CDN_ID_US }}
          - region: eu-west-1
            bucket: caso-10-eu-west-1
            cdn-id: ${{ vars.CDN_ID_EU }}
    steps:
      - uses: actions/checkout@v4
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ vars.AWS_ROLE_ARN }}
          aws-region: ${{ matrix.region }}
      - run: aws s3 sync ./caso-10-multiregion-dr s3://${{ matrix.bucket }} --delete
      - run: |
          aws cloudfront create-invalidation \
            --distribution-id ${{ matrix.cdn-id }} \
            --paths "/*"

  smoke-tests:
    name: Smoke test ${{ matrix.region }}
    runs-on: ubuntu-latest
    needs: deploy
    strategy:
      fail-fast: false
      matrix:
        include:
          - region: us-east-1
            url: ${{ vars.URL_US }}
          - region: eu-west-1
            url: ${{ vars.URL_EU }}
    steps:
      - name: Verificar endpoint ${{ matrix.region }}
        id: smoke
        run: |
          STATUS=$(curl -s -o /dev/null -w "%{http_code}" "${{ matrix.url }}")
          echo "region=${{ matrix.region }} status=$STATUS"
          echo "status=$STATUS" >> $GITHUB_OUTPUT
          [ "$STATUS" = "200" ] || exit 1

  update-dns:
    name: Actualizar DNS
    runs-on: ubuntu-latest
    needs: smoke-tests
    if: success()
    steps:
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ vars.AWS_ROLE_ARN }}
          aws-region: us-east-1
      - run: echo "Ambas regiones OK - DNS Route53 ya apunta a las distribuciones activas"

  rollback-dns:
    name: Rollback DNS
    runs-on: ubuntu-latest
    needs: smoke-tests
    if: failure()
    steps:
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ vars.AWS_ROLE_ARN }}
          aws-region: us-east-1
      - name: Revertir a region anterior
        run: |
          echo "Smoke tests fallaron - manteniendo DNS en estado anterior"
          # Aqui iria el comando aws route53 change-resource-record-sets de rollback
```

---

## Paso 5 — Verificacion

Verificar que Route53 apunta correctamente a ambas regiones:

```bash
dig caso-10.tudominio.com
# Debe devolver el CNAME de CloudFront primario

# Simular fallo de la region primaria
aws route53 update-health-check \
  --health-check-id <HC_ID_US> \
  --disabled

# Route53 debe conmutar automaticamente al SECONDARY (eu-west-1)
dig caso-10.tudominio.com
# Ahora debe devolver el CNAME de CloudFront eu-west-1
```

---

## Patrones de DR implementados

| Patron | RTO | RPO | Este caso |
|:---|:---|:---|:---|
| Backup and Restore | Horas | Horas | No |
| Pilot Light | 10 min | Minutos | No |
| Warm Standby | 1 min | Segundos | Si |
| Multi-site Active/Active | Segundos | 0 | Futuro |

---

## Siguiente paso

-> [Caso 11 — EKS + GitOps](../caso-11-eks-gitops/AWS_PASO_A_PASO.md): cierre del viaje con Kubernetes y GitOps.
