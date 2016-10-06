from flask import render_template, abort, session, redirect, url_for, current_app, flash
from flask_login import current_user, login_required
from .. import db
from ..models import User, Website, Category, WebsiteCategory
from . import main
from .forms import EditProfileForm, WebsiteForm, CategoryForm


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@main.route('/user/<username>')
def user(username):
    user1 = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user1)


@main.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('Your profile has been updated.')
        return redirect(url_for('.user', username=current_user.username))
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@main.route('/add_category', methods=['GET', 'POST'])
@login_required
def add_category():
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category()
        category.name = form.name.data
        category.user_id = current_user.id
        db.session.add(category)
        flash('Add category successful!')
        return redirect(url_for('main.index'))
    return render_template('add_category.html', form=form)


@main.route('/edit_category/<int:cid>', methods=['GET', 'POST'])
@login_required
def edit_category(cid):
    category = Category.query.get_or_404(cid)
    if category.user_id != current_user.id or category.is_del == 1:
        abort(403)
    form = CategoryForm()
    if form.validate_on_submit():
        category.name = form.name.data
        db.session.add(category)
        flash('Edit category successful!')
        return redirect(url_for('main.index'))
    form.name.data = category.name
    return render_template('add_category.html', form=form)


@main.route('/add_website', methods=['GET', 'POST'])
@login_required
def add_website():
    form = WebsiteForm(user=current_user)
    if form.validate_on_submit():
        website = Website()
        website.url = form.url.data
        website.description = form.description.data
        website.status = form.status.data
        website.user_id = current_user.id

        try:
            db.session.add(website)
            db.session.flush()
            website_category = WebsiteCategory()
            website_category.category_id = form.category.data
            website_category.website_id = website.id
            db.session.add(website_category)
            db.session.commit()
        except:
            db.session.rollback()
            raise RuntimeError('DB error')
        flash('Add Successful!')
        return redirect(url_for('main.index'))
    return render_template('add_website.html', form=form)


@main.route('/edit_website/<int:wid>', methods=['GET', 'POST'])
@login_required
def edit_website(wid):
    website = Website.query.get_or_404(wid)
    website_category = WebsiteCategory.query.get_or_404(website.id)  # 获得类别
    if website.user_id != current_user.id:
        abort(403)
    form = WebsiteForm(user=current_user)
    if form.validate_on_submit():
        website.url = form.url.data
        website.description = form.description.data
        website.status = form.status.data
        website.user_id = current_app.id

        try:
            db.session.add(website)
            db.session.flush()
            website_category.category_id = form.category.data
            website_category.website_id = website.id
            db.session.add(website_category)
            db.session.commit()
        except:
            db.session.rollback()
            raise RuntimeError('DB error')
        flash('Edit Successful!')
        return redirect(url_for('index.html'))
    form.url.data = website.url
    form.title.data = website.title
    form.description.data = website.description
    form.category.data = website_category.category_id
    form.status.data = website.status
    return render_template('add_website.html', form=form)
