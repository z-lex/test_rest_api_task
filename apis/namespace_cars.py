from flask_restx import Namespace, Resource, fields

api = Namespace('cars')

# list all available car brands with models count

# list all available car models (with parameters: brands, year, etc)

# create/update/delete particular car brand

# create/update/delete particular car model


@api.route('/')
class CarList(Resource):
    def get(self):
        return "List Of Cars"
