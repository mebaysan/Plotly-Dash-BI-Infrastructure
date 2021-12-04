from flaskapp.db import db
from flaskapp.dashboard.utilities.tarih_islemleri import AYLAR

class AyModel(db.Model):
    __tablename__ = 'Aylar'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)

    def __init__(self, _name):
        self.name = _name

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
