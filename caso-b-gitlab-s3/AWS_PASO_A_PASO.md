# ☁️ Guía Paso a Paso: S3 Static Website Hosting (Caso B)

Este caso enseña la forma "clásica" y artesanal de alojar sitios web estáticos en AWS: Usando un **Bucket S3** configurado como servidor web.

---

## 🛠️ 1. Prerrequisitos

1.  **AWS CLI** configurado: `aws configure`.
2.  Un nombre de bucket **único en todo el mundo** (ej: `tu-nombre-caso-b-2026`).

---

## 🚀 2. Flujo de Trabajo (Automatizado con Make)

Hemos simplificado el proceso de sincronización en el `Makefile`.

### Paso A: Crear y Configurar el Bucket (Manual - Una sola vez)
S3 Website Hosting requiere configuración manual específica para ser público.

1.  **Crear Bucket**:
    ```bash
    aws s3 mb s3://<TU_NOMBRE_DE_BUCKET> --region us-east-2
    ```
2.  **Hacerlo Público**:
    *   Ve a la consola de S3 -> Tu Bucket -> Permissions.
    *   Desactiva "Block all public access".
    *   Añade una Bucket Policy para permitir lectura pública (`s3:GetObject`).
3.  **Activar Hosting Estático**:
    *   Ve a Properties -> Static website hosting -> Enable.
    *   Index document: `index.html`.

### Paso B: Desplegar/Sincronizar
Una vez creado el bucket, puedes subir cambios ilimitadas veces usando nuestro comando.
**Importante:** Debes especificar tu bucket si no usas el por defecto.

```bash
# Sincroniza la carpeta local con el bucket en la nube
make deploy-b S3_BUCKET=<TU_NOMBRE_DE_BUCKET>
```

> **¿Qué hace esto?**
> Ejecuta `aws s3 sync`, subiendo solo los archivos modificados y borrando los que eliminaste localmente.

---

## 👀 3. Verificación

La URL de tu sitio seguirá este formato:
`http://<TU_NOMBRE_DE_BUCKET>.s3-website.<REGION>.amazonaws.com`

Ejemplo:
`http://vladimir-caso-b-site-2026.s3-website.us-east-2.amazonaws.com`

---

## 🧹 4. Limpieza

Para eliminar el bucket y evitar costos (aunque son ínfimos en S3):

1.  **Vaciar el bucket**:
    ```bash
    aws s3 rm s3://<TU_NOMBRE_DE_BUCKET> --recursive
    ```
2.  **Eliminar el bucket**:
    ```bash
    aws s3 rb s3://<TU_NOMBRE_DE_BUCKET>
    ```
