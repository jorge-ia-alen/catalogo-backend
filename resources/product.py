from models.product import ProductModel
from flask_restful import Resource,reqparse
from flasgger import swag_from
from flask import request
from utils import paginated_results, restrict
from sqlalchemy import func 


class Product(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id',type=int)
    parser.add_argument('nombre', type = str)
    parser.add_argument('descrip', type = str)
    parser.add_argument('estado', type=str)
    parser.add_argument('precio', type=float)
    parser.add_argument('proveedor_id',type=int)
    parser.add_argument('categoria_id',type=int)

    @swag_from('../swagger/product/get_producto.yaml')
    def get(self, id):
        producto = ProductModel.find_by_id(ProductModel.id)
        if producto:
            return producto.json()
        return {'message':'No se encuentra el producto'},404
    @swag_from('../swagger/product/put_producto.yaml')
    def put(self, id):
        producto = ProductModel.find_by_id(id)
        if producto:
            newdata = Product.parser.parse_args()
            producto.from_reqparse(newdata)
            producto.save_to_db()
            return producto.json()
    @swag_from('../swagger/product/delete_producto.yaml')
    def delete(self, id):
        producto = ProductModel.find_by_id(id)
        if producto:
            producto.delete_from_db()
        return {'message': "Se ha borrado el producto"}
class ProductList(Resource):
    @swag_from('../swagger/product/list_producto.yaml')
    def get(self):
        query = ProductModel.query
        return paginated_results(query)    
    @swag_from('../swagger/product/post_producto.yaml')
    def post(self):
        data = Product.parser.parse_args()

        producto = ProductModel(**data)

        try:
            producto.save_to_db()
        except Exception as e:
            print(e)
            return {'message':'Ocurrio un error al agregar el producto'},500
        return producto.json(),201
class ProductSearch(Resource):
    @swag_from('../swagger/product/search_producto.yaml')
    def post(self):
        query = ProductModel.query
        if request.json:
            filtros = request.json
            query = restrict(query,filtros,'id',lambda x: ProductModel.id == x)
            query = restrict(query,filtros,'nombre',lambda x: func.lower(ProductModel.nombre).contains(x.lower()))
            query = restrict(query,filtros,'descrip',lambda x: ProductModel.descrip.contains(x))
            query = restrict(query,filtros,'estado',lambda x: ProductModel.estado.contains(x))
            query = restrict(query,filtros,'precio',lambda x: ProductModel.precio.contains(x))
            query = restrict(query,filtros,'proveedor_id',lambda x: ProductModel.precio.contains(x))
            query = restrict(query,filtros,'categoria_id',lambda x: ProductModel.precio.contains(x))
        return paginated_results(query)