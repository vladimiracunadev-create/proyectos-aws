---
name: visualizacion-evidencia
description: Decide si un caso usa "Demo en Vivo" o "Reporte de Visualizacion y Resultados" basado en su costo, y genera el VISUALIZATION.md con instrucciones paso a paso extremadamente detalladas cuando corresponde. Usar cuando se completa un caso con recursos AWS de costo fijo (EKS, ALB, Fargate, NAT Gateway, CloudWatch Dashboard, WAF) y se necesita documentar la evidencia antes de destruir la infraestructura.
---

# Skill: Visualizacion y Evidencia de Casos AWS

Este skill aplica la logica de documentacion correcta segun el modelo de costo de cada caso.

---

## Paso 1 — Evaluar el tipo de caso

Antes de generar cualquier documento, leer el README.md del caso y, si existe, el template.yaml o main.tf.

### Tabla de decision: Demo en Vivo vs Evidencia Estatica

| Caso | Recurso de costo fijo | Decision |
|---|---|---|
| A | Ninguno | Demo en Vivo (👉 Ver Demo en Vivo) |
| B | Ninguno | Demo en Vivo |
| C | Ninguno (CloudFront free tier) | Demo en Vivo |
| D | Ninguno (serverless) | Demo en Vivo |
| E | Ninguno (serverless) | Demo en Vivo |
| F sin WAF | Ninguno | Demo en Vivo |
| F con WAF | WAF $5/mes (opcional) | Demo en Vivo + nota FinOps |
| G | Ninguno (pay-per-use) | Demo en Vivo |
| H | CloudWatch Dashboard $3/mes | Evidencia Estatica (🖼️ Reporte de Visualizacion) |
| J | ALB ~$16/mes + Fargate ~$15/mes | Evidencia Estatica |
| K | EKS $72/mes + NAT GW $32/mes | Evidencia Estatica |
| L | Ninguno | Demo en Vivo |
| M (futuro) | ALB + Fargate + Route 53 + NAT GW | Evidencia Estatica |

**Regla general:** Si el README del caso dice "DESACTIVADO POR COSTOS" o "deploy-validate-destroy", el caso necesita VISUALIZATION.md.

---

## Paso 2 — Si el caso es Demo en Vivo: verificar el README

Para casos de Demo en Vivo, verificar que el README.md tenga:
- URL de demo activa en formato `👉 [Ver Demo en Vivo](https://...)`
- La URL debe ser real (API Gateway, Amplify, CloudFront, S3 website)
- Si la URL es placeholder, marcarla con `(URL PENDIENTE DE DESPLIEGUE)`

No crear VISUALIZATION.md para estos casos.

---

## Paso 3 — Si el caso es Evidencia Estatica: generar VISUALIZATION.md

Crear el archivo `caso-X-nombre/VISUALIZATION.md` siguiendo esta estructura OBLIGATORIA:

### Estructura del VISUALIZATION.md

```markdown
# 📊 Reporte de Visualizacion y Resultados - Caso X (Nombre Completo)

## 🎯 Por que este documento?
[Explicar por que el caso no tiene demo en vivo: costo fijo del recurso, cantidad por hora, costo mensual exacto]

---

## 🏗️ Resumen de la Implementacion
[Describir que se construyo, tecnologias, logros tecnicos]

### Logros Tecnicos:
- [Logro 1]
- [Logro 2]
- [Estrategia FinOps: Ciclo de vida "Deploy-Validate-Destroy" documentado]

> [!CAUTION]
> **ESTRATEGIA FINOPS**
> [Detallar cada servicio con costo fijo, costo por hora, costo mensual aproximado]
> **Decision Arquitectonica**: Implementamos estrategia "Evidenciar y Destruir".

---

## 🖼️ Galeria de Evidencias (Flujo de Despliegue)

[Para CADA recurso AWS del caso: una seccion con instrucciones EXACTAS de navegacion en consola]

### N. Nombre del Recurso (Servicio AWS)
> **Instrucciones Paso a Paso**:
> 1. Ve a la **Consola de AWS** y busca el servicio **[Nombre exacto del servicio]**.
> 2. [Paso exacto con nombre del menu, seccion, pestaña]
> 3. Busca el recurso llamado `[nombre-exacto-del-recurso]`.
> 4. **Captura**: Toma una foto donde se vea [que campo, que estado, que dato especifico].

![Nombre descriptivo](./img/nombre-archivo.png "Descripcion")

---

## 📈 Tabla de Validacion Final

| Hito | Estado | Metodo |
| :--- | :--- | :--- |
| [Hito 1] | 🟢 Validado | [Donde se valida] |
| FinOps | ⚠️ Critico | Eliminacion verificada post-captura |

---

## 🏁 Instrucciones de Cierre (Baja del Servicio)

[Comandos exactos para destruir los recursos, con verificacion en consola]
```

---

## Paso 4 — Reglas de detalle para las instrucciones de consola

Las instrucciones de cada seccion DEBEN ser tan detalladas que alguien que nunca uso AWS pueda seguirlas:

1. **Nombrar el servicio EXACTAMENTE como aparece en la consola**: "Elastic Container Service (ECS)", no solo "ECS"
2. **Nombrar la ruta de navegacion**: "menu izquierdo > Clusters > pestaña Services"
3. **Nombrar el recurso exacto** con el nombre real del template: `vladimir-case-j-cluster`, no "el cluster"
4. **Decir que campo especifico capturar**: "donde se vea el campo Status: Active y Running tasks: 1"
5. **El nombre de la imagen** debe ser descriptivo y seguir el patron: `[servicio]-[lo-que-muestra].png`

---

## Paso 5 — Convencion de nombres de imagenes

Patron: `[servicio-abreviado]-[estado-o-accion].png`

Ejemplos correctos:
- `cloudwatch-dashboard-activo.png`
- `xray-trazas-lambda.png`
- `eks-cluster-active.png`
- `alb-active-dns.png`
- `ecs-service-running.png`
- `cognito-userpool-created.png`
- `waf-webacl-active.png`

Las imagenes van en `caso-X-nombre/img/`. El directorio `img/` puede no existir aun — solo documentar los nombres en el VISUALIZATION.md, el usuario los sube al momento del despliegue.

---

## Paso 6 — Instrucciones de destruccion

La seccion de destruccion DEBE incluir:

1. **Comando make** si existe en el Makefile
2. **Comando directo** (sam delete, terraform destroy, aws cli)
3. **Verificacion manual en consola**: lista de recursos especificos a confirmar que ya no existen
4. **Nota sobre logs**: indicar que CloudWatch Logs pueden quedar y si conviene borrarlos

---

## Paso 7 — Actualizar el README del caso

Cuando se crea VISUALIZATION.md, actualizar el README.md del caso:

- Cambiar `👉 [Ver Demo en Vivo](URL)` por `🖼️ [Reporte de Visualizacion y Resultados](VISUALIZATION.md)`
- Agregar la nota de FinOps si no existe: "Infraestructura destruida bajo principios FinOps."
- La URL original puede quedarse con la leyenda `(ESTADO: DESACTIVADO POR COSTOS)`

---

## Paso 8 — Casos de referencia

Antes de generar un VISUALIZATION.md nuevo, leer como referencia:
- `caso-j-containers-ecs/VISUALIZATION.md` — referencia para casos Terraform + contenedores
- `caso-k-kubernetes-eks/VISUALIZATION.md` — referencia para casos EKS + infraestructura de red

El tono y nivel de detalle de esos documentos es el estandar a seguir.

---

## Paso 9 — Actualizaciones de documentacion general

Cuando se genera un VISUALIZATION.md nuevo:
- Verificar que `docs/FINOPS_COSTOS.md` tenga la estrategia correcta para ese caso
- Verificar que el README principal del repositorio no tenga una URL de demo en vivo para ese caso si el recurso esta destruido
