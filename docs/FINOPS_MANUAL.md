# 💰 Manual de FinOps y Auditoría de Costos

> **Objetivo**: Este documento te enseña a interpretar los datos arrojados por el script de auditoría (`make finops-check`) y a tomar decisiones financieras inteligentes para evitar cargos sorpresa en AWS.

---

## 🚦 Semáforo de Riesgo Financiero

No todos los recursos cuestan lo mismo. Usa esta guía rápida para saber qué eliminar URGENTEMENTE.

| Recurso | Nivel de Riesgo | Costo Aprox. (USD/Mes) | Acción Recomendada |
| :--- | :--- | :--- | :--- |
| **NAT Gateway** | 🔴 CRÍTICO | ~$32 USD + Tráfico | **BORRAR INMEDIATAMENTE** si no se usa. |
| **EKS Cluster** | 🔴 CRÍTICO | ~$72 USD | **BORRAR** al terminar el laboratorio. |
| **EC2 (Running)** | 🔴 ALTO | Variable ($8 - $100+) | **DETENER** o **TERMINAR**. |
| **ALB (Load Balancer)** | 🔴 ALTO | ~$16 USD + LCU | **BORRAR** si no hay tráfico real. |
| **RDS (Base de Datos)** | 🟠 MEDIO | Variable ($12 - $50+) | **DETENER** o crear Snapshot final y borrar. |
| **EBS (Discos sueltos)** | 🟡 BAJO | ~$0.08 por GB | **BORRAR** si el estado es `available` (sin uso). |
| **EIP (IP Elástica)** | 🟡 BAJO | ~$3.60 USD | **LIBERAR** si no está asociada a una instancia. |
| **S3 (Storage)** | 🟢 ÍNFIMO | ~$0.023 por GB | Mantener (Costo despreciable para demos). |

---

## 🕵️ Cómo interpretar el script de auditoría

Al ejecutar `make finops-check`, verás tablas por región. Aquí te explicamos qué buscar:

### 1. EC2 Instances
*   **Running**: ¡Te están cobrando! Apágala (`Stop`) si vas a volver, o elimínala (`Terminate`) si terminaste.
*   **Stopped**: No cobra cómputo, **pero sí cobra el disco (EBS)**.

### 2. NAT Gateways
*   **Available**: Si ves uno aquí y no estás haciendo una práctica de redes privada, **ESTÁS QUEMANDO DINERO**. Ve a la consola de VPC y bórralo ya.

### 3. Load Balancers (ALB/NLB)
*   **Active**: Cobra por cada hora que existe, aunque nadie entre a tu web. Si terminaste el Caso J o K, destrúyelo.

---

## 🧠 Workflow de Toma de Decisiones

1.  **¿Estoy estudiando hoy?**
    *   **Sí**: Deja los recursos encendidos.
    *   **No**: Ejecuta `make finops-check`.

2.  **Si encuentro algo "Running"**:
    *   *¿Es la base de datos (RDS)?* -> Si tiene datos vitales, haz **Stop** (Detener). Si es de prueba, **Delete** (Borrar).
    *   *¿Es un Cluster EKS?* -> **Delete**. EKS no tiene "Stop".

3.  **¿Cómo elimino?**
    *   Lo ideal es usar `terraform destroy` o `make destroy` en la carpeta del caso correspondiente.
    *   Si eso falla, usa la consola de AWS para eliminación manual ("Nuclear Option").

---

## 🛠️ Automatización del Monorepo

Este repositorio incluye una herramienta personalizada para auditar tus costos:

```bash
make finops-check
```

*   **Windows**: Ejecuta un script de PowerShell optimizado.
*   **Mac/Linux**: Ejecuta un script de Bash nativo.
*   **Alcance**: Escanea `us-east-1`, `us-east-2` y `sa-east-1`.

> **Consejo Profesional**: Ejecuta esto **cada viernes** por la tarde para asegurar un fin de semana tranquilo sin costos fantasma.
