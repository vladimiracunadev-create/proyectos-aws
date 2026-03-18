---
name: docs-portal-sync
description: Keep ALL markdown files in sync when a new `caso-*` is completed or updated. Use whenever a case status changes (PROYECTADO → COMPLETADO), a new case is implemented, or a documentation sweep is requested. This skill enumerates every file that must change, what exactly to check in each one, and common mistakes to avoid.
---

# Docs Portal Sync

Tratar el repositorio como un producto: si un caso esta en produccion pero la documentacion dice PROYECTADO, el portafolio miente.

---

## Cuando usar este skill

- Se completa un nuevo `caso-*`
- Se despliega un stack SAM o Terraform por primera vez
- Se obtiene una URL de demo en vivo
- Se pide un "barrido profundo de todos los md"
- Se detecta cualquier inconsistencia de estado entre archivos

---

## Lista completa de archivos a revisar

### Nivel 1 — Archivos raiz (siempre tocar)

| Archivo | Que verificar |
|---|---|
| `README.md` | Entrada del caso en la seccion de niveles (status badge, links); tabla Backlog al final (status + proxima accion) |
| `CHANGELOG.md` | Entrada `[X.Y.Z]` con fecha, descripcion de Added/Changed/Fixed |
| `ROADMAP.md` | Items del caso marcados `[x]`; fecha `_Ultima actualizacion_` |
| `AWS_CLOUD_JOURNEY.md` | Caso en mapa Mermaid (`## Mapa de la jornada`); fila en tabla `## Resumen ejecutivo`; capitulo propio (`## Capitulo N`); referencia en `## Evolucion de mentalidad tecnica`; entrada en bibliografia |

### Nivel 2 — Carpeta `docs/` (revisar uno a uno)

| Archivo | Que verificar |
|---|---|
| `docs/ARCHITECTURE.md` | Tier correcto con subgrafo Mermaid del caso; descripcion en la seccion del tier |
| `docs/BEGINNERS_GUIDE.md` | Caso en la lista de `## Deep dive`; seccion "Idea clave para entender el Caso X" al final |
| `docs/COMPLETED_CASES_GUIDE.md` | Seccion `## Caso X` con los 4 bloques (que se hizo, por que, que resuelve, que mirar primero); caso incluido en `## Orden recomendado` |
| `docs/RECRUITER.md` | Caso como entrada destacada en `## Casos destacados`; pilar en `## Valor de negocio`; habilidad en `## Habilidades demostradas`; caso en `## Tour guiado sugerido` |
| `docs/FILE_STRUCTURE.md` | Entrada en el arbol de carpetas con estado (Completado); seccion de estructura interna del caso |
| `docs/IMPLEMENTATION_SUMMARY.md` | Conteo de casos completados; conteo de smoke tests; conteo de tests unitarios; version y fecha |
| `docs/QUICK_REFERENCE.md` | Seccion `## Caso X rapido` con comandos sam/terraform, validaciones curl y URL activa; entrada en tabla de documentacion; fecha |
| `docs/PROYECTADOS_ANALISIS.md` | Nodo `✅` en el diagrama Mermaid de dependencias; tabla de estado superior; si el caso tenia "Orden Recomendado", marcarlo como COMPLETADO con URL |
| `docs/TECHNICAL_SPECS.md` | Permisos IAM necesarios para el caso; flujo minimo de Lambda si aplica; herramientas de test |
| `wiki/home.md` | Fila en la tabla principal con stack, demo URL y link a docs |

### Nivel 3 — Carpeta `caso-X/` del caso nuevo

| Archivo | Que verificar |
|---|---|
| `caso-X/README.md` | Badge `Status-Completado`; URL de demo si existe; links a arquitectura y paso a paso |
| `caso-X/docs/architecture.md` | Estructura estandar (ver abajo) |
| `caso-X/AWS_PASO_A_PASO.md` | Comandos verificados; outputs reales; troubleshooting |

---

## Estructura estandar de architecture.md

Cada `caso-*/docs/architecture.md` debe tener estos bloques en orden:

```
# Emoji Titulo

> blockquote con stack, estado, region, demo URL

## Vision general

## Diagrama 1: [secuencia o flujo principal]
```mermaid ... ```

## Diagrama 2: [capas de defensa o componentes]
```mermaid ... ```

## Diagrama 3: [arquitectura SAM/IaC completa]
```mermaid ... ```

## Diagrama 4: [comparativa de decision o patron avanzado]
```mermaid ... ```

## Componentes
tabla con Componente | Rol | Costo | Notas

## Decisiones de diseno
tabla con Decision | Alternativa descartada | Razon

## Que aprende un reclutador
lista de bullets

## Siguiente paso natural
una oracion + link al siguiente caso

## Referencias
links oficiales AWS
```

---

## Cambios en README.md segun estado

Cuando un caso pasa de PROYECTADO a COMPLETADO:

1. Cambiar el badge de status en la entrada del caso
2. Agregar `👉 [Ver Demo en Vivo](URL)` si hay URL activa
3. Verificar que existen los links a `docs/architecture.md` y `AWS_PASO_A_PASO.md`
4. En la tabla Backlog al final: cambiar estado y descripcion de proxima accion

---

## Cambios en AWS_CLOUD_JOURNEY.md

Este archivo es el que mas se olvida actualizar. Tiene 4 puntos de cambio:

1. **Mapa Mermaid** (`## Mapa de la jornada`): agregar nodo del caso con sus dependencias
2. **Tabla resumen** (`## Resumen ejecutivo`): agregar fila con etapa, capacidad, servicios y leccion
3. **Capitulo propio**: agregar `## Capitulo N. Titulo` con secciones: Lo que demuestra / Aprendizajes tecnicos / Cambio de mentalidad / Trade-off real / Valor editorial / Referencias AWS
4. **Evolucion de mentalidad** (`## Evolucion de mentalidad tecnica`): agregar el paso correspondiente en la escalera
5. **Bibliografia**: agregar referencias oficiales AWS del caso

Numeracion de capitulos actual (actualizar si se agregan nuevos):
- I: Fundamentos y hosting (A, B)
- II: IaC y distribucion segura (C)
- III: Serverless y backend (D)
- IV: Datos y modelado (E)
- V: Seguridad perimetral (F)
- VI: Observabilidad como codigo (H)
- VII: Arquitectura event-driven (G)
- VIII: Contenedores (J)
- IX: Gobernanza y FinOps (L)
- X: Resiliencia (M)

---

## Cambios en ROADMAP.md

- Marcar items `[ ]` → `[x]` del caso completado
- Agregar `✅ COMPLETADO` al titulo de la seccion
- Actualizar `_Ultima actualizacion_` al final

---

## Cambios en wiki/home.md (submodulo git)

`wiki/` es un submodulo git separado. Para commitear cambios:

```bash
# 1. Entrar al submodulo y commitear dentro
cd wiki
git add home.md
git commit -m "docs: update home.md — add caso X"

# 2. Volver al repo principal y actualizar el puntero
cd ..
git add wiki
git commit -m "docs(wiki): update submodule pointer"
```

Si solo se hace `git add wiki` en el repo principal sin commitear dentro del submodulo, el estado queda como `m wiki` (dirty) sin resolver.

---

## Errores comunes a evitar

1. **Olvidar AWS_CLOUD_JOURNEY.md**: es el archivo mas olvidado. Tiene 4 puntos de cambio independientes.
2. **ROADMAP.md items sin marcar**: cuando un caso se completa, su seccion del roadmap sigue con `[ ]`.
3. **QUICK_REFERENCE.md sin seccion del caso**: cada caso Lambda/SAM necesita su seccion con comandos sam y curl.
4. **COMPLETED_CASES_GUIDE.md orden de lectura desactualizado**: al agregar casos, actualizar el orden numerado.
5. **PROYECTADOS_ANALISIS.md nodo Mermaid sin ✅**: el diagrama de dependencias no se actualiza automaticamente.
6. **wiki/home.md sin nueva fila**: el submodulo tiene su propio git, no basta con editar el archivo.
7. **Fechas desactualizadas**: `_Ultima actualizacion_` al final de cada doc debe reflejar la fecha real.
8. **README.md tabla Backlog**: es diferente a la seccion de casos. Ambas deben actualizarse.

---

## Orden eficiente de trabajo

Para un caso recien completado, procesar en este orden:

```
1. caso-X/README.md               ← badge + URL + links
2. caso-X/docs/architecture.md    ← estructura estandar con 4 diagramas
3. caso-X/AWS_PASO_A_PASO.md      ← comandos reales verificados
4. README.md                      ← entrada del caso + tabla backlog
5. CHANGELOG.md                   ← entrada con version semantica
6. ROADMAP.md                     ← items [x] + fecha
7. docs/ARCHITECTURE.md           ← subgrafo en el tier correcto
8. docs/COMPLETED_CASES_GUIDE.md  ← seccion + orden de lectura
9. docs/QUICK_REFERENCE.md        ← seccion rapida + tabla
10. docs/BEGINNERS_GUIDE.md       ← deep dive + idea clave
11. docs/RECRUITER.md             ← caso destacado + habilidades
12. docs/FILE_STRUCTURE.md        ← arbol + estructura interna
13. docs/IMPLEMENTATION_SUMMARY.md ← conteos + version
14. docs/PROYECTADOS_ANALISIS.md  ← nodo ✅ + estado + orden
15. docs/TECHNICAL_SPECS.md       ← permisos IAM + flujo Lambda
16. wiki/home.md                  ← fila tabla (commitear dentro del submodulo)
17. AWS_CLOUD_JOURNEY.md          ← mapa + tabla + capitulo + escalera + biblio
```

---

## Navegacion del portal

El root `index.html` carga markdown dinamicamente. Reglas:

- Preferir targets `.md` para contenido que debe renderizarse en el portal.
- No inventar URLs de demo; usar `—` o `deploy con sam deploy` si no hay URL activa.
- Los links relativos deben ser compatibles con el router hash.
- No enlazar a archivos que no existen.

---

## Codificacion

- Usar ASCII en markdown por defecto.
- Si el archivo fuente ya tiene texto con tildes y no-ASCII, preservarlo.
- No mezclar codificaciones dentro del mismo archivo.

_Ultima actualizacion: 2026-03-17_
