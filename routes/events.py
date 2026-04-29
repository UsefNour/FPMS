from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, Event, EventInterest
from forms import CreateEventForm, EventFilterForm, EventInterestForm
from datetime import datetime

events_bp = Blueprint('events', __name__)


@events_bp.route('/events')
def events():
    form = EventFilterForm()

    city = request.args.get('city', '').strip()
    country = request.args.get('country', '').strip()
    weight_class = request.args.get('weight_class', '')
    experience_level = request.args.get('experience_level', '')
    event_type = request.args.get('event_type', '')
    rules = request.args.get('rules', '')

    query = Event.query.filter(Event.date >= datetime.utcnow(), Event.is_approved == True)

    if city:
        query = query.filter(Event.city.ilike(f'%{city}%'))
    if country:
        query = query.filter(Event.country.ilike(f'%{country}%'))
    if weight_class:
        query = query.filter(Event.weight_classes.ilike(f'%{weight_class}%'))
    if experience_level:
        query = query.filter(Event.experience_levels.ilike(f'%{experience_level}%'))
    if event_type:
        query = query.filter(Event.event_type.ilike(f'%{event_type}%'))
    if rules:
        query = query.filter(Event.rules.ilike(f'%{rules}%'))

    events_list = query.order_by(Event.date.asc()).all()

    user_interests = {}
    if current_user.is_authenticated:
        interests = EventInterest.query.filter_by(user_id=current_user.id).all()
        user_interests = {i.event_id: i.status for i in interests}

    return render_template('events.html', events=events_list, form=form, user_interests=user_interests)


@events_bp.route('/events/create', methods=['GET', 'POST'])
@login_required
def create_event():
    form = CreateEventForm()

    if form.validate_on_submit():
        try:
            time_str = form.event_time.data.strip()
            event_datetime = None
            for fmt in ['%I:%M %p', '%I:%M%p', '%H:%M', '%I %p', '%I%p']:
                try:
                    time_obj = datetime.strptime(time_str.upper(), fmt)
                    event_datetime = datetime.combine(form.date.data, time_obj.time())
                    break
                except ValueError:
                    continue
            if not event_datetime:
                event_datetime = datetime.combine(form.date.data, datetime.strptime('12:00 PM', '%I:%M %p').time())
        except Exception:
            event_datetime = datetime.combine(form.date.data, datetime.strptime('12:00 PM', '%I:%M %p').time())

        reg_deadline = None
        if form.registration_deadline.data:
            reg_deadline = datetime.combine(form.registration_deadline.data, datetime.strptime('11:59 PM', '%I:%M %p').time())

        event = Event(
            name=form.name.data,
            description=form.description.data,
            event_type=form.event_type.data,
            date=event_datetime,
            registration_deadline=reg_deadline,
            venue_name=form.venue_name.data,
            location=form.location.data,
            city=form.city.data,
            state=form.state.data,
            country=form.country.data,
            weight_classes=','.join(form.weight_classes.data),
            experience_levels=','.join(form.experience_levels.data),
            rules=form.rules.data,
            entry_fee=form.entry_fee.data or 0,
            prize_info=form.prize_info.data,
            max_participants=form.max_participants.data,
            contact_email=form.contact_email.data,
            contact_phone=form.contact_phone.data,
            website=form.website.data,
            organizer_id=current_user.id
        )
        db.session.add(event)
        db.session.commit()
        flash(f'Event "{event.name}" created successfully!', 'success')
        return redirect(url_for('events.event_detail', event_id=event.id))

    return render_template('create_event.html', form=form)


@events_bp.route('/admin/events')
@login_required
def admin_events():
    if not getattr(current_user, 'is_admin', False):
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('events.events'))

    all_events = Event.query.order_by(Event.date.desc()).all()
    events_data = []
    total_registered = total_interested = upcoming_count = 0

    for event in all_events:
        participants = EventInterest.query.filter_by(event_id=event.id).order_by(EventInterest.created_at.desc()).all()
        registered_count = sum(1 for p in participants if p.status == 'registered')
        interested_count = sum(1 for p in participants if p.status == 'interested')
        total_registered += registered_count
        total_interested += interested_count
        if event.date >= datetime.utcnow():
            upcoming_count += 1
        events_data.append({
            'id': event.id,
            'name': event.name,
            'date': event.date,
            'city': event.city,
            'state': event.state,
            'country': event.country,
            'event_type': event.event_type,
            'rules': event.rules,
            'registered_count': registered_count,
            'interested_count': interested_count,
            'participants': participants
        })

    return render_template('admin_events.html',
                           events=events_data,
                           total_events=len(all_events),
                           total_registered=total_registered,
                           total_interested=total_interested,
                           upcoming_events=upcoming_count)


@events_bp.route('/events/<int:event_id>')
def event_detail(event_id):
    event = Event.query.get_or_404(event_id)

    interest_count = EventInterest.query.filter_by(event_id=event_id, status='interested').count()
    registered_count = EventInterest.query.filter_by(event_id=event_id, status='registered').count()

    user_interest = None
    if current_user.is_authenticated:
        user_interest = EventInterest.query.filter_by(event_id=event_id, user_id=current_user.id).first()

    interested_users = []
    is_admin = current_user.is_authenticated and getattr(current_user, 'is_admin', False)
    if current_user.is_authenticated and (current_user.id == event.organizer_id or is_admin):
        for interest in EventInterest.query.filter_by(event_id=event_id).order_by(EventInterest.created_at.desc()).all():
            interested_users.append({
                'user': interest.user,
                'status': interest.status,
                'weight_class': interest.weight_class,
                'notes': interest.notes,
                'date': interest.created_at
            })

    interest_form = EventInterestForm()
    interest_form.weight_class.choices = [(wc, wc) for wc in event.get_weight_classes_list()]

    return render_template('event_detail.html',
                           event=event,
                           interest_count=interest_count,
                           registered_count=registered_count,
                           user_interest=user_interest,
                           interested_users=interested_users,
                           interest_form=interest_form)


@events_bp.route('/events/<int:event_id>/interest', methods=['POST'])
@login_required
def express_interest(event_id):
    event = Event.query.get_or_404(event_id)

    if event.date < datetime.utcnow():
        flash('This event has already passed.', 'warning')
        return redirect(url_for('events.event_detail', event_id=event_id))

    if event.organizer_id == current_user.id:
        flash("You can't register for your own event.", 'warning')
        return redirect(url_for('events.event_detail', event_id=event_id))

    weight_class = request.form.get('weight_class')
    notes = request.form.get('notes', '')
    action = request.form.get('action', 'interest')

    existing = EventInterest.query.filter_by(event_id=event_id, user_id=current_user.id).first()

    if existing:
        if action == 'withdraw':
            existing.status = 'withdrawn'
            flash('You have withdrawn your interest.', 'info')
        elif action == 'register':
            existing.status = 'registered'
            existing.weight_class = weight_class
            existing.notes = notes
            flash('You are now registered for this event!', 'success')
        else:
            existing.status = 'interested'
            existing.weight_class = weight_class
            existing.notes = notes
            flash('Your interest has been updated.', 'success')
    else:
        interest = EventInterest(
            event_id=event_id,
            user_id=current_user.id,
            status='registered' if action == 'register' else 'interested',
            weight_class=weight_class,
            notes=notes
        )
        db.session.add(interest)
        flash('You are now registered for this event!' if action == 'register' else 'You have expressed interest in this event.', 'success')

    db.session.commit()
    return redirect(url_for('events.event_detail', event_id=event_id))


@events_bp.route('/events/my-events')
@login_required
def my_events():
    organized = Event.query.filter_by(organizer_id=current_user.id).order_by(Event.date.desc()).all()
    my_interests = EventInterest.query.filter(
        EventInterest.user_id == current_user.id,
        EventInterest.status.in_(['interested', 'registered'])
    ).all()
    interested_events = [{'event': i.event, 'status': i.status, 'weight_class': i.weight_class} for i in my_interests]
    return render_template('my_events.html', organized_events=organized, interested_events=interested_events)


@events_bp.route('/events/<int:event_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    event = Event.query.get_or_404(event_id)

    if event.organizer_id != current_user.id:
        flash("You don't have permission to edit this event.", 'danger')
        return redirect(url_for('events.event_detail', event_id=event_id))

    form = CreateEventForm(obj=event)

    if request.method == 'GET':
        form.weight_classes.data = event.get_weight_classes_list()
        form.experience_levels.data = event.get_experience_levels_list()
        form.event_time.data = event.date.strftime('%I:%M %p')
        form.date.data = event.date.date()
        if event.registration_deadline:
            form.registration_deadline.data = event.registration_deadline.date()

    if form.validate_on_submit():
        try:
            time_str = form.event_time.data.strip()
            for fmt in ['%I:%M %p', '%I:%M%p', '%H:%M', '%I %p', '%I%p']:
                try:
                    time_obj = datetime.strptime(time_str.upper(), fmt)
                    event.date = datetime.combine(form.date.data, time_obj.time())
                    break
                except ValueError:
                    continue
        except Exception:
            pass

        event.name = form.name.data
        event.description = form.description.data
        event.event_type = form.event_type.data
        event.venue_name = form.venue_name.data
        event.location = form.location.data
        event.city = form.city.data
        event.state = form.state.data
        event.country = form.country.data
        event.weight_classes = ','.join(form.weight_classes.data)
        event.experience_levels = ','.join(form.experience_levels.data)
        event.rules = form.rules.data
        event.entry_fee = form.entry_fee.data or 0
        event.prize_info = form.prize_info.data
        event.max_participants = form.max_participants.data
        event.contact_email = form.contact_email.data
        event.contact_phone = form.contact_phone.data
        event.website = form.website.data

        if form.registration_deadline.data:
            event.registration_deadline = datetime.combine(
                form.registration_deadline.data,
                datetime.strptime('11:59 PM', '%I:%M %p').time()
            )

        db.session.commit()
        flash('Event updated successfully!', 'success')
        return redirect(url_for('events.event_detail', event_id=event_id))

    return render_template('create_event.html', form=form, edit_mode=True, event=event)


@events_bp.route('/events/<int:event_id>/delete', methods=['POST'])
@login_required
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)

    if event.organizer_id != current_user.id:
        flash("You don't have permission to delete this event.", 'danger')
        return redirect(url_for('events.event_detail', event_id=event_id))

    EventInterest.query.filter_by(event_id=event_id).delete()
    event_name = event.name
    db.session.delete(event)
    db.session.commit()
    flash(f'Event "{event_name}" has been deleted.', 'info')
    return redirect(url_for('events.events'))
