---
paths:
  - "**/*.py"
---

# Python Coding Standards (Photobook Bot)

- Strictly follow PEP 8.
- Use type hints on every function, method, and variable where possible.
- Docstrings: Google style (or NumPy style) consistently.
- For image/PDF handling prefer Pillow → img2pdf; keep OpenCV only when strictly necessary.
- Use SQLAlchemy 2.0 async style everywhere.
- Redis FSM storage via aiogram 3.x.
- Keep all new code inside the existing `bot/` package structure; never alter top-level files unless explicitly requested.