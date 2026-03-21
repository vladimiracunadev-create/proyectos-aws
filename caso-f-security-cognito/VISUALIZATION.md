# Reporte de Visualizacion y Resultados - Caso F (Security First)

## Por que existe este documento?

El Caso F tiene una logica de evidencia distinta a la de un caso serverless simple:

- el `DEMO` principal puede quedar vivo porque su costo base es practicamente cero
- la pagina WAF auxiliar no conviene dejarla activa indefinidamente porque AWS WAF agrega costo fijo mensual

Por esa razon, este documento sigue la misma regla que ya aparece en los casos del repositorio con costo fijo:

**Deploy -> Validar -> Capturar -> Destroy**

> [!IMPORTANT]
> `VISUALIZATION.md` no describe otro producto.
>
> Describe:
> - la ventana real de evidencia de la pagina WAF
> - la relacion correcta entre `DEMO` y WAF
> - las capturas que deben salir de AWS y del navegador
> - el cierre FinOps del stack auxiliar

---

## Despliegue validado del laboratorio

Durante esta ventana se validaron estas URLs reales:

- `DEMO principal`: [https://tmi7kgebl9.execute-api.us-east-2.amazonaws.com/](https://tmi7kgebl9.execute-api.us-east-2.amazonaws.com/)
- `Pagina WAF auxiliar`: [https://2i88ijfu54.execute-api.us-east-2.amazonaws.com/Prod](https://2i88ijfu54.execute-api.us-east-2.amazonaws.com/Prod)

Estado esperado del laboratorio:

- `DEMO`: puede seguir activo
- `Pagina WAF`: debe destruirse al terminar la ventana de evidencia

---

## Resumen de la implementacion

El producto principal del Caso F vive en el `DEMO`. Ahi el usuario:

1. crea una cuenta real en Cognito
2. inicia sesion
3. obtiene un `idToken`
4. abre `/profile`

Eso demuestra identidad y autorizacion nativa.

La pagina WAF existe para completar la misma historia de seguridad:

- mismo usuario
- mismo `User Pool`
- mismo `idToken`
- pero otra puerta de entrada: `REST API + Cognito Authorizer + WAF`

La explicacion correcta para un novato es:

- el `DEMO` responde `quien eres`
- la pagina WAF responde `que trafico ni siquiera deberia entrar`

### Logros tecnicos

- `HTTP API + JWT Authorizer` para el `DEMO`
- `REST API + Cognito Authorizer + WAF` para la pagina auxiliar
- `User Pool` compartido entre ambas piezas
- prueba real de `403` antes de la Lambda
- estrategia FinOps para destruir solo la capa WAF

> [!CAUTION]
> **ESTRATEGIA FINOPS**
>
> La pagina WAF agrega costo fijo aproximado de `~$7 USD/mes` mientras exista:
> - `Web ACL`: ~`$5 USD/mes`
> - `2 managed rule groups`: ~`$2 USD/mes`
>
> Por eso esta capa se levanta solo durante la ventana de evidencia y luego se destruye.

---

## Preparacion de la sesion de captura

### 1. Desplegar el DEMO

```bash
cd caso-f-security-cognito/backend
sam build
sam deploy --stack-name caso-f-security-cognito --region us-east-2 --resolve-s3 --capabilities CAPABILITY_IAM --no-confirm-changeset --no-fail-on-empty-changeset
```

### 2. Recuperar outputs del DEMO

```bash
aws cloudformation describe-stacks \
  --stack-name caso-f-security-cognito \
  --region us-east-2 \
  --query "Stacks[0].Outputs"
```

Debes guardar:

- `ApiBaseUrl`
- `UserPoolId`
- `UserPoolArn`
- `UserPoolClientId`

### 3. Desplegar la pagina WAF con la misma identidad del DEMO

```bash
cd caso-f-security-cognito/backend
sam build --template-file template-visualization.yaml
sam deploy --template-file template-visualization.yaml \
  --stack-name caso-f-security-cognito-visualization \
  --region us-east-2 \
  --resolve-s3 \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides \
    DemoPageUrl=https://tmi7kgebl9.execute-api.us-east-2.amazonaws.com/ \
    ExistingUserPoolArn=arn:aws:cognito-idp:us-east-2:689978033715:userpool/us-east-2_B3eYYMIQ9 \
    ExistingUserPoolId=us-east-2_B3eYYMIQ9 \
    ExistingUserPoolClientId=657959dqo83ovffn0qrjmfpn4l
```

### 4. Enlazar el DEMO con la pagina WAF

```bash
cd caso-f-security-cognito/backend
sam deploy \
  --stack-name caso-f-security-cognito \
  --region us-east-2 \
  --resolve-s3 \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides SupportPageUrl=https://2i88ijfu54.execute-api.us-east-2.amazonaws.com/Prod
```

---

## Nota sobre idioma de la consola AWS

AWS puede mostrar menus en ingles o en espanol. En este documento, cuando aparezca un nombre de menu, interpretalo asi:

- `Stacks` = `Pilas`
- `Overview` = `Informacion general` o `Resumen`
- `Outputs` = `Salidas`
- `APIs` = `API`
- `Routes` = `Rutas`
- `Authorizers` = `Autorizadores`
- `User pools` = `Pools de usuarios`
- `Web ACLs` = `Web ACLs`
- `Associated AWS resources` = `Recursos AWS asociados`
- `Functions` = `Funciones`
- `Configuration` = `Configuracion`

> [!IMPORTANT]
> Si no encuentras un recurso, lo mas comun es una de estas tres cosas:
> 1. estas en otra region distinta de `us-east-2`
> 2. la pagina WAF ya fue destruida
> 3. estas mirando el stack equivocado (`caso-f-security-cognito` vs `caso-f-security-cognito-visualization`)

---

## Problema real que un novato suele tener en Windows

En PowerShell, `curl` suele ser alias de `Invoke-WebRequest`.

Si un comando con `curl -X` falla, usa:

```powershell
curl.exe "https://tmi7kgebl9.execute-api.us-east-2.amazonaws.com/health"
```

o bien:

```powershell
Invoke-RestMethod "https://tmi7kgebl9.execute-api.us-east-2.amazonaws.com/health"
```

---

## Orden recomendado de ventanas

No intentes capturar todo en una sola pestana. Este caso tiene varios estados visuales que se pisan entre si:

1. Ventana A: `DEMO` hero inicial
2. Ventana B: `DEMO` flujo antes de interactuar
3. Ventana C: `DEMO` login exitoso y token visible
4. Ventana D: `DEMO` `/profile` con identidad validada
5. Ventana E: pagina WAF recien cargada
6. Ventana F: pagina WAF con el mismo token del `DEMO`
7. Ventana G: pagina WAF despues del `403`
8. Consola AWS 1: CloudFormation
9. Consola AWS 2: Cognito
10. Consola AWS 3: API Gateway
11. Consola AWS 4: WAF

---

## Galeria de evidencias (flujo de despliegue)

### 1. Stack base del DEMO desplegado (CloudFormation)
> **Instrucciones paso a paso**:
> 1. Ve a **CloudFormation**.
> 2. Verifica region `us-east-2`.
> 3. Entra a **Stacks** (`Pilas`).
> 4. Busca `caso-f-security-cognito`.
> 5. Haz clic en el stack.
> 6. **Captura**: muestra:
>    - `Stack name: caso-f-security-cognito`
>    - `Status: CREATE_COMPLETE` o `UPDATE_COMPLETE`
>    - output `ApiBaseUrl`
>    - output `UserPoolId`

![CloudFormation DEMO](./img/case-f-demo-stack.png "Stack principal del Caso F")

### 2. DEMO principal - hero inicial
> **Instrucciones paso a paso**:
> 1. Abre `https://tmi7kgebl9.execute-api.us-east-2.amazonaws.com/`
> 2. No hagas clic todavia.
> 3. **Captura**: muestra:
>    - el titulo principal
>    - la explicacion del producto
>    - la idea de identidad primero y WAF despues

![DEMO Hero](./img/case-f-demo-hero.png "Landing principal del DEMO")

### 3. DEMO principal - token emitido
> **Instrucciones paso a paso**:
> 1. Crea un usuario.
> 2. Haz login.
> 3. **Captura**: muestra:
>    - token visible parcialmente
>    - mensaje de copiar token para la pagina WAF
>    - feedback de login exitoso

![DEMO Token](./img/case-f-demo-token.png "Token emitido por el DEMO")

### 4. DEMO principal - identidad validada en `/profile`
> **Instrucciones paso a paso**:
> 1. Ejecuta `/profile`.
> 2. **Captura**: muestra:
>    - `email`
>    - `sub`
>    - mensaje que indica pasar luego a WAF

![DEMO Profile](./img/case-f-demo-profile.png "Identidad validada en el DEMO")

### 5. Stack WAF desplegado (CloudFormation)
> **Instrucciones paso a paso**:
> 1. Vuelve a **CloudFormation > Stacks** (`CloudFormation > Pilas`).
> 2. Busca `caso-f-security-cognito-visualization`.
> 3. Haz clic en el stack.
> 4. **Captura**: muestra:
>    - `ApiBaseUrl`
>    - `WebAclArn`
>    - estado `CREATE_COMPLETE` o `UPDATE_COMPLETE`

![CloudFormation WAF](./img/case-f-waf-stack.png "Stack WAF auxiliar")

### 6. Cognito - mismo User Pool del DEMO
> **Instrucciones paso a paso**:
> 1. Ve a **Amazon Cognito > User pools** (`Amazon Cognito > Pools de usuarios`).
> 2. Abre el pool del `DEMO`.
> 3. **Captura**: muestra:
>    - `UserPoolId`
>    - `App client`
>    - politica de password
>
> Esta captura es importante porque explica que la pagina WAF no inventa otra identidad.

![Cognito Shared Pool](./img/case-f-cognito-shared-pool.png "User Pool compartido")

### 7. Pagina WAF - estado inicial explicativo
> **Instrucciones paso a paso**:
> 1. Abre `https://2i88ijfu54.execute-api.us-east-2.amazonaws.com/Prod`
> 2. No pegues token todavia.
> 3. **Captura**: muestra:
>    - la explicacion `mismo usuario, mismo token, otro front door`
>    - la referencia al `DEMO`
>    - la instruccion de pegar el mismo token

![WAF Intro](./img/case-f-waf-intro.png "Landing explicativa del WAF")

### 8. Pagina WAF - mismo token del DEMO
> **Instrucciones paso a paso**:
> 1. Copia el `idToken` del `DEMO`.
> 2. Pegalo en la pagina WAF.
> 3. Ejecuta la prueba de `/profile`.
> 4. **Captura**: muestra:
>    - `email`
>    - `sub`
>    - mensaje de `misma identidad`
>
> Esta es la captura que hace visible la relacion entre ambos despliegues.

![WAF Shared Identity](./img/case-f-waf-shared-identity.png "Mismo token del DEMO validado en la pagina WAF")

### 9. Pagina WAF - bloqueo `403`
> **Instrucciones paso a paso**:
> 1. Ejecuta la prueba SQLi controlada.
> 2. **Captura**: muestra:
>    - estado `403`
>    - mensaje de bloqueo antes de Lambda

![WAF 403](./img/case-f-waf-403.png "Bloqueo perimetral de WAF")

### 10. API Gateway - DEMO principal
> **Instrucciones paso a paso**:
> 1. Ve a **API Gateway > APIs**.
> 2. Entra al `HTTP API` del `DEMO`.
> 3. Abre **Routes** (`Rutas`).
> 4. **Captura**: muestra:
>    - `GET /`
>    - `GET /health`
>    - `POST /auth/register`
>    - `POST /auth/login`
>    - `GET /profile`
>    - el `JWT Authorizer`

![HTTP API DEMO](./img/case-f-http-api-demo.png "HTTP API del DEMO")

### 11. API Gateway - pagina WAF auxiliar
> **Instrucciones paso a paso**:
> 1. Ve a **API Gateway > APIs**.
> 2. Entra al `REST API` del stack WAF.
> 3. Abre **Resources** (`Recursos`) o la vista equivalente.
> 4. **Captura**: muestra:
>    - `GET /`
>    - `GET /health`
>    - `GET /profile`
>    - el `Cognito Authorizer`

![REST API WAF](./img/case-f-rest-api-waf.png "REST API de la pagina WAF")

### 12. WAF - asociacion del Web ACL
> **Instrucciones paso a paso**:
> 1. Ve a **AWS WAF & Shield > Web ACLs**.
> 2. Abre `caso-f-security-cognito-visualization`.
> 3. Ve a **Associated AWS resources** (`Recursos AWS asociados`).
> 4. **Captura**: muestra:
>    - el `REST API` asociado
>    - las managed rules activas
>    - el `Web ACL`

![WAF Association](./img/case-f-web-acl-associated.png "Web ACL asociado al REST API auxiliar")

---

## Tabla de validacion final

| Hito | Estado esperado | Metodo |
| :--- | :--- | :--- |
| DEMO principal activo | OK | Navegador + CloudFormation |
| Registro y login reales | OK | DEMO |
| `/profile` del DEMO devuelve claims | OK | DEMO |
| Pagina WAF activa | OK | Navegador + CloudFormation |
| Pagina WAF acepta el mismo token del DEMO | OK | `/profile` en stack WAF |
| Bloqueo SQLi devuelve `403` | OK | WAF |
| `Web ACL` asociado al `REST API` | OK | Consola AWS |
| Destruccion de la pagina WAF | CRITICO | CLI + CloudFormation |

---

## Instrucciones de cierre (baja FinOps)

### Alcance seguro de la baja

Debes destruir solo:

- `caso-f-security-cognito-visualization`

No debes destruir:

- `caso-f-security-cognito`

### Comando de eliminacion

```powershell
cd caso-f-security-cognito/backend
sam delete --stack-name caso-f-security-cognito-visualization --region us-east-2 --no-prompts
```

### Verificacion recomendada

```powershell
aws cloudformation describe-stacks --stack-name caso-f-security-cognito-visualization --region us-east-2
aws wafv2 list-web-acls --scope REGIONAL --region us-east-2
aws apigateway get-rest-apis --region us-east-2
```

Resultados esperados:

- el stack WAF ya no existe
- el `Web ACL` del caso ya no aparece
- el `REST API` auxiliar ya no aparece

### Lo que debe seguir vivo

Despues del cierre correcto:

- el `DEMO` principal sigue funcionando
- el producto sigue siendo demostrable
- el costo fijo del WAF queda detenido

---

*Documentacion de evidencia del Caso F. El `DEMO` se mantiene solo en espanol; las referencias EN/ES se usan aqui solo para orientar menus e instrucciones del entorno AWS.*
