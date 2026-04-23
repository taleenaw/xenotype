from flask import Blueprint, request, redirect, url_for, flash, render_template
from flask_login import login_required, current_user
from app import db
from app.models import Run, Scenario

game = Blueprint('game', __name__)

@game.route('/play/<int:scenario_id>')
@login_required
def play_scenario(scenario_id):
    scenario = Scenario.query.get_or_404(scenario_id)
    return render_template('play.html', scenario=scenario)

@game.route('/submit_run/<int:scenario_id>', methods=['POST'])
@login_required
def submit_run(scenario_id):
    scenario = Scenario.query.get_or_404(scenario_id)

    wpm = float(request.form.get('wpm', 0))
    accuracy = float(request.form.get('accuracy', 0))
    time_remaining = int(request.form.get('time_remaining', 0))
    errors = int(request.form.get('errors', 0))
    grade = request.form.get('grade', 'F')
    wpm_history = request.form.get('wpm_history', '')

    run = Run(
        user_id=current_user.id,
        scenario_id=scenario.id,
        wpm=wpm,
        accuracy=accuracy,
        time_remaining=time_remaining,
        errors=errors,
        grade=grade,
        wpm_history=wpm_history
    )

    db.session.add(run)
    db.session.commit()

    flash('Run saved successfully.')
    return redirect(url_for('main.leaderboard'))


"""
from flask import Blueprint, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Run, Scenario

game = Blueprint('game', __name__)

@game.route('/submit_run/<int:scenario_id>', methods=['POST'])
@login_required
def submit_run(scenario_id):
    scenario = Scenario.query.get_or_404(scenario_id)

    wpm = float(request.form.get('wpm', 0))
    accuracy = float(request.form.get('accuracy', 0))
    time_remaining = int(request.form.get('time_remaining', 0))
    errors = int(request.form.get('errors', 0))
    grade = request.form.get('grade', 'F')
    wpm_history = request.form.get('wpm_history', '')

    run = Run(
        user_id=current_user.id,
        scenario_id=scenario.id,
        wpm=wpm,
        accuracy=accuracy,
        time_remaining=time_remaining,
        errors=errors,
        grade=grade,
        wpm_history=wpm_history
    )

    db.session.add(run)
    db.session.commit()

    flash('Run saved successfully.')
    return redirect(url_for('main.leaderboard'))
"""
