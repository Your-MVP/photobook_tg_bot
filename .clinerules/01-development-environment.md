# Photobook Bot Development Environment & Workflow

## Mandatory Setup
- All development MUST be performed exclusively inside Visual Studio Code with the **Cline** extension active.
- The following VSCode extensions MUST be installed and actively used where relevant:
  - Container Tools
  - Dev Containers
  - ESLint
  - GitLens
  - PostgreSQL
  - Prettier
  - Pylance
  - Python
  - Python Debugger
- Always open the project via Dev Containers (`.devcontainer/devcontainer.json` when present) to guarantee identical Python 3.12, Docker, Redis, and PostgreSQL environment.
- Run the bot locally only through `docker compose up -d --build`.
- For production deployment follow the exact steps from DEPLOYMENT.md.

## Rule Activation
- This file has no YAML frontmatter → always active for every file and conversation.