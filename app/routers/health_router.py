from app import api
from flask_restx import Resource
from flask import Response
health_ns = api.namespace(
    name='health',
    description='Rutas de health',
    path='/health'
)

@health_ns.route('')
class healt(Resource):
    def get(self):
        return Response(status=200)