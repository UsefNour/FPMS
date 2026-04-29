from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_required, current_user
from flask_socketio import join_room, leave_room, emit
from sqlalchemy import func
from models import db, User, FriendRequest, Friendship, ChatMessage
from forms import FriendRequestForm
from extensions import socketio

social_bp = Blueprint('social', __name__)

# Tracks which friend each user is currently chatting with (for unread-count suppression)
current_chats = {}


# ── Friend routes ─────────────────────────────────────────────────────────────

@social_bp.route('/friends', methods=['GET', 'POST'])
@login_required
def friends():
    form = FriendRequestForm()
    if form.validate_on_submit():
        username = form.username.data
        user = User.query.filter_by(username=username).first()
        if not user:
            flash('User not found')
        elif user.id == current_user.id:
            flash('You cannot send a friend request to yourself')
        elif FriendRequest.query.filter_by(sender_id=current_user.id, receiver_id=user.id, status='pending').first():
            flash('Friend request already sent')
        elif Friendship.query.filter(
            ((Friendship.user1_id == current_user.id) & (Friendship.user2_id == user.id)) |
            ((Friendship.user1_id == user.id) & (Friendship.user2_id == current_user.id))
        ).first():
            flash('You are already friends')
        else:
            friend_request = FriendRequest(sender_id=current_user.id, receiver_id=user.id)
            db.session.add(friend_request)
            db.session.commit()
            flash('Friend request sent successfully')

    pending_requests = FriendRequest.query.filter_by(receiver_id=current_user.id, status='pending').all()

    friendships = Friendship.query.filter(
        (Friendship.user1_id == current_user.id) | (Friendship.user2_id == current_user.id)
    ).all()
    friends_list = []
    for friendship in friendships:
        friend_id = friendship.user2_id if friendship.user1_id == current_user.id else friendship.user1_id
        friends_list.append(User.query.get(friend_id))

    return render_template('friends.html', form=form, pending_requests=pending_requests, friends_list=friends_list)


@social_bp.route('/add_friend/<int:user_id>', methods=['POST', 'GET'])
@login_required
def add_friend(user_id):
    user = User.query.get_or_404(user_id)

    if user.id == current_user.id:
        flash('You cannot send a friend request to yourself')
    elif FriendRequest.query.filter_by(sender_id=current_user.id, receiver_id=user.id, status='pending').first():
        flash('Friend request already sent')
    elif Friendship.query.filter(
        ((Friendship.user1_id == current_user.id) & (Friendship.user2_id == user.id)) |
        ((Friendship.user1_id == user.id) & (Friendship.user2_id == current_user.id))
    ).first():
        flash('You are already friends')
    else:
        friend_request = FriendRequest(sender_id=current_user.id, receiver_id=user.id)
        db.session.add(friend_request)
        db.session.commit()
        flash('Friend request sent successfully')

    return redirect(request.referrer or url_for('sparring.sparring_dashboard'))


@social_bp.route('/accept_friend/<int:request_id>', methods=['POST'])
@login_required
def accept_friend(request_id):
    friend_request = FriendRequest.query.filter_by(id=request_id, receiver_id=current_user.id, status='pending').first()
    if friend_request:
        friend_request.status = 'accepted'
        # Normalize friendship IDs (smaller ID first)
        user1_id = min(friend_request.sender_id, friend_request.receiver_id)
        user2_id = max(friend_request.sender_id, friend_request.receiver_id)
        db.session.add(Friendship(user1_id=user1_id, user2_id=user2_id))
        db.session.commit()
        flash('Friend request accepted')
    else:
        flash('Friend request not found')
    return redirect(url_for('social.friends'))


@social_bp.route('/decline_friend/<int:request_id>', methods=['POST'])
@login_required
def decline_friend(request_id):
    friend_request = FriendRequest.query.filter_by(id=request_id, receiver_id=current_user.id, status='pending').first()
    if friend_request:
        friend_request.status = 'declined'
        db.session.commit()
        flash('Friend request declined')
    else:
        flash('Friend request not found')
    return redirect(url_for('social.friends'))


@social_bp.route('/remove_friend/<int:friend_id>', methods=['POST'])
@login_required
def remove_friend(friend_id):
    friendship = Friendship.query.filter(
        ((Friendship.user1_id == current_user.id) & (Friendship.user2_id == friend_id)) |
        ((Friendship.user1_id == friend_id) & (Friendship.user2_id == current_user.id))
    ).first()
    if friendship:
        db.session.delete(friendship)
        FriendRequest.query.filter(
            ((FriendRequest.sender_id == current_user.id) & (FriendRequest.receiver_id == friend_id)) |
            ((FriendRequest.sender_id == friend_id) & (FriendRequest.receiver_id == current_user.id))
        ).delete()
        db.session.commit()
        flash('Friend removed successfully')
    else:
        flash('Friend not found')
    return redirect(url_for('social.friends'))


@social_bp.route('/friend_profile/<int:friend_id>')
@login_required
def friend_profile(friend_id):
    friendship = Friendship.query.filter(
        ((Friendship.user1_id == current_user.id) & (Friendship.user2_id == friend_id)) |
        ((Friendship.user1_id == friend_id) & (Friendship.user2_id == current_user.id))
    ).first()
    if not friendship:
        flash('You can only view profiles of your friends')
        return redirect(url_for('social.friends'))

    friend = User.query.get_or_404(friend_id)
    from models import FighterProfile, CampPlan, GamePlan, WeightLog
    profile = FighterProfile.query.filter_by(user_id=friend_id).first()
    latest_weight = WeightLog.query.filter_by(user_id=friend_id).order_by(WeightLog.date.desc()).first()
    current_weight = latest_weight.weight if latest_weight else (profile.walk_around_weight if profile else None)
    camp_plans = CampPlan.query.filter_by(user_id=friend_id).order_by(CampPlan.id.desc()).all()
    game_plans = GamePlan.query.filter_by(user_id=friend_id).order_by(GamePlan.id.desc()).all()

    return render_template('friend_profile.html', friend=friend, profile=profile,
                           current_weight=current_weight, camp_plans=camp_plans, game_plans=game_plans)


# ── Chat routes ───────────────────────────────────────────────────────────────

@social_bp.route('/chat')
@login_required
def chat_page():
    friendships = Friendship.query.filter(
        (Friendship.user1_id == current_user.id) | (Friendship.user2_id == current_user.id)
    ).all()

    chats = []
    for friendship in friendships:
        friend_id = friendship.user2_id if friendship.user1_id == current_user.id else friendship.user1_id
        friend = User.query.get(friend_id)

        last_message = ChatMessage.query.filter(
            ((ChatMessage.sender_id == current_user.id) & (ChatMessage.receiver_id == friend_id)) |
            ((ChatMessage.sender_id == friend_id) & (ChatMessage.receiver_id == current_user.id))
        ).order_by(ChatMessage.timestamp.desc()).first()

        if last_message:
            chats.append({'friend': friend, 'last_message': last_message})

    chats.sort(key=lambda x: x['last_message'].timestamp, reverse=True)
    return render_template('chats.html', chats=chats)


@social_bp.route('/chat/<int:friend_id>')
@login_required
def chat(friend_id):
    friendship = Friendship.query.filter(
        ((Friendship.user1_id == current_user.id) & (Friendship.user2_id == friend_id)) |
        ((Friendship.user1_id == friend_id) & (Friendship.user2_id == current_user.id))
    ).first()
    if not friendship:
        flash('You can only chat with friends')
        return redirect(url_for('social.friends'))

    friend = User.query.get_or_404(friend_id)

    session['current_chat_friend_id'] = friend_id

    ChatMessage.query.filter_by(sender_id=friend_id, receiver_id=current_user.id, is_read=False).update({'is_read': True})
    db.session.commit()

    messages = ChatMessage.query.filter(
        ((ChatMessage.sender_id == current_user.id) & (ChatMessage.receiver_id == friend_id)) |
        ((ChatMessage.sender_id == friend_id) & (ChatMessage.receiver_id == current_user.id))
    ).order_by(ChatMessage.timestamp).all()

    friendships = Friendship.query.filter(
        (Friendship.user1_id == current_user.id) | (Friendship.user2_id == current_user.id)
    ).all()

    chats = []
    for fs in friendships:
        chat_friend_id = fs.user2_id if fs.user1_id == current_user.id else fs.user1_id
        chat_friend = User.query.get(chat_friend_id)

        last_message = ChatMessage.query.filter(
            ((ChatMessage.sender_id == current_user.id) & (ChatMessage.receiver_id == chat_friend_id)) |
            ((ChatMessage.sender_id == chat_friend_id) & (ChatMessage.receiver_id == current_user.id))
        ).order_by(ChatMessage.timestamp.desc()).first()

        unread_count = ChatMessage.query.filter_by(
            sender_id=chat_friend_id,
            receiver_id=current_user.id,
            is_read=False
        ).count()

        if last_message:
            chats.append({'friend': chat_friend, 'last_message': last_message, 'unread_count': unread_count})

    chats.sort(key=lambda x: x['last_message'].timestamp, reverse=True)

    unread_counts = db.session.query(
        ChatMessage.sender_id,
        func.count(ChatMessage.id).label('unread_count')
    ).filter_by(receiver_id=current_user.id, is_read=False).group_by(ChatMessage.sender_id).all()

    unread_dict = {str(count.sender_id): count.unread_count for count in unread_counts}

    socketio.emit('unread_count_update', {
        'unread_counts': unread_dict,
        'new_message_from': None
    }, room=f"user_{current_user.id}")

    return render_template('chat.html', friend=friend, messages=messages, chats=chats)


# ── SocketIO event handlers ───────────────────────────────────────────────────

@socketio.on('join')
def on_join(data):
    username = data.get('username')
    room = data.get('room')
    if username and room:
        join_room(room)


@socketio.on('leave')
def on_leave(data):
    username = data.get('username')
    room = data.get('room')
    if username and room:
        leave_room(room)
        emit('status', {'msg': username + ' has left the room.'}, room=room)


@socketio.on('join_chat')
def on_join_chat(data):
    user_id = data.get('user_id')
    friend_id = data.get('friend_id')
    if user_id and friend_id:
        current_chats[int(user_id)] = int(friend_id)


@socketio.on('leave_chat')
def on_leave_chat(data):
    user_id = data.get('user_id')
    if user_id and int(user_id) in current_chats:
        del current_chats[int(user_id)]


@socketio.on('send_message')
def handle_send_message(data, ack=None):
    sender_id = data.get('sender_id')
    recipient_id = data.get('recipient_id')
    message_text = data.get('message')

    if not sender_id or not recipient_id or not message_text:
        if ack:
            ack({'success': False, 'error': 'Invalid data'})
        return

    try:
        message = ChatMessage(
            sender_id=sender_id,
            receiver_id=recipient_id,
            message=message_text
        )
        db.session.add(message)
        db.session.commit()

        sender = User.query.get(sender_id)
        conversation_room = f"chat_{min(sender_id, recipient_id)}_{max(sender_id, recipient_id)}"

        message_data = {
            'sender_id': sender_id,
            'sender_username': sender.username if sender else 'Unknown',
            'message': message_text,
            'timestamp': message.timestamp.isoformat()
        }

        emit('receive_message', message_data, room=conversation_room)

        # Calculate updated unread counts for the recipient
        unread_counts = db.session.query(
            ChatMessage.sender_id,
            func.count(ChatMessage.id).label('unread_count')
        ).filter_by(receiver_id=recipient_id, is_read=False).group_by(ChatMessage.sender_id).all()

        unread_dict = {str(count.sender_id): count.unread_count for count in unread_counts}

        if int(recipient_id) in current_chats and current_chats[int(recipient_id)] == int(sender_id):
            unread_dict[str(sender_id)] = 0

        emit('unread_count_update', {
            'unread_counts': unread_dict,
            'new_message_from': sender_id
        }, room=f"user_{recipient_id}")

        if ack:
            ack({'success': True, 'message_id': message.id})

    except Exception as e:
        if ack:
            ack({'success': False, 'error': str(e)})
