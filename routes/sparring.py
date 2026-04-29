from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, User, FighterProfile, SparringProfile, SparringSession, SkillAssessment, Friendship
from forms import SparringProfileForm, SparringSessionForm, SkillAssessmentForm
from datetime import datetime
import math

sparring_bp = Blueprint('sparring', __name__)


def haversine_distance(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    return c * 3959  # miles


def get_sparring_matches(user_id, user_profile):
    matches = []
    all_profiles = SparringProfile.query.filter(SparringProfile.user_id != user_id).all()

    striking_styles = ['Striking', 'Kickboxing', 'Boxing', 'Muay Thai', 'Krav Maga']
    grappling_styles = ['Grappling', 'Wrestling', 'BJJ']

    for profile in all_profiles:
        compatibility = 40
        distance = None

        skill_levels = ['Beginner', 'Intermediate', 'Advanced', 'Expert']
        try:
            user_skill_idx = skill_levels.index(user_profile.skill_level)
            profile_skill_idx = skill_levels.index(profile.skill_level)
            skill_diff = abs(user_skill_idx - profile_skill_idx)
            if skill_diff == 0:
                compatibility += 25
            elif skill_diff == 1:
                compatibility += 20
            elif skill_diff == 2:
                compatibility += 10
        except ValueError:
            compatibility += 10

        user_style = user_profile.preferred_styles
        partner_style = profile.preferred_styles

        if user_style == partner_style:
            compatibility += 25
        elif user_style == 'Mixed' or partner_style == 'Mixed':
            compatibility += 20
        elif user_style in striking_styles and partner_style in striking_styles:
            compatibility += 18
        elif user_style in grappling_styles and partner_style in grappling_styles:
            compatibility += 18
        elif (user_style in striking_styles and partner_style in grappling_styles) or \
             (user_style in grappling_styles and partner_style in striking_styles):
            compatibility += 10

        if user_profile.latitude and user_profile.longitude and profile.latitude and profile.longitude:
            distance = haversine_distance(
                user_profile.latitude, user_profile.longitude,
                profile.latitude, profile.longitude
            )
            if distance > user_profile.max_distance:
                continue
            if distance <= 10:
                compatibility += 20
            elif distance <= 25:
                compatibility += 15
            elif distance <= 50:
                compatibility += 12
            elif distance <= 100:
                compatibility += 8
            else:
                compatibility += 5
        else:
            user_parts = set(user_profile.location.lower().replace(',', '').split())
            profile_parts = set(profile.location.lower().replace(',', '').split())
            common = user_parts.intersection(profile_parts) - {'usa', 'us', 'the', 'of'}
            if common:
                compatibility += min(20, len(common) * 7)
            elif user_profile.location.lower().strip() == profile.location.lower().strip():
                compatibility += 15

        compatibility = max(0, min(100, compatibility))
        if compatibility >= 50:
            matches.append({
                'user': User.query.get(profile.user_id),
                'profile': profile,
                'compatibility': compatibility,
                'distance': round(distance, 1) if distance else None
            })

    matches.sort(key=lambda x: x['compatibility'], reverse=True)
    return matches[:20]


@sparring_bp.route('/sparring_profile', methods=['GET', 'POST'])
@login_required
def sparring_profile():
    form = SparringProfileForm()
    profile = SparringProfile.query.filter_by(user_id=current_user.id).first()

    if request.method == 'GET' and profile:
        form.location.data = profile.location
        form.latitude.data = profile.latitude
        form.longitude.data = profile.longitude
        form.skill_level.data = profile.skill_level
        form.preferred_styles.data = profile.preferred_styles
        form.availability.data = profile.availability
        form.max_distance.data = profile.max_distance
        form.self_skill_rating.data = profile.self_skill_rating

    if form.validate_on_submit():
        if profile:
            profile.location = form.location.data
            profile.latitude = form.latitude.data
            profile.longitude = form.longitude.data
            profile.skill_level = form.skill_level.data
            profile.preferred_styles = form.preferred_styles.data
            profile.availability = form.availability.data
            profile.max_distance = form.max_distance.data
            profile.self_skill_rating = form.self_skill_rating.data
            profile.updated_at = datetime.utcnow()
        else:
            profile = SparringProfile(
                user_id=current_user.id,
                location=form.location.data,
                latitude=form.latitude.data,
                longitude=form.longitude.data,
                skill_level=form.skill_level.data,
                preferred_styles=form.preferred_styles.data,
                availability=form.availability.data,
                max_distance=form.max_distance.data,
                self_skill_rating=form.self_skill_rating.data
            )
            db.session.add(profile)
        db.session.commit()
        flash('Sparring profile updated successfully')
        return redirect(url_for('sparring.sparring_dashboard'))

    return render_template('sparring_profile.html', form=form)


@sparring_bp.route('/sparring_dashboard')
@login_required
def sparring_dashboard():
    profile = SparringProfile.query.filter_by(user_id=current_user.id).first()
    if not profile:
        flash('Please complete your sparring profile first')
        return redirect(url_for('sparring.sparring_profile'))

    potential_matches = get_sparring_matches(current_user.id, profile)
    my_sessions = SparringSession.query.filter(
        (SparringSession.requester_id == current_user.id) | (SparringSession.partner_id == current_user.id)
    ).order_by(SparringSession.session_date.desc()).all()

    return render_template('sparring_dashboard.html', profile=profile,
                           potential_matches=potential_matches, my_sessions=my_sessions)


@sparring_bp.route('/sparring_partner_profile/<int:partner_id>')
@login_required
def sparring_partner_profile(partner_id):
    partner = User.query.get_or_404(partner_id)
    partner_sparring_profile = SparringProfile.query.filter_by(user_id=partner_id).first()
    partner_fighter_profile = FighterProfile.query.filter_by(user_id=partner_id).first()

    if not partner_sparring_profile:
        flash('This user does not have a sparring profile')
        return redirect(url_for('sparring.sparring_dashboard'))

    distance = None
    user_profile = SparringProfile.query.filter_by(user_id=current_user.id).first()
    if user_profile and user_profile.latitude and user_profile.longitude and \
       partner_sparring_profile.latitude and partner_sparring_profile.longitude:
        distance = round(haversine_distance(
            user_profile.latitude, user_profile.longitude,
            partner_sparring_profile.latitude, partner_sparring_profile.longitude
        ), 1)

    assessments = SkillAssessment.query.filter_by(assessed_id=partner_id).order_by(SkillAssessment.created_at.desc()).limit(5).all()
    all_assessments = SkillAssessment.query.filter_by(assessed_id=partner_id).all()
    avg_peer_rating = round(sum(a.skill_rating for a in all_assessments) / len(all_assessments), 1) if all_assessments else None

    is_friend = Friendship.query.filter(
        ((Friendship.user1_id == current_user.id) & (Friendship.user2_id == partner_id)) |
        ((Friendship.user1_id == partner_id) & (Friendship.user2_id == current_user.id))
    ).first() is not None

    return render_template('sparring_partner_profile.html',
                           partner=partner,
                           sparring_profile=partner_sparring_profile,
                           fighter_profile=partner_fighter_profile,
                           distance=distance,
                           assessments=assessments,
                           avg_peer_rating=avg_peer_rating,
                           total_assessments=len(all_assessments),
                           is_friend=is_friend)


@sparring_bp.route('/request_sparring_session/<int:partner_id>', methods=['GET', 'POST'])
@login_required
def request_sparring_session(partner_id):
    form = SparringSessionForm()
    partner = User.query.get_or_404(partner_id)

    if form.validate_on_submit():
        session_datetime_str = f"{form.session_date.data} {form.session_time.data}"
        try:
            session_datetime = datetime.strptime(session_datetime_str, '%Y-%m-%d %I:%M %p')
        except ValueError:
            flash('Invalid date/time format')
            return redirect(request.url)

        sparring_session = SparringSession(
            requester_id=current_user.id,
            partner_id=partner_id,
            session_date=session_datetime,
            duration_minutes=form.duration_minutes.data,
            location=form.location.data,
            notes=form.notes.data
        )
        db.session.add(sparring_session)
        db.session.commit()
        flash('Sparring session request sent successfully')
        return redirect(url_for('sparring.sparring_dashboard'))

    return render_template('request_sparring_session.html', form=form, partner=partner)


@sparring_bp.route('/respond_session/<int:session_id>/<action>', methods=['POST'])
@login_required
def respond_session(session_id, action):
    sparring_session = SparringSession.query.filter_by(id=session_id).filter(
        (SparringSession.requester_id == current_user.id) | (SparringSession.partner_id == current_user.id)
    ).first()

    if not sparring_session:
        flash('Session not found')
        return redirect(url_for('sparring.sparring_dashboard'))

    if action == 'accept':
        sparring_session.status = 'accepted'
        flash('Sparring session accepted')
    elif action == 'decline':
        sparring_session.status = 'declined'
        flash('Sparring session declined')
    elif action == 'complete':
        sparring_session.status = 'completed'
        sparring_session.completed_at = datetime.utcnow()
        flash('Sparring session marked as completed')

    db.session.commit()
    return redirect(url_for('sparring.sparring_dashboard'))


@sparring_bp.route('/assess_session/<int:session_id>', methods=['GET', 'POST'])
@login_required
def assess_session(session_id):
    sparring_session = SparringSession.query.filter_by(id=session_id, status='completed').filter(
        (SparringSession.requester_id == current_user.id) | (SparringSession.partner_id == current_user.id)
    ).first()

    if not sparring_session:
        flash('Session not found or not completed')
        return redirect(url_for('sparring.sparring_dashboard'))

    assessed_id = sparring_session.partner_id if sparring_session.requester_id == current_user.id else sparring_session.requester_id
    assessed_user = User.query.get(assessed_id)

    existing_assessment = SkillAssessment.query.filter_by(
        session_id=session_id,
        assessor_id=current_user.id,
        assessed_id=assessed_id
    ).first()

    if existing_assessment:
        flash('You have already assessed this session')
        return redirect(url_for('sparring.sparring_dashboard'))

    form = SkillAssessmentForm()
    if form.validate_on_submit():
        assessment = SkillAssessment(
            session_id=session_id,
            assessor_id=current_user.id,
            assessed_id=assessed_id,
            skill_rating=form.skill_rating.data,
            assessment_notes=form.assessment_notes.data
        )
        db.session.add(assessment)

        sparring_profile = SparringProfile.query.filter_by(user_id=assessed_id).first()
        if sparring_profile:
            assessments = SkillAssessment.query.filter_by(assessed_id=assessed_id).all()
            peer_ratings = [a.skill_rating for a in assessments if a.assessor_id != assessed_id]
            if peer_ratings:
                avg_peer_rating = sum(peer_ratings) / len(peer_ratings)
                honesty_diff = abs(sparring_profile.self_skill_rating - avg_peer_rating)
                if honesty_diff <= 1:
                    sparring_profile.honesty_score = min(1.0, sparring_profile.honesty_score + 0.1)
                elif honesty_diff >= 3:
                    sparring_profile.honesty_score = max(0.5, sparring_profile.honesty_score - 0.1)

        db.session.commit()
        flash('Assessment submitted successfully')
        return redirect(url_for('sparring.sparring_dashboard'))

    return render_template('assess_session.html', form=form, session=sparring_session, assessed_user=assessed_user)
