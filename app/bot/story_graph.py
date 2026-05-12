STORY_GRAPH = {
    "intro": {
        "investigate": "signal_lobby",
        "talk": "npc_echo",
        "hack": "ghost_terminal",
        "status": "intro",
        "help": "intro",
    },

    "signal_lobby": {
        "investigate": "archive_hall",
        "talk": "npc_echo",
        "hack": "ghost_terminal",
        "repair": "medbay",
        "run": "quarantine_door",
        "status": "signal_lobby",
        "help": "signal_lobby",
    },

    "npc_echo": {
        "talk": "guide_warning",
        "investigate": "archive_hall",
        "hack": "ghost_terminal",
        "run": "quarantine_door",
        "status": "npc_echo",
        "help": "npc_echo",
    },

    "guide_warning": {
        "talk": "secret_hint",
        "investigate": "archive_hall",
        "hack": "ghost_terminal",
        "fight": "corrupted_patrol",
        "run": "quarantine_door",
        "status": "guide_warning",
        "help": "guide_warning",
    },

    "ghost_terminal": {
        "hack": "secret_hint",
        "investigate": "archive_hall",
        "repair": "reactor_core",
        "fight": "corrupted_patrol",
        "run": "quarantine_door",
        "status": "ghost_terminal",
        "help": "ghost_terminal",
    },

    "archive_hall": {
        "investigate": "hidden_room",
        "talk": "npc_echo",
        "hack": "ghost_terminal",
        "use": "data_vault",
        "fight": "corrupted_patrol",
        "status": "archive_hall",
        "help": "archive_hall",
    },

    "hidden_room": {
        "investigate": "data_vault",
        "hack": "secret_hint",
        "repair": "medbay",
        "fight": "corrupted_patrol",
        "run": "quarantine_door",
        "status": "hidden_room",
        "help": "hidden_room",
    },

    "medbay": {
        "repair": "reactor_core",
        "investigate": "hidden_room",
        "talk": "npc_echo",
        "use": "data_vault",
        "status": "medbay",
        "help": "medbay",
    },

    "quarantine_door": {
        "hack": "ghost_terminal",
        "repair": "reactor_core",
        "use": "data_vault",
        "fight": "corrupted_patrol",
        "run": "corrupted_patrol",
        "status": "quarantine_door",
        "help": "quarantine_door",
    },

    "corrupted_patrol": {
        "fight": "reactor_core",
        "run": "quarantine_door",
        "hack": "ghost_terminal",
        "repair": "medbay",
        "status": "corrupted_patrol",
        "help": "corrupted_patrol",
    },

    "secret_hint": {
        "investigate": "data_vault",
        "hack": "data_vault",
        "talk": "choice_bridge",
        "use": "choice_bridge",
        "status": "secret_hint",
        "help": "secret_hint",
    },

    "data_vault": {
        "hack": "choice_bridge",
        "use": "choice_bridge",
        "investigate": "reactor_core",
        "fight": "corrupted_patrol",
        "status": "data_vault",
        "help": "data_vault",
    },

    "reactor_core": {
        "repair": "choice_bridge",
        "hack": "data_vault",
        "fight": "corrupted_patrol",
        "run": "quarantine_door",
        "status": "reactor_core",
        "help": "reactor_core",
    },

    "choice_bridge": {
        "hack": "ending_decode",
        "repair": "ending_restore",
        "fight": "ending_destroy",
        "talk": "ending_negotiate",
        "use": "ending_decode",
        "status": "choice_bridge",
        "help": "choice_bridge",
    },

    "ending_decode": {
        "status": "ending_decode",
        "help": "ending_decode",
    },

    "ending_restore": {
        "status": "ending_restore",
        "help": "ending_restore",
    },

    "ending_destroy": {
        "status": "ending_destroy",
        "help": "ending_destroy",
    },

    "ending_negotiate": {
        "status": "ending_negotiate",
        "help": "ending_negotiate",
    },
}
