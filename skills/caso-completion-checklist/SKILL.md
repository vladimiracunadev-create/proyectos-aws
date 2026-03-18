---
name: caso-completion-checklist
description: Lista ordenada y exhaustiva de todos los archivos a actualizar cuando un caso pasa de PROYECTADO a COMPLETADO en este monorepo. Usar al terminar la implementacion de cualquier caso nuevo para garantizar que ningun archivo quede desactualizado. Previene el problema de "seguro faltan mas archivos".
---

# Caso Completion Checklist

Cuando un caso se completa, hay exactamente 18 puntos de documentacion a verificar.
Seguir el orden: primero el caso, luego el repositorio, luego los docs globales, por ultimo portal y wiki.

---

## Bloque 1 — Archivos del propio caso (5)

### 1. `caso-X-nombre/README.md`
- Cambiar estado de `PROYECTADO` a `COMPLETADO` o `COMPLETADO (VALIDADO)`
- Completar la tabla de endpoints con URLs reales
- Agregar la URL de demo en vivo si aplica
- Si el caso tiene costo fijo: cambiar link de demo a `VISUALIZATION.md`
- Verificar que el stack name real este documentado

### 2. `caso-X-nombre/docs/architecture.md`
- Verificar que sigue el estandar de 4 diagramas Mermaid (usar skill `architecture-doc-standard`)
- Actualizar cualquier referencia a estado "proyectado" o "pendiente"

### 3. `caso-X-nombre/AWS_PASO_A_PASO.md`
- Verificar que los comandos de despliegue sean los reales (no placeholders)
- Confirmar URLs de API Gateway reales en los curl de ejemplo
- Agregar seccion de troubleshooting si no existe

### 4. `caso-X-nombre/VISUALIZATION.md` (solo si aplica)
- Obligatorio para casos H, J, K, M y cualquier caso con recurso de costo fijo
- Si no existe y el caso lo necesita: usar skill `visualizacion-evidencia`

### 5. Tests y smoke tests
- Verificar que `pytest` pasa en el directorio del caso
- Verificar que el smoke test de `scripts/smoke/smoke_caso_X.sh` existe

---

## Bloque 2 — Archivos raiz del repositorio (3)

### 6. `README.md` (raiz)
- Cambiar estado del caso en la tabla principal de `PROYECTADO` a `COMPLETADO`
- Agregar links a architecture.md y AWS_PASO_A_PASO.md del caso
- Verificar que el conteo total de casos completados es correcto

### 7. `CHANGELOG.md`
- Agregar entrada nueva con el numero de version siguiente
- Incluir los servicios AWS usados, decisiones clave y tests escritos
- Formato: `[X.Y.0] — YYYY-MM-DD`

### 8. `ROADMAP.md`
- Marcar como completado el caso en la seccion correspondiente
- Mover el caso a la lista de "Completados" si habia una seccion de proyectados

---

## Bloque 3 — Documentacion global en docs/ (7)

### 9. `docs/IMPLEMENTATION_SUMMARY.md`
- Actualizar el conteo: "N Completados (A, B, C, ...)"
- Actualizar numero de smoke tests y tests unitarios
- Actualizar version y fecha

### 10. `docs/FILE_STRUCTURE.md`
- Cambiar la entrada del caso de "Proyectado" a "Completado"
- Agregar la estructura interna del caso si es nueva (backend/, terraform/, etc.)
- Actualizar la fecha de ultima actualizacion

### 11. `docs/COMPLETED_CASES_GUIDE.md`
- Agregar seccion del nuevo caso en el orden correcto (A→L→M)
- Incluir: descripcion, servicios, endpoints, decisiones clave

### 12. `docs/TECHNICAL_SPECS.md`
- Agregar permisos IAM requeridos por el caso nuevo
- Agregar el flujo minimo de Lambda si es serverless
- Agregar los comandos de test del caso

### 13. `docs/RECRUITER.md`
- Si el caso aporta algo relevante para reclutadores: agregar en la tabla de valor
- Actualizar la seccion "tour guiado" si el caso debe aparecer en el recorrido
- Actualizar la lista de skills demostrados

### 14. `docs/BEGINNERS_GUIDE.md`
- Cambiar el caso de "futuro" o "proyectado" a "completado" con explicacion
- Agregar la "Idea clave" del caso en lenguaje accesible

### 15. `docs/PROYECTADOS_ANALISIS.md`
- Actualizar el estado del caso en la tabla de estado
- Marcar con check en el diagrama Mermaid de dependencias si aparece

---

## Bloque 4 — Portal y wiki (3)

### 16. `index.html` (portal GitLab Pages)
- Agregar link al caso en el grupo correcto del sidebar
- Si el caso tiene demo o visualization: agregar ese link tambien

### 17. `wiki/home.md`
- Agregar fila del caso en la tabla principal
- Actualizar el orden de lectura sugerido si el caso cambia la secuencia

### 18. CI/CD: `.gitlab-ci.yml`
- Agregar job `test_caso_X` si el caso tiene tests unitarios
- Verificar que el job usa `changes: caso-X-nombre/**/*`
- Agregar target en `Makefile` y script en `package.json`

---

## Orden recomendado de ejecucion

```
Bloque 1 (caso) → Bloque 2 (raiz) → Bloque 3 (docs/) → Bloque 4 (portal/wiki)
```

No mezclar bloques. Terminar cada bloque antes de pasar al siguiente.

---

## Verificacion final

Antes de hacer commit, ejecutar:

```bash
# Verificar que los tests del caso pasan
make test-X

# Verificar que el smoke test funciona (si hay stack activo)
make smoke-X

# Verificar que no quedaron referencias a "PROYECTADO" en el caso
grep -r "PROYECTADO" caso-X-nombre/
```

Si `grep` devuelve resultados, revisar cuales son intencionales (historico) y cuales son omisiones.

---

## Casos especiales

### Caso con solo documentacion (sin deploy real)
Si el caso es un lab teorico o fue validado y destruido:
- Completar todos los bloques igualmente
- En el README del caso, indicar: "Validado y destruido bajo principios FinOps"
- El VISUALIZATION.md es la evidencia del deploy

### Caso que reemplaza a otro
Si el caso nuevo evoluciona un caso anterior (ejemplo: E evoluciona D):
- Actualizar el README del caso anterior para mencionar el sucesor
- En `docs/ARCHITECTURE.md` verificar que el diagrama de tiers refleja la relacion
