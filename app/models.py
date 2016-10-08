# coding=utf-8
from datetime import datetime
from . import db, login_manage
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
# from flask_wtf import Form


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.BOOLEAN, default=False)
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)

    @property
    def password(self):
        raise AttributeError('password can not read')

    @password.setter
    def password(self, password):
        """
        生成hash类型的密码串
        :param password:
        :return:
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        验证密码登陆用
        :param password:
        :return:
        """
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def __repr__(self):
        return '<User %r>' % self.username


@login_manage.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    is_del = db.Column(db.BOOLEAN, default=False)
    create_time = db.Column(db.DateTime(), default=datetime.utcnow)
    modify_time = db.Column(db.DateTime(), default=datetime.utcnow)
    user_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Category %r>' % self.name


class WebsiteCategory(db.Model):
    __tablename__ = 'websites_category'
    id = db.Column(db.Integer, primary_key=True)
    website_id = db.Column(db.Integer, index=True)
    category_id = db.Column(db.Integer, index=True)


class Website(db.Model):
    __tablename__ = 'websites'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(64), index=True)
    title = db.Column(db.String(64))
    description = db.Column(db.Text())
    status = db.Column(db.BOOLEAN, default=False)  # 状态
    is_del = db.Column(db.BOOLEAN, default=False)  # 默认不删除
    create_time = db.Column(db.DateTime(), default=datetime.utcnow)
    modify_time = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer,nullable=False)

    def __repr__(self):
        return '<Website %r>' % self.url
