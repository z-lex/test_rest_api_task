from flask_restx import Namespace, Resource, fields
from core import db
from http import HTTPStatus
from core.models_cars import Car, CarBody, CarBrand, CarModel
from core.models_dealers import Dealer, DealerCenter # for foreign key processing

api = Namespace('cars')

brand = api.model('CarBrand', {
    'id': fields.Integer(required=True),
    'name': fields.String(required=True),
    'description': fields.String(required=False),
})

brand_no_id = api.model('CarBrandNoID', {
    'name': fields.String(required=True),
    'description': fields.String(required=False),
})

# id = db.Column(db.Integer, primary_key=True)
car_model = api.model('CarModel', {
    'car_body_id': fields.Integer(required=True),
    'car_brand_id': fields.Integer(required=True),
    'name': fields.String(required=True),
    'model_year': fields.Integer(required=True),
    'horsepower': fields.Integer(required=True),
    'engine_size': fields.Integer(required=True),
    'engine_type': fields.String(required=True),
    'description': fields.String(required=False),
})


@api.route('/brands')
class RouteBrandList(Resource):
    @api.doc('list_brands')
    def get(self):
        """List all car brands"""
        result = CarBrand.query.all()
        if len(result) > 0:
            return api.marshal(result, brand), HTTPStatus.OK
        return HTTPStatus.NO_CONTENT

    @api.doc('add_car_brands_list')
    @api.expect(brand_no_id)
    def post(self):
        """Add car brands list"""
        data = api.payload
        something_added = False
        response_data = dict(
            status="success",
            message="all brands added"
        )
        response_code = HTTPStatus.CREATED
        if not isinstance(data, list):
            data = list(data)

        for b in data:
            if CarBrand.query.filter(CarBrand.name.ilike(b['name'])).first() is None:
                db.session.add(CarBrand(name=b['name'], description=b['description']))
                something_added = True
            else:
                if not response_data['message'].startswith('Already exist: '):
                    response_data['message'] = 'Already exist: '
                response_data['message'] += b['name'] + ', '

        if response_data['message'].endswith(', '):
            response_data['message'] = response_data['message'].rstrip(', ')
        if not something_added:
            response_data['status'] = 'failure'
            response_data['message'] = 'no brands added'
            response_code = HTTPStatus.CONFLICT
        else:
            db.session.commit()

        return response_data, response_code


@api.route('/brands/<int:id>')
class RouteBrand(Resource):
    """
    create/update/delete particular car brand
    """
    @api.doc('get_brand')
    def get(self, id):
        """Get car brand info"""
        result = CarBrand.query.get(id)
        if len(result) > 0:
            return api.marshal(result, brand), HTTPStatus.OK
        return HTTPStatus.NO_CONTENT

    @api.expect(brand_no_id)
    @api.doc('update_brand')
    def put(self, id):
        """Update car brand info"""
        data = api.payload
        br = CarBrand.query.get(id)
        if br is not None:
            br.name = data['name']
            br.description = data['description']
            db.session.commit()
            return HTTPStatus.OK
        return HTTPStatus.NO_CONTENT

    @api.doc('delete_brand')
    def delete(self, id):
        """Delete car brand and all car models recursively"""
        br = CarBrand.query.get(id)
        if br is not None:
            db.session.delete(br)
            db.session.commit()
            return HTTPStatus.OK
        return HTTPStatus.NO_CONTENT


@api.route('/brands/<int:brand_id>/models')
class RouteCarModelList(Resource):
    @api.doc('list_models')
    def get(self, brand_id):
        """List all car models of specified brand"""
        if CarBrand.query.get(brand_id) is None:
            return 'Wrong brand id', HTTPStatus.BAD_REQUEST

        result = CarModel.query.filter_by(car_brand_id=brand_id).all()
        if len(result) > 0:
            return api.marshal(result, car_model), HTTPStatus.OK
        return HTTPStatus.NO_CONTENT

    @api.doc('create_car_model')
    @api.expect(car_model)
    def post(self, brand_id):
        """Create new car model"""
        # car brand not exist
        if CarBrand.query.get(brand_id) is None:
            return 'Wrong brand id', HTTPStatus.BAD_REQUEST

        data = api.payload
        response_data = dict(
            status='success',
            message='successfully added'
        )
        if isinstance(data, list):
            data = data[0]

        if CarModel.query.filter(CarModel.name.ilike(data['name'])).\
                filter_by(car_brand_id=brand_id).first() is not None:
            response_data['status'] = 'failure'
            response_data['message'] = 'Model \"{}\" already exists'.format(data['name'])
            return response_data, HTTPStatus.CONFLICT

        # car body not exist
        if CarBody.query.get(data['car_body_id']) is None:
            return 'Wrong car body id', HTTPStatus.CONFLICT

        new_car_model = CarModel(
            name=data['name'],
            car_body_id=data['car_body_id'],
            car_brand_id=brand_id,
            model_year=data['model_year'],
            horsepower=data['horsepower'],
            engine_size=data['engine_size'],
            engine_type=data['engine_type'],
            description=data['description'],
        )

        db.session.add(new_car_model)
        db.session.commit()
        response_data['id'] = new_car_model.id
        response_data['message'] = 'Model \"{}\" successfully added'.format(new_car_model.name)
        return response_data, HTTPStatus.CREATED


@api.route('/brands/<int:brand_id>/models/<int:model_id>')
class RouteCarModel(Resource):
    """Create/update/delete particular car model"""
    @api.doc('list_car_model')
    def get(self, brand_id, model_id):
        """List car models of specified brand"""
        result = CarModel.query.filter_by(car_brand_id=brand_id, id=model_id).first()
        if result is not None:
            return api.marshal(result, car_model), HTTPStatus.OK
        return HTTPStatus.NO_CONTENT

    @api.doc('update_car_model')
    @api.expect(car_model)
    def put(self, brand_id, model_id):
        """Update car model info"""
        if CarBrand.query.get(brand_id) is None:
            return 'Wrong brand id {}'.format(brand_id), HTTPStatus.BAD_REQUEST

        car_model_updated = CarModel.query.get(model_id)
        if car_model_updated is None:
            return 'Wrong model id {}'.format(model_id), HTTPStatus.BAD_REQUEST

        data = api.payload
        if isinstance(data, list):
            data = data[0]

        car_model_updated.name = data['name']
        car_model_updated.car_body_id = data['car_body_id']
        car_model_updated.model_year = data['model_year']
        car_model_updated.horsepower = data['horsepower']
        car_model_updated.engine_size = data['engine_size']
        car_model_updated.engine_type = data['engine_type']
        if 'description' in data.keys():
            car_model_updated.description = data['description']

        db.session.commit()
        return HTTPStatus.OK

    @api.doc('delete_car_model')
    def delete(self, brand_id, model_id):
        """Delete car model and all its instances recursively"""
        if CarBrand.query.get(brand_id) is None:
            return 'Wrong brand id {}'.format(brand_id), HTTPStatus.BAD_REQUEST

        car_model_to_delete = CarModel.query.get(model_id)
        if car_model_to_delete is None:
            return 'Wrong model id {}'.format(model_id), HTTPStatus.BAD_REQUEST

        db.session.delete(car_model_to_delete)
        db.session.commit()
        return HTTPStatus.OK

