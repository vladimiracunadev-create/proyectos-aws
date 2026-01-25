# Guía de Contribución

¡Gracias por tu interés en contribuir a este proyecto! 🚀

Este documento es un conjunto de pautas para contribuir al proyecto. Estas son solo pautas, no reglas estrictas. Usa tu mejor juicio y siéntete libre de proponer cambios a este documento en un Merge Request.

## 🛠️ Cómo empezar

1.  **Haz un Fork** del repositorio en GitLab.
2.  **Clona** el proyecto a tu máquina local.
3.  Crea una **nueva rama** para tu contribución:
    ```bash
    git checkout -b feat/mi-nueva-feature
    ```

## 🐛 Reportando Bugs

Si encuentras un bug, por favor crea un [Issue](https://gitlab.com/vladimir.acuna.dev-group/proyectos-aws-gitlab/-/issues) utilizando la plantilla de Bug Report. Asegúrate de incluir:

*   Pasos para reproducir.
*   Comportamiento esperado vs observado.
*   Screenshots si es relevante.

## 💡 Sugiriendo Mejoras

Para sugerir una nueva funcionalidad, abre un Issue utilizando la plantilla de Feature Request. Explica claramente por qué sería útil esta funcionalidad.

## 💻 Desarrollo

### Estilo de Código
*   Usamos **Prettier** para el formato. Asegúrate de correr `npm run format` antes de hacer commit.
*   Usamos **ESLint** para el linting. Corre `npm run lint` para verificar errores.

### Commits
Seguimos la convención de **Conventional Commits**.
*   `feat`: Nueva funcionalidad
*   `fix`: Arreglo de bugs
*   `docs`: Cambios en documentación
*   `style`: Cambios de formato (espacios, puntos y comas, etc.)
*   `refactor`: Refactorización de código
*   `test`: Añadir o corregir tests

Ejemplo: `feat(api): añadir endpoint de usuarios`

##  Pull/Merge Requests

1.  Asegúrate de que tu código está actualizado con la rama `main`.
2.  Completa la plantilla del MR con toda la información necesaria.
3.  Espera a la revisión y realiza los cambios solicitados si los hay.

¡Gracias por ayudar a hacer este proyecto mejor! ✨
