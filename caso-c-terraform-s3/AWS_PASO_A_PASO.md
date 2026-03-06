# ☁️ Guía Paso a Paso: Infraestructura como Código (Caso C)

Este caso profesionaliza el alojamiento estático usando **Terraform** para crear toda la infraestructura (S3 + CloudFront + OAC) de forma automática y segura. ¡Adiós a la configuración manual!

---

## 🛠️ 1. Prerrequisitos

1.  **AWS CLI** configurado (`aws configure`).
2.  **Terraform** instalado (`terraform version`).

---

## 🚀 2. Flujo de Trabajo (Make + Terraform)

### Paso A: Inicializar e Instalar
Primero, Terraform necesita descargar los "drivers" para hablar con AWS.

```bash
make tf-init
```

### Paso B: Planificar (Preview)
Antes de crear nada, visualiza qué cambios se harán. Esto es una buena práctica.

```bash
make tf-plan
```

### Paso C: Aplicar (Crear Infraestructura)
Ahora sí, construye la nube. Terraform creará el Bucket S3, la distribución de CloudFront (CDN) y configurará los permisos bloqueando el acceso directo al bucket (OAC - Origin Access Control).

```bash
make tf-apply
```
*(Escribe `yes` para confirmar)*.

> **Toma un café ☕**: CloudFront tarda entre 3 y 5 minutos en crearse/actualizarse por primera vez.

---

Al terminar `tf-apply`, Terraform te mostrará outputs importantes, incluyendo la URL de tu distribución CloudFront (`d1234abcd.cloudfront.net`).

Si te la perdiste, recupérala con:
```bash
cd caso-c-terraform-s3 && terraform output
```

Visita esa URL. ¡Tu sitio está alojado en una CDN global con HTTPS gratis!

---

## 🔐 4. Seguridad y Auditoría

Este caso incluye **tfsec** para auditoría estática. Si ejecutas `make tf-security`, verás que algunos hallazgos (WAF, KMS, Logging) están omitidos mediante `#tfsec:ignore`. 
- **¿Por qué?**: En este entorno demo, priorizamos la eficiencia de costos. 
- **Automatización**: El pipeline de GitLab no permitirá el despliegue si `tfsec` detecta errores no documentados/ignorados.

---

## 🧹 5. Limpieza (Destruir)

Terraform lleva un registro de todo lo que creó, así que puede destruirlo con precisión quirúrgica.

```bash
make tf-destroy
```
*(Confirma con `yes`).*

Esto eliminará el Bucket y la Distribución, limpiando tu cuenta.
