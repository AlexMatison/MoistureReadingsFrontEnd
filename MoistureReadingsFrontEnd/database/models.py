# The examples in this file come from the Flask-SQLAlchemy documentation
# For more information take a look at:
# http://flask-sqlalchemy.pocoo.org/2.1/quickstart/#simple-relationships

from datetime import datetime

from MoistureReadingsFrontEnd.database import db


class MoistureReading(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer)
    moisture_value = db.Column(db.Float)
    timestamp = db.Column(db.DateTime)
    inGoogleSheets = db.Column(db.Boolean)

    # Used to send to google sheets.
    def toList(self):
        return [self.id, self.location_id, self.moisture_value, self.timestamp.strftime("%Y-%m-%d %H:%M:%S")]

    def __init__(self, location_id, moisture_value, timestamp=None):
        self.location_id = location_id
        self.moisture_value = moisture_value
        if timestamp is None:
            timestamp = datetime.utcnow()
        self.timestamp = timestamp
        self.inGoogleSheets = False


    def __repr__(self):
        return (self.location_id, self.moisture_value, self.timestamp, self.inGoogleSheets)

        #return '<MoistureReading %r>' % self.id

