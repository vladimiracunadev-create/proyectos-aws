# 🪜 AWS Paso a Paso - **Estado**: ¡100% OPERATIVO! ✅
- **URL**: [k8s-default-vladimir-fd9bd8dc79-d4392d3db0728cc7.elb.us-east-1.amazonaws.com](http://k8s-default-vladimir-fd9bd8dc79-d4392d3db0728cc7.elb.us-east-1.amazonaws.com)
- **Región**: `us-east-1` (N. Virginia).

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

### 3.1. Configurar Acceso al Clúster (Access Entries) - ¡PASO OBLIGATORIO!
Kubernetes rechaza a cualquier usuario que no sea el "dueño" original del clúster. Como tu terminal usa el usuario `terraform-user`, debemos darle permisos administrativos en la consola:
1.  En la consola de EKS, entra en tu clúster **vladimir-eks-cluster**.
2.  Haz clic en la pestaña **"Acceso" (Access)**.
3.  En la sección **Access entries**, haz clic en el botón naranja **Create access entry**.
4.  **IAM user or role ARN**: Pega `arn:aws:iam::689978033715:user/terraform-user`.
5.  Haz clic en **Next**.
6.  En **Add access policy**, haz clic en el botón **Add policy**.
7.  En el desplegable, selecciona: **AmazonEKSClusterAdminPolicy**.
8.  **Access scope**: Déjalo como **Cluster**.
9.  Haz clic en **Add policy**, luego en **Next** y finalmente en **Create**.
> [!IMPORTANT]
> Una vez creada la entrada de acceso, tu terminal ya tendrá "superpoderes" para desplegar la aplicación sin errores de credenciales.

### 4. Configuración de Cómputo (Nodos)

Existen dos maneras de manejar el cómputo en EKS. Dependiendo de lo que hayas visto al crear el clúster, elige tu camino:

#### 🟢 Opción A: EKS Auto Mode (El más sencillo y recomendado)
Si al crear el clúster seleccionaste o te apareció por defecto el **Auto Mode**, no verás opciones de "Node Groups" tradicionales.
*   **Acción**: ¡No necesitas buscar ninguna pestaña ni crear nada manualmente! 
*   **Concepto**: EKS gestiona el cómputo como un recurso "serverless". Los nodos aparecerán mágicamente en la pestaña **"Recursos" (Resources)** o **"Nodos" (Nodes)** una vez que despliegues la aplicación en la Fase 2.
*   **Siguiente paso**: Salta directamente a la **Fase 2**.

#### 🟡 Opción B: Modo Estándar (Manual)
Si prefieres el control manual o no usas Auto Mode, sigue estos clics minuciosos:
1.  En la página de tu clúster, haz clic en la pestaña **"Informática" (Compute)**.
2.  Desplázate hacia abajo hasta encontrar **Managed Node Groups** y haz clic en **Add node group**.
3.  **Configuración de Identidad**:
    - **Name**: `vladimir-standard-nodes`.
    - **Node IAM Role**: Selecciona el `Vladimir-EKS-Node-Role` (que creamos en la Fase 1).
4.  **Configuración de Cómputo (Compute Configuration)**:
    - **Tipo de AMI**: Selecciona **Amazon Linux 2023 (AL2023_x86_64_STANDARD)**. Es la versión más moderna y eficiente.
    - **Tipo de capacidad**: On-Demand (Bajo demanda).
    - **Tipos de instancias**: Selecciona **t3.medium** (es el mínimo recomendado para que el clúster no se sature).
    - **Tamaño del disco**: Ingresa **20 GiB** (suficiente para el laboratorio).
5.  **Configuración de Escalado (Scaling Configuration)**:
    - **Minimum size**: 2. **Maximum size**: 2. **Desired size**: 2.
6.  **Red (Networking)**:
    - Asegúrate de que solo las **subredes privadas** estén seleccionadas para mayor seguridad.
7.  Haz clic en **Create**. Los nodos tardarán unos 5 minutos en estar listos (**Ready**).

---

## 🚀 Fase 2: Conexión y Despliegue de Aplicación

Una vez el clúster y los nodos estén **Active**, es momento de desplegar el código.

### 1. Configurar Acceso Local (Kubeconfig)
Debes "decirle" a tu terminal cómo hablar con el nuevo clúster de AWS:
```bash
aws eks update-kubeconfig --region us-east-1 --name vladimir-eks-cluster
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
5.  **Verificación Final**:
    ```bash
    kubectl get service vladimir-app-service
    ```
    - Copia el **EXTERNAL-IP** (DNS de AWS).
    - ¡Pégalo en tu navegador y disfruta de tu app operativa! 🚀

### 2. Prueba de Resiliencia (Self-Healing)
Para demostrar que el despliegue es industrial, borra un pod manualmente y mira cómo Kubernetes lo recrea:
1.  `kubectl delete pod <nombre-de-un-pod>`
2.  `kubectl get pods` -> Verás que hay uno nuevo creándose automáticamente para mantener las 3 réplicas.

---

## 🧹 Limpieza Final (Estrategia FinOps) - ¡DINERO REAL! 💰🔥
Para evitar cargos innecesarios, sigue este orden EXACTO de eliminación. Si saltas un paso, AWS podría bloquear la eliminación de los siguientes recursos.

### 🪜 Paso a Paso para "Matar" todo:

1.  **Eliminar Balanceador (Servicio K8s)**:
    - En tu terminal: `kubectl delete service vladimir-app-service`.
    - *Esto elimina el recurso que genera cobro por tráfico.*

2.  **Eliminar Nodos de Cómputo**:
    - Ve a **EKS** -> **Clusters** -> `vladimir-eks-cluster` -> Pestaña **"Informática" (Compute)**.
    - Selecciona el **Node Group** y dale a **Delete**.
    - Espera a que los nodos desaparezcan antes de seguir.

3.  **Eliminar Clúster EKS**:
    - Ve a la lista de clústeres, selecciona `vladimir-eks-cluster` y dale a **Delete**.
    - (Toma ~5-10 minutos).

4.  **Eliminar Red (VPC)**:
    - Ve a la consola de **VPC**.
    - Selecciona `vladimir-eks-vpc` (VPC ID real).
    - **Actions** -> **Delete VPC**.
    - Esto borrará automáticamente: Subredes, NAT Gateways e Internet Gateways.

5.  **Bonus**: Elimina la VPC duplicada si aún existe para mayor limpieza.

---

## 🔍 Resolución de Problemas Comunes
- **Error: "ErrImagePull" o "ImagePullBackOff"**: 
  - Esto ocurre porque el clúster no encuentra la imagen en el registro público.
  - **Solución**: Debes construir y subir la imagen a tu Docker Hub:
    ```bash
    # 1. Entra a la carpeta de la app
    cd caso-k-kubernetes-eks/app
    # 2. Construye la imagen (reemplaza 'vladimiracunadev' con tu usuario)
    docker build -t vladimiracunadev/vladimir-eks-app:latest .
    # 3. Sube la imagen
    docker push vladimiracunadev/vladimir-eks-app:latest
    ```
- **Error: "push access denied" en Docker**:
  - Significa que no estás autenticado en tu terminal o el nombre de usuario es incorrecto.
  - **Solución**:
    1. Ejecuta `docker login` e ingresa tus credenciales de Docker Hub.
    2. Asegúrate de que el prefijo `vladimiracunadev/` coincida con tu **Docker ID**. Si tu usuario es distinto, debes cambiarlo en el comando `docker build` y también en el archivo `deployment.yaml`.
- **Error: "Failed build model... unable to resolve at least one subnet"**:
  - AWS no sabe cuáles de tus subredes son públicas para poner el Balanceador.
  - **Solución (Tags en VPC)**: 
    > [!IMPORTANT]
    > **Verifica tu VPC ID**: Como tienes dos VPCs con el mismo nombre, ve a la consola de **EKS** -> **Clusters** -> **vladimir-eks-cluster** -> Pestaña **Networking**. Copia el **VPC ID** (ej: `vpc-0a1b2c...`).
    1. Ve a la consola de **VPC** -> **Subnets**.
    2. Asegúrate de filtrar las subredes que pertenezcan EXCLUSIVAMENTE a ese **VPC ID** detectado en el paso anterior.
    3. Selecciona tus **2 Subredes Públicas** de ESA VPC.
    3. Ve a la pestaña **Tags** -> **Manage tags**.
    4. Añade el siguiente tag exactamente:
       - **Key**: `kubernetes.io/role/elb`
       - **Value**: `1`
    5. Selecciona tus **2 Subredes Privadas** y añade el tag:
       - **Key**: `kubernetes.io/role/internal-elb`
       - **Value**: `1`
  - Tras esto, el Load Balancer se creará en menos de 1 minuto.
- **External-IP: <pending>**: Es normal. AWS tarda de 2 a 5 minutos en aprovisionar el Load Balancer físico. Vuelve a ejecutar `kubectl get svc` en un momento.
- **Pods en estado "Pending"**: Verifica que los nodos tengan recursos suficientes (`kubectl describe node`).
- **ELB no carga**: Los Load Balancers clásicos de AWS pueden tardar hasta 5 minutos en propagar el DNS.

---
*Guía técnica profesional para el portafolio de Vladimir Acuña.*
