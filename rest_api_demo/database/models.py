# The examples in this file come from the Flask-SQLAlchemy documentation
# For more information take a look at:
# http://flask-sqlalchemy.pocoo.org/2.1/quickstart/#simple-relationships

from datetime import datetime

from rest_api_demo.database import db


class MoistureReading(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer)
    moisture_value = db.Column(db.Float)
    timestamp = db.Column(db.DateTime)


    def __init__(self, location_id, moisture_value, timestamp=None):
        self.location_id = location_id
        self.moisture_value = moisture_value
        if timestamp is None:
            timestamp = datetime.utcnow()
        self.timestamp = timestamp


    def __repr__(self):
        return '<MoistureReading %r>' % self.id

