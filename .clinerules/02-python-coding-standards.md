# Python Coding Standards (Photobook Bot)

- Strictly follow PEP 8.
- Use type hints on every function, method, and variable where possible.
- Docstrings: Google style (or NumPy style) consistently.
- All string constants, bot messages, button texts, captions, error messages, comments, and documentation MUST be in perfect, natural, professional English ONLY.
- Variable and function names in English; semantic clarity preferred.
- Never output any Russian text inside source files or generated artifacts.
- For image/PDF handling prefer Pillow → img2pdf; keep OpenCV only when strictly necessary.
- Use SQLAlchemy 2.0 async style everywhere.
- Redis FSM storage via aiogram 3.x.
- Keep all new code inside the existing `bot/` package structure; never alter top-level files unless explicitly requested.

## Conditional Activation
---
paths:
  - "**/*.py"
---