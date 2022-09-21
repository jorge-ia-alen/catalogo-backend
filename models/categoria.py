from argparse import Namespace
from db import db
from flask_restful.reqparse import Namespace
from utils import _assign_if_something

class CategoriaModel(db.Model):
    __tablename__ = 'categoria'

    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String)

    def __init__(self, id, descripcion):
        self.id = id
        self.descripcion = descripcion

    def json(self, depth=0):
        json = {
            'id': self.id,
            'descripcion': self.descripcion
        }

        return json
    
    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def from_reqparse(self, newdata: Namespace):
        for no_pk_key in ['descripcion']:
            _assign_if_something(self, newdata, no_pk_key)