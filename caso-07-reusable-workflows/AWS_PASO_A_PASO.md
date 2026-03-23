# Caso 07 — Guia paso a paso: Reusable Workflows + Composite Actions

> Estado: Implementacion proyectada — Q3 2026.
> Tiempo estimado: 45 minutos.

---

## Que resuelve este caso

Los casos 03 al 06 repiten la configuracion de OIDC y los steps de deploy
en cada workflow. Este caso extrae esa logica comun a una libreria interna
de GitHub Actions reutilizable, siguiendo el principio DRY.

---

## Prerrequisitos

| Requisito | Verificacion |
|:---|:---|
| Casos 03-06 funcionando | Workflows con OIDC y deploy operativos |
| Acceso al directorio `.github/` | Sin restricciones de CODEOWNERS |

---

## Paso 1 — Crear la Composite Action para OIDC

Una Composite Action agrupa steps repetidos en una unidad reutilizable.

```text
.github/actions/setup-aws-oidc/
└── action.yml
```

```yaml
# .github/actions/setup-aws-oidc/action.yml
name: Setup AWS OIDC
description: Configura credenciales AWS via OIDC federation

inputs:
  role-arn:
    description: ARN del rol IAM a asumir
    required: true
  aws-region:
    description: Region AWS
    required: false
    default: us-east-1

outputs:
  account-id:
    description: AWS Account ID autenticado
    value: ${{ steps.auth.outputs.aws-account-id }}

runs:
  using: composite
  steps:
    - name: Configurar credenciales AWS via OIDC
      id: auth
      uses: aws-actions/configure-aws-credentials@v4
      with:
        role-to-assume: ${{ inputs.role-arn }}
        aws-region: ${{ inputs.aws-region }}
        output-credentials: true
```

---

## Paso 2 — Crear el Reusable Workflow para deploy a S3

```text
.github/workflows/deploy-s3-oidc.yml
```

```yaml
# .github/workflows/deploy-s3-oidc.yml
name: Deploy S3 (Reusable)

on:
  workflow_call:
    inputs:
      source-dir:
        description: Directorio fuente a sincronizar
        required: true
        type: string
      bucket:
        description: Nombre del bucket S3 destino
        required: true
        type: string
      aws-region:
        description: Region AWS
        required: false
        type: string
        default: us-east-1
      cloudfront-distribution-id:
        description: ID de distribucion CloudFront (opcional)
        required: false
        type: string
        default: ''
    secrets:
      aws-role-arn:
        required: true

permissions:
  id-token: write
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup AWS OIDC
        uses: ./.github/actions/setup-aws-oidc
        with:
          role-arn: ${{ secrets.aws-role-arn }}
          aws-region: ${{ inputs.aws-region }}

      - name: Sync S3
        run: aws s3 sync ${{ inputs.source-dir }} s3://${{ inputs.bucket }} --delete

      - name: Invalidar CloudFront
        if: inputs.cloudfront-distribution-id != ''
        run: |
          aws cloudfront create-invalidation \
            --distribution-id ${{ inputs.cloudfront-distribution-id }} \
            --paths "/*"
```

---

## Paso 3 — Refactorizar el Caso 03 para usar el reusable workflow

Antes (workflow del Caso 03, repetitivo):

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ vars.AWS_ROLE_ARN }}
          aws-region: us-east-1
      - run: aws s3 sync ./caso-03-cloudfront-oidc s3://caso-03-bucket --delete
      - run: aws cloudfront create-invalidation --distribution-id $CDN_ID --paths "/*"
```

Despues (usando el reusable workflow):

```yaml
jobs:
  deploy:
    uses: ./.github/workflows/deploy-s3-oidc.yml
    with:
      source-dir: ./caso-03-cloudfront-oidc
      bucket: caso-03-bucket
      cloudfront-distribution-id: ${{ vars.CDN_DISTRIBUTION_ID }}
    secrets:
      aws-role-arn: ${{ secrets.AWS_ROLE_ARN }}
```

El workflow del caso pasa de ~20 lineas a 10.

---

## Paso 4 — Crear el Reusable Workflow para smoke tests

```yaml
# .github/workflows/smoke-test.yml
name: Smoke Test (Reusable)

on:
  workflow_call:
    inputs:
      url:
        description: URL a verificar
        required: true
        type: string
      expected-status:
        description: HTTP status esperado
        required: false
        type: number
        default: 200

jobs:
  smoke-test:
    runs-on: ubuntu-latest
    steps:
      - name: Verificar endpoint
        run: |
          STATUS=$(curl -s -o /dev/null -w "%{http_code}" "${{ inputs.url }}")
          echo "Status: $STATUS"
          if [ "$STATUS" != "${{ inputs.expected-status }}" ]; then
            echo "Fallo: esperado ${{ inputs.expected-status }}, obtenido $STATUS"
            exit 1
          fi
          echo "OK: endpoint responde $STATUS"
```

---

## Paso 5 — Verificacion

Verificar que la Composite Action funciona de forma aislada:

```bash
# En un workflow de prueba
- uses: ./.github/actions/setup-aws-oidc
  with:
    role-arn: ${{ vars.AWS_ROLE_ARN }}
- run: aws sts get-caller-identity
  # Debe mostrar el rol asumido, no el usuario original
```

Verificar que los casos refactorizados (03-06) siguen funcionando:

```bash
# Hacer un cambio en caso-03 y pushear
touch caso-03-cloudfront-oidc/test.txt
git add -A && git commit -m "test: verificar reusable workflow"
git push origin main
# El workflow de caso-03 debe usar deploy-s3-oidc.yml y completarse correctamente
```

---

## Estructura final de .github/

```text
.github/
├── actions/
│   ├── setup-aws-oidc/
│   │   └── action.yml          (Composite Action para OIDC)
│   └── notify-deploy/
│       └── action.yml          (Composite Action para notificaciones)
└── workflows/
    ├── deploy-s3-oidc.yml      (Reusable: deploy a S3 con OIDC)
    ├── deploy-lambda-sam.yml   (Reusable: deploy Lambda con SAM)
    ├── smoke-test.yml          (Reusable: verificacion post-deploy)
    ├── despliegue.yml          (Caso 02 - legacy)
    ├── caso-03-deploy.yml      (refactorizado -> usa reusable)
    ├── caso-04-deploy.yml      (refactorizado -> usa reusable)
    └── ...
```

---

## Siguiente paso

-> [Caso 08 — Containers + GHCR](../caso-08-containers-ghcr/AWS_PASO_A_PASO.md): containerizar y desplegar en ECS Fargate.
