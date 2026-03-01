# PhotobookBotDev Response & Project Rules

## Response Format (STRICT)
- For any code change or new file: Output ONLY the updated/complete file.
- Each file MUST start with the full path in a comment, followed by the appropriate fenced code block.
- Example:
```text
# bot/handlers/commands.py
```python
[full code here]
```
```
- Never add explanations unless the user explicitly asks.
- Provide at most a one-sentence summary in professional Russian before the files.
- Maintain exact existing project structure and naming conventions.

## Project Constraints (MVP v0.1.0)
- Current features: /start, /build (one-photo-per-page PDF), /clear, photo album handling, Redis storage.
- Do NOT implement roadmap items (AI filtering, collages, Celery, MinIO, webhook/FastAPI) unless user explicitly moves to v0.2.
- Always reference DEPLOYMENT.md for any deployment notes (universal Linux VPS guide).
- Use aiogram 3.x, asyncio, Redis, PostgreSQL (SQLAlchemy async), Pillow/ReportLab.

## Language Rule (Global)
- Every generated file (code, README, docs, etc.) MUST contain only perfect, natural, professional English.
- Outside of files, use perfect, natural, professional Russian when communicating with the user.

This file has no YAML frontmatter → always active.