from flask import render_template, url_for, redirect, request, Blueprint
from mainpackage.authentication import login_required, role_required, roles_required
from mainpackage import User, Opportunity, Poster, db
from datetime import datetime
from pytz import timezone

bp = Blueprint('opportunities', __name__, url_prefix='/posts')


@bp.route('/', methods=['GET', 'POST'])
@login_required
@roles_required('admin', 'community-partner')
def posts():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['post']
        post_author = request.form['author']
        post_occurance = request.form['occurance_from']
        new_post = Poster(title=post_title,
                          content=post_content, posted_by=post_author, posted_on=datetime.now(timezone('US/Eastern')),
                          occurance_from=post_occurance)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('opportunities.posts'))
    else:
        all_posts = Poster.query.order_by(Poster.posted_on).all()
        return render_template('posts.html', posts=all_posts)


@bp.route('/new', methods=['GET', 'POST'])
@login_required
@roles_required('admin', 'community-partner')
def new_post():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['post']
        post_author = request.form['author']
        post_occurance = request.form['occurance_from']
        new_post = Poster(title=post_title,
                          content=post_content, posted_by=post_author, posted_on=datetime.now(timezone('US/Eastern')),
                          occurance_from=post_occurance)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('opportunities.post'))
    else:
        return render_template('new_post.html')


@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@roles_required('admin', 'community-partner')
def edit(id):
    to_edit = Poster.query.get_or_404(id)
    if request.method == 'POST':
        to_edit.title = request.form['title']
        to_edit.posted_by = request.form['author']
        to_edit.content = request.form['post']
        to_edit.occurance_from = request.form['occurance_from']
        db.session.commit()
        return redirect(url_for('opportunities.posts'))
    else:
        return render_template('edit.html', post=to_edit)


@bp.route('/delete/<int:id>')
@login_required
@roles_required('admin', 'community-partner')
def delete(id):
    to_delete = Poster.query.get_or_404(id)
    db.session.delete(to_delete)
    db.session.commit()
    return redirect(url_for('opportunities.posts'))
