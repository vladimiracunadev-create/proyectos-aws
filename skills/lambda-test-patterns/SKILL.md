---
name: lambda-test-patterns
description: Patrones de testing con pytest para funciones Lambda en este monorepo. Cubre como mockear boto3 correctamente, cuando probar a traves de handler() vs funciones individuales, estructura de eventos SAM, y los errores de CI mas frecuentes. Usar al escribir o corregir tests en cualquier caso serverless (D, E, F, G, H o futuros).
---

# Lambda Test Patterns

Este skill evita los errores de testing mas frecuentes en los casos serverless de este repositorio.
La mayoria de los fallos de CI tienen la misma causa raiz: no entender donde se capturan las excepciones.

---

## Regla fundamental: ValueError y ClientError solo viven en handler()

En todos los casos serverless de este repositorio, el `handler()` principal tiene un bloque `try/except` que captura:
- `ValueError` — validacion de campos requeridos
- `botocore.exceptions.ClientError` — errores de AWS (recurso no existe, credenciales, etc.)

Las funciones individuales (`handle_register`, `handle_login`, `handle_create_order`, etc.) NO capturan estas excepciones: las propagan hacia arriba.

**Consecuencia directa para los tests:**

```python
# MAL — este test fallara porque handle_register() NO captura ValueError
def test_registro_sin_email():
    event = {"body": json.dumps({"password": "123456"})}
    response = app.handle_register(event)  # Lanza ValueError, no retorna 400

# BIEN — pasar por handler() donde SI se captura la excepcion
def test_registro_sin_email():
    event = {
        "requestContext": {"http": {"method": "POST"}},
        "rawPath": "/auth/register",
        "body": json.dumps({"password": "123456"})
    }
    response = app.handler(event, None)
    assert response["statusCode"] == 400
```

Regla practica: **si el test espera un 400 o 500 por una excepcion, debe llamar a `app.handler(event, None)`**.

---

## Como mockear boto3 correctamente

### El patron correcto: parchear el cliente en el modulo app

En `app.py`, el cliente boto3 se crea a nivel de modulo:

```python
# En app.py
dynamodb = boto3.resource("dynamodb")
cognito_client = boto3.client("cognito-idp")
```

El mock correcto parchea el objeto ya creado en el modulo `app`, no `boto3` globalmente:

```python
# BIEN — parchea el cliente que ya existe en app
@patch("app.dynamodb")
def test_crear_orden(mock_dynamodb):
    mock_table = MagicMock()
    mock_dynamodb.Table.return_value = mock_table
    mock_table.put_item.return_value = {}
    ...

# BIEN — para cognito
@patch("app.cognito_client")
def test_login(mock_cognito):
    mock_cognito.initiate_auth.return_value = {
        "AuthenticationResult": {
            "AccessToken": "token-falso",
            "IdToken": "id-token-falso",
            "RefreshToken": "refresh-token-falso"
        }
    }
    ...
```

```python
# MAL — parchear boto3 directamente no funciona si el cliente ya fue creado
@patch("boto3.client")  # Demasiado tarde: app.py ya creo el cliente al importar
def test_login(mock_boto3):
    ...
```

---

## Estructura del event dict para cada tipo de ruta

El evento que recibe `handler()` simula lo que API Gateway HTTP envia a Lambda.

### GET sin parametros

```python
event = {
    "requestContext": {"http": {"method": "GET"}},
    "rawPath": "/health",
    "queryStringParameters": None,
    "body": None
}
```

### POST con body JSON

```python
event = {
    "requestContext": {"http": {"method": "POST"}},
    "rawPath": "/auth/register",
    "body": json.dumps({"email": "test@test.com", "password": "Test1234!"}),
    "queryStringParameters": None
}
```

### GET con ruta protegida por JWT Authorizer

Cuando API Gateway valida el JWT, agrega los claims al evento bajo `requestContext.authorizer.jwt.claims`:

```python
event = {
    "requestContext": {
        "http": {"method": "GET"},
        "authorizer": {
            "jwt": {
                "claims": {
                    "sub": "uuid-del-usuario",
                    "email": "test@test.com",
                    "cognito:username": "test@test.com"
                }
            }
        }
    },
    "rawPath": "/profile",
    "body": None,
    "queryStringParameters": None
}
```

### GET con query string

```python
event = {
    "requestContext": {"http": {"method": "GET"}},
    "rawPath": "/orders",
    "queryStringParameters": {"customer_id": "CUST-001"},
    "body": None
}
```

---

## Como simular errores de AWS (ClientError)

```python
from botocore.exceptions import ClientError

def make_client_error(code, message="error simulado"):
    return ClientError(
        {"Error": {"Code": code, "Message": message}},
        "operation_name"
    )

# Uso en test
@patch("app.cognito_client")
def test_usuario_ya_existe(mock_cognito):
    mock_cognito.sign_up.side_effect = make_client_error("UsernameExistsException")
    event = {
        "requestContext": {"http": {"method": "POST"}},
        "rawPath": "/auth/register",
        "body": json.dumps({"email": "existing@test.com", "password": "Test1234!"})
    }
    response = app.handler(event, None)
    assert response["statusCode"] == 409
```

Codigos de ClientError frecuentes en este repositorio:

| Codigo | Caso | HTTP esperado |
|---|---|---|
| `UsernameExistsException` | F — Cognito | 409 |
| `NotAuthorizedException` | F — Cognito | 401 |
| `UserNotFoundException` | F — Cognito | 404 |
| `ResourceNotFoundException` | D, E — DynamoDB | 404 |
| `ConditionalCheckFailedException` | E — DynamoDB | 409 |
| `ProvisionedThroughputExceededException` | D, E | 429 |

---

## Estructura recomendada de un archivo test_app.py

```python
import json
import pytest
from unittest.mock import patch, MagicMock
from botocore.exceptions import ClientError
import app

# Helper para eventos comunes
def post_event(path, body):
    return {
        "requestContext": {"http": {"method": "POST"}},
        "rawPath": path,
        "body": json.dumps(body),
        "queryStringParameters": None
    }

def get_event(path, claims=None):
    ctx = {"http": {"method": "GET"}}
    if claims:
        ctx["authorizer"] = {"jwt": {"claims": claims}}
    return {
        "requestContext": ctx,
        "rawPath": path,
        "body": None,
        "queryStringParameters": None
    }

def client_error(code):
    return ClientError({"Error": {"Code": code, "Message": ""}}, "op")

# --- Tests del happy path (llaman a funciones directamente o a handler) ---
class TestHealthEndpoint:
    def test_health_returns_200(self):
        event = get_event("/health")
        response = app.handler(event, None)
        assert response["statusCode"] == 200

# --- Tests de validacion (SIEMPRE a traves de handler) ---
class TestValidacion:
    def test_registro_sin_email_retorna_400(self):
        response = app.handler(post_event("/auth/register", {"password": "pw"}), None)
        assert response["statusCode"] == 400

# --- Tests de errores AWS (SIEMPRE a traves de handler) ---
class TestErroresAWS:
    @patch("app.cognito_client")
    def test_usuario_duplicado_retorna_409(self, mock_cognito):
        mock_cognito.sign_up.side_effect = client_error("UsernameExistsException")
        response = app.handler(post_event("/auth/register", {"email": "a@a.com", "password": "pw"}), None)
        assert response["statusCode"] == 409
```

---

## Errores frecuentes en CI y su solucion

### "ValueError: Campos requeridos: email"
- Causa: el test llama a `app.handle_register(event)` directamente
- Solucion: cambiar a `app.handler(event, None)` con el evento completo

### "botocore.exceptions.ClientError: UsernameExistsException"
- Causa: igual que el anterior, el test llama a la funcion directamente
- Solucion: pasar por handler()

### "AttributeError: 'NoneType' object has no attribute 'put_item'"
- Causa: el mock de DynamoDB no devuelve una tabla
- Solucion: `mock_dynamodb.Table.return_value = mock_table` antes de llamar a la funcion

### "KeyError: 'body'"
- Causa: el event dict del test no tiene la clave `body`
- Solucion: agregar `"body": None` o `"body": json.dumps({...})`

---

## Instalacion de dependencias para tests locales

```bash
pip install pytest boto3 botocore

# Ejecutar tests de un caso
pytest caso-X-nombre/backend/tests/ -v --tb=short

# O via Makefile
make test-X
```

Las dependencias de test NO deben estar en `requirements.txt` del Lambda (solo en desarrollo).
En el `.gitlab-ci.yml`, el job de test instala `pytest boto3` antes de correr los tests.
