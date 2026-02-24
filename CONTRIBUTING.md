# 🤝 Guía de Contribución

Este repositorio es un ecosistema de ingeniería. Para mantener el estándar de calidad y seguridad, sigue estas directrices.

---

## 🚀 Inicio Rápido (Local Setup)

1. **Clonar y Ramas**:
   ```bash
   git clone https://github.com/vladimiracunadev-create/proyectos-aws.git
   cd proyectos-aws
   git checkout dev
   ```

2. **Requisitos**:
   - Docker Desktop (recomendado para validaciones).
   - PowerShell 7+ o Bash.
   - Cuenta de AWS (opcional para pruebas locales con CLI).

3. **Herramientas de Calidad**:
   ```bash
   # Instalar pre-commit para auditoría local de secretos
   pip install pre-commit
   pre-commit install
   ```

---

## 🛠️ Uso del Hub CLI

Utilizamos una capa de abstracción para estandarizar comandos entre Windows, Mac y Linux.

| Comando (PS / Bash) | Descripción |
| :--- | :--- |
| `.\hub.ps1 list-projects` | Lista todos los proyectos disponibles. |
| `.\hub.ps1 validate` | Ejecuta el contenedor de tooling para validar seguridad y sintaxis. |
| `.\hub.ps1 help` | Muestra la ayuda del Hub. |

---

## 🧭 Flujo de Trabajo (Git Flow Simplicado)

1. **Desarrollo**: Realiza tus cambios siempre sobre la rama `dev`.
2. **Validación**: Ejecuta `.\hub.ps1 validate` antes de cada commit.
3. **Commit**: Usa mensajes descriptivos (ej: `feat: add lambda demo`, `docs: fix typo`).
4. **Pull Request**: Crea un PR de `dev` hacia `main`. No se permiten pushes directos a la rama principal.

---

## ✅ Estándares de Código

- **Documentación**: Todo nuevo proyecto debe incluir su propio `README.md` y `AWS_PASO_A_PASO.md`.
- **Seguridad**: Nunca incluyas secretos. El pre-commit hook bloqueará automáticamente el commit si detecta potenciales llaves o tokens.
- **Portabilidad**: Si el proyecto requiere dependencias complejas, documéntalo en un Dockerfile.

---
*Gracias por ayudar a que este portafolio siga siendo un ejemplo de excelencia técnica.*
