from models.product import ProductModel
from flask_restful import Resource,reqparse
from flasgger import swag_from
from flask import request
from utils import paginated_results, restrict


class Product(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id',type=int)
    parser.add_argument('nombre', type = str)
    parser.add_argument('descrip', type = str)
    parser.add_argument('estado', type=str)
    parser.add_argument('precio', type=float)

    @swag_from('../swagger/task/get_product.yaml')
    def get(self, id):
        producto = ProductModel.find_by_id(id)
        if producto:
            return producto.json()
        return {'message':'No se encuentra el producto'},404
    
    @swag_from('../swagger/task/put_product.yaml')
    def put(self, id):
        producto = ProductModel.find_by_id(id)
        if producto:
            newdata = Product.parser.parse_args()
            producto.from_reqparse(newdata)
            producto.save_to_db()
            return producto.json()

    @swag_from('../swagger/task/delete_product.yaml')
    def delete(self, id):
        producto = ProductModel.find_by_id(id)
        if producto:
            producto.delete_from_db()
        return {'message': "Se ha borrado el producto"}

class TaskList(Resource):
    @swag_from('../swagger/task/list_product.yaml')
    def get(self):
        query = ProductModel.query
        return paginated_results(query)
        
    @swag_from('../swagger/task/post_product.yaml')
    def post(self):
        data = Product.parser.parse_args()

        producto = ProductModel(**data)

        try:
            producto.save_to_db()
        except Exception as e:
            print(e)
            return {'message':'Ocurrio un error al agregar el producto'},500
        return producto.json(),201

class TaskSearch(Resource):
    @swag_from('../swagger/task/search_task.yaml')
    def post(self):
        query = ProductModel.query
        if request.json:
            filtros = request.json
            query = restrict(query,filtros,'id',lambda x: ProductModel.id == x)
            query = restrict(query,filtros,'nombre',lambda x: ProductModel.nombre.contains(x))
            query = restrict(query,filtros,'descrip',lambda x: ProductModel.descrip.contains(x))
            query = restrict(query,filtros,'estado',lambda x: ProductModel.estado.contains(x))
            query = restrict(query,filtros,'precio',lambda x: ProductModel.precio.contains(x))

        return paginated_results(query)
