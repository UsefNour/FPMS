from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, Fighter
from forms import FighterForm

fighters_bp = Blueprint('fighters', __name__)


@fighters_bp.route('/fighters', methods=['GET', 'POST'])
@login_required
def fighters():
    form = FighterForm()
    search_query = request.args.get('search', '')
    weight_class_filter = request.args.get('weight_class', '')

    if form.validate_on_submit():
        fighter = Fighter(
            name=form.name.data,
            nickname=form.nickname.data,
            weight_class=form.weight_class.data,
            record=form.record.data,
            fighting_style=form.fighting_style.data,
            strengths=form.strengths.data,
            weaknesses=form.weaknesses.data,
            notable_fights=form.notable_fights.data
        )
        db.session.add(fighter)
        db.session.commit()
        flash('Fighter added successfully')
        return redirect(url_for('fighters.fighters'))

    query = Fighter.query
    if search_query:
        query = query.filter(Fighter.name.ilike(f'%{search_query}%'))
    if weight_class_filter:
        query = query.filter_by(weight_class=weight_class_filter)

    fighters_list = query.order_by(Fighter.name).all()
    weight_classes = [wc[0] for wc in db.session.query(Fighter.weight_class).distinct().all()]

    return render_template('fighters.html', form=form, fighters=fighters_list,
                           search_query=search_query, weight_class_filter=weight_class_filter,
                           weight_classes=weight_classes)


@fighters_bp.route('/compare_fighters')
@login_required
def compare_fighters():
    all_fighters = Fighter.query.order_by(Fighter.name).all()
    fighter1_id = request.args.get('fighter1', type=int)
    fighter2_id = request.args.get('fighter2', type=int)
    fighter1 = Fighter.query.get(fighter1_id) if fighter1_id else None
    fighter2 = Fighter.query.get(fighter2_id) if fighter2_id else None
    return render_template('compare_fighters.html', all_fighters=all_fighters,
                           fighter1=fighter1, fighter2=fighter2)


@fighters_bp.route('/fighter/<int:fighter_id>')
@login_required
def fighter_detail(fighter_id):
    fighter = Fighter.query.get_or_404(fighter_id)
    return render_template('fighter_detail.html', fighter=fighter)


@fighters_bp.route('/edit_fighter/<int:fighter_id>', methods=['GET', 'POST'])
@login_required
def edit_fighter(fighter_id):
    fighter = Fighter.query.get_or_404(fighter_id)
    form = FighterForm()

    if request.method == 'GET':
        form.name.data = fighter.name
        form.nickname.data = fighter.nickname
        form.weight_class.data = fighter.weight_class
        form.record.data = fighter.record
        form.fighting_style.data = fighter.fighting_style
        form.strengths.data = fighter.strengths
        form.weaknesses.data = fighter.weaknesses
        form.notable_fights.data = fighter.notable_fights

    if form.validate_on_submit():
        fighter.name = form.name.data
        fighter.nickname = form.nickname.data
        fighter.weight_class = form.weight_class.data
        fighter.record = form.record.data
        fighter.fighting_style = form.fighting_style.data
        fighter.strengths = form.strengths.data
        fighter.weaknesses = form.weaknesses.data
        fighter.notable_fights = form.notable_fights.data
        db.session.commit()
        flash('Fighter updated successfully')
        return redirect(url_for('fighters.fighter_detail', fighter_id=fighter.id))

    return render_template('edit_fighter.html', form=form, fighter=fighter)


@fighters_bp.route('/delete_fighter/<int:fighter_id>', methods=['POST'])
@login_required
def delete_fighter(fighter_id):
    fighter = Fighter.query.get_or_404(fighter_id)
    db.session.delete(fighter)
    db.session.commit()
    flash('Fighter deleted successfully')
    return redirect(url_for('fighters.fighters'))


@fighters_bp.route('/use_fighter/<int:fighter_id>')
@login_required
def use_fighter(fighter_id):
    Fighter.query.get_or_404(fighter_id)
    return redirect(url_for('training.game_plan', fighter_id=fighter_id))
