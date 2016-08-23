# coding=utf-8
from . import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
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
