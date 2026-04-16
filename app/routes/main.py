from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')

def lobby():
    return render_template('lobby.html')
