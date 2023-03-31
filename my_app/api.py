from flasgger import Swagger
from flask import g
from flask_restful import Api

from my_app import app
from my_app.models import db
from my_app.resources import Driver, Drivers, Report

api = Api(app)
swagger = Swagger(app=app)


@app.before_request
def before_request():
    g.db = db
    g.db.connect()


@app.after_request
def after_request(response):
    g.db.close()
    return response


api.add_resource(Report, '/api/v1/report/')
api.add_resource(Drivers, '/api/v1/report/drivers/')
api.add_resource(Driver, '/api/v1/report/drivers/<driver_id>/')
