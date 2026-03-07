**Technical Specification for Telegram Bot Development “Photobook Bot”**

**1. Project Goal**
Develop a Telegram bot that allows users to collect photos from private chat with the bot or from a family group chat (where the user manually adds the bot), create photobooks in PDF format and prepare them for printing. The bot must support photobook list management per user, store data in a database and provide monitoring for administrators via a dedicated supergroup.

**2. Core Functional Requirements**
- Photo reception: the bot receives photos both in private chat and in group chats (family albums) where it was added.
- Data storage: PostgreSQL (SQLAlchemy async) — users, sessions, photo id lists, generated book ids.
- Monitoring via supergroup: for each active user the bot automatically creates a separate forum topic in a pre-prepared supergroup. Only administrators (owners and assigned moderators) are present in the supergroup; end users are not added.

**3. Supergroup and Topics Handling (Telegram Bot API)**
3.1. Supergroup creation steps (performed manually only):
- The bot owner must manually create a regular group and upgrade it to a supergroup (chat type = supergroup).
- Enable “Topics” mode (forum = true) in supergroup settings.
- Add the bot as administrator with permissions: can_manage_topics, can_post_messages, can_edit_messages, can_delete_messages.
- Manually appoint additional human administrators via Telegram interface.
- Obtain the supergroup chat_id (negative number) and main topic message_thread_id.
- Store SUPERGROUP_CHAT_ID in .env file or bot configuration. This is the only way to make the supergroup “known” to the bot — Telegram Bot API does not allow the bot to create or discover supergroups itself.

3.2. Automatic bot actions (after manual setup):
- On first interaction of a new user (/start) the bot calls createForumTopic with chat_id = SUPERGROUP_CHAT_ID, name = “User {user_id} — {username}”, icon_color.
- All subsequent user messages and bot actions (if needed) are forwarded or duplicated to the created topic using message_thread_id.
- Administrators see the list of topics and can track the progress for each user.

**4. Greetings and User Differentiation**
- Standard greeting (for regular users): short, friendly message with photo upload instructions.
- Owner greeting (bot owner, checked by user.id from config): extended, with access to admin commands and statistics.
- Greeting for assigned supergroup administrators (checked against admin_ids list in config): special message with links to all active topics and user statuses.

**5. Understanding of Telegram Bot API Capabilities and Limitations**
- The bot operates with structures: Chat, Message, MessageEntity, ForumTopic, User.
- Can: receive updates via polling or webhook, send photos/documents (PDF), create topics, manage topic permissions.
- Cannot: create supergroups itself, find existing chats without invitation, read chat history before being added.
- Everything related to supergroup creation and initial administrator assignment can only be done manually. Only topic creation and work inside topics is automated.

**6. Additional Requirements**
- Full containerization: Docker Compose (bot + Redis + PostgreSQL).

**7. Technology Stack**
- Python 3.12,
- aiogram 3.x,
- asyncio,
- Redis FSM storage,
- Pillow/OpenCV for image handling,
- img2pdf/ReportLab for PDF generation,
- Docker Compose,
- PostgreSQL (SQLAlchemy async).

**8. Coding Standards**
- Strictly follow PEP 8.
- Use type hints on every function, method, and variable where possible.
- Docstrings: Google style (or NumPy style) consistently.
- For image/PDF handling prefer Pillow → img2pdf; keep OpenCV only when strictly necessary.
- Use SQLAlchemy 2.0 async style everywhere.
- Redis FSM storage via aiogram 3.x.
- Keep all new code inside the existing `bot/` package structure; never alter top-level files unless explicitly requested.
