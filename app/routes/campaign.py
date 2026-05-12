from flask import Blueprint, jsonify, render_template, request
from flask_login import current_user, login_required

from app import db
from app.BOT.bot import CampaignBot
from app.models import CampaignProgress


campaign = Blueprint('campaign', __name__, url_prefix='/campaign')


def get_or_create_campaign_progress():
    progress = CampaignProgress.query.filter_by(
        user_id=current_user.id,
        mode='bot'
    ).first()

    if progress is None:
        progress = CampaignProgress(
            user_id=current_user.id,
            mode='bot',
            world='xenotype_signal',
            current_node='intro',
        )
        db.session.add(progress)
        db.session.commit()

    return progress


@campaign.route('/')
@login_required
def campaign_home():
    progress = get_or_create_campaign_progress()
    bot = CampaignBot()
    opening = bot.opening_message(current_user.username)

    return render_template(
        'campaign.html',
        progress=progress,
        opening_message=opening,
    )


@campaign.route('/chat', methods=['POST'])
@login_required
def campaign_chat():
    data = request.get_json(silent=True) or {}
    player_message = data.get('message', '').strip()

    if not player_message:
        return jsonify({'error': 'Message cannot be empty.'}), 400

    progress = get_or_create_campaign_progress()
    bot = CampaignBot()
    reply = bot.respond(progress, player_message)

    db.session.add(progress)
    db.session.commit()

    return jsonify({
        'speaker': reply.speaker,
        'text': reply.text,
        'role': 'bot',
        'progress': {
            'current_node': progress.current_node,
            'health': progress.health,
            'fear': progress.fear,
            'confidence': progress.confidence,
            'completed': progress.completed,
        }
    })


@campaign.route('/reset', methods=['POST'])
@login_required
def reset_campaign():
    progress = get_or_create_campaign_progress()
    progress.reset()

    db.session.add(progress)
    db.session.commit()

    return jsonify({'status': 'reset'})
