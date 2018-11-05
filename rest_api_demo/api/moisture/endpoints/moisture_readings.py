import logging

from flask import request
from flask_restplus import Resource
from rest_api_demo.api.moisture.business import create_moisture_reading, update_moisture_reading, delete_post
from rest_api_demo.api.moisture.serializers import moisture_reading, page_of_moisture_readings
from rest_api_demo.api.moisture.parsers import pagination_arguments
from rest_api_demo.api.restplus import api
from rest_api_demo.database.models import MoistureReading

log = logging.getLogger(__name__)

ns = api.namespace('moisture/readings', description='Operations related to moisture readings')


@ns.route('/')
class MoistureReadingCollection(Resource):

    @api.expect(pagination_arguments)
    @api.marshal_with(page_of_moisture_readings)
    def get(self):
        """
        Returns list of moisture posts.
        """
        args = pagination_arguments.parse_args(request)
        page = args.get('page', 1)
        per_page = args.get('per_page', 10)

        posts_query = MoistureReading.query
        posts_page = posts_query.paginate(page, per_page, error_out=False)

        return posts_page

    @api.expect(moisture_reading)
    def post(self):
        """
        Creates a new moisture post.
        """
        create_moisture_reading(request.json)
        return None, 201


@ns.route('/<int:id>')
@api.response(404, 'MoistureReading not found.')
class PostItem(Resource):

    @api.marshal_with(moisture_reading)
    def get(self, id):
        """
        Returns a moisture post.
        """
        return MoistureReading.query.filter(MoistureReading.id == id).one()

    @api.expect(moisture_reading)
    @api.response(204, 'MoistureReading successfully updated.')
    def put(self, id):
        """
        Updates a moisture post.
        """
        data = request.json
        update_moisture_reading(id, data)
        return None, 204

    @api.response(204, 'MoistureReading successfully deleted.')
    def delete(self, id):
        """
        Deletes moisture post.
        """
        delete_post(id)
        return None, 204


@ns.route('/archive/<int:year>/')
@ns.route('/archive/<int:year>/<int:month>/')
@ns.route('/archive/<int:year>/<int:month>/<int:day>/')
class MoistureReadingArchiveCollection(Resource):

    @api.expect(pagination_arguments, validate=True)
    @api.marshal_with(page_of_moisture_readings)
    def get(self, year, month=None, day=None):
        """
        Returns list of moisture posts from a specified time period.
        """
        args = pagination_arguments.parse_args(request)
        page = args.get('page', 1)
        per_page = args.get('per_page', 10)

        start_month = month if month else 1
        end_month = month if month else 12
        start_day = day if day else 1
        end_day = day + 1 if day else 31
        start_date = '{0:04d}-{1:02d}-{2:02d}'.format(year, start_month, start_day)
        end_date = '{0:04d}-{1:02d}-{2:02d}'.format(year, end_month, end_day)
        moisture_readings_query = MoistureReading.query.filter(MoistureReading.pub_date >= start_date).filter(MoistureReading.pub_date <= end_date)

        posts_page = moisture_readings_query.paginate(page, per_page, error_out=False)

        return posts_page
