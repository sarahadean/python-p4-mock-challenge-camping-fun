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

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    difficulty = db.Column(db.Integer)

    # Add relationship
    activity_signups = db.relationship('Signup', back_populates='activity')
    # Add serialization rules
    
    def __repr__(self):
        return f'<Activity {self.id}: {self.name}>'


class Camper(db.Model, SerializerMixin):
    __tablename__ = 'campers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer)

    # Add relationship
    signups = db.relationship('Signup', back_populates='camper')
    
    # Add serialization rules
    serialize_rules = ('-signups.camper',)
    # Add validation
    @validates('name', 'age')
    def validates_camper(self, key, input):
        if key == 'name':
            if not input:
                raise ValueError('Camper must have name')
            return input
        elif key == 'age':
            if input > 18 or input < 8:
                raise ValueError('Camper must be between 8 and 18 years old')
            return input
    
    def __repr__(self):
        return f'<Camper {self.id}: {self.name}>'


class Signup(db.Model, SerializerMixin):
    __tablename__ = 'signups'

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer)
    camper_id = db.Column(db.Integer, db.ForeignKey('campers.id'))
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'))

    # Add relationships
    camper = db.relationship('Camper', back_populates='signups')
    activity = db.relationship('Activity', back_populates='activity_signups')
    # Add serialization rules
    serialize_rules = ('-camper.signups', '-activity.activity_signups')
    # Add validation
    @validates('time')
    def validates_time(self, key, input_time):
        if input_time < 0 or input_time > 23:
            raise ValueError('Time must be between 0 and 23')
        return input_time
    
    def __repr__(self):
        return f'<Signup {self.id}>'


# add any models you may need.
