# import the Flask class from the flask module
from flask import Flask, render_template,redirect,url_for, request , jsonify,json,make_response
import sys
sys.path.append("/usr/local/lib/python2.7/dist-packages" )
import pygal
sys.path.append("/usr/lib/python2.7/dist-packages")
import numpy as np

sys.path.append("/usr/lib/pymodules/python2.7")

import pandas as pd
from pandas import Series, DataFrame, Panel
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd

#from myapp import app
# create the application object
app = Flask(__name__)

@app.route('/graph')
def graph(chartID = 'chart_ID', chart_type = 'line', chart_height = 500):
   
    return render_template('index_3D.html', chartID=chartID)
 
@app.route('/')
def index():
    return render_template('layout/index_3D.html')

@app.route('/', methods=['POST'])
def my_form_post():
    x, y, z = np.random.multivariate_normal(np.array([0,0,0]), np.eye(3), 200).transpose()
    trace1 = go.Scatter3d(
        x=x,
        y=y,
        z=z,
        mode='markers',
        marker=dict(
            size=12,
            line=dict(
                color='rgba(217, 217, 217, 0.14)',
                width=0.5
            ),
            opacity=0.8
        )
    )

    x2, y2, z2 = np.random.multivariate_normal(np.array([0,0,0]), np.eye(3), 200).transpose()
    trace2 = go.Scatter3d(
        x=x2,
        y=y2,
        z=z2,
        mode='markers',
        marker=dict(
            color='rgb(127, 127, 127)',
            size=12,
            symbol='circle',
            line=dict(
                color='rgb(204, 204, 204)',
                width=1
            ),
            opacity=0.9
        )
    )
    data = [trace1, trace2]
    layout = go.Layout(
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=0
        )
    )
    plot_url = py.plot(data, filename='new plot', fileopt='new')
    #fig = go.Figure(data=data, layout=layout)
    #graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('layout/index_3D.html',
                           graphJSON=plot_url)



    #return render_template('index.html')





@app.route("/simple.png")
def simple():
    import datetime
    import StringIO
    import random

    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    from matplotlib.dates import DateFormatter

    fig=Figure()
    ax=fig.add_subplot(111)
    x=[]
    y=[]
    now=datetime.datetime.now()
    delta=datetime.timedelta(days=1)
    for i in range(10):
        x.append(now)
        now+=delta
        y.append(random.randint(0, 1000))
    ax.plot_date(x, y, '-')
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()
    canvas=FigureCanvas(fig)
    png_output = StringIO.StringIO()
    canvas.print_png(png_output)
    data = png_output.getvalue().encode('base64')
    data_url = 'data:image/png;base64,{}'.format(urllib.quote(data.rstrip('\n')))
    response=make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response







@app.route('/welcome')
def welcome():
    return render_template('welcome.html')  # render a template


@app.route('/testing')
def test():
    return render_template('testing.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
            return "ased"
        else:
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)
