# Caso A — AWS Amplify + GitLab (hosting automático)

## Qué hace
- Conecta el repo de GitLab con **AWS Amplify Hosting**.
- Cada `git push` a tu rama (ej. `main`) despliega automáticamente tu web estática.

## Pasos (sin afectar otros entornos)
1) En AWS, crea una **nueva Amplify App** (no reutilices una existente).
2) Conecta tu repo GitLab y selecciona la rama (ej. `main`).
3) Marca **My app is a monorepo** y pon el path: `caso-a-amplify`.
4) (Recomendado) Para que quede "infra como código" en el repo:
   - Copia `caso-a-amplify/amplify.yml` a la **raíz** del repositorio (quedará como `./amplify.yml`).
   - Haz commit y push.

Amplify usa el `amplify.yml` del repositorio para el buildspec cuando está presente.
