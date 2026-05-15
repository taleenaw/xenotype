import os
from uuid import uuid4

from flask import (
    Blueprint,
    abort,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from app import db
from app.models import User, Run, Scenario
from app.ranking import RANKED_BORDER_FILES

main = Blueprint('main', __name__)

ALLOWED_PROFILE_PHOTO_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}


def allowed_profile_photo(filename):
    """Return True when the uploaded profile photo has a safe image extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_PROFILE_PHOTO_EXTENSIONS


@main.route('/rank-borders/<filename>')
def rank_border(filename):
    if filename not in RANKED_BORDER_FILES:
        abort(404)

    border_dir = os.path.join(
        os.path.dirname(current_app.root_path),
        'assets',
        'Borders',
    )
    return send_from_directory(border_dir, filename)


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
        .join(User, Run.user_id == User.id)
        .join(Scenario, Run.scenario_id == Scenario.id)
        .order_by(Run.wpm.desc(), Run.accuracy.desc())
        .all()
    )

    best_runs_by_user = {}
    for run in all_runs:
        if run.user_id not in best_runs_by_user:
            best_runs_by_user[run.user_id] = run

    leaderboard_entries = []
    for run in best_runs_by_user.values():
        rank_tier = run.user.get_rank_tier()
        leaderboard_entries.append({
            'run': run,
            'rank_tier': rank_tier,
        })

    leaderboard_entries.sort(
        key=lambda entry: (
            entry['rank_tier']['score'] is not None,
            entry['rank_tier']['score'] or 0,
            entry['run'].wpm,
            entry['run'].accuracy,
        ),
        reverse=True,
    )

    top_entries = leaderboard_entries[:10]

    return render_template('leaderboard.html', top_entries=top_entries)


@main.route('/missions')
def missions():
    return render_template('Missions.html')


@main.route('/profile/<username>', methods=['GET', 'POST'])
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()

    if request.method == 'POST':
        if user.id != current_user.id:
            flash("You can only update your own profile photo.")
            return redirect(url_for('main.profile', username=user.username))

        photo = request.files.get('profile_photo')

        if not photo or photo.filename == '':
            flash("Choose an image file before uploading.")
            return redirect(url_for('main.profile', username=user.username))

        if not allowed_profile_photo(photo.filename):
            flash("Profile photo must be PNG, JPG, JPEG, GIF, or WEBP.")
            return redirect(url_for('main.profile', username=user.username))

        original_filename = secure_filename(photo.filename)
        extension = original_filename.rsplit('.', 1)[1].lower()
        unique_filename = f"user_{user.id}_{uuid4().hex}.{extension}"

        profile_photo_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], 'profile_photos')
        os.makedirs(profile_photo_dir, exist_ok=True)

        save_path = os.path.join(profile_photo_dir, unique_filename)
        photo.save(save_path)

        user.profile_photo = f"uploads/profile_photos/{unique_filename}"
        db.session.commit()

        flash("Profile photo updated.")
        return redirect(url_for('main.profile', username=user.username))

    # Recent runs are shown newest first in the table.
    runs = Run.query.filter_by(user_id=user.id).order_by(Run.completed_at.desc()).all()

    # Graph data is oldest first, so the x-axis is Attempt 1, Attempt 2, etc.
    runs_for_graph = list(reversed(runs))
    wpm_labels = [f"Attempt {index}" for index in range(1, len(runs_for_graph) + 1)]
    wpm_values = [round(run.wpm, 2) for run in runs_for_graph]

    best_wpm = max((run.wpm for run in runs), default=0)
    avg_accuracy = round(sum(run.accuracy for run in runs) / len(runs), 2) if runs else 0
    rank_tier = user.get_rank_tier()

    return render_template(
        'profile.html',
        user=user,
        runs=runs,
        best_wpm=best_wpm,
        avg_accuracy=avg_accuracy,
        rank_tier=rank_tier,
        wpm_labels=wpm_labels,
        wpm_values=wpm_values
    )
