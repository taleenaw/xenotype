from app.models import BotConversation


def get_recent_conversation(user, limit=5):
    conversations = (
        BotConversation.query
        .filter_by(user_id=user.id)
        .order_by(BotConversation.created_at.desc())
        .limit(limit)
        .all()
    )

    conversations.reverse()

    return conversations


def summarize_recent_conversation(conversations):
    if not conversations:
        return ""

    summary_parts = []

    for conversation in conversations:
        summary_parts.append(f"User: {conversation.player_message}")
        summary_parts.append(f"Bot: {conversation.bot_response}")

    return "\n".join(summary_parts)
