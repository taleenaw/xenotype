from flask import Blueprint, jsonify, render_template, request
from flask_login import current_user, login_required

from app import db
from app.models import ChatMessage, ChatRoom

chat = Blueprint('chat', __name__, url_prefix='/chat')


DEFAULT_ROOM_NAME = 'general'


def get_or_create_room(room_name=DEFAULT_ROOM_NAME):
    room_name = (room_name or DEFAULT_ROOM_NAME).strip().lower()

    room = ChatRoom.query.filter_by(name=room_name).first()

    if room is None:
        room = ChatRoom(
            name=room_name,
            description='General Xenotype player chat room',
            is_public=True,
        )
        db.session.add(room)
        db.session.commit()

    return room


@chat.route('/')
@login_required
def chat_home():
    room = get_or_create_room()
    recent_messages = (
        ChatMessage.query
        .filter_by(room_id=room.id)
        .order_by(ChatMessage.id.desc())
        .limit(50)
        .all()
    )
    recent_messages.reverse()

    return render_template(
        'chat.html',
        room=room,
        messages=recent_messages,
    )


@chat.route('/api/messages')
@login_required
def get_messages():
    room = get_or_create_room(request.args.get('room', DEFAULT_ROOM_NAME))
    after_id = request.args.get('after_id', 0, type=int)

    query = ChatMessage.query.filter_by(room_id=room.id)

    if after_id > 0:
        query = query.filter(ChatMessage.id > after_id)

    messages = (
        query
        .order_by(ChatMessage.id.asc())
        .limit(100)
        .all()
    )

    return jsonify({
        'messages': [message.to_dict() for message in messages]
    })


@chat.route('/api/send', methods=['POST'])
@login_required
def send_message():
    data = request.get_json(silent=True) or {}
    body = (data.get('message') or '').strip()
    room_name = (data.get('room') or DEFAULT_ROOM_NAME).strip().lower()

    if not body:
        return jsonify({'error': 'Message cannot be empty.'}), 400

    if len(body) > 1000:
        return jsonify({'error': 'Message is too long. Maximum length is 1000 characters.'}), 400

    room = get_or_create_room(room_name)

    message = ChatMessage(
        room_id=room.id,
        user_id=current_user.id,
        body=body,
    )

    db.session.add(message)
    db.session.commit()

    return jsonify({
        'message': message.to_dict()
    }), 201
