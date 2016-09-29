from flask import render_template, abort, session, redirect, url_for, current_app, flash
from flask_login import current_user
from .. import db
from ..models import User, Website, Category, WebsiteCategory
from . import main
from .forms import EditProfileForm, WebsiteForm


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@main.route('/user/<username>')
def user(username):
	user = User.query.filter_by(username=username).first_or_404()
	return render_template('user.html', user=user)


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


@main.route('/add_website', methods=['GET', 'POST'])
@login_required
def add_website():
	form = WebsiteForm(user=current_user)
	if form.validate_on_submit():
		website = Website()
		website.url = form.url.data
		website.description = form.description.data
		website.status = form.status.data
		website.user_id = current_app.id
		# 事务
		# 推入消息队列

