from flask_restx import Namespace, Resource, fields
import datetime
from core import db
from http import HTTPStatus
from core.models_cars import Car, CarBody, CarBrand, CarModel
from core.models_dealers import Dealer, DealerCenter # for foreign key processing

api = Namespace('dealers')

# list available car brands in region

# list available car models of selected brand

# create/update/delete dealer

# create/update/delete dealer center

# create/update/delete car
dealer = api.model('Dealer', {
    'id': fields.Integer(required=False),
    'name': fields.String(required=True),
    'description': fields.String(required=False),
})

dealer_center = api.model('DealerCenter', {
    'id': fields.Integer(required=True),
    'dealer_id': fields.Integer(required=True),
    'name': fields.String(required=True),
    'email': fields.String(required=False),
    'phone': fields.String(required=False),
    'country': fields.String(required=False),
    'city': fields.String(required=False),
    'city_address': fields.String(required=False),
    'description': fields.String(required=False),
})

car = api.model('Car', {
    'id': fields.Integer(required=True),
    'car_model_id': fields.Integer(required=True),
    'manufacture_date': fields.Date(required=True),
    'kilometrage': fields.Float(required=True),
    'dealer_center_id': fields.Integer(required=True),
    'price': fields.Integer(required=True),
    'description': fields.String(required=False),
})

car_id = api.model('CarID', {
    'id': fields.Integer(required=True),
    'car_model_id': fields.Integer(required=True)
})


@api.route('/')
class RouteDealerList(Resource):
    @api.doc('list_dealers')
    def get(self):
        """List all car dealers"""
        result = Dealer.query.all()
        if len(result) > 0:
            return api.marshal(result, dealer), HTTPStatus.OK
        return HTTPStatus.NO_CONTENT

    @api.doc('add_car_dealers_list')
    @api.expect(dealer)
    def post(self):
        """Add car dealers list"""
        data = api.payload
        something_added = False
        response_data = dict(
            status='success',
            message='all dealers added'
        )
        response_code = HTTPStatus.CREATED
        if not isinstance(data, list):
            data = list(data)

        for dl in data:
            if Dealer.query.filter(Dealer.name.ilike(dl['name'])).first() is None:
                db.session.add(Dealer(name=dl['name'],
                                      description=dl.get('description', '')))
                something_added = True
            else:
                if not response_data['message'].startswith('Already exist: '):
                    response_data['message'] = 'Already exist: '
                response_data['message'] += dl['name'] + ', '

        if response_data['message'].endswith(', '):
            response_data['message'] = response_data['message'].rstrip(', ')
        if not something_added:
            response_data['status'] = 'failure'
            response_data['message'] = 'no brands added'
            response_code = HTTPStatus.CONFLICT
        else:
            db.session.commit()

        return response_data, response_code


@api.route('/<int:id>')
class RouteDealer(Resource):
    """
    create/update/delete particular car dealer
    """
    @api.doc('get_dealer')
    def get(self, id):
        """Get dealer info"""
        result = Dealer.query.get(id)
        if len(result) > 0:
            return api.marshal(result, dealer), HTTPStatus.OK
        return HTTPStatus.NO_CONTENT

    @api.expect(dealer)
    @api.doc('update_dealer')
    def put(self, id):
        """Update dealer info"""
        data = api.payload
        br = Dealer.query.get(id)
        if br is not None:
            br.name = data['name']
            br.description = data['description']
            db.session.commit()
            return HTTPStatus.OK
        return HTTPStatus.NO_CONTENT

    @api.doc('delete_dealer')
    def delete(self, id):
        """Delete dealer and all its centers"""
        dl = Dealer.query.get(id)
        if dl is not None:
            db.session.delete(dl)
            db.session.commit()
            return HTTPStatus.OK
        return HTTPStatus.NO_CONTENT


@api.route('/<int:dealer_id>/centers')
class RouteDealerCenterList(Resource):
    @api.doc('list_centers')
    def get(self, dealer_id):
        """List all dealing centers of specified dealer"""
        if Dealer.query.get(dealer_id) is None:
            return 'Wrong dealer id', HTTPStatus.BAD_REQUEST

        result = DealerCenter.query.filter_by(dealer_id=dealer_id).all()
        if len(result) > 0:
            return api.marshal(result, dealer_center), HTTPStatus.OK
        return HTTPStatus.NO_CONTENT

    @api.doc('create_dealer_center')
    @api.expect(dealer_center)
    def post(self, dealer_id):
        """Create new dealer center"""
        # car dealer not exist
        if Dealer.query.get(dealer_id) is None:
            return 'Wrong dealer id', HTTPStatus.BAD_REQUEST

        data = api.payload
        response_data = dict(
            status='success',
            message='successfully added'
        )
        if isinstance(data, list):
            data = data[0]

        if DealerCenter.query.filter(DealerCenter.name.ilike(data['name'])). \
                filter_by(dealer_id=dealer_id).first() is not None:
            response_data['status'] = 'failure'
            response_data['message'] = 'Dealer center\"{}\" already exists'.format(data['name'])
            return response_data, HTTPStatus.CONFLICT

        new_dealer_center = DealerCenter(
            dealer_id=dealer_id,
            name=data['name'],
            email=data['email'],
            phone=data['phone'],
            country=data['country'],
            city=data['city'],
            city_address=data['city_address'],
            description=data.get('description', None),
        )

        db.session.add(new_dealer_center)
        db.session.commit()
        response_data['id'] = new_dealer_center.id
        response_data['message'] = 'Dealer center \"{}\" successfully added'.format(new_dealer_center.name)
        return response_data, HTTPStatus.CREATED


@api.route('/<int:dealer_id>/centers/<int:center_id>')
class RouteDealerCenter(Resource):
    """Create/update/delete dealer center"""
    @api.doc('list_dealer_center')
    def get(self, dealer_id, center_id):
        """Get dealer center info"""
        result = DealerCenter.query.filter_by(dealer_id=dealer_id, id=center_id).first()
        if result is not None:
            return api.marshal(result, dealer_center), HTTPStatus.OK
        return HTTPStatus.NO_CONTENT

    @api.doc('update_dealer_center')
    @api.expect(dealer_center)
    def put(self, dealer_id, center_id):
        """Update dealer center info"""
        if Dealer.query.get(dealer_id) is None:
            return 'Wrong dealer id {}'.format(dealer_id), HTTPStatus.BAD_REQUEST

        dealer_center_updated = DealerCenter.query.get(center_id)
        if dealer_center_updated is None:
            return 'Wrong dealer center id {}'.format(center_id), HTTPStatus.BAD_REQUEST

        data = api.payload
        if isinstance(data, list):
            data = data[0]

        dealer_center_updated.name = data['name']
        dealer_center_updated.dealer_id = data['dealer_id']
        dealer_center_updated.email = data['email']
        dealer_center_updated.phone = data['phone']
        dealer_center_updated.country = data['country']
        dealer_center_updated.city = data['city']
        dealer_center_updated.city_address = data['city_address']
        if 'description' in data.keys():
            dealer_center_updated.description = data['description']

        db.session.commit()
        return HTTPStatus.OK

    @api.doc('delete_dealer_center')
    def delete(self, dealer_id, center_id):
        """Delete dealer center"""
        if Dealer.query.get(dealer_id) is None:
            return 'Wrong dealer id {}'.format(dealer_id), HTTPStatus.BAD_REQUEST

        dealer_center_to_delete = DealerCenter.query.get(center_id)
        if dealer_center_to_delete is None:
            return 'Wrong dealer center id {}'.format(center_id), HTTPStatus.BAD_REQUEST

        db.session.delete(dealer_center_to_delete)
        db.session.commit()
        return HTTPStatus.OK


@api.route('/<int:dealer_id>/centers/<int:center_id>/cars')
class RouteDealerCenterCar(Resource):
    """Create/update/delete cars in dealer center"""
    @api.doc('register_car_in_dealer_center')
    @api.expect(car)
    def post(self, dealer_id, center_id):
        """Register car in dealer center"""
        if Dealer.query.get(dealer_id) is None:
            return 'Wrong dealer id {}'.format(dealer_id), HTTPStatus.BAD_REQUEST
        if DealerCenter.query.get(center_id) is None:
            return 'Wrong dealer center id {}'.format(center_id), HTTPStatus.BAD_REQUEST

        data = api.payload
        if isinstance(data, list):
            data = data[0]

        if Car.query.filter_by(id=data['id'], car_model_id=data['car_model_id'])\
                .first() is not None:
            return 'Car already exists', HTTPStatus.CONFLICT

        new_car = Car(
            id=data['id'],
            car_model_id=data['car_model_id'],
            manufacture_date=datetime.datetime.strptime(data['manufacture_date'], '%Y-%m-%d'),
            kilometrage=data['kilometrage'],
            dealer_center_id=center_id,
            price=data['price'],
            description=data.get('description', None)
        )

        db.session.add(new_car)
        db.session.commit()
        return 'Car successfully added', HTTPStatus.CREATED

    @api.doc('update_car_info')
    @api.expect(car)
    def put(self, dealer_id, center_id):
        """Update car info"""
        if Dealer.query.get(dealer_id) is None:
            return 'Wrong dealer id {}'.format(dealer_id), HTTPStatus.BAD_REQUEST
        if DealerCenter.query.get(center_id) is None:
            return 'Wrong dealer center id {}'.format(center_id), HTTPStatus.BAD_REQUEST
        data = api.payload
        if isinstance(data, list):
            data = data[0]

        car_to_update = Car.query.\
            filter_by(id=data['id'], car_model_id=data['car_model_id']).first()
        if car_to_update is None:
            return 'Car with this IDs not exist', HTTPStatus.NOT_FOUND

        car_to_update.manufacture_date = datetime.datetime.strptime(data['manufacture_date'], '%Y-%m-%d')
        car_to_update.kilometrage = data['kilometrage']
        car_to_update.dealer_center_id = center_id
        car_to_update.price = data['price']
        car_to_update.description = data.get('description', None)
        db.session.commit()
        return 'Car successfully updated', HTTPStatus.CREATED

    @api.doc('delete_car')
    @api.expect(car_id)
    def delete(self, dealer_id, center_id):
        """Delete car"""
        if Dealer.query.get(dealer_id) is None:
            return 'Wrong dealer id {}'.format(dealer_id), HTTPStatus.BAD_REQUEST
        if DealerCenter.query.get(center_id) is None:
            return 'Wrong dealer center id {}'.format(center_id), HTTPStatus.BAD_REQUEST
        data = api.payload
        if isinstance(data, list):
            data = data[0]

        car_to_delete = Car.query. \
            filter_by(id=data['id'], car_model_id=data['car_model_id']).first()
        if car_to_delete is None:
            return 'Car with this IDs not exist', HTTPStatus.NOT_FOUND
        db.session.delete(car_to_delete)
        db.session.commit()
        return HTTPStatus.OK
