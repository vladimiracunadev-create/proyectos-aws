# security-verify.ps1 - Script de verificación completa de seguridad (Windows)
# Ejecuta todas las verificaciones del security checklist

param()

$ErrorActionPreference = "Continue"

function Write-Status {
    param(
        [string]$Status,
        [string]$Message
    )
    
    switch ($Status) {
        "OK" {
            Write-Host "✅ $Message" -ForegroundColor Green
        }
        "WARN" {
            Write-Host "⚠️  $Message" -ForegroundColor Yellow
            $script:Warnings++
        }
        "FAIL" {
            Write-Host "❌ $Message" -ForegroundColor Red
            $script:Errors++
        }
    }
}

$script:Errors = 0
$script:Warnings = 0

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "🔍 Verificación de Seguridad - proyectos-aws" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# 1. Verificar .gitignore
Write-Host "1️⃣ Verificando .gitignore..." -ForegroundColor Cyan
if (Test-Path ".gitignore") {
    $gitignoreContent = Get-Content ".gitignore" -Raw
    if ($gitignoreContent -match "\.tfstate" -and $gitignoreContent -match "\.env" -and $gitignoreContent -match "\.pem") {
        Write-Status "OK" ".gitignore contiene patrones de seguridad"
    } else {
        Write-Status "FAIL" ".gitignore incompleto"
    }
} else {
    Write-Status "FAIL" ".gitignore no encontrado"
}
Write-Host ""

# 2. Verificar pre-commit
Write-Host "2️⃣ Verificando pre-commit hooks..." -ForegroundColor Cyan
if (Test-Path ".pre-commit-config.yaml") {
    Write-Status "OK" ".pre-commit-config.yaml existe"
    
    if (Get-Command pre-commit -ErrorAction SilentlyContinue) {
        Write-Status "OK" "pre-commit instalado"
    } else {
        Write-Status "WARN" "pre-commit no instalado (instale con: pip install pre-commit)"
    }
} else {
    Write-Status "FAIL" ".pre-commit-config.yaml no encontrado"
}
Write-Host ""

# 3. Verificar GitHub Actions
Write-Host "3️⃣ Verificando GitHub Actions..." -ForegroundColor Cyan
if (Test-Path ".github\workflows\security-scan.yml") {
    Write-Status "OK" "security-scan.yml configurado"
} else {
    Write-Status "FAIL" "security-scan.yml no encontrado"
}
Write-Host ""

# 4. Verificar Docker security
Write-Host "4️⃣ Verificando seguridad de Docker..." -ForegroundColor Cyan
if (Test-Path "tooling\Dockerfile.tooling") {
    Write-Status "OK" "Dockerfile.tooling existe"
    
    $dockerfileContent = Get-Content "tooling\Dockerfile.tooling" -Raw
    if ($dockerfileContent -match "USER tooling") {
        Write-Status "OK" "Dockerfile usa usuario no-root"
    } else {
        Write-Status "FAIL" "Dockerfile no especifica usuario no-root"
    }
    
    if ($dockerfileContent -match "HEALTHCHECK") {
        Write-Status "OK" "Dockerfile incluye HEALTHCHECK"
    } else {
        Write-Status "WARN" "Dockerfile no incluye HEALTHCHECK"
    }
    
    try {
        $images = docker images | Select-String "proyectos-aws/tooling"
        if ($images) {
            $user = docker run --rm proyectos-aws/tooling:1.0.0 whoami 2>$null
            if ($user -eq "tooling") {
                Write-Status "OK" "Contenedor corre como usuario no-root: $user"
            } else {
                Write-Status "FAIL" "Contenedor corre como: $user (debería ser 'tooling')"
            }
        } else {
            Write-Status "WARN" "Imagen de tooling no construida (ejecuta: make tooling-build)"
        }
    } catch {
        Write-Status "WARN" "No se pudo verificar usuario del contenedor"
    }
} else {
    Write-Status "FAIL" "Dockerfile.tooling no encontrado"
}
Write-Host ""

# 5. Verificar Kubernetes security
Write-Host "5️⃣ Verificando seguridad de Kubernetes..." -ForegroundColor Cyan
if (Test-Path "k8s\tooling-job\job.yaml") {
    Write-Status "OK" "job.yaml existe"
    
    $jobContent = Get-Content "k8s\tooling-job\job.yaml" -Raw
    if ($jobContent -match "runAsNonRoot: true") {
        Write-Status "OK" "Job configura runAsNonRoot"
    } else {
        Write-Status "FAIL" "Job no configura runAsNonRoot"
    }
    
    if ($jobContent -match "readOnlyRootFilesystem: true") {
        Write-Status "OK" "Job configura readOnlyRootFilesystem"
    } else {
        Write-Status "WARN" "Job no configura readOnlyRootFilesystem"
    }
    
    if ($jobContent -match "resources:") {
        Write-Status "OK" "Job define resource limits"
    } else {
        Write-Status "FAIL" "Job no define resource limits"
    }
} else {
    Write-Status "FAIL" "k8s\tooling-job\job.yaml no encontrado"
}

if (Test-Path "k8s\tooling-job\networkpolicy.yaml") {
    Write-Status "OK" "NetworkPolicy configurada"
} else {
    Write-Status "WARN" "NetworkPolicy no encontrada"
}
Write-Host ""

# 6. Verificar documentación
Write-Host "6️⃣ Verificando documentación de seguridad..." -ForegroundColor Cyan
$docs = @("SECURITY.md", "docs\killed.md", "docs\TOOLING.md", "docs\SECURITY_CHECKLIST.md")
foreach ($doc in $docs) {
    if (Test-Path $doc) {
        Write-Status "OK" "$doc existe"
    } else {
        Write-Status "FAIL" "$doc no encontrado"
    }
}
Write-Host ""

# 7. Verificar Makefile
Write-Host "7️⃣ Verificando Makefile..." -ForegroundColor Cyan
if (Test-Path "Makefile") {
    Write-Status "OK" "Makefile existe"
    
    $makefileContent = Get-Content "Makefile" -Raw
    $requiredTargets = @("tooling-build", "tooling-validate", "security-scan", "k8s-demo")
    foreach ($target in $requiredTargets) {
        if ($makefileContent -match "^${target}:") {
            Write-Status "OK" "Target '$target' definido"
        } else {
            Write-Status "FAIL" "Target '$target' no encontrado"
        }
    }
} else {
    Write-Status "FAIL" "Makefile no encontrado"
}
Write-Host ""

# 8. Verificar Hub CLI
Write-Host "8️⃣ Verificando Hub CLI..." -ForegroundColor Cyan
if (Test-Path "hub.sh") {
    Write-Status "OK" "hub.sh existe"
} else {
    Write-Status "FAIL" "hub.sh no encontrado"
}

if (Test-Path "hub.ps1") {
    Write-Status "OK" "hub.ps1 existe"
} else {
    Write-Status "FAIL" "hub.ps1 no encontrado"
}
Write-Host ""

# Resumen final
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "📊 Resumen de Verificación" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Errores:      $($script:Errors)" -ForegroundColor $(if ($script:Errors -gt 0) { "Red" } else { "Green" })
Write-Host "Advertencias: $($script:Warnings)" -ForegroundColor $(if ($script:Warnings -gt 0) { "Yellow" } else { "Green" })
Write-Host ""

if ($script:Errors -gt 0) {
    Write-Host "❌ Verificación FALLIDA - Hay errores críticos que deben corregirse" -ForegroundColor Red
    exit 1
} elseif ($script:Warnings -gt 0) {
    Write-Host "⚠️  Verificación COMPLETADA con advertencias" -ForegroundColor Yellow
    Write-Host "   Revisa las advertencias para mejorar la seguridad" -ForegroundColor Yellow
    exit 0
} else {
    Write-Host "✅ Verificación EXITOSA - Todas las medidas de seguridad están implementadas" -ForegroundColor Green
    exit 0
}
