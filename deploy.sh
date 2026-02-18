#!/bin/bash
set -e # Terminar si hay error

echo "🔹 Autenticando con AWS OIDC..."

# Obtener credenciales temporales
CREDS=$(aws sts assume-role-with-web-identity \
  --role-arn "${AWS_ROLE_ARN}" \
  --role-session-name "GitLabDeploy-${CI_PIPELINE_ID}" \
  --web-identity-token "${GITLAB_OIDC_TOKEN}" \
  --duration-seconds 3600 \
  --query 'Credentials.[AccessKeyId,SecretAccessKey,SessionToken]' \
  --output text)

# Exportar las credenciales como variables de entorno
export AWS_ACCESS_KEY_ID=$(echo $CREDS | cut -d' ' -f1)
export AWS_SECRET_ACCESS_KEY=$(echo $CREDS | cut -d' ' -f2)
export AWS_SESSION_TOKEN=$(echo $CREDS | cut -d' ' -f3)

# Verificar identidad
aws sts get-caller-identity

echo "🔹 Desplegando archivos a S3..."
# Sincronizar carpeta
aws s3 sync caso-l-finops-optimization/app/public/ s3://${S3_BUCKET_CASE_L} --delete

echo "✅ Despliegue completado con éxito."
echo "🌍 Tu sitio web: http://${S3_BUCKET_CASE_L}.s3-website-${AWS_REGION}.amazonaws.com"
