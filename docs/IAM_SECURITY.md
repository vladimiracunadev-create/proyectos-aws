# Ejemplo de política IAM para despliegue a S3 y invalidación de CloudFront

A continuación hay un ejemplo de política JSON con **permisos mínimos** para que un usuario/rol pueda sincronizar contenido a un bucket S3 y crear invalidaciones en CloudFront (opcional).

**IMPORTANTE:** Reemplaza `arn:aws:s3:::tu-bucket` y `arn:aws:cloudfront::123456789012:distribution/XXXXXXXX` por tus recursos reales. Ajusta los `Resource` para limitar al mínimo necesario.

# Ejemplo de política IAM para Terraform (S3 + CloudFront)

Esta política otorga los permisos necesarios para que Terraform pueda crear y gestionar los recursos del **Caso C**.

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "TerraformS3Permissions",
            "Effect": "Allow",
            "Action": [
                "s3:CreateBucket",
                "s3:DeleteBucket",
                "s3:GetBucket*",
                "s3:PutBucket*",
                "s3:ListBucket",
                "s3:PutEncryptionConfiguration",
                "s3:PutObject",
                "s3:GetObject",
                "s3:DeleteObject"
            ],
            "Resource": "arn:aws:s3:::caso-c-terraform-s3-*"
        },
        {
            "Sid": "TerraformCloudFrontPermissions",
            "Effect": "Allow",
            "Action": [
                "cloudfront:CreateDistribution",
                "cloudfront:GetDistribution",
                "cloudfront:UpdateDistribution",
                "cloudfront:DeleteDistribution",
                "cloudfront:CreateOriginAccessControl",
                "cloudfront:GetOriginAccessControl",
                "cloudfront:DeleteOriginAccessControl",
                "cloudfront:CreateInvalidation"
            ],
            "Resource": "*"
        }
    ]
}
```

> [!CAUTION]
> Esta política usa comodines (`*`) para simplificar el laboratorio. En entornos de producción reales, siempre debes restringir los recursos al ARN específico de tu distribución y buckets.


Recomendaciones:
- Crea un usuario o rol específico para CI y asigna esta política.
- Usa credenciales rotativas y evita claves de larga vida.
- Protege estas variables como "Protected" y "Masked" en GitLab CI/CD.
