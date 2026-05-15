import random

from app.bot.parser import detect_intent
from app.bot.story_graph import STORY_GRAPH
from app.bot.templates import SCENE_TEMPLATES
from app.bot.worlds import STORY_WORLDS


def _clamp(value, minimum=0, maximum=100):
    return max(minimum, min(maximum, value))


class CampaignEngine:
    def build_status_text(self, progress):
        return (
            f"Status — Health: {progress.health}, "
            f"Fear: {progress.fear}, "
            f"Confidence: {progress.confidence}, "
            f"Node: {progress.current_node}"
        )

    def build_help_text(self):
        return (
            "Commands you can try: look, search, inspect, talk, run, fight, "
            "hack, repair, use, status, or help."
        )

    def generate_scene(self, progress):
        world = STORY_WORLDS.get(progress.world, STORY_WORLDS["xenotype_signal"])
        node = progress.current_node

        templates = SCENE_TEMPLATES.get(node, SCENE_TEMPLATES["intro"])
        template = random.choice(templates)
        random_object = random.choice(world["objects"])

        return template.format(
            setting=world["setting"],
            villain=world["villain"],
            goal=world["goal"],
            object=random_object,
        )

    def apply_node_effects(self, progress, next_node):
        effects = {
            "signal_lobby": {"confidence": 3},
            "npc_echo": {"confidence": 5},
            "guide_warning": {"fear": 5},
            "ghost_terminal": {"fear": 5, "confidence": 5},
            "archive_hall": {"confidence": 5},
            "hidden_room": {"confidence": 10},
            "medbay": {"health": 15, "fear": -5},
            "quarantine_door": {"fear": 10},
            "corrupted_patrol": {"health": -12, "fear": 10},
            "secret_hint": {"confidence": 15, "fear": -5},
            "data_vault": {"confidence": 12},
            "reactor_core": {"health": -5, "confidence": 8},
            "choice_bridge": {"confidence": 10},
            "ending_decode": {"confidence": 20},
            "ending_restore": {"health": 20, "confidence": 15, "fear": -10},
            "ending_destroy": {"fear": 15, "confidence": 10},
            "ending_negotiate": {"confidence": 25, "fear": -15},
        }

        node_effects = effects.get(next_node, {})

        progress.health = _clamp(progress.health + node_effects.get("health", 0))
        progress.fear = _clamp(progress.fear + node_effects.get("fear", 0))
        progress.confidence = _clamp(progress.confidence + node_effects.get("confidence", 0))

        if next_node.startswith("ending_"):
            progress.completed = True

    def process_turn(self, progress, message, wpm=0):
        intent = detect_intent(message)
        required_wpm = {

            "run": 25,

            "fight": 35,

            "hack": 45,

            "repair": 30,

            "use": 20,

        }

        if intent in required_wpm and wpm < required_wpm[intent]:

            progress.fear = _clamp(progress.fear + 5)

            progress.confidence = _clamp(progress.confidence - 5)

            return (

                f"You tried to {intent}, but your signal speed was too low. "

                f"This action requires at least {required_wpm[intent]} WPM. "

                f"Your current speed was {wpm} WPM.\n\n"

                f"{self.build_status_text(progress)}"

            )
        if intent == "help":
            return self.build_help_text()
        if intent == "status":
            return self.build_status_text(progress)

        current_node = progress.current_node
        possible_paths = STORY_GRAPH.get(current_node, STORY_GRAPH["intro"])

        if intent not in possible_paths:
            return (
                "That action is not possible from this situation. Try a different command: "
                "look, talk, run, fight, hack, repair, use, status, or help."
            )

        next_node = possible_paths[intent]

        progress.add_visited_node(current_node)
        progress.current_node = next_node
        self.apply_node_effects(progress, next_node)

        scene = self.generate_scene(progress)
        return f"{scene}\n\n{self.build_status_text(progress)}"
