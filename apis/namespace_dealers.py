from flask_restx import Namespace, Resource, fields

api = Namespace('dealers')

# list available car brands in region

# list available car models of selected brand

# create/update/delete dealer

# create/update/delete dealer center

# create/update/delete car


@api.route('/')
class DealerList(Resource):
    def get(self):
        return "List Of Dealers"
