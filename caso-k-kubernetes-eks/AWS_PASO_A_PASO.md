# 🪜 AWS Paso a Paso - Caso K: Despliegue de EKS Industrial

Este documento detalla el proceso técnico para levantar un clúster de **Kubernetes (EKS)** en AWS, desplegar la aplicación con diseño premium y realizar la limpieza de recursos.

---

## 📋 Requisitos Previos
1. **AWS CLI** configurado con permisos de Administrador.
2. **Terraform** instalado (v1.0+).
3. **kubectl** instalado (compatible con la versión 1.31 de K8s).
4. **Docker** instalado para la gestión de imágenes (opcional si usas imágenes existentes).

---

## 🖥️ Fase 1.5: Despliegue Manual Detallado (Consola Web AWS)

Si prefieres realizar el despliegue mediante clics para entender cada componente, sigue esta guía minuciosa:

### 1. Infraestructura de Red (VPC)
1.  Ve a **VPC Dashboard** -> Botón naranja **Create VPC**.
2.  Selecciona la opción **"VPC and more"** (genera automáticamente subredes y tablas de ruteo).
3.  **Name tag auto-generation**: Escribe `vladimir-eks`.
4.  **IPv4 CIDR block**: `10.0.0.0/16`.
5.  **Number of Availability Zones (AZs)**: **2** (para alta disponibilidad).
6.  **Number of Public subnets**: **2**.
7.  **Number of Private subnets**: **2** (Aquí es donde vivirán tus nodos EKS).
8.  **NAT Gateways**: Selecciona **1 per AZ**. 
    > [!IMPORTANT]
    > Esto permite que tus nodos en subredes privadas salgan a internet para descargar imágenes de contenedores. Tiene un costo asociado por hora.
9.  **VPC Endpoints**: Selecciona **None** para ahorrar costos adicionales.
10. Haz clic en **Create VPC** y espera a que el diagrama de flujo termine (aprox. 1 min).

### 2. Gestión de Identidad (IAM Roles)
Esta es la fase más crítica para la seguridad. Kubernetes en AWS funciona bajo un modelo de **responsabilidad compartida**, donde el clúster (plano de control) y los trabajadores (nodos) requieren permisos distintos para interactuar con la API de AWS.

#### A. Rol para el Plano de Control (EKS Cluster Role)
*   **Propósito**: Permite que el servicio administrado EKS cree y gestione recursos en tu nombre (como Load Balancers, interfaces de red y grupos de seguridad).
*   **Pasos Detallados**:
    1.  Ve a **IAM** -> **Roles** -> **Create role**.
    2.  **Trusted Entity**: Selecciona **AWS Service**.
    3.  **Use Case**: Busca **EKS** en la lista y selecciona **EKS - Cluster**. Esto configura automáticamente la "Trust Relationship" para que el servicio `eks.amazonaws.com` pueda asumir este rol.
    4.  **Permissions**: AWS adjuntará por defecto la política `AmazonEKSClusterPolicy`. Esta política otorga los permisos necesarios para que EKS gestione la infraestructura del clúster.
    5.  **Name**: `Vladimir-EKS-Cluster-Role`.

#### B. Rol para los Nodos (Worker Node Role)
*   **Propósito**: Permite que las instancias EC2 (los nodos) se unan al clúster y realicen tareas operativas.
*   **Políticas Requeridas (Explicación)**:
    - `AmazonEKSWorkerNodePolicy`: Permite a los nodos conectarse a la API de EKS.
    - `AmazonEKS_CNI_Policy`: Permite que el plugin de red de Kubernetes gestione las IPs de las interfaces de red (ENIs) en la VPC.
    - `AmazonEC2ContainerRegistryReadOnly`: Permite que los nodos descarguen (pull) tus imágenes de Docker desde ECR.
*   **Pasos Detallados**:
    1.  **IAM** -> **Roles** -> **Create role**.
    2.  **Trusted Entity**: Selecciona **AWS Service** -> **EC2**.
    3.  **Permissions**: Busca y marca manualmente las 3 políticas mencionadas arriba.
    4.  **Name**: `Vladimir-EKS-Node-Role`.

> [!TIP]
> Sin estos roles correctamente configurados, el clúster se quedará en estado "Pending" o los nodos nunca aparecerán como "Ready". 

### 3. Lanzamiento del Clúster EKS
1.  Ve a **EKS** -> **Clusters** -> **Add cluster** -> **Create**.
2.  **Name**: `vladimir-eks-cluster`. **Kubernetes version**: `1.31`.
3.  **Cluster service role**: Selecciona el `Vladimir-EKS-Cluster-Role` creado antes.
4.  **Networking**: 
    - **VPC**: Selecciona `vladimir-eks-vpc`.
    - **Subnets**: Asegúrate de que las 4 estén seleccionadas (2 públicas, 2 privadas).
    - **Cluster endpoint access**: **Public and private** (recomendado para facilidad de uso).
5.  Mantén el resto por defecto y haz clic en **Create**. (Toma entre 10 y 15 minutos).

### 4. Configuración del Grupo de Nodos (Cómputo)
1.  Una vez el clúster pase a estado **Active**, ve a la pestaña **Compute**.
2.  Haz clic en **Add node group**.
3.  **Name**: `vladimir-standard-nodes`.
4.  **Node IAM Role**: Selecciona `Vladimir-EKS-Node-Role`.
5.  **Node Group compute configuration**:
    - **AMI type**: Amazon Linux 2 (AL2_x86_64).
    - **Instance type**: `t3.medium`.
6.  **Node Group scaling configuration**:
    - **Minimum/Desired size**: `2`. **Maximum size**: `2`.
7.  **Node Group network configuration**: Asegúrate de que solo las **Private subnets** estén seleccionadas para máxima seguridad.
8.  Haz clic en **Create**.

---

## 🚨 Fase 4: Estrategia Maestra de Limpieza (FinOps)

**¡ORDEN CRÍTICO!** Si borras la VPC antes que el clúster, podrías dejar recursos "huérfanos" (como Load Balancers) que seguirán cobrando.

1.  **Cierre de Aplicación**: En tu terminal, ejecuta `kubectl delete -f caso-k-kubernetes-eks/deployment.yaml`. Esto eliminará el Load Balancer automáticamente.
2.  **Eliminar Node Group**: En la consola de EKS -> Pestaña Compute -> Selecciona el grupo de nodos y dale a **Delete**. Espera a que desaparezca.
3.  **Eliminar Clúster EKS**: Una vez los nodos ya no existan, pulsa **Delete** en la página principal del clúster. Confirmar escribiendo el nombre del clúster.
4.  **Eliminar VPC**: Ve al dashboard de VPC -> Selecciona `vladimir-eks-vpc` -> Acciones -> **Delete VPC**. 
    - AWS te confirmará que borrará subredes, NAT Gateways e IGWs asociados. Escribe `delete` para confirmar.
5.  **Auditoría de Residuos**: Ve a **EC2** -> **Load Balancers** y **Target Groups**. Asegúrate de que la lista esté vacía. Revisa también **EBS Volumes**; debería estar libre de discos creados por los nodos.

---

## 🔍 Resolución de Problemas Comunes
- **Error: "Unauthorized" al usar kubectl**: Revisa que tus credenciales de `aws configure` sean las mismas que crearon el clúster.
- **Pods en estado "Pending"**: Verifica que los nodos tengan recursos suficientes (`kubectl describe node`).
- **ELB no carga**: Los Load Balancers clásicos de AWS pueden tardar hasta 5 minutos en propagar el DNS.

---
*Guía técnica profesional para el portafolio de Vladimir Acuña.*
