from models.proveedor import ProveedorModel
from flask_restful import Resource,reqparse
from flasgger import swag_from
from flask import request
from utils import paginated_results, restrict


class Proveedor(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id',type=int)
    parser.add_argument('nombre', type = str)
    parser.add_argument('direccion', type=str)
    parser.add_argument('telefono', type=str)

    @swag_from('../swagger/proveedor/get_proveedor.yaml')
    def get(self, id):
        proveedor = ProveedorModel.find_by_id(ProveedorModel.id)
        if proveedor:
            return proveedor.json()
        return {'message':'No se encuentra al proveedor'},404

class ProveedorList(Resource):
    @swag_from('../swagger/proveedor/list_proveedor.yaml')
    def get(self):
        query = ProveedorModel.query
        return paginated_results(query)
