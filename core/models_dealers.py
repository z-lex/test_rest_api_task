from . import db


class Dealer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)

    # one dealer can have multiple distribution centers
    centers = db.relationship('DealerCenter', backref='dealer')


class DealerCenter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    dealer_id = db.Column(db.Integer, db.ForeignKey('dealer.id'), nullable=False)
    contacts_id = db.Column(db.Integer, db.ForeignKey('contacts.id'), nullable=False)
    description = db.Column(db.Text, nullable=True)

    # multiple cars belong to a particular dealing center
    cars = db.relationship('Car', backref='dealer_center')


class Contacts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    country = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    city_address = db.Column(db.Text, nullable=False)

    # one-to-one relationship with dealer center
    center = db.relationship('DealerCenter', backref='contacts', uselist=False)
