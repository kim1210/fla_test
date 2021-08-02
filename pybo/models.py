from sqlalchemy.orm import backref
from pybo import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, unique=True, nullable=False)
    user_pw = db.Column(db.String, nullable=False)

# 글쓰기 관련

class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    content = db.Column(db.Text())
    user_id = db.Column(db.String, db.ForeignKey('user.user_id', ondelete = 'CASCADE'))
    user = db.relationship('User', backref = db.backref('board_set'))

