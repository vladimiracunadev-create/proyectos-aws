# Caso 01 — Guía paso a paso: AWS Amplify Hosting

Guía completa para reproducir este caso desde una cuenta AWS vacía hasta tener
el sitio en producción con despliegue automático por rama.

> **Tiempo estimado:** 15–20 minutos la primera vez. Deploys posteriores: ~2 min automáticos.

---

## Prerrequisitos

| Requisito | Verificación |
|:---|:---|
| Cuenta AWS activa | `aws sts get-caller-identity` |
| Repositorio GitHub con el código | Este mismo repo |
| Rama `main` y `dev` existentes | `git branch -a` |
| `amplify.yml` en la raíz del repo | Ya incluido en este repo |

---

## Paso 1 — Abrir AWS Amplify Console

1. Acceder a [AWS Console](https://console.aws.amazon.com/) → buscar **Amplify** en la barra de servicios
2. Seleccionar región **us-east-1** (recomendada para Amplify — menor latencia de build)
3. Clic en **"All apps"** en el panel izquierdo → **"New app"** → **"Host web app"**

> **Nota:** Si es tu primera vez, verás la pantalla de bienvenida de Amplify. El botón puede
> llamarse "Get Started" bajo "Deliver".

---

## Paso 2 — Conectar repositorio GitHub

1. Seleccionar **GitHub** como proveedor de código fuente → clic **"Continue"**
2. Amplify pedirá autorización OAuth a GitHub — clic **"Authorize aws-amplify"**
3. En el selector de repositorio: buscar `proyectos-aws` → seleccionarlo
4. Seleccionar rama: **`main`** → clic **"Next"**

> **Por qué `main` primero:** Amplify crea la app con la rama principal. Las ramas adicionales
> (`dev`) se conectan en el siguiente paso dentro de la configuración de la app.

---

## Paso 3 — Configurar build settings

Amplify detecta automáticamente que no hay framework y muestra la configuración de build.

**Verificar que `amplify.yml` se está usando** — Amplify tiene prioridad sobre su autodetección
cuando encuentra este archivo en el repo. El contenido relevante es:

```yaml
version: 1
applications:
  - appRoot: caso-01-amplify-hosting    # ← carpeta del caso dentro del monorepo
    frontend:
      phases:
        build:
          commands: []                   # ← sin build: vanilla JS puro
      artifacts:
        baseDirectory: .
        files:
          - '**/*'
```

**Si Amplify no detecta el `amplify.yml`** → en "Build settings" → "Edit" → reemplazar
el YAML autogenerado con el de arriba.

Clic **"Next"**.

---

## Paso 4 — Revisar y desplegar

1. Revisar el resumen: repositorio, rama, configuración de build
2. Clic **"Save and deploy"**
3. Amplify inicia el primer build — la barra de progreso muestra las fases:
   - **Provision** — preparar el entorno de build (~30 seg)
   - **Build** — ejecutar los comandos del `amplify.yml` (~20 seg, sin build commands es casi instantáneo)
   - **Deploy** — subir artefactos a S3 y distribuir en CloudFront (~60 seg)
   - **Verify** — verificación de disponibilidad

> **Build exitoso:** La barra se pone en verde. La URL de producción ya está disponible.

---

## Paso 5 — Conectar la rama `dev`

Para tener el entorno de previsualización automático:

1. En la app de Amplify → panel izquierdo → **"Hosting"** → **"Branches"**
2. Clic **"Connect branch"**
3. Seleccionar rama **`dev`**
4. En build settings: Amplify reutiliza la misma configuración del `amplify.yml`
5. Clic **"Save and deploy"**

**Resultado:** Amplify asigna automáticamente una URL única para `dev`:

- `main` → `https://main.<app-id>.amplifyapp.com`
- `dev`  → `https://dev.<app-id>.amplifyapp.com`

---

## Paso 6 — Verificación completa

### Verificar el deploy en producción

```bash
# La URL varía por app — obtenerla desde Amplify Console
curl -I https://main.d3r1wuymolxagh.amplifyapp.com/

# Respuesta esperada:
# HTTP/2 200
# content-type: text/html
# server: CloudFront
# x-cache: Hit from cloudfront     ← confirma que CDN está activo
```

### Verificar SSL

```bash
# Comprobar el certificado
curl -v https://main.d3r1wuymolxagh.amplifyapp.com/ 2>&1 | grep -E "SSL|TLS|certificate"

# Debe mostrar:
# *  SSL connection using TLSv1.3 / TLS_AES_128_GCM_SHA256
# *  subject: CN=*.amplifyapp.com
```

### Verificar el webhook automático

```bash
# Hacer un cambio y pushear
echo "<!-- test deploy $(date) -->" >> caso-01-amplify-hosting/index.html
git add -A
git commit -m "test: verificar trigger automático de Amplify"
git push origin main

# En Amplify Console → app → rama main → ver nuevo build iniciándose en ~10 segundos
```

### Verificar la PWA

Abrir la URL en Chrome → `F12` → pestaña **"Application"** → **"Service Workers"**:

- Status: `activated and is running`
- Source: `service-worker.js`

---

## Paso 7 — Configurar dominio personalizado (opcional)

Si tienes un dominio propio en Route53:

1. Amplify Console → app → **"Hosting"** → **"Custom domains"** → **"Add domain"**
2. Seleccionar el dominio de Route53 (detectado automáticamente)
3. Amplify crea el certificado ACM y configura los registros DNS — sin intervención manual
4. Tiempo de propagación: 2–5 minutos

---

## Errores comunes y soluciones

### Error: "appRoot not found"

```text
Build failed: The 'appRoot' directory 'caso-01-amplify-hosting' was not found
```

**Causa:** El `amplify.yml` está en la raíz del repo pero la carpeta del caso no existe
o tiene otro nombre.

**Solución:** Verificar que la carpeta existe exactamente como `caso-01-amplify-hosting/`:

```bash
ls -la caso-01-amplify-hosting/
```

---

### Error: Build timeout

**Causa:** Los `build commands` están intentando instalar dependencias innecesarias.

**Solución:** Confirmar que `commands: []` está vacío en el `amplify.yml` — este sitio
es vanilla JS, no necesita `npm install` ni `npm run build`.

---

### Error: Archivos PDF no se sirven

**Causa:** Amplify a veces excluye archivos grandes por defecto.

**Solución:** Verificar en `amplify.yml` que `files: - '**/*'` incluye todos los archivos.
Si persiste, añadir explícitamente:

```yaml
artifacts:
  baseDirectory: .
  files:
    - '**/*'
  exclude:
    - node_modules/**
```

---

### El sitio se despliega pero muestra la carpeta raíz en lugar del caso

**Causa:** `appRoot` no está configurado correctamente.

**Verificación:**

```bash
# El amplify.yml raíz debe tener:
grep -A2 "appRoot" amplify.yml
# Debe mostrar:  appRoot: caso-01-amplify-hosting
```

---

## Costos reales de este caso

| Recurso | Uso típico | Costo |
|:---|:---|:---|
| **Amplify Build** | ~500 min/mes (Free Tier: 1000 min) | $0.00 |
| **Amplify Hosting** | ~5 GB transfer/mes (Free Tier: 15 GB) | $0.00 |
| **CloudFront** | Incluido en Amplify | $0.00 |
| **ACM Certificate** | Incluido | $0.00 |
| **Total estimado** | | **$0.00 / mes** |

> Free Tier cubre este caso completamente durante los primeros 12 meses y probablemente siempre
> dado el tráfico típico de un portafolio personal.

---

## Lo que Amplify gestiona automáticamente

Para entender qué se delega a Amplify vs qué controla GitHub Actions:

| Tarea | Quién la hace | Visible en |
|:---|:---|:---|
| Detectar el push | Amplify webhook | Amplify Console → Activity |
| Provisionar el build container | Amplify | Amplify Console → Build logs |
| Ejecutar `amplify.yml` | Amplify | Amplify Console → Build logs |
| Subir artefactos a S3 | Amplify (S3 interno) | No visible |
| Invalidar caché de CloudFront | Amplify | No visible |
| Servir via CDN global | CloudFront | Headers `x-cache` |
| Renovar certificado SSL | ACM automático | ACM Console |

**Limitación clave:** No puedes añadir steps propios (tests, linters, notificaciones)
sin usar un framework de build o recurrir a un workflow de GitHub Actions separado.
Esta limitación es la motivación del **Caso 02**.

---

## Siguiente paso

-> [Caso 02 — S3 + GitHub Actions](../caso-02-s3-github-actions/AWS_PASO_A_PASO.md): control total del pipeline sin depender de Amplify.
