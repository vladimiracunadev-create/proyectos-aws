# 📊 Reporte de Visualización y Resultados - Caso K (EKS)

> **Nota**: Este documento sirve como evidencia del despliegue exitoso del clúster de EKS, dado que la infraestructura se destruye tras la validación para optimizar costos.

---

## 🏗️ Resumen del Despliegue
Se ha implementado una arquitectura de orquestación industrial utilizando **AWS EKS**. A diferencia de arquitecturas de contenedores simples, aquí el plano de control gestiona activamente la salud y el escalado de la flota.

### Logros Técnicos:
- **Infraestructura**: VPC con 4 subredes (públicas/privadas), NAT Gateway y Clúster EKS version 1.27.
- **Orquestación**: 3 réplicas del pod `vladimir-api` distribuidas en nodos `t3.medium`.
- **Exposición**: Balanceador de carga elástico (ELB) con DNS único.

---

## 🖼️ Galería de Evidencias (Screenshots)

### 1. Dashboard con Glassmorphism
*Inserta aquí la imagen de la web cargada a través del ELB. Se debe apreciar el diseño tipo "espejo" y los blobs animados.*

> **Lo que se resolvió**: Se integró una interfaz premium que consume metadatos internos de Kubernetes mediante el **Downward API**.

### 2. Auto-Sanación (Self-Healing)
*Inserta aquí una captura de la terminal ejecutando `kubectl delete pod` y la web mostrando un nuevo Pod ID segundos después.*

> **Lo que se resolvió**: Resiliencia automática. Si un proceso falla, Kubernetes lo restaura sin intervención humana.

### 3. Balanceo de Carga y Nodos
*Inserta aquí capturas que muestren diferentes IPs de nodos o IDs de pods al refrescar la página.*

> **Lo que se resolvió**: Distribución de tráfico y alta disponibilidad.

---

## 📈 Métricas de Verificación

| Característica | Resultado | Método de Validación |
| :--- | :--- | :--- |
| **Escalado** | 3/3 Pods Ready | `kubectl get pods` |
| **Salud** | Liveness/Readiness OK | Kubernetes Events |
| **Red** | Acceso Público ELB | HTTP GET a la URL de AWS |
| **FinOps** | Limpieza Exitosa | `terraform destroy` verificado |

---

## 🏁 Conclusión
El **Caso K** demuestra la capacidad de gestionar entornos productivos complejos, donde la infraestructura no es estática, sino un organismo vivo que se adapta y se recupera automáticamente.

---
*Documentación generada para el perfil de Vladimir Acuña.*
