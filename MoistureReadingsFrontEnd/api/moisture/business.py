from MoistureReadingsFrontEnd.database import db
from MoistureReadingsFrontEnd.database.models import MoistureReading
import MoistureReadingsFrontEnd.google.google_sheets as googlesheets
from MoistureReadingsFrontEnd import settings

def create_moisture_reading(data):
    location_id = data.get('location_id')
    moisture_value = data.get('moisture_value')
    moisture = MoistureReading(location_id, moisture_value)
    db.session.add(moisture)
    db.session.commit()
    if googlesheets.moisture_to_google(moisture.toList(), settings.GOOGLE_SHEETS_SPREADSHEET_ID):
        # Update moisture reading to indicate it is in Google sheets.
        moisture.inGoogleSheets = True
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


def push_outstanding_readings_to_google():
    readings = MoistureReading.query.filter(MoistureReading.inGoogleSheets == False)
    for reading in readings:
        if googlesheets.moisture_to_google(reading.toList(), settings.GOOGLE_SHEETS_SPREADSHEET_ID):
            # Update moisture reading to indicate it is in Google sheets.
            reading.inGoogleSheets = True
            db.session.add(reading)
            db.session.commit()


