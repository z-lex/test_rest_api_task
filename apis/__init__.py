from flask_restx import Api
from .namespace_cars import api as ns_cars
from .namespace_dealers import api as ns_dealers

api = Api()
api.add_namespace(ns_cars, path='/api/cars')
api.add_namespace(ns_dealers, path='/api/dealers')

