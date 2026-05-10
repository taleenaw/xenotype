# Player-to-player AJAX Chat

This update adds real user-to-user chat separate from the campaign bot.

## What was added

- `ChatRoom` model
- `ChatMessage` model
- `app/routes/chat.py`
- `app/templates/chat.html`
- `/chat/` page
- AJAX message send endpoint: `/chat/api/send`
- AJAX polling endpoint: `/chat/api/messages`
- navigation link for logged-in users
- Alembic migration for chat tables

## How it works

Users must be logged in. Messages are saved to the database and the browser polls every 2 seconds for new messages.

This is AJAX polling, not WebSockets, so it is simple and works with normal Flask.

## Run after pulling these changes

```bash
python3 -m flask db upgrade
python3 -m flask run
```

Then open:

```text
http://127.0.0.1:5000/chat/
```
