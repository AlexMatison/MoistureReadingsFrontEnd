from flask_restplus import fields
from MoistureReadingsFrontEnd.api.restplus import api

moisture_reading = api.model('Moisture reading', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a moisture reading'),
    'location_id': fields.Integer(required=True, description='The location id of the moisture sensor'),
    'moisture_value': fields.Float(required=True, description='The moisture reading'),
    'timestamp': fields.DateTime,
    'inGoogleSheets': fields.Boolean
})

pagination = api.model('A page of results', {
    'page': fields.Integer(description='Number of this page of results'),
    'pages': fields.Integer(description='Total number of pages of results'),
    'per_page': fields.Integer(description='Number of items per page of results'),
    'total': fields.Integer(description='Total number of results'),
})

page_of_moisture_readings = api.inherit('Page of moisture readings', pagination, {
    'items': fields.List(fields.Nested(moisture_reading))
})
