#!/usr/bin/env python3

import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'instance/app.db')}")

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Activity, Camper

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
api = Api(app)

db.init_app(app)

@app.route('/')
def home():
    return ''

class Campers(Resource):
    def get(self):
        all_campers = [camper.to_dict(only=('id', 'name', 'age')) for camper in Camper.query.all()]
        return make_response(all_campers, 200)
    
api.add_resource(Campers, '/campers')

class CamperByID(Resource):
    def get(self, id):
        single_camper = Camper.query.filter_by(id=id).first().to_dict(only=())
        return make_response(single_camper, 200)
    
    


api.add_resource(CamperByID, '/campers/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
