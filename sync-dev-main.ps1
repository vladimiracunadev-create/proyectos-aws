param(
  [switch]$ForceMerge
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Run($cmd) {
  Write-Host ">> $cmd"
  iex $cmd
}

# 1) Asegurar que estamos dentro de un repo git
Run "git rev-parse --is-inside-work-tree | Out-Null"

# 2) No permitir cambios sin commit (para evitar líos)
$dirty = git status --porcelain
if ($dirty) {
  throw "Tienes cambios sin commit. Haz commit o stash antes de sincronizar."
}

# 3) Traer estado remoto
Run "git fetch origin --prune"

# 4) Asegurar que dev esté actualizado
Run "git checkout dev"
Run "git pull --ff-only origin dev"

# 5) Pasar dev -> main
Run "git checkout main"
Run "git pull --ff-only origin main"

try {
  # Fast-forward (lo más limpio)
  Run "git merge --ff-only dev"
} catch {
  if ($ForceMerge) {
    # Merge normal (crea merge commit) si el historial diverge
    Run "git merge dev"
  } else {
    throw "No se pudo hacer fast-forward main <- dev (historial divergió). Ejecuta: .\sync-dev-main.ps1 -ForceMerge"
  }
}

Run "git push origin main"

# 6) Mantener dev igual que main (recomendado)
Run "git checkout dev"
try {
  Run "git merge --ff-only main"
} catch {
  if ($ForceMerge) {
    Run "git merge main"
  } else {
    throw "No se pudo hacer fast-forward dev <- main. Ejecuta: .\sync-dev-main.ps1 -ForceMerge"
  }
}

Run "git push origin dev"

Write-Host "✅ Sincronizado: dev ↔ main"
