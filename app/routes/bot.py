from flask import Blueprint, jsonify, render_template, request
from flask_login import current_user, login_required

from app import db
from app.bot.chat_engine import BotEngine
from app.models import BotConversation, BotProfile

bot = Blueprint('bot', __name__, url_prefix='/bot')


def get_or_create_bot_profile(user):
    profile = BotProfile.query.filter_by(user_id=user.id).first()

    if profile is None:
        profile = BotProfile(user_id=user.id)
        db.session.add(profile)
        db.session.commit()

    return profile


@bot.route('/')
@login_required
def bot_home():
    return render_template('bot.html')


@bot.route('/message', methods=['POST'])
@login_required
def bot_message():
    data = request.get_json(silent=True) or {}
    message = data.get('message', '').strip()

    if not message:
        return jsonify({'error': 'Empty message'}), 400

    profile = get_or_create_bot_profile(current_user)

    engine = BotEngine()
    result = engine.process_message(current_user, message)

    profile.total_messages += 1
    profile.favorite_topic = result.get('topic', profile.favorite_topic)

    conversation = BotConversation(
        user_id=current_user.id,
        player_message=message,
        bot_response=result['response'],
        sentiment=result['sentiment']
    )

    db.session.add(profile)
    db.session.add(conversation)
    db.session.commit()

    return jsonify({
        'response': result['response'],
        'sentiment': result['sentiment'],
        'topic': result.get('topic', 'general'),
        'intent': result.get('intent', 'general')
    })
