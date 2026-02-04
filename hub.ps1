# hub.ps1 - Hub CLI para proyectos-aws (Windows PowerShell)
# Comandos: list-projects, validate

param(
    [Parameter(Position=0)]
    [string]$Command = "help"
)

# Colors for output
function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Color
}

# Show help
function Show-Help {
    Write-ColorOutput "🚀 Hub CLI - proyectos-aws" -Color Green
    Write-Host ""
    Write-ColorOutput "Uso:" -Color Cyan
    Write-Host "  .\hub.ps1 <comando>"
    Write-Host ""
    Write-ColorOutput "Comandos disponibles:" -Color Cyan
    Write-ColorOutput "  list-projects" -Color Green
    Write-Host "    Lista todos los proyectos AWS (carpetas aws-*)"
    Write-ColorOutput "  validate" -Color Green
    Write-Host "    Ejecuta validaciones usando tooling Docker"
    Write-ColorOutput "  help" -Color Green
    Write-Host "    Muestra esta ayuda"
    Write-Host ""
    Write-ColorOutput "Ejemplos:" -Color Cyan
    Write-Host "  .\hub.ps1 list-projects"
    Write-Host "  .\hub.ps1 validate"
    Write-Host ""
    Write-ColorOutput "Requisitos:" -Color Cyan
    Write-Host "  - Docker Desktop instalado y corriendo"
    Write-Host "  - make (opcional, para comandos avanzados)"
    Write-Host ""
}

# List projects
function List-Projects {
    Write-ColorOutput "📂 Proyectos AWS encontrados:" -Color Green
    Write-Host ""
    
    $scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
    $projects = Get-ChildItem -Path $scriptDir -Directory -Filter "aws-*"
    
    $count = 0
    foreach ($project in $projects) {
        $fileCount = (Get-ChildItem -Path $project.FullName -Recurse -File).Count
        Write-Host "  ▸ " -NoNewline
        Write-ColorOutput $project.Name -Color Cyan -NoNewline
        Write-ColorOutput " ($fileCount archivos)" -Color Yellow
        $count++
    }
    
    Write-Host ""
    if ($count -eq 0) {
        Write-ColorOutput "⚠️  No se encontraron proyectos (carpetas aws-*)" -Color Yellow
    } else {
        Write-ColorOutput "✅ Total: $count proyecto(s)" -Color Green
    }
}

# Validate
function Invoke-Validate {
    Write-ColorOutput "🔍 Ejecutando validaciones con tooling..." -Color Green
    Write-Host ""
    
    # Check if Docker is running
    try {
        docker info | Out-Null
    } catch {
        Write-ColorOutput "❌ Error: Docker no está corriendo" -Color Red
        Write-ColorOutput "   Inicia Docker Desktop y vuelve a intentar" -Color Yellow
        exit 1
    }
    
    # Check if tooling image exists
    $imageExists = docker images | Select-String "proyectos-aws/tooling"
    if (-not $imageExists) {
        Write-ColorOutput "⚠️  Imagen de tooling no encontrada. Construyendo..." -Color Yellow
        
        # Check if make is available
        if (Get-Command make -ErrorAction SilentlyContinue) {
            make tooling-build
        } else {
            # Build manually if make is not available
            docker build -t proyectos-aws/tooling:1.0.0 -t proyectos-aws/tooling:latest -f tooling/Dockerfile.tooling tooling/
        }
        Write-Host ""
    }
    
    # Run validation
    $workspacePath = (Get-Location).Path
    docker run --rm -v "${workspacePath}:/workspace:ro" proyectos-aws/tooling:1.0.0 /opt/tooling/scripts/validate.sh
}

# Main
switch ($Command.ToLower()) {
    "list-projects" {
        List-Projects
    }
    "validate" {
        Invoke-Validate
    }
    "help" {
        Show-Help
    }
    default {
        Write-ColorOutput "❌ Comando desconocido: $Command" -Color Red
        Write-Host ""
        Show-Help
        exit 1
    }
}
