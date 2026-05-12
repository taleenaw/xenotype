from flask import Blueprint, request, redirect, url_for, flash, render_template
from flask_login import login_required, current_user
from app import db
from app.models import Run, Scenario
from app.routes.own_missions import stories

game = Blueprint('game', __name__)

@game.route('/missions/play/<mission_id>')
@login_required
def mission_play(mission_id):
    mission = stories.get(mission_id)
    if not mission:
        flash('Mission not found.')
        return redirect(url_for('main.lobby'))
    return render_template('mission_play.html', mission=mission, mission_id=mission_id)

@game.route('/submit_mission_run/<mission_id>', methods=['POST'])
@login_required
def submit_mission_run(mission_id):
    wpm = float(request.form.get('wpm', 0))
    accuracy = float(request.form.get('accuracy', 0))
    errors = int(request.form.get('errors', 0))
    grade = request.form.get('grade', 'F')

    run = Run(
        user_id=current_user.id,
        scenario_id=1,
        wpm=wpm,
        accuracy=accuracy,
        time_remaining=0,
        errors=errors,
        grade=grade,
        wpm_history=""
    )
    db.session.add(run)
    db.session.commit()

    flash('Mission run saved successfully.')
    return redirect(url_for('main.leaderboard'))


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

    return redirect(url_for('game.outcome', run_id=run.id))

@game.route('/outcome/<int:run_id>')
@login_required
def outcome(run_id):
    run = Run.query.get_or_404(run_id)
    scenario = run.scenario

    if run.wpm >= 80 and run.accuracy >= 95:
        outcome_text = scenario.outcome_high
    elif run.wpm >= 45:
        outcome_text = scenario.outcome_mid
    else:
        outcome_text = scenario.outcome_low
  
    import json
    try:
        wpm_history = json.loads(run.wpm_history or '[]')
    except:
        wpm_history = []

    return render_template('outcome.html',
        run=run,
        scenario=scenario,
        outcome_text=outcome_text,
        wpm_history=wpm_history
    )
