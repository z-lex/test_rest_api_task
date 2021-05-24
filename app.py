from flask import Flask
from flask.cli import with_appcontext
import click
from config import get_config
from apis import api
from core import db, db_create, db_create_and_populate


@click.command('create-empty-db')
@with_appcontext
def create_empty_db():
    db_create()
    click.echo('Empty database created')


@click.command('create-db')
@with_appcontext
def create_db():
    db_create_and_populate()
    click.echo('Database created and populated')


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(get_config(config_name))
    api.init_app(app)
    db.init_app(app)
    app.cli.add_command(create_db)
    app.cli.add_command(create_empty_db)
    return app

