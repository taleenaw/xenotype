from flask import Blueprint, jsonify, render_template, request, session
from flask_login import current_user, login_required
from app.BOT.bot import CampaignBot

campaign = Blueprint('campaign', __name__, url_prefix='/campaign')


def _get_history():
    """Return the current browser session's campaign chat history."""
    return session.get('campaign_chat_history', [])


def _save_history(history):
    """Save chat history back into the browser session."""
    session['campaign_chat_history'] = history
    session.modified = True


@campaign.route('/')
@login_required
def campaign_home():
    """Campaign mode page with an interactive bot chat panel."""
    bot = CampaignBot()
    history = _get_history()

    if not history:
        opening = bot.opening_message(current_user.username)
        history = [{'speaker': opening.speaker, 'text': opening.text, 'role': 'bot'}]
        _save_history(history)

    return render_template('campaign.html', history=history)


@campaign.route('/chat', methods=['POST'])
@login_required
def campaign_chat():
    """Receive a player message and return the bot's reply as JSON."""
    data = request.get_json(silent=True) or {}
    player_message = data.get('message', '').strip()

    history = _get_history()

    if not player_message:
        return jsonify({'error': 'Message cannot be empty.'}), 400

    history.append({
        'speaker': current_user.username,
        'text': player_message,
        'role': 'player'
    })

    bot = CampaignBot()
    reply = bot.respond(player_message, history)

    bot_message = {
        'speaker': reply.speaker,
        'text': reply.text,
        'role': 'bot'
    }
    history.append(bot_message)
    _save_history(history)

    return jsonify(bot_message)


@campaign.route('/reset', methods=['POST'])
@login_required
def reset_campaign_chat():
    """Clear the current session's campaign chat history."""
    session.pop('campaign_chat_history', None)
    session.modified = True
    return jsonify({'status': 'reset'})
