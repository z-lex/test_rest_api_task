from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()


def db_create():
    """
    create empty database
    :param app: flask application
    """
    from .models_cars import Car, CarBody, CarBrand, CarModel
    from .models_dealers import Dealer, DealerCenter, Contacts
    db.drop_all()
    db.create_all()
    db.session.commit()


def db_create_and_populate():
    """
    create database and populate it with values
    :param app: flask application
    :return:
    """
    from .models_cars import Car, CarBody, CarBrand, CarModel
    from .models_dealers import Dealer, DealerCenter, Contacts
    db.drop_all()
    db.create_all()

    # car bodies and car brands
    car_bodies = [CarBody(id=1, name='Coupe'), CarBody(id=2, name='SUV'), CarBody(id=3, name='Sedan'),
                  CarBody(id=4, name='Pickup'), CarBody(id=5, name='Hatchback'),
                  CarBody(id=6, name='Estate')]
    car_brands = [CarBrand(id=1, name='Audi'), CarBrand(id=2, name='BMW'),
                  CarBrand(id=3, name='Cadillac'), CarBrand(id=4, name='Ford')]
    db.session.add_all(car_bodies)
    db.session.add_all(car_brands)

    car_models = [
        CarModel(id=1, name='Audi A6 Avant 40 TFSI S tronic',
                 model_year=2021, horsepower=190, engine_size=1984,
                 engine_type='40 TFSI', car_body_id=6, car_brand_id=1),
        CarModel(id=2, name='Audi Q7 45 TDI quattro tiptronic',
                 model_year=2020, horsepower=249, engine_size=2967,
                 engine_type='45 TDI', car_body_id=2, car_brand_id=1),
    ]
    db.session.add_all(car_models)

    dealers = [
        Dealer(id=1, name='Audi Official Dealer'),
        Dealer(id=2, name='BMW center'),
    ]
    db.session.add_all(dealers)

    contacts = [
        Contacts(id=1, email='audi@audi-vitebskiy.ru',
                 phone='+7 (812) 210-7696',
                 country='Russia', city='Saint-Petersburg',
                 city_address='17 Vitebskiy ave., Saint-Petersburg, Russia, 196105'),
    ]
    dealer_centers = [
        DealerCenter(id=1, name='Audi Center Vitebskiy',
                     dealer_id=1, contacts_id=1),
    ]
    db.session.add_all(contacts)
    db.session.add_all(dealer_centers)

    # cars list
    cars = [
        Car(id=1, car_model_id=1, manufacture_date=datetime.date(2021, 2, 1),
            kilometrage=0.0, dealer_center_id=1, price=4035000),
    ]
    db.session.add_all(cars)

    db.session.commit()
