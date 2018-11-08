from MoistureReadingsFrontEnd.database.models import db
from MoistureReadingsFrontEnd.database.models import MoistureReading
from flask import Blueprint, render_template, abort, request
from flask_wtf import Form
from wtforms import DateField

import random
from bokeh.models import (HoverTool, FactorRange, Plot, LinearAxis, Grid,
                          Range1d)
from bokeh.models.glyphs import VBar
from bokeh.plotting import figure
#from bokeh.charts import Bar
from bokeh.embed import components
from bokeh.models.sources import ColumnDataSource
import datetime

web_blueprint = Blueprint('web', __name__, template_folder='templates')


class DateForm(Form):
    dt = DateField('Pick a Date', format="%m/%d/%Y")


@web_blueprint.route('/', methods=['GET'])
def show():
    form = DateForm()
    if form.validate_on_submit():
        return form.dt.data.strftime('%x')
    return render_template('index.html', form=form)


@web_blueprint.route('/testplot/')
def testplot():
    location_id = request.args.get('location', default = 1, type=int)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    # XOR start_date and end_date

    if start_date is not None:
        start_date = validate_date(start_date)
        if end_date is None:
            end_date = start_date + datetime.timedelta(days=30)
        else:
            end_date = validate_date(end_date)
    else:
        if end_date is None:
            start_date = datetime.datetime.now() - datetime.timedelta(days=30)
            end_date = datetime.datetime.now()
        else:
            end_date = validate_date(end_date)
            start_date = end_date - datetime.timedelta(days=30)
    print(start_date)
    print(end_date)
    if start_date >= end_date:
        return render_template("error.html", error_message=
                """You've got something wrong with your dates.
                Maybe the start date is after the end date?!?
                Or you've formated the dates wrong, use the format YYYY-MM-DD.
                """)

    plot = create_simple_line_chart(location_id, start_date, end_date)
    script, div = components(plot)
    plot_title = 'Line plot for location {0} from {1} to {2}'.format(location_id,start_date,end_date)
    return render_template("chart.html", plot_title=plot_title,
                           the_div=div, the_script=script)


def create_simple_line_chart(location_id, start_date = None, end_date = None):
    import pandas as pd
    #readings = MoistureReading.query.filter(MoistureReading.location_id == location_id)
    df = pd.read_sql(db.session.query(MoistureReading.timestamp, MoistureReading.moisture_value).filter(MoistureReading.location_id == location_id).statement,
                     con=db.session.bind)
    print(df)
    source = ColumnDataSource(df)

    p = figure(x_axis_type="datetime", plot_width=800, plot_height=350)
    p.line('timestamp', 'moisture_value', source=source)
    return p


def validate_date(date):
    print('attempting to validate !{0}!'.format(date))
    try:
        converted_date = datetime.datetime.strptime(date, "%Y-%m-%d")
        print('successfully converted string to datetime')
        return converted_date
    except:
        print('failed to convert string to datetime')
        return None

