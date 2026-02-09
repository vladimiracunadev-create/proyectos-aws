# ☁️ Guía Paso a Paso: Despliegue en AWS (Caso J)

Esta guía te llevará de 0 a 100 para desplegar tu aplicación en un entorno profesional de contenedores usando **Amazon ECS (Fargate)** y **Terraform**.

---

## 🛠️ 1. Prerrequisitos

Asegúrate de tener en tu terminal:
1.  **AWS CLI** configurado: `aws configure` (con tus credenciales).
2.  **Terraform** instalado: `terraform version`.
3.  **Docker** corriendo: `docker ps`.

---

## 🚀 2. Flujo de Trabajo (Automatizado con Make)

Hemos creado comandos simples en el `Makefile` de la raíz para que no tengas que memorizar comandos largos.

### Paso A: Crear la Infraestructura (El "Cascarón")
Primero necesitamos crear el registro de imágenes (ECR), el clúster y el balanceador de carga.

Ejecuta desde la raíz del repositorio:

```bash
# 1. Inicializar Terraform (descarga plugins)
make case-j-init

# 2. Crear los recursos en AWS
make case-j-apply
```
*(Escribe `yes` cuando se te pida confirmar).*

> **¿Qué acaba de pasar?**
> Terraform creó:
> *   Un repositorio **ECR** privado para tus imágenes.
> *   Un **ALB (Load Balancer)** público para recibir internet.
> *   Un **Cluster ECS Fargate** listo para correr contenedores.

---

### Paso B: Construir y Subir tu Aplicación
Ahora que la infraestructura existe, subimos tu código como una imagen Docker.

```bash
# 3. Autenticarse en ECR (usa tus credenciales de AWS locales)
make docker-login

# 4. Construir y Subir la imagen
make docker-push
```

> **¿Qué acaba de pasar?**
> *   Se construyó `vladimir-api:latest`.
> *   Se etiquetó con la URL de tu repositorio ECR.
> *   Se subió a la nube de AWS.

---

### Paso C: Actualizar el Servicio (Opcional la primera vez)
Si es la primera vez, el servicio de ECS esperará a que la imagen exista. Si ya habías desplegado y solo subiste una nueva versión del código, a veces es necesario forzar un nuevo despliegue:

```bash
make case-j-apply
```
*(Esto refresca el estado y asegura que el servicio esté corriendo con la configuración deseada).*

---

## 👀 3. Verificación y Uso

Tu aplicación ya debería estar corriendo detrás del Balanceador de Carga.

**Obtener la URL:**
```bash
cd caso-j-containers-ecs/terraform && terraform output alb_dns_name
```

Copia esa dirección (ej: `vladimir-case-j-alb-12345.us-east-2.elb.amazonaws.com`) y pégala en tu navegador. 
¡Deberías ver el mensaje de "Hola Vladimir"!

---

## 🧹 4. Limpieza (IMPORTANTE)

Los recursos de este laboratorio (ALB y Fargate) **cuestan dinero** si los dejas encendidos. Cuando termines tu sesión de estudio:

```bash
make case-j-destroy
```
*(Confirma con `yes`).*

Esto eliminará el Balanceador, el Clúster y el Repositorio, deteniendo cualquier costo.
