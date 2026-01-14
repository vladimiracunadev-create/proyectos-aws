# Caso C: Infraestructura como Código (Terraform) 🏗️

> **Nivel 2**: Profesionalización

## Objetivo
Dejar atrás la gestión manual ("ClickOps") y definir toda la infraestructura de AWS mediante código. Esto permite reproducibilidad, versionado y auditoría.

## Stack Tecnológico
- **Terraform** (o OpenTofu)
- **AWS S3** (Almacenamiento Web)
- **AWS CloudFront** (CDN y HTTPS)
- **AWS ACM** (Certificados SSL)

## Estructura
```
caso-c-terraform-s3/
├── main.tf        # Definición principal de recursos
├── variables.tf   # Variables configurables (nombre bucket, región)
├── outputs.tf     # Outputs (URL de CloudFront)
└── public/        # Código web (html/css/js)
```

## Instrucciones (Próximamente)
1. Instalar Terraform.
2. Configurar credenciales AWS.
3. Ejecutar `terraform init` y `terraform apply`.
