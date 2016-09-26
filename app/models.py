# coding=utf-8
from . import db, login_manage
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
# from flask_wtf import Form


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

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

    def __repr__(self):
        return '<User %r>' % self.username


@login_manage.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
