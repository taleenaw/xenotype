from flask import Blueprint, render_template
from flask_login import login_required
from app.models import User, Run, Scenario

main = Blueprint('main', __name__)

@main.route('/')
def lobby():
    return render_template('lobby.html')

@main.route('/scenarios')
def scenarios():
    scenarios = Scenario.query.order_by(Scenario.created_at.desc()).all()
    return render_template('scenarios.html', scenarios=scenarios)

@main.route('/leaderboard')
def leaderboard():
    all_runs = (
        Run.query
        .join(User)
        .join(Scenario)
        .order_by(Run.wpm.desc(), Run.accuracy.desc())
        .all()
    )

    best_runs_by_user = {}
    for run in all_runs:
        if run.user_id not in best_runs_by_user:
            best_runs_by_user[run.user_id] = run

    top_runs = list(best_runs_by_user.values())[:10]

    return render_template('leaderboard.html', top_runs=top_runs)

@main.route('/profile/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    runs = Run.query.filter_by(user_id=user.id).order_by(Run.completed_at.desc()).all()

    best_wpm = max((run.wpm for run in runs), default=0)
    avg_accuracy = round(sum(run.accuracy for run in runs) / len(runs), 2) if runs else 0

    return render_template(
        'profile.html',
        user=user,
        runs=runs,
        best_wpm=best_wpm,
        avg_accuracy=avg_accuracy
    )



"""
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import User, Run


main = Blueprint('main', __name__)

@main.route('/test_db')
def test_db():
    from app.models import Scenario
    scenarios = Scenario.query.all()
    return f"{len(scenarios)} scenarios in DB"

@main.route('/')

def lobby():
    return render_template('lobby.html')

@main.route('/scenarios')
def scenarios():
    return render_template('scenarios.html')

@main.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html')

@main.route('/profile/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()

    runs = Run.query.filter_by(user_id=user.id).order_by(Run.completed_at.desc()).all()

    best_wpm = max((run.wpm for run in runs), default=0)

    avg_accuracy = round(sum(run.accuracy for run in runs) / len(runs), 2) if runs else 0

    return render_template(

        'profile.html',

        user=user,

        runs=runs,

        best_wpm=best_wpm,

        avg_accuracy=avg_accuracy

    )
    #return render_template('profile.html', username=username)
"""
