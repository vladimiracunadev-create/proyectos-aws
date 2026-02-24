# 🆘 Guía de Resolución de Problemas (TROUBLESHOOTING)

Este manual proporciona soluciones paso a paso para los fallos técnicos más comunes identificados en el ecosistema.

---

## 🏗️ Fallos en el Entorno Local

### 1. Error de Ejecución de Scripts en PowerShell
- **Error**: `UnauthorizedAccess` al intentar correr `.\hub.ps1`.
- **Causa**: La política de ejecución de Windows bloquea scripts de terceros.
- **Solución**:
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```

### 2. Docker Tooling no arranca
- **Error**: `docker: error during connect: ...`.
- **Causa**: El daemon de Docker Desktop no ha iniciado.
- **Solución**: Inicia Docker Desktop, espera al estado "Running" y reinicia la terminal.

---

## ☁️ Problemas de Despliegue (AWS)

### 3. Error en `sync` de S3 (Access Denied)
- **Causa**: Las credenciales en los GitHub Secrets han expirado o el usuario de IAM no tiene permisos sobre el bucket.
- **Solución**: 
  - Verifica que el bucket name en `despliegue.yml` sea correcto.
  - Revisa la **Bucket Policy** en la consola de S3 para asegurar que permite acciones de `PutObject`.

### 4. Amplify falla en el Build
- **Causa**: Fallo al detectar el `appRoot`.
- **Solución**: Verifica que el archivo `amplify.yml` en la raíz coincida exactamente con la estructura de carpetas (case sensitive).

---

## 🌍 Problemas en el Navegador (PWA)

### 5. La web muestra contenido antiguo tras un deploy
- **Causa**: El Service Worker está sirviendo una versión cacheada y no se ha actualizado.
- **Solución**:
  1. Abre el sitio en el navegador.
  2. Pulsa `F12` > pestaña `Application`.
  3. En `Service Workers`, haz clic en `Unregister`.
  4. Recarga la página. 
  - *Nota: Implementar un botón "Update Available" es un hito de la Fase 2 del Roadmap.*

### 6. La página Offline no aparece
- **Causa**: El archivo `offline.html` no se cacheó correctamente durante la instalación.
- **Solución**: Verifica la consola de desarrollador para errores 404 durante el evento `install` en `service-worker.js`.

---

## 🔒 Errores de Seguridad (CI/CD)

### 7. El Pipeline falla por "Secrets Detected"
- **Causa**: Has incluido accidentalmente un token o una palabra que parece una llave.
- **Solución**: 
  - Si es un secreto real: Bórralo, revócalo y haz un nuevo commit.
  - Si es un falso positivo: Añade la firma al `.secrets.baseline` usando:
    ```bash
    detect-secrets scan > .secrets.baseline
    ```

---
*Para reportar errores nuevos que no estén aquí, abre un Issue en GitHub.*
