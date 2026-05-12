import random

from app.BOT.parser import detect_intent
from app.BOT.story_graph import STORY_GRAPH
from app.BOT.templates import SCENE_TEMPLATES
from app.BOT.worlds import STORY_WORLDS


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
        return "Commands you can try: look, search, inspect, talk, run, fight, status, help."

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
        if next_node == "first_clue":
            progress.confidence = _clamp(progress.confidence + 5)
        elif next_node == "guide_warning":
            progress.fear = _clamp(progress.fear + 5)
        elif next_node == "hidden_room":
            progress.confidence = _clamp(progress.confidence + 10)
        elif next_node == "sealed_exit":
            progress.fear = _clamp(progress.fear + 10)
        elif next_node == "secret_hint":
            progress.confidence = _clamp(progress.confidence + 15)
            progress.fear = _clamp(progress.fear - 5)
        elif next_node == "security_encounter":
            progress.health = _clamp(progress.health - 10)
            progress.fear = _clamp(progress.fear + 10)
        elif next_node == "final_gate":
            progress.confidence = _clamp(progress.confidence + 10)
        elif next_node == "completed":
            progress.completed = True
            progress.confidence = _clamp(progress.confidence + 20)

    def process_turn(self, progress, message):
        intent = detect_intent(message)

        if intent == "help":
            return self.build_help_text()
        if intent == "status":
            return self.build_status_text(progress)

        current_node = progress.current_node
        possible_paths = STORY_GRAPH.get(current_node, STORY_GRAPH["intro"])

        if intent not in possible_paths:
            return "That action is not possible here. Try: look, talk, run, fight, status, or help."

        next_node = possible_paths[intent]

        progress.add_visited_node(current_node)
        progress.current_node = next_node
        self.apply_node_effects(progress, next_node)

        scene = self.generate_scene(progress)
        return f"{scene}\n\n{self.build_status_text(progress)}"
