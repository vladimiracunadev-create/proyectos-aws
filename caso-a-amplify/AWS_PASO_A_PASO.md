# ☁️ Guía Paso a Paso: Despliegue en AWS Amplify (Caso A)

Este caso demuestra la forma más rápida y moderna de desplegar un sitio estático: **AWS Amplify Hosting**. Amplify se conecta a tu repositorio y despliega automáticamente cada vez que haces `git push`.

---

## 🛠️ 1. Prerrequisitos

1.  Tener acceso a tu **Consola de AWS**.
2.  Tener tu código subido a **GitLab** (o GitHub/Bitbucket).

---

## 🚀 2. Flujo de Despliegue (Consola Web)

A diferencia de otros métodos manuales, aquí **AWS hace el trabajo por ti**. Configúralo una vez y olvídate.

### Paso A: Conectar AWS con GitLab
1.  Ingresa a la consola de AWS y busca el servicio **Amplify**.
2.  Haz clic en **"Create New App"** (Crear nueva aplicación) -> **"Host web app"**.
3.  Selecciona **GitLab** como tu proveedor de código.
4.  Autoriza a AWS para leer tus repositorios.

### Paso B: Configurar el Branch
1.  Selecciona tu repositorio: `proyectos-aws-gitlab` (o el nombre que le hayas dado).
2.  Elige la rama: `main` (o la que quieras desplegar).
3.  **Configuración de Monorepo (¡Crucial!):**
    *   Como este proyecto tiene muchas carpetas, debes decirle a Amplify dónde está **este** sitio web.
    *   Edita la configuración de "Monorepo" o "Build Settings".
    *   Asegúrate de que la ruta base apunte a: `caso-a-amplify`.

### Paso C: Desplegar
1.  Haz clic en **"Save and Deploy"**.
2.  AWS Amplify empezará a:
    *   Clonar tu código.
    *   Construir el sitio (si hubiera build steps).
    *   Desplegarlo en una CDN global.

---

## 👀 3. Verificación

En unos minutos, verás tildes verdes en la consola de Amplify.
AWS te dará una URL pública terminada en `.amplifyapp.com`.
¡Ábrela y verás tu sitio en vivo!

---

## 🔄 4. Actualización Automática

Prueba hacer un cambio en `index.html` y súbelo:
```bash
git add caso-a-amplify/index.html
git commit -m "update: cambio en titulo"
git push
```

¡Amplify detectará el cambio y actualizará el sitio automáticamente!

---

## 🧹 5. Limpieza

Si quieres dejar de alojar el sitio:
1.  Ve a la consola de Amplify.
2.  Selecciona tu App.
3.  Acciones -> **Delete App**.
