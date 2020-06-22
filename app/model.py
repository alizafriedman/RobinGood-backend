from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    nickname = db.Column(db.String(50), nullable=False)
    charity = db.Column(ARRAY(db.String), nullable=True, unique=True)

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'nickname': self.nickname,
            'charity': [c.to_dict() for c in self.charity]
        }
