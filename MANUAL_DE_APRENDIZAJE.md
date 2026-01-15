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

## 🔬 Deep Dive: Análisis de los Casos

Aquí explicamos el porqué, el cómo y la importancia de cada enfoque.

### 🐣 Caso A: AWS Amplify (El Camino Rápido)
**Ubicación:** `./caso-a-amplify/`

**¿Qué es?**
AWS Amplify es como un "mayordomo" que hace todo por ti. Tú solo le das tu código y él configura el servidor, el dominio, el HTTPS y las actualizaciones automáticas.

**Archivos Clave:**
*   `amplify.yml`: Es el único archivo de configuración que necesitas aquí. Le dice a Amplify cómo "construir" tu sitio (por ejemplo, si necesitas instalar dependencias antes de copiar los archivos HTML).

**Alcance e Importancia:**
*   **Ideal para:** Prototipos rápidos, hackathons, sitios personales simples.
*   **Limitación:** Si quieres hacer algo muy específico fuera de lo "estándar", pelar con Amplify puede ser difícil. Es "magia negra": funciona genial, pero difícil saber qué pasa por dentro.
*   **Lección:** Aprendes la velocidad de entrega.

### 🛠️ Caso B: GitLab CI + S3 (El Camino Artesanal)
**Ubicación:** `./caso-b-gitlab-s3/`

**¿Qué es?**
Aquí le quitamos la magia. Creamos un bucket S3 (una carpeta en la nube) manualmente y configuramos un pipeline de GitLab para que copie nuestros archivos allí.

**Archivos Clave:**
*   `.gitlab-ci.yml`: Aquí escribimos los comandos explícitos.
    *   `deploy: script: aws s3 sync . s3://mi-bucket`: Literalmente le decimos "copia estos archivos a ese bucket".
    *   **Variables**: Usamos variables de entorno ( $AWS_ACCESS_KEY_ID ) para no guardar contraseñas en el código.

**Alcance e Importancia:**
*   **Ideal para:** Entender los fundamentos de CI/CD.
*   **Importancia:** Aprendes que "la nube" no es magia, son comandos de Linux ejecutándose en servidores de otra persona. Aprendes sobre permisos (IAM) y automatización básica.

### 🏗️ Caso C: Terraform (El Camino Profesional - IaC)
**Ubicación:** `./caso-c-terraform-s3/`

**¿Qué es?**
**Infraestructura como Código (IaC)**. En lugar de crear el bucket con clicks en la consola (que es propenso a errores humanos), escribimos un archivo de texto que *describe* la infraestructura deseada. Terraform lee ese archivo y hace que la realidad coincida con él.

**Archivos Clave:**
*   `main.tf`: El plano arquitectónico. Dice "Quiero un bucket, quiero una distribución de CloudFront, quiero una política de acceso".
*   `variables.tf`: Los parámetros ajustables (nombre del proyecto, región).
*   `terraform.tfstate`: ¡CRÍTICO! Es la "memoria" de Terraform. Guarda el estado actual de tu infraestructura para saber qué cambiar la próxima vez. *Nota: En equipos reales, esto se guarda en la nube, no en tu PC.*

**Alcance e Importancia:**
*   **Ideal para:** Empresas, equipos grandes, proyectos de producción.
*   **Importancia:**
    *   **Reproducibilidad**: Puedes crear 10 copias exactas del entorno en segundos.
    *   **Auditoría**: Puedes ver en el historial de Git quién cambió la infraestructura y por qué.
    *   **Seguridad**: Evita errores manuales como dejar un bucket público por accidente.
    *   **Estado Actual**: ✅ Desplegado en [https://d3otfpeykrm536.cloudfront.net/](https://d3otfpeykrm536.cloudfront.net/)

### 🚀 Próximos Pasos (Proyectados)

*   **Caso G (Contenedores)**: Para cuando un simple HTML no basta y necesitas correr una API completa (Node.js/Python) en la nube de forma aislada y escalable.

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
