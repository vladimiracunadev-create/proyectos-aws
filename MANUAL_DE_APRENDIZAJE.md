# 📘 Manual de Aprendizaje: La Guía del Novato

¡Bienvenido! 👋 Si estás aquí, es porque quieres entender qué hay "bajo el capó" de este proyecto. Piensa en este repositorio como un **Gimnasio de Arquitectura Cloud**. Cada carpeta es una máquina de ejercicios diferente, y los archivos sueltos son las reglas del gimnasio y las herramientas de limpieza.

Este documento te explicará **en español simple** (sin tecnicismos innecesarios) qué hace cada cosa y por qué existe.

---

## 🏗️ Los Fundamentos: ¿Qué estamos usando?

### 1. Git (La Máquina del Tiempo)
Es el sistema que guarda el historial de todo.
*   **¿Por qué lo usamos?**: Para poder "volver al pasado" si rompemos algo y para trabajar en equipo sin sobreescribir el trabajo del otro.

### 2. GitLab (La Fábrica de Robots)
GitLab no es solo donde guardamos el código; tiene "robots" (CI/CD) que trabajan por nosotros.
*   **¿Qué hacen?**: Cada vez que subes un cambio, un robot se despierta, descarga tu código, revisa si está bien escrito (Linting) y, si es el caso, lo despliega en la nube.

### 3. AWS (El Terreno en la Nube)
Es Amazon Web Services. Es donde "viven" nuestras aplicaciones (servidores, bases de datos, almacenamiento).
*   **El objetivo**: Este proyecto te enseña a construir edificios (apps) en este terreno usando diferentes métodos.

### 4. Node.js & NPM (La Caja de Herramientas)
Aunque despleguemos infraestructura, usamos herramientas creadas en JavaScript para gestionar el proyecto.
*   **Node.js**: El motor que permite correr las herramientas.
*   **NPM**: El gestor de paquetes. Es como una "App Store" de librerías para programadores.

---

## 📂 Tour de Archivos: ¿Qué es esto y para qué sirve?

### ⚙️ Archivos de Configuración (Los Cerebros)

#### `package.json` 🆔
**Analogía**: Es el **DNI** y el **Libro de Recetas** del proyecto.
*   **DNI**: Dice cómo se llama el proyecto, la versión y quién lo creó.
*   **Recetas (Scripts)**: Define comandos cortos para tareas largas.
    *   `npm run lint` -> "Oye robot, revisa si escribí bien el código".
    *   `npm run format` -> "Oye robot, ordena mi código para que se vea bonito".
*   **Dependencias**: Una lista de compras de las herramientas que necesitamos instalar para que esto funcione.

#### `.gitlab-ci.yml` 🤖
**Analogía**: Es el **Manual de Instrucciones del Robot**.
*   Le dice a GitLab qué hacer paso a paso cuando subes código.
*   Ejemplo: "Primero descarga Node.js, luego instala las dependencias, luego corre el linter, y si todo sale bien, sube los archivos a AWS".

#### `.eslintrc.js` 👮‍♂️
**Analogía**: El **Policía de Tránsito**.
*   Define las leyes del código. Ejemplo: "No puedes dejar variables sin usar", "No puedes usar `var` antiguo".
*   Si rompes una regla, te pone una "multa" (error) y no te deja avanzar hasta que lo arregles.

#### `.prettierrc` 🎨
**Analogía**: El **Estilista**.
*   Se asegura de que todos escriban con el mismo estilo: ¿Usamos comillas dobles o simples? ¿Ponemos punto y coma al final?
*   Hace que el código se vea uniforme, sin importar quién lo escribió.

#### `.gitignore` 🙈
**Analogía**: La **Lista de cosas ignoradas**.
*   Le dice a Git qué archivos NO debe guardar.
*   Por ejemplo: `node_modules` (que pesa muchísimo y se puede regenerar) o archivos con contraseñas secretas.

---

## 🗺️ Los Niveles (Carpetas `caso-*`)

Cada carpeta es un nivel de dificultad progresiva:

*   **`caso-a-amplify` (Nivel Bebé)**: Usas una herramienta que hace todo mágico (Amplify). Es fácil, pero tienes poco control.
*   **`caso-b-gitlab-s3` (Nivel Manual)**: Aquí aprendes a subir archivos "a mano" (con scripts) a un almacenamiento simple (S3). Entiendes las bases.
*   **`caso-c-terraform-s3` (Nivel Profesional)**: Usas "Infraestructura como Código". Es el estándar de la industria.
    *   **Estado**: ✅ Desplegado en [https://d3otfpeykrm536.cloudfront.net/](https://d3otfpeykrm536.cloudfront.net/)
    *   **¿Qué aprendemos?**: A escribir código (HCL) que crea recursos reales en AWS (S3, CloudFront) de forma automática.
*   **`caso-g-containers-ecs` (Nivel Experto)**: Despliegas aplicaciones complejas usando Docker y orquestadores. Esto es lo que usan las grandes empresas.

---

## 🚀 ¿Cómo se conecta todo?

1.  Haces un cambio en tu PC.
2.  Corres `npm run lint` para verificar que el Policía (`eslint`) no te multe.
3.  Haces `git commit`. Aquí `Husky` (el portero) verifica tus mensajes.
4.  Haces `git push`.
5.  GitLab lee `.gitlab-ci.yml`, despierta al robot y ejecuta las tareas.
6.  ¡Tu cambio llega a la nube (AWS)!

---

¿Listo para aprender? **¡Empieza explorando las carpetas y rompiendo cosas!** Es la mejor forma de aprender.
