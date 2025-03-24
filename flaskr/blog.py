from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, created, author_id, firstname'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        driver = request.form['driver']
        sponsor = request.form['sponsor']
        number = request.form['number']
        year = request.form['year']
        picture = request.form['picture']
        error = None

        if not title:
            error = 'Title is required.'
        if not driver:
            error = 'Driver is required.'
        if not sponsor:
            error = 'Sponsor is required.'
        if not number:
            error = 'Number is required.'
        if not year:
            error = 'Year is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, driver, sponsor, number, year, picture, author_id)'
                ' VALUES (?, ?, ?, ?, ?, ?, ?)',
                (title, driver, sponsor, number, year, picture, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        driver = request.form['driver']
        sponsor = request.form['sponsor']
        number = request.form['number']
        year = request.form['year']
        picture = request.form['picture']
        error = None

        if not title:
            error = 'Title is required.'
        if not driver:
            error = 'Driver is required.'
        if not sponsor:
            error = 'Sponsor is required.'
        if not number:
            error = 'Number is required.'
        if not year:
            error = 'Year is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, driver = ?, sponsor = ?, number = ?, year = ?, picture = ?'
                ' WHERE id = ?',
                (title, driver, sponsor, number, year, picture, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))

@bp.route('/post/<int:id>')
def view_post(id):
    post = get_post(id, check_author=False)
    return render_template('blog/view.html', post=post)
