from flask import Blueprint, render_template
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

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
    return render_template('profile.html', username=username)
