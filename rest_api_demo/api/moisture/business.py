from rest_api_demo.database import db
from rest_api_demo.database.models import MoistureReading


def create_moisture_reading(data):
    location_id = data.get('location_id')
    moisture_value = data.get('moisture_value')
    moisture = MoistureReading(location_id, moisture_value)
    db.session.add(moisture)
    db.session.commit()


def update_moisture_reading(moisture_reading_id, data):
    moisture = MoistureReading.query.filter(MoistureReading.id == moisture_reading_id).one()
    moisture.location_id = data.get('location_id')
    moisture.moisture_value = data.get('moisture_value')
    db.session.add(moisture)
    db.session.commit()


def delete_post(post_id):
    post = MoistureReading.query.filter(MoistureReading.id == post_id).one()
    db.session.delete(post)
    db.session.commit()


