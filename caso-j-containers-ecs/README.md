# 🐳 Caso J: Dockerización (Empaquetado Industrial)

[![Nivel-9](https://img.shields.io/badge/Nivel-9_Contenedores-blue?style=for-the-badge)]()
[![Status](https://img.shields.io/badge/Status-Nuevo-blue?style=for-the-badge)]()

Empaquetar aplicaciones es el estándar de la industria moderna. Este caso demuestra cómo crear un entorno aislado y reproducible que corre igual en tu PC que en AWS ECS/Fargate.

---

## 🎯 Objetivo
Portabilidad absoluta. Aprenderás a escribir Dockerfiles eficientes, gestionar registros de imágenes (**ECR**) y desplegar servicios que pueden escalar de forma masiva.

## 🛠️ Stack Tecnológico
- **Docker**: Motor de contenedores.
- **Amazon ECR**: Almacén privado de imágenes.
- **Amazon ECS**: Orquestador serverless (Fargate).

## 🚀 Uso rápido
```bash
make docker-build  # Construye la imagen localmente
```

## ☁️ Despliegue en AWS (Terraform)

Este caso incluye una configuración completa de Terraform para desplegar en ECS Fargate con Load Balancer.

### Prerrequisitos
- AWS CLI configurado (`aws configure`)
- Terraform instalado

### Comandos Disponibles
Simplemente ejecuta desde la raíz del proyecto:

1. **Inicializar Infraestructura**:
   ```bash
   make case-j-init
   ```

2. **Crear Recursos (ECR, ECS, ALB)**:
   ```bash
   make case-j-apply
   ```

3. **Subir Imagen a ECR**:
   (Solo funciona después de aplicar la infraestructura, ya que necesita la URL del repo)
   ```bash
   make docker-login
   make docker-push
   ```

4. **Verificar**:
   Obtén la URL del balanceador de carga:
   ```bash
   cd caso-j-containers-ecs/terraform && terraform output alb_dns_name
   ```

5. **Destruir Todo**:
   ¡Importante para evitar costos!
   ```bash
   make case-j-destroy
   ```


## 🔗 Enlaces Relacionados
- ⬅️ **[Regresar al Roadmap Principal](../README.md)**
- 🚀 **[Guía de Instalación](../docs/INSTALL.md)**
