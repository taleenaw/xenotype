"""
Campaign bot skeleton for Xenotype.

This file is intentionally simple so you can replace the rule-based replies
with your own game logic later.

Ideas you can add here:
- track player choices
- unlock campaign chapters
- connect replies to Scenario records
- score typing performance and change the story
- call an AI API later, if your assignment allows it
"""

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class BotReply:
    """Structured response returned by the campaign bot."""
    speaker: str
    text: str


class CampaignBot:
    """
    Very small interactive chatbot skeleton.

    The route passes in the player's message and the current chat history.
    This class returns the bot's next reply.
    """

    def __init__(self, bot_name: str = "Echo-7"):
        self.bot_name = bot_name

    def opening_message(self, username: str | None = None) -> BotReply:
        """First message shown when a player opens campaign mode."""
        name = username or "operator"
        return BotReply(
            speaker=self.bot_name,
            text=(
                f"Connection established. Welcome, {name}. "
                "I am your campaign guide. Type 'mission' to begin, "
                "or ask me about the world."
            ),
        )

    def respond(self, player_message: str, history: List[Dict[str, str]] | None = None) -> BotReply:
        """
        Return a bot reply for one player message.

        Replace this method with your own campaign logic. For example, you could:
        - check which chapter the player is on
        - branch based on choices
        - query your database for scenarios
        - generate a typing challenge
        """
        history = history or []
        message = player_message.strip().lower()

        if not message:
            return BotReply(self.bot_name, "Signal lost. Send me a command when ready.")

        if "mission" in message or "start" in message:
            return BotReply(
                self.bot_name,
                "Mission 01: decode the alien transmission. Your first task is to enter the Scenarios section and complete a typing run.",
            )

        if "help" in message:
            return BotReply(
                self.bot_name,
                "Available commands: mission, status, lore, help. You can also type normal messages and I will respond.",
            )

        if "status" in message:
            return BotReply(
                self.bot_name,
                f"Campaign link is stable. Messages exchanged this session: {len(history)}.",
            )

        if "lore" in message or "world" in message:
            return BotReply(
                self.bot_name,
                "The Xenotype network is waking up. Every typing test reveals another fragment of the signal.",
            )

        return BotReply(
            self.bot_name,
            f"I received: '{player_message}'. Add your own response logic in app/bot.py.",
        )
