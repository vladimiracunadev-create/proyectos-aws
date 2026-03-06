# 🏗️ Caso C: Terraform + CloudFront (Infraestructura como Código)

[![Nivel-2](https://img.shields.io/badge/Nivel-2_Profesionalizaci%C3%B3n-blueviolet?style=for-the-badge)](https://gitlab.com/vladimir.acuna.dev-group/proyectos-aws-gitlab)
[![Status](https://img.shields.io/badge/Status-Deployed-success?style=for-the-badge)](https://d3otfpeykrm536.cloudfront.net/)
[![IaC](https://img.shields.io/badge/IaC-Terraform_1.14-844FBA?style=for-the-badge&logo=terraform)](https://www.terraform.io/)
[![tfsec](https://img.shields.io/badge/tfsec-Passing-brightgreen?style=for-the-badge)](./docs/architecture.md)

Este caso representa el estándar industrial de despliegue: la infraestructura de AWS **no se crea con clics**, sino que se define en código con **Terraform**, se audita con **tfsec** y se despliega automáticamente en **GitLab CI/CD**.

---

## 🎯 Objetivo

Eliminar el error humano mediante **Infraestructura como Código (IaC)**. Garantizar que el entorno sea 100% reproducible y auditable, usando estado remoto y una CDN global con S3 privado + OAC.

---

## 🧩 Componentes del Stack

| Componente | Tecnología | Rol |
|---|---|---|
| **IaC** | Terraform 1.14 | Orquesta toda la infraestructura |
| **Almacenamiento** | AWS S3 (privado) | Aloja los archivos de la web |
| **CDN** | AWS CloudFront | HTTPS global, cache en 400+ edge locations |
| **Seguridad acceso** | Origin Access Control (OAC) | Solo CloudFront puede leer S3 (SigV4) |
| **Estado remoto** | S3 + DynamoDB Lock | Estado compartido con bloqueo anti-race conditions |
| **Análisis IaC** | tfsec v1.28.1 | Análisis de misconfigurations en Terraform |

---

## 🔄 Pipeline de CI/CD (4 stages)

```
security          → plan-infrastructure  → deploy (×2 jobs)
──────────────      ─────────────────────  ──────────────────────────────────
scan_infrastructure  plan_case_c            deploy_case_c → invalidate_cloudfront_c
(tfsec)              (tf plan -out tfplan)  (tf apply)       (aws cloudfront invalidation)
```

### ⚠️ Variable CI/CD requerida

El job `invalidate_cloudfront_c` requiere esta variable configurada en **GitLab → Settings → CI/CD → Variables**:

| Variable | Valor actual | Descripción |
|---|---|---|
| `CLOUDFRONT_DISTRIBUTION_ID_C` | `EPLVRZI6H1QQM` | ID de la distribución CloudFront del Caso C |

---

## 🔐 Seguridad: Hallazgos tfsec y Decisiones

tfsec detecta 5 potenciales hallazgos. Todos están **intencionalmente ignorados** con `#tfsec:ignore` comentados directamente en el código, ya que son overkill para un proyecto de portafolio:

| Hallazgo | Severidad | Justificación del ignore |
|---|---|---|
| `aws-cloudfront-enable-waf` | HIGH | WAF cuesta ~$5/mes mínimo |
| `aws-cloudfront-use-secure-tls-policy` | HIGH | Requiere dominio propio + certificado ACM |
| `aws-s3-encryption-customer-key` | HIGH | KMS añade costo y complejidad para demo |
| `aws-cloudfront-enable-logging` | MEDIUM | Requiere bucket S3 adicional con permisos especiales |
| `aws-s3-enable-bucket-logging` | MEDIUM | Idem — requiere bucket adicional |

> En un entorno de **producción real**, todos estos controles deberían estar activos.

---

## 🛠️ Comandos de Gestión Local

```bash
make tf-init      # Conecta con el estado remoto en S3 (Ohio)
make tf-plan      # Preview de cambios: qué se va a crear/modificar/destruir
make tf-apply     # Despliega (pide confirmación)
make tf-security  # Ejecuta tfsec localmente
make tf-destroy   # Destruye toda la infraestructura de este caso
```

---

## 🔗 Enlaces Relacionados

- ⬅️ **[Regresar al Roadmap Principal](../README.md)**
- 🏗️ **[Arquitectura Detallada (Mermaid)](./docs/architecture.md)**
- 🛡️ **[Seguridad IAM](../docs/IAM_SECURITY.md)**
- 🚀 **[Guía de Instalación](../docs/INSTALL.md)**
- ☁️ **[Guía Paso a Paso AWS](./AWS_PASO_A_PASO.md)**
- 🧪 **[Demo en Vivo](https://d3otfpeykrm536.cloudfront.net/)**
