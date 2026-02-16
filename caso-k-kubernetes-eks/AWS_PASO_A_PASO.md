# 🪜 AWS Paso a Paso - Caso K: Despliegue de EKS Industrial

Este documento detalla el proceso técnico para levantar un clúster de **Kubernetes (EKS)** en AWS, desplegar la aplicación con diseño premium y realizar la limpieza de recursos.

---

## 📋 Requisitos Previos
1. **AWS CLI** configurado con permisos de Administrador.
2. **Terraform** instalado (v1.0+).
3. **kubectl** instalado (compatible con la versión 1.31 o 1.32 de K8s).
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
*   **Propósito**: Permite que el servicio administrado EKS gestione recursos en tu nombre. En las versiones modernas (1.31+), si utilizas **EKS Auto Mode**, el clúster toma el control total de cómputo, red y almacenamiento, por lo que requiere permisos extra.
*   **Pasos Detallados**:
    1.  Ve a **IAM** -> **Roles** -> **Create role**.
    2.  **Trusted Entity**: AWS Service. **Use Case**: EKS - Cluster.
    3.  **Permisos (Crucial para Modo Automático)**: Debes adjuntar las siguientes **5 políticas**:
        - `AmazonEKSClusterPolicy` (La estándar).
        - `AmazonEKSBlockStoragePolicy` (Para gestionar discos EBS).
        - `AmazonEKSComputePolicy` (Para gestionar nodos automáticos).
        - `AmazonEKSLoadBalancingPolicy` (Para gestionar el tráfico).
        - `AmazonEKSNetworkingPolicy` (Para gestionar la red).
    4.  **Configuración de Confianza (Trust Policy)**: 
        Al finalizar la creación, debes editar la pestaña **Trust relationships** y asegurarte de que incluya la acción `"sts:TagSession"`.
        ```json
        {
          "Version": "2012-10-17",
          "Statement": [
            {
              "Effect": "Allow",
              "Principal": { "Service": "eks.amazonaws.com" },
              "Action": [ "sts:AssumeRole", "sts:TagSession" ]
            }
          ]
        }
        ```
    5.  **Name**: `Vladimir-EKS-Cluster-Role`.

#### B. Rol para los Nodos (Worker Node Role)
*   **¿Por qué es necesario?**: A diferencia de una instancia EC2 normal, un nodo de EKS necesita "hablar" con el clúster para recibir instrucciones y con otros servicios de AWS para funcionar.
*   **Anatomía del Rol**:
    - **Trusted Entity**: Debe ser **EC2** (`ec2.amazonaws.com`). Esto permite que las máquinas virtuales "asuman" la identidad del rol.
    - **Políticas (El Tridente de Permisos)**:
        1. `AmazonEKSWorkerNodePolicy`: El "DNI" del nodo. Sin esto, el nodo no puede registrarse en el clúster.
        2. `AmazonEKS_CNI_Policy`: El "Cerebro de Red". Permite que los Pods tengan IPs reales de tu VPC. Si falla, los Pods no tendrán internet ni comunicación entre ellos.
        3. `AmazonEC2ContainerRegistryReadOnly`: El "Pasaporte de Imágenes". Permite bajar el código de tu aplicación desde los repositorios de Amazon (ECR).
*   **Nombre Sugerido**: `Vladimir-EKS-Node-Role`.

> [!IMPORTANT]
> **Relación de Confianza (Trust Relationship)**: Al crear el rol, AWS te preguntará por el servicio. Asegúrate de elegir **EC2** para los nodos y **EKS** para el clúster. Si los cruzas, nada funcionará y recibirás errores de "Unauthorized".

> [!TIP]
> Sin estos roles correctamente configurados, el clúster se quedará en estado "Pending" o los nodos nunca aparecerán como "Ready". 

### 3. Lanzamiento del Clúster EKS
1.  Ve a **EKS** -> **Clusters** -> **Add cluster** -> **Create**.
2.  **Name**: `vladimir-eks-cluster`. **Kubernetes version**: `1.32`.
3.  **Cluster service role**: Selecciona el `Vladimir-EKS-Cluster-Role` creado antes.
4.  **Networking**: 
    - **VPC**: Selecciona `vladimir-eks-vpc`.
    - **Subnets**: Asegúrate de que las 4 estén seleccionadas (2 públicas, 2 privadas).
    - **Cluster endpoint access**: **Public and private** (recomendado para facilidad de uso).
5.  Mantén el resto por defecto y haz clic en **Create**. (Toma entre 10 y 15 minutos).

### 4. Configuración de Cómputo (Nodos)
> [!IMPORTANT]
> **Si usas EKS Auto Mode (Recomendado)**: No necesitas buscar la pestaña "Compute" ni añadir un "Node Group" manualmente. AWS creará los nodos automáticamente cuando despliegues la aplicación en la Fase 2. Puedes saltar al siguiente paso.

**Si usas Modo Estándar**:
1.  Una vez el clúster pase a estado **Active**, ve a la pestaña **Compute**.
2.  Haz clic en **Add node group**.
3.  **Name**: `vladimir-standard-nodes`. **Node IAM Role**: `Vladimir-EKS-Node-Role`.
4.  **Instance type**: `t3.medium`. **Scaling**: 2 nodos.
5.  Haz clic en **Create**.

---

## 🚀 Fase 2: Conexión y Despliegue de Aplicación

Una vez el clúster y los nodos estén **Active**, es momento de desplegar el código.

### 1. Configurar Acceso Local (Kubeconfig)
Debes "decirle" a tu terminal cómo hablar con el nuevo clúster de AWS:
```bash
aws eks update-kubeconfig --region us-east-2 --name vladimir-eks-cluster
```
*   **Verificación**: Ejecuta `kubectl get nodes`. Deberías ver tus 2 nodos en estado `Ready`.

### 2. Despliegue de Manifiestos
Aplica la configuración de Kubernetes que define la aplicación, el diseño premium y el balanceador de carga:
1.  Asegúrate de estar en la raíz de la carpeta del proyecto.
2.  Ejecuta:
    ```bash
    kubectl apply -f deployment.yaml
    ```
3.  **Verificación de Pods**:
    ```bash
    kubectl get pods
    ```
    Espera a que las 3 réplicas digan `Running`.

---

## 🌐 Fase 3: Acceso y Verificación Final

### 1. Obtener URL de la Aplicación
Kubernetes solicitará a AWS un **Load Balancer** automáticamente. Para encontrar su dirección:
```bash
kubectl get service vladimir-app-service
```
*   Busca la columna **EXTERNAL-IP**. Verás una dirección larga terminada en `.elb.amazonaws.com`.
*   Copia esa dirección y pégala en tu navegador para ver el dashboard premium.

### 2. Prueba de Resiliencia (Self-Healing)
Para demostrar que el despliegue es industrial, borra un pod manualmente y mira cómo Kubernetes lo recrea:
1.  `kubectl delete pod <nombre-de-un-pod>`
2.  `kubectl get pods` -> Verás que hay uno nuevo creándose automáticamente para mantener las 3 réplicas.

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
