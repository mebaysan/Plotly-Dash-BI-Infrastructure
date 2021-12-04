from flaskapp.db import db
from slugify import slugify
import pandas as pd
import numpy as np
import os


class FileModel(db.Model):
    __tablename__ = 'files'
    __mapper_args__ = {
        'confirm_deleted_rows': False
    }
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String, nullable=False)
    file_path = db.Column(db.String, nullable=False)
    file_full = db.Column(db.String, nullable=False)
    slug = db.Column(db.String)

    def __init__(self, _file_name, _file_path):
        self.file_name = _file_name
        self.file_path = _file_path
        self.file_full = os.path.join(_file_path, _file_name)
        self.slug = FileModel.get_slug(_file_name)

    def __repr__(self):
        return self.file_name

    @classmethod
    def create_csv_and_return_url(cls, _file_name, _file_path, _df, _url='/access/csv/'):
        file_model = FileModel(_file_name, _file_path)
        file_model.save_to_db(_df)
        return '{}{}'.format(_url, file_model.slug)

    @classmethod
    def find_by_slug(cls, _slug):
        return cls.query.filter_by(slug=_slug).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def get_slug(cls, file_name):
        slug = slugify(file_name)
        if FileModel.find_by_slug(slug):
            FileModel.find_by_slug(slug).delete_from_db()
        return slug

    def save_to_db(self, _df):
        _df = _df.replace(np.nan, 'Bos')
        _df.to_csv(self.file_full, encoding='utf-8')
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        if os.path.exists(self.file_full):
            os.remove(self.file_full)
        db.session.delete(self)
        db.session.commit()
