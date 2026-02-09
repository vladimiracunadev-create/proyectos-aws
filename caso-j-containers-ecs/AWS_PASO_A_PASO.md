# 🚀 Despliegue en AWS ECS Fargate: Bitácora Completa de Comandos

Este documento registra **exactamente** los comandos y pasos realizados en la consola para desplegar exitosamente el Caso J, incluyendo la resolución de errores comunes encontrados durante el proceso.

## 1. Preparación del Entorno Local

### 1.1 Configuración de Credenciales AWS
Para permitir que Terraform y Docker interactúen con AWS, configuramos las credenciales del usuario IAM.

```powershell
aws configure
# AWS Access Key ID: [TU_ACCESS_KEY]
# AWS Secret Access Key: [TU_SECRET_KEY]
# Default region name: us-east-2
# Default output format: json
```

> **Nota:** Si encuentras errores de autorización (`UnauthorizedOperation`), asegúrate de que el usuario IAM tenga adjunta la política `AdministratorAccess` o permisos equivalentes en la consola de AWS.

### 1.2 Resolución de Dependencias (npm ci)
Intentamos construir la imagen Docker, pero falló el comando `npm ci` debido a la falta de `package-lock.json`.

**Error:**
`npm error The npm ci command can only install with an existing package-lock.json`

**Solución aplicada:**
Generamos el archivo de bloqueo localmente y lo subimos al repositorio.

```powershell
# En la carpeta caso-j-containers-ecs
npm install --package-lock-only
# (Si falla por políticas de PowerShell, usar: cmd /c "npm install --package-lock-only")

git add package-lock.json
git commit -m "fix(deps): generate package-lock.json for npm ci"
git push
```

## 2. Despliegue de Infraestructura (Terraform)

Creamos la red (VPC), el balanceador de carga (ALB), el clúster ECS y el repositorio ECR.

```powershell
cd terraform
terraform init
terraform apply -auto-approve
```

**Salida crítica (Outputs):**
Al finalizar, Terraform nos entregó dos valores clave:
*   `alb_dns_name`: `vladimir-case-j-alb-683413891.us-east-2.elb.amazonaws.com` (URL pública)
*   `ecr_repository_url`: `689978033715.dkr.ecr.us-east-2.amazonaws.com/vladimir-case-j-repo` (URL del registro)

## 3. Construcción y Publicación de la Imagen Docker

### 3.1 Autenticación en ECR
Docker necesita permiso para subir imágenes a tu cuenta AWS.

```powershell
# Obtiene el token de login y se lo pasa al cliente Docker
aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 689978033715.dkr.ecr.us-east-2.amazonaws.com
```

> **Error posible:** `push access denied` o `no basic auth credentials`.
> **Solución:** Ejecutar el comando de login de arriba. El token expira cada 12 horas.

### 3.2 Build, Tag & Push
Volvimos a la carpeta raíz del caso (donde está el `Dockerfile`) y ejecutamos:

```powershell
cd .. # Asegurarse de estar en caso-j-containers-ecs/

# 1. Construir la imagen localmente
docker build -t vladimir-case-j-repo .

# 2. Etiquetar la imagen con la URL del repositorio remoto
docker tag vladimir-case-j-repo:latest 689978033715.dkr.ecr.us-east-2.amazonaws.com/vladimir-case-j-repo:latest

# 3. Subir la imagen a AWS ECR
docker push 689978033715.dkr.ecr.us-east-2.amazonaws.com/vladimir-case-j-repo:latest
```

## 4. Actualización del Servicio ECS

Una vez que la imagen estuvo en ECR, forzamos al servicio ECS a actualizarse para descargar la nueva versión.

```powershell
aws ecs update-service --cluster vladimir-case-j-cluster --service vladimir-case-j-service --force-new-deployment --region us-east-2
```

## 5. Validación Final

Esperamos unos minutos a que Fargate provisionara la tarea y accedimos a la URL del ALB:

🔗 **[http://vladimir-case-j-alb-683413891.us-east-2.elb.amazonaws.com](http://vladimir-case-j-alb-683413891.us-east-2.elb.amazonaws.com)**

La aplicación respondió correctamente, confirmando el despliegue exitoso.
