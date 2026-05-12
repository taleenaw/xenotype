from dataclasses import dataclass

from app.BOT.engine import CampaignEngine


@dataclass
class BotReply:
    speaker: str
    text: str


class CampaignBot:
    def __init__(self, bot_name="Echo-7"):
        self.bot_name = bot_name
        self.engine = CampaignEngine()

    def opening_message(self, username=None):
        name = username or "operator"
        return BotReply(
            speaker=self.bot_name,
            text=(
                f"Connection established. Welcome, {name}. "
                "Campaign progress is now saved. "
                "Try: look, talk, run, fight, status, or help."
            ),
        )

    def respond(self, progress, player_message):
        text = self.engine.process_turn(progress, player_message)
        return BotReply(speaker=self.bot_name, text=text)
