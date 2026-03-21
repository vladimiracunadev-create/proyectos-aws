# VISUALIZATION - Costo, Ventana WAF y Cierre Seguro

## Regla de lectura

En el Caso F:

- `DEMO` es el producto principal y la URL que demuestra el flujo completo.
- La pagina WAF es un despliegue auxiliar enlazado desde el DEMO.
- `VISUALIZATION.md` no describe otro producto: documenta costo, ventana de uso y destruccion segura del stack WAF.

## Que controla este documento

Este archivo responde solo estas preguntas:

1. cuando conviene levantar el stack WAF
2. cuanto cuesta mantenerlo encendido
3. que evidencia debe sacarse mientras esta activo
4. como apagarlo al terminar

## Modelo operativo

| Elemento | Rol | Estado recomendado |
|---|---|---|
| `DEMO` | Producto principal con Cognito + HTTP API + JWT Authorizer | Puede quedar vivo |
| Pagina WAF auxiliar | Explica el perimetro y prueba el bloqueo con WAF | Levantar solo cuando se necesite evidencia |
| `VISUALIZATION.md` | Control de costo y procedimiento de cierre | Siempre presente en el repo |

## Costo

El costo base del Caso F sigue siendo:

- `DEMO`: `$0`
- Pagina WAF auxiliar: `~$7/mes` mientras el stack exista

Ese costo viene de:

- `Web ACL`: ~`$5/mes`
- `2 managed rule groups`: ~`$2/mes`

## Cuando levantar la pagina WAF

Activa el stack WAF solo en estas situaciones:

- necesitas capturas reales del perimetro
- quieres demostrar un `403` antes de la Lambda
- estas preparando una revision tecnica o una entrevista

Si no necesitas esa evidencia puntual, mantente solo en el `DEMO`.

## Comandos de ventana WAF

```bash
cd caso-f-security-cognito/backend

sam build --template-file template-visualization.yaml
sam deploy --template-file template-visualization.yaml \
  --stack-name caso-f-security-cognito-visualization \
  --region us-east-2 \
  --resolve-s3 \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides DemoPageUrl=https://<demo-url>
```

## Evidencia minima a capturar mientras esta activa

La captura funcional del producto sale del `DEMO`.

De la pagina WAF auxiliar solo necesitas evidencia de:

- landing explicativa del despliegue WAF
- `GET /health` respondiendo `200`
- prueba SQLi controlada devolviendo `403`
- `AWS WAF & Shield > Web ACLs` mostrando la asociacion

## Senal de que ya puedes destruirla

Puedes destruir el stack WAF cuando ya tengas:

- URL del `DEMO`
- capturas funcionales del producto
- captura de la pagina WAF
- captura del bloqueo `403`
- captura de la asociacion del `WebACL`

## Destruccion segura

```bash
cd caso-f-security-cognito/backend

sam delete --stack-name caso-f-security-cognito-visualization \
  --region us-east-2 \
  --no-prompts
```

## Checklist de cierre

| Punto | Estado esperado |
|---|---|
| DEMO sigue vivo | SI |
| Pagina WAF ya fue explicada/capturada | SI |
| Prueba SQLi devolvio `403` | SI |
| Stack WAF destruido | SI |
| Costo fijo detenido | SI |

## Frase guia

La idea del Caso F es simple: dejar el producto principal siempre claro y barato, y usar la pagina WAF solo durante la ventana exacta en que necesitas demostrar la capa perimetral.
