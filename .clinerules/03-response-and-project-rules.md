# Project & Response Rules

## Project Context and Constraints
- Current features: /start, /build (one-photo-per-page PDF), /clear, photo album handling, Redis storage.
- Do NOT implement roadmap items (AI filtering, collages, Celery, MinIO, webhook/FastAPI) unless user explicitly moves to v0.2.
- Always reference DEPLOYMENT.md for any deployment notes (universal Linux VPS guide).
- Use aiogram 3.x, asyncio, Redis, PostgreSQL (SQLAlchemy async), Pillow/ReportLab.

## Response Rules (STRICT)
- Make sure you are aware of all the project files.
- For any code change or new file: Output ONLY the updated/complete file listing.
- Each file listing MUST start with the full path in a comment.
- Always render markdown responses using a method that avoids breaking when triple backticks are nested. Prefer one of the following in order:
  1. Use outer code blocks with four backticks (````) if the content includes nested triple backticks
  2. Escape inner backticks using \```
  3. Use indented code blocks
- Never add explanations unless the user explicitly asks.
- Provide at most a one-sentence summary in professional Russian before the files.
- Maintain exact existing project structure and naming conventions.

## Language Rules (STRICT, Global)
- Every generated file (code, README, docs, etc.) MUST contain only perfect, natural, professional English.
- Outside of files, use perfect, natural, professional Russian when communicating with the user.

This file has no YAML frontmatter → always active.