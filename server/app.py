#!/usr/bin/env python3

from models import db, Activity, Camper, Signup
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)
api = Api(app)


@app.route('/')
def home():
    return ''

class Campers(Resource):
    def get(self):
        camper_list = [camper.to_dict(only=('id', 'name', 'age')) for camper in Camper.query.all()]
        return make_response(camper_list, 200)

    def post(self):
        data = request.get_json()
        try:
            new_camper = Camper(
                name=data.get('name'),
                age=data.get('age')
            )
            db.session.add(new_camper)
            db.session.commit()
            return make_response(new_camper.to_dict(), 201)
        except:
            return {"errors":"Validation Errors"},400

api.add_resource(Campers, '/campers')

class CampersById(Resource):
    def get(self, id):
        try:
            camper = Camper.query.filter_by(id=id).first()
            return make_response(camper.to_dict(only=()), 200)
        except:
            return {"error":"Camper not found"}, 404

    def patch(self, id):
        data=request.get_json()
        try:
            camper = Camper.query.filter_by(id=id).first()
            if not camper:
                return {"error":"Camper not found"}, 404
            else:
                for attr in data:
                    setattr(camper, attr, data.get(attr))
                db.session.add(camper)
                db.session.commit()
                return make_response(camper.to_dict(), 202)
        except:
            return {"errors": ["validation errors"]}, 400

api.add_resource(CampersById, '/campers/<int:id>')


class Activities(Resource):
    def get(self):
        activities_list = [activity.to_dict() for activity in Activity.query.all()]
        return make_response(activities_list, 200)

api.add_resource(Activities, '/activities')
class ActivitiesById(Resource):
    def delete(self, id):
        try:
            activity=Activity.query.filter_by(id=id).first()
            db.session.delete(activity)
            db.session.commit()
            return {},204
        except:
            return {"error":"Activity not found"}, 404

api.add_resource(ActivitiesById, '/activities/<int:id>')

class Signups(Resource):
    def post(self):
        data = request.get_json()
        try:
            new_signup = Signup(
                camper_id=data.get('camper_id'),
                activity_id=data.get('activity_id'),
                time=data.get('time')
            )
            db.session.add(new_signup)
            db.session.commit()
            return make_response(new_signup.to_dict(), 201)
        except:
            return {
                "errors": ["validation errors"]
                }, 400

api.add_resource(Signups, '/signups')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
