import os
from uuid import uuid4

from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from app import db
from app.models import User, Run, Scenario

main = Blueprint('main', __name__)

ALLOWED_PROFILE_PHOTO_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}


def allowed_profile_photo(filename):
    """Return True when the uploaded profile photo has a safe image extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_PROFILE_PHOTO_EXTENSIONS


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

        user.profile_photo = f"profile_photos/{unique_filename}"
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

    return render_template(
        'profile.html',
        user=user,
        runs=runs,
        best_wpm=best_wpm,
        avg_accuracy=avg_accuracy,
        wpm_labels=wpm_labels,
        wpm_values=wpm_values
    )
