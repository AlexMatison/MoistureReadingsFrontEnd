from MoistureReadingsFrontEnd.database.models import db
from MoistureReadingsFrontEnd.database.models import MoistureReading
from flask import Blueprint, render_template, abort

import random
from bokeh.models import (HoverTool, FactorRange, Plot, LinearAxis, Grid,
                          Range1d)
from bokeh.models.glyphs import VBar
from bokeh.plotting import figure
#from bokeh.charts import Bar
from bokeh.embed import components
from bokeh.models.sources import ColumnDataSource

web_blueprint = Blueprint('web', __name__, template_folder='templates')


@web_blueprint.route('/', methods=['GET'])
def show():
    return render_template('index.html')


@web_blueprint.route('/testplot/<int:location_id>/')
def chart(location_id):

    plot = create_simple_line_chart(location_id)
    script, div = components(plot)
    return render_template("chart.html", location_id=location_id,
                           the_div=div, the_script=script)


def create_simple_line_chart(location_id):
    import pandas as pd
    #readings = MoistureReading.query.filter(MoistureReading.location_id == location_id)
    df = pd.read_sql(db.session.query(MoistureReading.timestamp, MoistureReading.moisture_value).filter(MoistureReading.location_id == location_id).statement,
                     con=db.session.bind)
    print(df)
    source = ColumnDataSource(df)

    p = figure(x_axis_type="datetime", plot_width=800, plot_height=350)
    p.line('timestamp', 'moisture_value', source=source)
    return p
