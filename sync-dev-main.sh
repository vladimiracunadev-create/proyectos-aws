#!/usr/bin/env bash
set -euo pipefail

FORCE_MERGE=0
if [[ "${1:-}" == "--force-merge" ]]; then
  FORCE_MERGE=1
fi

run() {
  echo ">> $*"
  "$@"
}

# Verifica que estás dentro de un repo git
run git rev-parse --is-inside-work-tree >/dev/null

# Evita sincronizar si tienes cambios sin commit
if [[ -n "$(git status --porcelain)" ]]; then
  echo "ERROR: Tienes cambios sin commit. Haz commit o stash antes de sincronizar."
  exit 1
fi

# Trae info del remoto
run git fetch origin --prune

# Actualiza dev
run git checkout dev
run git pull --ff-only origin dev

# Actualiza main
run git checkout main
run git pull --ff-only origin main

# Merge dev -> main
if git merge --ff-only dev; then
  :
else
  if [[ "$FORCE_MERGE" -eq 1 ]]; then
    run git merge dev
  else
    echo "ERROR: No se pudo fast-forward main <- dev (divergió). Ejecuta: ./sync-dev-main.sh --force-merge"
    exit 1
  fi
fi

run git push origin main

# Mantener dev igual que main (recomendado)
run git checkout dev
if git merge --ff-only main; then
  :
else
  if [[ "$FORCE_MERGE" -eq 1 ]]; then
    run git merge main
  else
    echo "ERROR: No se pudo fast-forward dev <- main (divergió). Ejecuta: ./sync-dev-main.sh --force-merge"
    exit 1
  fi
fi

run git push origin dev

echo "✅ Sincronizado: dev ↔ main"
