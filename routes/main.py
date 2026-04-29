from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models import FighterProfile, WeightLog, Friendship, ChatMessage
from datetime import datetime

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
@main_bp.route('/dashboard')
@login_required
def dashboard():
    profile = FighterProfile.query.filter_by(user_id=current_user.id).first()
    if not profile:
        flash('Please complete your fighter profile first')
        return redirect(url_for('training.profile'))

    fight_date = profile.fight_date
    today = datetime.today().date()
    days_until_fight = (fight_date - today).days

    latest_weight = WeightLog.query.filter_by(user_id=current_user.id).order_by(WeightLog.date.desc()).first()
    current_weight = latest_weight.weight if latest_weight else profile.walk_around_weight

    target_weight = profile.walk_around_weight - 10
    weight_status = "On Track" if current_weight <= target_weight else "Over Target"

    weeks_remaining = max(1, (fight_date - today).days // 7)
    if weeks_remaining > 8:
        camp_phase = "Base Conditioning"
    elif weeks_remaining > 4:
        camp_phase = "Skill Sharpening"
    elif weeks_remaining > 1:
        camp_phase = "Sparring Peak"
    else:
        camp_phase = "Taper Week"

    warnings = []
    if weight_status == "Over Target":
        warnings.append("Weight cut may be too aggressive")
    if profile.training_availability < 4:
        warnings.append("Low training availability may impact readiness")

    recent_chats = []
    friendships = Friendship.query.filter(
        (Friendship.user1_id == current_user.id) | (Friendship.user2_id == current_user.id)
    ).all()

    for friendship in friendships:
        friend_id = friendship.user2_id if friendship.user1_id == current_user.id else friendship.user1_id
        from models import User
        friend = User.query.get(friend_id)

        last_message = ChatMessage.query.filter(
            ((ChatMessage.sender_id == current_user.id) & (ChatMessage.receiver_id == friend_id)) |
            ((ChatMessage.sender_id == friend_id) & (ChatMessage.receiver_id == current_user.id))
        ).order_by(ChatMessage.timestamp.desc()).first()

        unread_count = ChatMessage.query.filter_by(
            sender_id=friend_id,
            receiver_id=current_user.id,
            is_read=False
        ).count()

        if last_message:
            recent_chats.append({
                'friend': friend,
                'last_message': last_message,
                'unread_count': unread_count
            })

    recent_chats.sort(key=lambda x: x['last_message'].timestamp, reverse=True)
    recent_chats = recent_chats[:5]

    return render_template('dashboard.html', profile=profile, days_until_fight=days_until_fight,
                           current_weight=current_weight, weight_status=weight_status,
                           camp_phase=camp_phase, warnings=warnings, recent_chats=recent_chats)
