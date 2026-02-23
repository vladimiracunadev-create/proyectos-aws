# ☁️ AWS Paso a Paso: Amplify Deployment

Esta guía detalla el proceso para configurar y desplegar este portafolio utilizando **AWS Amplify**.

## 1. Requisitos Previos

- Cuenta de AWS activa.
- Repositorio conectado (GitHub/GitLab).

## 2. Configuración en la Consola de AWS

1. **Ir a AWS Amplify Console:** Busca "Amplify" en el panel de AWS.
2. **Conectar App:** Selecciona "New app" > "Host web app".
3. **Elegir Proveedor:** Selecciona GitHub/GitLab y autoriza el acceso.
4. **Seleccionar Repositorio:** Escoge el repositorio `proyectos-aws`.
5. **Ajustes de Build:**
   - Amplify detectará automáticamente la configuración.
   - **IMPORTANTE:** En la configuración de la aplicación, asegúrate de que el directorio base apunte a `aws-amplify-mi-sitio-1/`.
   - Verifica que el archivo `amplify.yml` en la raíz del monorepo gestione correctamente este subdirectorio.

## 3. Estrategia de Ramas

Amplify permite el despliegue automático por rama:
- **Rama `main`**: URL de producción (ej. `https://main.id.amplifyapp.com`).
- **Rama `dev`**: URL de pruebas/staging (ej. `https://dev.id.amplifyapp.com`).

## 4. Dominio Personalizado y SSL

1. En la consola de Amplify, ve a "Domain management".
2. Haz clic en "Add domain".
3. Amplify gestionará automáticamente el certificado **SSL (HTTPS)** a través de AWS Certificate Manager (ACM).

## 5. Verificación

Una vez finalizado el build, Amplify proporcionará una URL pública. Puedes verificar el estado directamente en la consola o ver los registros de construcción en tiempo real.
