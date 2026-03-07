This file has no YAML frontmatter → always active.

# Project & Response Rules

## Project Context and Constraints
- Detailed functionality and a list of features that must be implemented are described at `./docs/Technical_Specification.EN.md`.
- Future roadmap items (DO NOT implement yet) are described at `./ROADMAP.md`.

## Response Rules (STRICT)
- Make sure you are aware of all the project files.
- Everything described in `./docs/Technical_Specification.EN.md` has higher priority than the Russian translation of this file and than all functionality implemented in other project files.
- First, ask the user to clarify his request if there are any unclear points or ambiguities in his request, or if there are several fundamentally different options for fulfilling the user's request. And only after receiving clarification should you proceed with fulfilling his request or answering his question.
- Maintain project integrity and consistency: if a user requests the implementation of new functionality or the modification or deletion of existing ones, ensure that, where necessary, documentation and other project files have been modified accordingly, including cross-references between files.
- Do not make changes to files that are not directly related to what the user explicitly requested in his last statement. If there are discrepancies between the content of certain files and your general instructions, inform the user about this, describing the discrepancy in detail.
- Always think step-by-step before answering (use internal reasoning, do not show it).
- For any code change or new file: Output ONLY the updated/complete file listing.
- Each file listing MUST start with the full path in a comment.
- Always render markdown responses using a method that avoids breaking when triple backticks are nested. Prefer one of the following in order:
  1. Use outer code blocks with four backticks (````) if the content includes nested triple backticks
  2. Escape inner backticks using \```
  3. Use indented code blocks
- Never add explanations unless the user explicitly asks.
- Provide at most a one-sentence summary in professional Russian before the files.
- Maintain exact existing structure and naming conventions. Extend only when requested.
- Always reference DEPLOYMENT.md for any deployment notes (universal Linux VPS guide).

## Language Rules (STRICT, Global)
- EVERY FILE you generate MUST comply with the following rules:
  - All code comments and docstrings must be in English ONLY.
  - All documentation files must be in two versions: the original in English (as *.EN.md files) AND a translation into Russian (as *.RU.md files).
  - All variable/function names must be in English ONLY.
  - All string constants meant to be shown to the end users (bot messages, button texts, captions, error messages) should be in Russian.
- Outside of file contents use Russian language where appropriate.
- Whatever language you use to generate content (English or Russian), use its perfect, natural, professional version.
