from argparse import Namespace
from db import db
from flask_restful.reqparse import Namespace
from utils import _assign_if_something
from models.proveedor import ProveedorModel
from models.categoria import CategoriaModel

class ProductModel(db.Model):
    __tablename__ = 'producto'

    id = db.Column(db.Integer, primary_key=True)
    proveedor_id = db.Column(db.Integer, db.ForeignKey(ProveedorModel.id))
    categoria_id = db.Column(db.Integer, db.ForeignKey(CategoriaModel.id))
    nombre = db.Column(db.String)
    descrip = db.Column(db.String)
    estado = db.Column(db.String)
    precio = db.Column(db.Float)


    _proveedor = db.relationship('ProveedorModel', 
        uselist = False, primaryjoin= 'ProveedorModel.id == ProductModel.proveedor_id',
        foreign_keys= 'ProductModel.proveedor_id')

    _categoria = db.relationship('CategoriaModel', 
        uselist = False, primaryjoin= 'CategoriaModel.id == ProductModel.categoria_id',
        foreign_keys= 'ProductModel.categoria_id')

    def __init__(self, id, nombre, descrip, estado, precio, proveedor_id, categoria_id):
        self.id = id
        self.proveedor_id = proveedor_id
        self.categoria_id = categoria_id
        self.nombre = nombre
        self.descrip = descrip
        self.estado = estado
        self.precio = precio


    def json(self, depth=0):
        json = {
            'id': self.id,
            'proveedor_id': self.proveedor_id,
            'categoria_id': self.categoria_id,
            'nombre': self.nombre,
            'descrip': self.descrip,
            'estado': self.estado,
            'precio': self.precio,
        }

        if depth >0:
            if self._proveedor:
                json['_proveedor']= self._proveedor.json(depth)

        if depth >0:
            if self._categoria:
                json['_categoria']= self._categoria.json(depth)

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
        for no_pk_key in ['nombre', 'descrip','estado', 'precio', 'proveedor_id', 'categoria_id']:
            _assign_if_something(self, newdata, no_pk_key)