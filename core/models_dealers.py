from . import db
# from .models_cars import Car


class Dealer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)

    # one dealer can have multiple distribution centers
    centers = db.relationship('DealerCenter', cascade='delete,all', backref='dealer')


class DealerCenter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    dealer_id = db.Column(db.Integer, db.ForeignKey('dealer.id'), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    country = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    city_address = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=True)

    # multiple cars belong to a particular dealing center
    cars = db.relationship('Car', cascade='delete,all', backref='dealer_center')

