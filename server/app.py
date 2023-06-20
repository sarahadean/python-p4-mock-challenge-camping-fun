#!/usr/bin/env python3

import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'instance/app.db')}")

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Activity, Camper, Signup

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
    
    def post(self):
        data = request.get_json()
        try: 
            new_camper = Camper(
                name = data.get('name'),
                age = data.get('age')
            )
            db.session.add(new_camper)
            db.session.commit()

            return make_response(new_camper.to_dict(), 201)
        except:
            return {"error": "400: Validation error"}, 400
    
api.add_resource(Campers, '/campers')

class CamperByID(Resource):
    def get(self, id):
        single_camper = Camper.query.filter_by(id=id).first()
        if single_camper:
            return make_response(single_camper.to_dict(only=('id', 'name', 'age', 'activity_list')), 200)
        return {"error": "400: Validation error"}, 404
    
api.add_resource(CamperByID, '/campers/<int:id>')

class Activities(Resource):
    def get(self):
        all_activities = [activity.to_dict() for activity in Activity.query.all()]
        return make_response(all_activities, 200)
    
api.add_resource(Activities, '/activities')

class ActivitiesById(Resource):
    def delete(self, id):
        try:
            activity = Activity.query.filter_by(id=id).first()
            db.session.delete(activity)
            return make_response({}, 204)
        except:
            return {"error": "404: Activity not found"}, 404

api.add_resource(ActivitiesById, '/activities/<int:id>')

class Signups(Resource):
    def post(self):
        data = request.get_json()
        try: 
            new_signup = Signup(
                time = data.get('time'),
                camper_id = data.get('camper_id'),
                activity_id = data.get('activity_id')
            )
            db.session.add(new_signup)
            db.session.commit()
            return make_response(new_signup.to_dict(), 201)
        except:
            return {"error": "400: Validation error"}, 400
        
api.add_resource(Signups, '/signups')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
