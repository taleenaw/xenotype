MIN_RANKED_RUNS = 3

RANK_TIERS = {
    "unranked": {
        "name": "Unranked",
        "border": None,
        "score_floor": None,
    },
    "wood": {
        "name": "Wood",
        "border": "Wood.png",
        "score_floor": 0,
    },
    "silver": {
        "name": "Silver",
        "border": "Silver.png",
        "score_floor": 55,
    },
    "gold": {
        "name": "Gold",
        "border": "Gold.png",
        "score_floor": 75,
    },
}

RANKED_BORDER_FILES = {
    tier["border"]
    for tier in RANK_TIERS.values()
    if tier["border"]
}


def calculate_rank_score(runs):
    if not runs:
        return 0

    best_wpm = max(run.wpm for run in runs)
    average_accuracy = sum(run.accuracy for run in runs) / len(runs)
    pass_rate = (
        sum(1 for run in runs if run.is_passing()) / len(runs)
    ) * 100

    return round(
        (best_wpm * 0.55)
        + (average_accuracy * 0.35)
        + (pass_rate * 0.10),
        1,
    )


def get_rank_tier(runs):
    completed_runs = len(runs)

    if completed_runs < MIN_RANKED_RUNS:
        tier = RANK_TIERS["unranked"]
        return {
            "key": "unranked",
            "name": tier["name"],
            "border": tier["border"],
            "score": None,
            "missions_until_ranked": MIN_RANKED_RUNS - completed_runs,
        }

    score = calculate_rank_score(runs)

    if score >= RANK_TIERS["gold"]["score_floor"]:
        rank_key = "gold"
    elif score >= RANK_TIERS["silver"]["score_floor"]:
        rank_key = "silver"
    else:
        rank_key = "wood"

    tier = RANK_TIERS[rank_key]

    return {
        "key": rank_key,
        "name": tier["name"],
        "border": tier["border"],
        "score": score,
        "missions_until_ranked": 0,
    }
