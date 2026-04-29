import random
from flask import Blueprint, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Scenario

scenario = Blueprint('scenario', __name__)

def generate_random_scenario_data():
    genres = {
        "Sci-Fi": {
            "settings": ["a ruined moon base", "an orbital relay", "a drifting research vessel"],
            "threats": ["oxygen loss", "reactor instability", "signal corruption"],
            "objectives": ["decode the distress signal", "restore communications", "recover navigation logs"],
            "passages": [
                "WARNING... oxygen reserves below critical threshold... crew evacuation advised...",
                "SOS... main relay offline... request immediate assistance from allied command...",
                "Navigation systems failing... route data corrupted... manual override required..."
            ]
        },
        "Cyberpunk": {
            "settings": ["a neon server vault", "an underground data market", "a hidden hacker den"],
            "threats": ["ICE countermeasures", "hostile intrusion", "encryption spikes"],
            "objectives": ["extract the access key", "decode the black-site archive", "recover stolen data"],
            "passages": [
                "Firewall breach detected... encryption layer rising... manual bypass required...",
                "Datastream unstable... hostile trace in progress... sever connection or continue...",
                "Archive fragment found... partial decryption complete... continue extraction..."
            ]
        },
        "Military": {
            "settings": ["a forward command bunker", "a surveillance outpost", "a desert operations base"],
            "threats": ["enemy interception", "comms blackout", "drone activity"],
            "objectives": ["relay the coordinates", "decode the intel report", "restore the secure uplink"],
            "passages": [
                "Enemy movement detected north of checkpoint... reinforce sector immediately...",
                "Secure channel unstable... transmission integrity dropping... continue relay...",
                "Recon data incoming... encryption valid... command verification required..."
            ]
        }
    }

    genre = random.choice(list(genres.keys()))
    pool = genres[genre]

    setting = random.choice(pool["settings"])
    threat = random.choice(pool["threats"])
    objective = random.choice(pool["objectives"])
    passage = random.choice(pool["passages"])
    difficulty = random.choice(["Easy", "Medium", "Hard"])

    return {
        "title": f"Operation {setting.title()}",
        "genre": genre,
        "difficulty": difficulty,
        "intro_text": f"You arrive at {setting}. Your objective is to {objective} while facing {threat}.",
        "passage": passage,
        "outcome_high": "You completed the mission flawlessly and secured the objective.",
        "outcome_mid": "You completed the mission, but with partial losses and delays.",
        "outcome_low": "The mission failed before the signal could be fully recovered."
    }

@scenario.route('/generate')
@login_required
def generate_scenario():
    data = generate_random_scenario_data()

    new_scenario = Scenario(
        title=data["title"],
        genre=data["genre"],
        difficulty=data["difficulty"],
        intro_text=data["intro_text"],
        passage=data["passage"],
        outcome_high=data["outcome_high"],
        outcome_mid=data["outcome_mid"],
        outcome_low=data["outcome_low"],
        created_by=current_user.id,
        is_official=False
    )

    db.session.add(new_scenario)
    db.session.commit()

    flash("Random scenario generated successfully.")
    return redirect(url_for('main.scenarios'))
