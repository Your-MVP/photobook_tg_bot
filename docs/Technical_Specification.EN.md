# ./docs/Technical_Specification.EN.md

# Technical Specification for Photobook Telegram Bot Development (MVP v0.1.0)

## 1. Project Goal
Develop a Telegram bot that allows users to collect photos from a private chat with the bot or from a family group chat (where the user adds the bot manually). The bot should support the storage of the minimum necessary data in the database (the photos themselves should be stored in Telegram, and only the photo IDs should be stored in the bot's database) and monitoring by administrators through a dedicated supergroup called the moderation supergroup.

## 2. Core Functional Requirements
- Monitoring via supergroup: for each active user, the bot automatically creates a separate forum topic in a pre-prepared moderation supergroup. Only administrators (owners and appointed moderators) are in the supergroup; end users are not added to it.
- Photo reception: the bot receives photos both in its private chat with the user and in group chats (family albums) where the user has added it, forwarding them (photos) to the corresponding user topic in the moderation supergroup and reporting the number of photos added for that user.
- Data storage: PostgreSQL (SQLAlchemy async) — users, sessions, photo list.

## 3. Moderation Supergroup and Topics Handling (Telegram Bot API)
The supergroup whose ID is stored in SUPERGROUP_CHAT_ID is referred to as the "moderation supergroup".

### 3.1. Moderation supergroup creation steps (performed manually only):
- The bot owner must manually create a regular group and upgrade it to a supergroup (chat type = supergroup).
- Enable “Topics” mode (forum = true) in moderation supergroup settings.
- Add the bot as administrator with permissions: can_manage_topics, can_post_messages, can_edit_messages, can_delete_messages.
- Manually appoint additional human administrators via Telegram interface.
- Obtain the moderation supergroup chat_id (negative number) and main topic message_thread_id.
- Store SUPERGROUP_CHAT_ID in .env file or bot configuration. This is the only way to make the moderation supergroup “known” to the bot — Telegram Bot API does not allow the bot to create or discover supergroups itself.

### 3.2. Automatic bot actions (after manual setup):
- On first interaction of a new user (/start) the bot calls createForumTopic with chat_id = SUPERGROUP_CHAT_ID, name = “User {user_id} — {username}”, icon_color.
- All subsequent user messages and bot actions (if needed) are forwarded or duplicated to the created topic using message_thread_id.
- Administrators see the list of topics and can track the progress for each user.

## 4. Greetings and User Differentiation
- Standard greeting (for regular users): short, friendly message with instructions on adding photos.
- Greeting for bot owner (checked against user.id from config): extended, with access to admin commands and statistics.
- Greeting for assigned moderation supergroup administrators (checked against admin_ids list in config): special message with links to all active topics and user statuses.

## 5. Understanding of Telegram Bot API Capabilities and Limitations
- Bot operates with structures: Chat, Message, MessageEntity, ForumTopic, User.
- Can: receive updates via polling or webhook, send photos/documents (PDF), create topics, manage permissions in topics.
- Cannot: create supergroups itself, find existing chats without invitation, read chat history before being added.
- Everything related to moderation supergroup creation and initial administrator assignment can only be done manually. Only topic creation and work inside topics is automated.

## 6. Additional Requirements
- Full containerization: Docker Compose (bot + Redis + PostgreSQL).

## 7. Technology Stack
- Python 3.12,
- aiogram 3.x,
- asyncio,
- Redis FSM storage,
- Pillow/OpenCV for image handling,
- img2pdf/ReportLab for PDF generation,
- Docker Compose,
- PostgreSQL (SQLAlchemy async).

## 8. Coding Standards
- Strictly follow PEP 8.
- Use type hints on every function, method, and variable where possible.
- Docstrings: Google style (or NumPy style) consistently.
- For image/PDF handling prefer Pillow → img2pdf; keep OpenCV only when strictly necessary.
- Use SQLAlchemy 2.0 async style everywhere.
- Redis FSM storage via aiogram 3.x.
- Keep all new code inside the existing `bot/` package structure; never alter top-level files unless explicitly requested.
