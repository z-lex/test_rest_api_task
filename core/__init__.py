from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def db_create(app):
    """
    create empty database
    :param app: flask application
    """
    with app.app_context():
        from .models_cars import Car, CarBody, CarBrand, CarModel
        from .models_dealers import Dealer, DealerCenter, Contacts
        db.create_all()
        db.session.commit()
