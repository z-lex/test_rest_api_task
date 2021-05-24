from flask_restx import Namespace, Resource, fields

api = Namespace('dealers')

# list available car brands in region

# list available car models of selected brand

# create/update/delete dealer

# create/update/delete dealer center

# create/update/delete car

"""
car_model = api.model('CarModel', {
    'name': fields.String(required=True),
    'description': fields.String(required=False),
    'car_model_id': fields.Integer(required=True),
    'manufacture_date': fields.Date(required=False),
    'kilometrage': fields.Float(required=True),
    'dealer_center_id': fields.Integer(required=True),
    'price': fields.Integer(required=False),
    'description': fields.Text(required=False)
})
"""

@api.route('/')
class DealerList(Resource):
    def get(self):
        return "List Of Dealers"
