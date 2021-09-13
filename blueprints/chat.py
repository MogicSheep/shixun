import os
import sys
sys.path.append("..")
from flask import render_template, redirect, url_for, request, Blueprint, current_app, abort
from flask_login import current_user, login_required
from flask_socketio import emit
from models import Message, User,db
from utils import to_html, flash_errors

chat_bp = Blueprint('chat', __name__)

online_users = []


@socketio.on('new message')
def new_message(message_body):
    html_message = to_html(message_body)
    message = Message(author=current_user._get_current_object(), body=html_message)
    db.session.add(message)
    db.session.commit()
    emit('new message',
         {'message_html': message,
          'message_body': html_message,
          'gravatar': current_user.gravatar,
          'nickname': current_user.name,
          'user_id': current_user.id},
         broadcast=True)


@socketio.on('connect')
def connect():
    global online_users
    if current_user.is_authenticated and current_user.id not in online_users:
        online_users.append(current_user.id)
    emit('user count', {'count': len(online_users)}, broadcast=True)


@socketio.on('disconnect')
def disconnect():
    global online_users
    if current_user.is_authenticated and current_user.id in online_users:
        online_users.remove(current_user.id)
    emit('user count', {'count': len(online_users)}, broadcast=True)


@chat_bp.route('/api/v1/messages')
def get_messages():
    page = request.args.get('page', 1, type=int)
    pagination = Message.query.order_by(Message.timestamp.desc()).paginate(
        page, per_page=current_app.config['CATCHAT_MESSAGE_PER_PAGE'])
    messages = pagination.items
    return jsonify({
        'Success':True,
        'message': messages[::-1]
    })


@chat_bp.route('/api/v1/message/home')
def home():
    amount = current_app.config['CATCHAT_MESSAGE_PER_PAGE']
    messages = Message.query.order_by(Message.timestamp.asc())[-amount:]
    return jsonify({
        'Success':True,
        'messages': messages
    })

@chat_bp.route('/api/v1/message/delete/<message_id>', methods=['DELETE'])
def delete_message(message_id):
    message = Message.query.get_or_404(message_id)
    if current_user != message.author and not current_user.is_admin:
        abort(403)
    db.session.delete(message)
    db.session.commit()
    return '', 204
