from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

convention = {
  "ix": "ix_%(column_0_label)s",
  "uq": "uq_%(table_name)s_%(column_0_name)s",
  "ck": "ck_%(table_name)s_%(constraint_name)s",
  "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
  "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)




class Activity(db.Model, SerializerMixin):
    __tablename__ = 'activities'

    serialize_rules = ('-created_at', '-updated_at')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    difficulty = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    activity_signups = db.relationship('Signup', back_populates='activity')

    camper_list = association_proxy('activity_signups', 'camper')

    def __repr__(self):
        return f'<Activity {self.id}: {self.name}>'

'''
In CAMPER WITH -CAMPER_SIGNUPS.ACTIVITY
Serialize_rules: '-camper_signups.activity', '-camper_signups.camper', '-activity_list.camper_list':
"age": 18,
    "camper_signups": [
        {
            "activity_id": 12,
            "camper_id": 1,
            "id": 88,
            "time": 2
        },
    ],
    "id": 1,
    "name": "Tara Reese"

WITHOUT -CAMPER_SIGNUPS.ACTIVITY
"age": 18,
    "camper_signups": [
        {
            "activity": {
                "difficulty": 5,
                "id": 12,
                "name": "Production film themselves seat indicate environmental daughter write."
            },
            "activity_id": 12,
            "camper_id": 1,
            "id": 88,
            "time": 2
        },
        {
            "activity": {
                "difficulty": 4,
                "id": 13,
                "name": "Participant mother part during approach relationship."
            },
            "activity_id": 13,
            "camper_id": 1,
            "id": 279,
            "time": 9
        },
        {
            "activity": {
                "difficulty": 5,
                "id": 5,
                "name": "Exactly fire I yard international floor."
            },
            "activity_id": 5,
            "camper_id": 1,
            "id": 474,
            "time": 21
        }
    ],
    "id": 1,
    "name": "Tara Reese"
}
'''




class Camper(db.Model, SerializerMixin):
    __tablename__ = 'campers'

    serialize_rules = ('-created_at', '-updated_at')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    camper_signups = db.relationship('Signup', back_populates='camper')

    activity_list = association_proxy('camper_signups', 'activity')

    

    @validates('name')
    def validates_name(self, key, name):
        if not name:
            raise ValueError('Must enter name')
        return name
    
    @validates('age')
    def validate_age(self, key, age):
        if age < 8 or age > 18:
            raise ValueError('Must be between the ages of 8 and 18')
        return age

    def __repr__(self):
        return f'<Camper {self.id}: {self.name}>'
    
class Signup(db.Model, SerializerMixin):
    __tablename__ = 'signups'

    serialize_rules = ('-created_at', '-updated_at','-camper.camper_signups', '-activity.activity_signups')

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
  
    camper_id = db.Column(db.Integer, db.ForeignKey('campers.id'))
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'))

    camper = db.relationship('Camper', back_populates='camper_signups')
    activity = db.relationship('Activity', back_populates='activity_signups')

    @validates('time')
    def validate_time(self, key, input_time):
        if input_time < 0 or input_time > 23:
            raise ValueError('Time must be between 0 and 23')
        return input_time

    def __repr__(self):
        return f'<Signup {self.id}>'


# add any models you may need. 