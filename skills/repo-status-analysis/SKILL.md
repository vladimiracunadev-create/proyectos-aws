---
name: repo-status-analysis
description: Analiza el estado actual del repositorio, identifica gaps, genera el documento docs/ESTADO_Y_ROADMAP.md actualizado con diagramas Mermaid y tabla de mejoras priorizadas. Usar al inicio de una sesion para tener contexto completo, o al final para documentar el estado tras cambios importantes.
---

# Repo Status Analysis

Este skill produce una radiografia completa del repositorio en un documento estructurado con diagramas.
Usarlo como primer paso en sesiones largas, o como cierre de sesion para dejar registro del estado.

---

## Paso 1 — Recolectar el estado real

Leer los siguientes archivos para construir el diagnostico:

```
README.md                          ← lista de casos y su estado
CHANGELOG.md                       ← ultima version, fecha, que se hizo
ROADMAP.md                         ← que esta pendiente
docs/IMPLEMENTATION_SUMMARY.md     ← conteo de casos, tests, smoke tests
docs/FINOPS_COSTOS.md              ← estrategia de costo por caso
skills/README.md                   ← skills disponibles
.gitlab-ci.yml                     ← jobs de test activos
```

Para cada caso completado, verificar:
- Tiene `README.md` con estado COMPLETADO
- Tiene `docs/architecture.md` con 4 diagramas
- Tiene `AWS_PASO_A_PASO.md`
- Si tiene costo fijo: tiene `VISUALIZATION.md`
- Tiene job en `.gitlab-ci.yml` si hay tests

---

## Paso 2 — Identificar gaps

Revisar los siguientes puntos de forma sistematica:

### Gaps de documentacion por caso
- `VISUALIZATION.md` faltante en casos con costo fijo (H, J, K, M)
- `architecture.md` que no cumple el estandar de 4 diagramas
- `AWS_PASO_A_PASO.md` con URLs placeholder sin completar

### Gaps de infraestructura global
- Skills desactualizados o no registrados en `skills/README.md` y `docs/SKILLS.md`
- `ESTADO_Y_ROADMAP.md` desactualizado respecto al ultimo commit
- README principal con links rotos o secciones faltantes

### Gaps de CI/CD
- Casos con tests que no tienen job en `.gitlab-ci.yml`
- Smoke tests que no tienen target en el `Makefile`

---

## Paso 3 — Generar o actualizar docs/ESTADO_Y_ROADMAP.md

El documento debe seguir esta estructura fija:

### Secciones obligatorias

1. **Barra de estado general** — 6 dimensiones con porcentaje y barra visual:
   ```
   Madurez técnica:     ████████░░  80%
   Documentación:       █████████░  90%
   Skills y flujos:     █████████░  90%
   FinOps:              ████████░░  80%
   Evidencia visual:    ███████░░░  70%
   Casos futuros:       ████░░░░░░  40%
   ```

2. **Diagrama de progresion de casos** — `graph TB` con tiers (T1 a T5), colores por estado:
   - Verde `#2ea043` = COMPLETADO
   - Naranja `#f0883e` = EN PROGRESO / Fase 0
   - Gris `#8b949e` = PROYECTADO

3. **Tabla de casos completados** — caso, nombre, tecnologia, tipo de demo

4. **Diagrama de documentacion global** — `flowchart LR` con los 4 subsistemas: raiz, docs/, skills/, portal

5. **Diagrama del sistema de skills** — `flowchart TD` desde "Nueva tarea" a cada skill

6. **Seccion de gaps actuales** — `flowchart TD` con subgrafos por prioridad (CRITICO, MEDIO, BAJO)

7. **Mejoras futuras con diagramas** — una seccion por mejora de prioridad alta, con diagrama Mermaid propio si aplica

8. **Tabla consolidada de mejoras** — # | Mejora | Prioridad | Esfuerzo | Costo lab | Prerequisito

9. **Proxima sesion recomendada** — lista de 2-3 acciones concretas con el skill a usar

---

## Paso 4 — Actualizar archivos vinculantes

Cuando se actualiza `docs/ESTADO_Y_ROADMAP.md`, verificar y actualizar si es necesario:

| Archivo | Que actualizar |
|---|---|
| `README.md` | Link a ESTADO_Y_ROADMAP.md en seccion "Estado y Hoja de Ruta" |
| `docs/IMPLEMENTATION_SUMMARY.md` | Conteo de casos, version, fecha |
| `CHANGELOG.md` | Nueva entrada si hubo cambios estructurales |
| `wiki/home.md` | Si el estado del repo cambio significativamente |

---

## Paso 5 — Criterios de porcentaje para la barra de estado

Usar estos criterios para calcular los porcentajes con consistencia entre sesiones:

| Dimension | 100% significa | Calculo |
|---|---|---|
| Madurez tecnica | 13 casos completados (A-M + I) | casos_completados / 13 |
| Documentacion | Todos los docs existen y estan actualizados | (docs_ok / total_docs) |
| Skills y flujos | Todos los workflows tienen skill asignado | (flujos_con_skill / flujos_totales) |
| FinOps | Costos documentados + calculadora con datos reales | parcial hasta Cost Explorer real |
| Evidencia visual | Todos los casos con costo tienen VISUALIZATION.md | visualization_ok / casos_con_costo |
| Casos futuros | M + I + N completados | casos_futuros_completados / 3 |

---

## Frecuencia recomendada de ejecucion

- **Al inicio de cada sesion larga**: para tener contexto del estado real antes de trabajar
- **Al terminar un caso**: para actualizar el estado y documentar que cambio
- **Mensualmente**: como revision de salud del repositorio

---

## Salida esperada

Al terminar este skill deben existir o estar actualizados:
- `docs/ESTADO_Y_ROADMAP.md` — documento completo con diagramas
- Link desde `README.md` en la seccion "Estado y Hoja de Ruta"
- Commit con mensaje: `docs(estado): update repo status — [resumen de cambios]`
