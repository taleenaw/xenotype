from dataclasses import dataclass
from app.bot.parser import detect_intent
from app.bot.engine import CampaignEngine


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

    def respond(self, progress, player_message, wpm=0):
        required_wpm = {
            "run": 25,
            "fight": 35,
            "hack": 45,
            "repair": 30,
            "use": 20,
        }

        intent = detect_intent(player_message)

        if intent in required_wpm and wpm < required_wpm[intent]:
            progress.fear = min(progress.fear + 5, 100)
            progress.confidence = max(progress.confidence - 5, 0)

            return BotReply(
                speaker=self.bot_name,
                text=(
                    f"You attempted to {intent}, but your response speed was too slow.\n\n"
                    f"Required WPM: {required_wpm[intent]}\n"
                    f"Your WPM: {wpm}\n\n"
                    f"The delay causes hesitation and danger spreads through the area."
                ),
            )

        text = self.engine.process_turn(progress, player_message, wpm)
        return BotReply(speaker=self.bot_name, text=text)
