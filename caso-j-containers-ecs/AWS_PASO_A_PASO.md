# 🚀 Despliegue en AWS ECS Fargate (Paso a Paso)

Este documento detalla el proceso validado para construir, publicar y desplegar la aplicación en AWS ECS usando Terraform y Docker.

## 📋 Prerequisitos

Antes de comenzar, asegúrate de tener configurado tu entorno:

1.  **AWS CLI configurado**:
    Ejecuta `aws configure` e introduce tus credenciales (Access Key, Secret Key, Región `us-east-2`).
2.  **Permisos IAM**:
    El usuario debe tener permisos suficientes (ej. `AdministratorAccess` o `PowerUserAccess` + IAMFullAccess) para gestionar VPCs, ECS, ECR y IAM Roles.

## 🛠️ 1. Infraestructura como Código (Terraform)

Desplegamos la infraestructura base (VPC, ALB, Cluster ECS, Repositorio ECR).

```powershell
cd terraform
terraform init
terraform apply -auto-approve
```

> **Nota:** Al finalizar, Terraform mostrará los `Outputs` importantes:
>
> *   `alb_dns_name`: URL pública de la aplicación.
> *   `ecr_repository_url`: URL del repositorio de imágenes Docker.

## 🐳 2. Construcción y Publicación de la Imagen Docker

Una vez creada la infraestructura, debemos subir nuestra aplicación al registro (ECR).

1.  **Autenticarse en ECR:**
    ```powershell
    aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin <TU_CUENTA_ID>.dkr.ecr.us-east-2.amazonaws.com
    ```
    *(Reemplaza `<TU_CUENTA_ID>` con tu ID de cuenta AWS, ej: `689978033715`)*

2.  **Construir la imagen:**
    Asegúrate de estar en la raíz de la carpeta `caso-j-containers-ecs`.
    ```powershell
    docker build -t vladimir-case-j-repo .
    ```

3.  **Etiquetar la imagen:**
    ```powershell
    docker tag vladimir-case-j-repo:latest <ECR_REPOSITORY_URL>:latest
    ```

4.  **Subir la imagen (Push):**
    ```powershell
    docker push <ECR_REPOSITORY_URL>:latest
    ```

## 🔄 3. Actualizar el Servicio ECS

Si el servicio ya estaba corriendo (pero fallando por falta de imagen), forzamos una nueva actualización para que descargue la imagen recién subida:

```powershell
aws ecs update-service --cluster vladimir-case-j-cluster --service vladimir-case-j-service --force-new-deployment --region us-east-2
```

## ✅ 4. Verificación

Espera unos minutos a que el servicio se estabilice (estado RUNNING). Luego accede a la URL del ALB:

👉 **[http://vladimir-case-j-alb-683413891.us-east-2.elb.amazonaws.com](http://vladimir-case-j-alb-683413891.us-east-2.elb.amazonaws.com)**

---

## 🐛 Solución de Problemas Comunes

*   **Error `npm ci` en Docker build:**
    *   Causa: Falta de `package-lock.json`.
    *   Solución: Generarlo localmente con `npm install --package-lock-only` y subirlo al repo.
*   **Error `UnauthorizedOperation` en Terraform:**
    *   Causa: Usuario IAM sin permisos.
    *   Solución: Adjuntar política `AdministratorAccess` al usuario en consola AWS.
*   **Error `push access denied`:**
    *   Causa: Token de autenticación de Docker expirado o inexistente.
    *   Solución: Volver a ejecutar el comando `aws ecr get-login-password | docker login ...`.
