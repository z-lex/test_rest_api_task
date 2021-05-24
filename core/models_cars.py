from . import db


class CarBody(db.Model):
    """
    Class represents car form factor (sedan, minivan, etc)
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)

    cars_models = db.relationship('CarModel', cascade='all,delete', backref='car_body')


class CarBrand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)

    cars_models = db.relationship('CarModel', cascade='all,delete', backref='car_brand')


class CarModel(db.Model):
    """
    Class represents particular car model with its technical characteristics
    """
    id = db.Column(db.Integer, primary_key=True)
    car_body_id = db.Column(db.Integer, db.ForeignKey('car_body.id'), nullable=False)
    car_brand_id = db.Column(db.Integer, db.ForeignKey('car_brand.id'), nullable=False)
    name = db.Column(db.String(80), unique=True, nullable=False)
    model_year = db.Column(db.Integer, nullable=False)
    horsepower = db.Column(db.Integer, nullable=False)
    engine_size = db.Column(db.Integer, nullable=False) # cm**3
    engine_type = db.Column(db.String(80), nullable=False)

    description = db.Column(db.Text, nullable=True)

    # many cars of particular model can be manufactured
    cars = db.relationship('Car', cascade='all,delete', backref='car_model')


class Car(db.Model):
    """
    Class represents particular vehicle
    """
    # primary key: serial id + model id
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    car_model_id = db.Column(db.Integer, db.ForeignKey('car_model.id'), nullable=False, primary_key=True)

    manufacture_date = db.Column(db.DateTime, nullable=True)
    kilometrage = db.Column(db.Float, nullable=True)
    dealer_center_id = db.Column(db.Integer, db.ForeignKey('dealer_center.id'), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=True)
