from flask import render_template

from web import app

@app.route('/')
@app.route('/index')
def index():
    title = app.config.get('TITLE')
    return render_template('index.html',
                           title=title)
