import random
from flask import Blueprint, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Scenario
from app.routes.scenarios_pool import Scenarios

scenario = Blueprint('scenario', __name__)

def calculate_passage_difficulty(passage):
    words = passage.split()
    word_count = len(words)

    if word_count == 0:
        return "Easy"

    average_word_length = sum(len(word) for word in words) / word_count

    punctuation_count = sum(
        1 for char in passage
        if char in ",.;:!?\"'()[]{}—-"
    )

    long_word_count = sum(1 for word in words if len(word) >= 8)

    complexity_score = 0

    if word_count > 120:
        complexity_score += 2
    elif word_count > 70:
        complexity_score += 1

    if average_word_length >= 6:
        complexity_score += 2
    elif average_word_length >= 5:
        complexity_score += 1

    if punctuation_count >= 25:
        complexity_score += 2
    elif punctuation_count >= 12:
        complexity_score += 1

    if long_word_count >= 18:
        complexity_score += 2
    elif long_word_count >= 8:
        complexity_score += 1

    if complexity_score >= 5:
        return "Hard"

    if complexity_score >= 3:
        return "Medium"

    return "Easy"


def generate_random_scenario_data():
    data = random.choice(Scenarios).copy()

    data["difficulty"] = calculate_passage_difficulty(data["passage"])

    return data

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
