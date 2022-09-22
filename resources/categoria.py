from models.categoria import CategoriaModel
from flask_restful import Resource,reqparse
from flasgger import swag_from
from flask import request
from utils import paginated_results, restrict


class Categoria(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id',type=int)
    parser.add_argument('descripcion', type = str)

    @swag_from('../swagger/categoria/get_categoria.yaml')
    def get(self, id):
        categoria = CategoriaModel.find_by_id(CategoriaModel.id)
        if categoria:
            return categoria.json()
        return {'message':'No se encuentra al categoria'},404

class CategoriaList(Resource):
    @swag_from('../swagger/categoria/list_categoria.yaml')
    def get(self):
        query = CategoriaModel.query
        return paginated_results(query)
