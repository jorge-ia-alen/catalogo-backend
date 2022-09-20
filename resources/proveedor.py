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

    @swag_from('../swagger/task/get_proveedor.yaml')
    def get(self, id):
        proveedor = ProveedorModel.find_by_id(id)
        if proveedor:
            return proveedor.json()
        return {'message':'No se encuentra al proveedor'},404

class ProveedorList(Resource):
    @swag_from('../swagger/task/list_proveedor.yaml')
    def get(self):
        query = ProveedorModel.query
        return paginated_results(query)
        
    # @swag_from('../swagger/task/post_task.yaml')
    # def post(self):
    #     data = Proveedor.parser.parse_args()

    #     tarea = Proveedor(**data)

    #     try:
    #         tarea.save_to_db()
    #     except Exception as e:
    #         print(e)
    #         return {'message':'Ocurrio un error al crear la tarea'},500
    #     return tarea.json(),201
    """ 
    @swag_from('../swagger/task/put_task.yaml')
    def put(self, id):
        tarea = Proveedor.find_by_id(id)
        if tarea:
            newdata = Task.parser.parse_args()
            tarea.from_reqparse(newdata)
            tarea.save_to_db()
            return tarea.json()

    @swag_from('../swagger/task/delete_task.yaml')
    def delete(self, id):
        tarea = Proveedor.find_by_id(id)
        if tarea:
            tarea.delete_from_db()
        return {'message': "Se ha borrado la tarea"} """


"""
class TaskSearch(Resource):
    @swag_from('../swagger/task/search_task.yaml')
    def post(self):
        query = Proveedor.query
        if request.json:
            filtros = request.json
            query = restrict(query,filtros,'id',lambda x: Proveedor.id == x)
            query = restrict(query,filtros,'descrip',lambda x: Proveedor.descrip.contains(x))
            query = restrict(query,filtros,'status',lambda x: Proveedor.status.contains(x))
        return paginated_results(query)
 """