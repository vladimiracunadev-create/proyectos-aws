# 🤝 Contributing Guide

Gracias por tu interés en contribuir a este repositorio.

Este proyecto está pensado como portafolio profesional con prácticas reales de CI/CD y documentación.

---

## 🧭 Flujo de trabajo (branching)

- `main`: estable / producción
- `dev`: integración / pruebas

Regla general: **no hacer push directo a `main`**. Usar Pull Request desde `dev`.

---

## 🧑‍💻 Setup rápido

```bash
git clone <URL_DEL_REPO>
cd <CARPETA_DEL_REPO>

git checkout dev
git pull origin dev
