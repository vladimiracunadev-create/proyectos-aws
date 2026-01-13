# Ejemplo de política IAM para despliegue a S3 y invalidación de CloudFront

A continuación hay un ejemplo de política JSON con **permisos mínimos** para que un usuario/rol pueda sincronizar contenido a un bucket S3 y crear invalidaciones en CloudFront (opcional).

**IMPORTANTE:** Reemplaza `arn:aws:s3:::tu-bucket` y `arn:aws:cloudfront::123456789012:distribution/XXXXXXXX` por tus recursos reales. Ajusta los `Resource` para limitar al mínimo necesario.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::tu-bucket"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject",
        "s3:PutObjectAcl"
      ],
      "Resource": [
        "arn:aws:s3:::tu-bucket/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "cloudfront:CreateInvalidation"
      ],
      "Resource": [
        "arn:aws:cloudfront::123456789012:distribution/XXXXXXXX"
      ]
    }
  ]
}
```

Recomendaciones:
- Crea un usuario o rol específico para CI y asigna esta política.
- Usa credenciales rotativas y evita claves de larga vida.
- Protege estas variables como "Protected" y "Masked" en GitLab CI/CD.
