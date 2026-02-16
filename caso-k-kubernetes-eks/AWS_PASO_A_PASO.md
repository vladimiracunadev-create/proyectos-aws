# 🪜 AWS Paso a Paso - Caso K: Despliegue de EKS Industrial

Este documento detalla el proceso técnico para levantar un clúster de **Kubernetes (EKS)** en AWS, desplegar la aplicación con diseño premium y realizar la limpieza de recursos.

---

## 📋 Requisitos Previos
1. **AWS CLI** configurado con permisos de Administrador.
2. **Terraform** instalado (v1.0+).
3. **kubectl** instalado (compatible con la versión 1.27 de K8s).
4. **Docker** instalado para la gestión de imágenes (opcional si usas imágenes existentes).

---

---

## 🖥️ Fase 1.5: Despliegue Manual (Consola Web AWS)

Si prefieres no usar CLI/Terraform, sigue estos pasos precisos:

### 1. Red (VPC)
- Ve a **VPC Dashboard** -> **Create VPC**.
- Selecciona **"VPC and more"**.
- Configura: 2 AZs, 2 Public Subnets, 2 Private Subnets.
- NAT Gateways: **1 per AZ** (necesario para nodos).
- Clic en **Create VPC**.

### 2. Identidad (IAM Roles)
- **EKS Cluster Role**: Crea un rol para EKS con `AmazonEKSClusterPolicy`.
- **EKS Node Role**: Crea un rol para EC2 con `AmazonEKSWorkerNodePolicy`, `AmazonEKS_CNI_Policy` y `AmazonEC2ContainerRegistryReadOnly`.

### 3. Clúster y Cómputo
- **Clúster**: Crea el clúster en la VPC previa, seleccionando el Cluster Role.
- **Node Group**: En la pestaña **Compute**, añade un grupo de nodos con el Node Role, tipo `t3.medium`, y escalado 1-2.

---

## 🚨 Fase 4: Limpieza y FinOps (Crítico)

**¡ATENCIÓN!** Para evitar cargos de ~$72 USD mensuales, debes destruir los recursos en este orden exacto:

1. **Eliminar Node Group**: Ve a la pestaña Compute del clúster y borra el grupo de nodos primero.
2. **Eliminar Clúster EKS**: Una vez los nodos se hayan eliminado, borra el clúster.
3. **Eliminar VPC**: Borra la VPC `vladimir-eks`. Esto eliminará el NAT Gateway (que tiene costo por hora) y las subnets.
4. **Verificación Final**: Revisa que no queden volúmenes EBS ni Load Balancers activos en EC2.

---

## 🔍 Resolución de Problemas Comunes
- **Error: "Unauthorized" al usar kubectl**: Revisa que tus credenciales de `aws configure` sean las mismas que crearon el clúster.
- **Pods en estado "Pending"**: Verifica que los nodos tengan recursos suficientes (`kubectl describe node`).
- **ELB no carga**: Los Load Balancers clásicos de AWS pueden tardar hasta 5 minutos en propagar el DNS.

---
*Guía técnica profesional para el portafolio de Vladimir Acuña.*
