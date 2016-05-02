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


#from myapp import app
# create the application object
app = Flask(__name__)

@app.route('/hello')
def hello():
    return render_template('layout/test.html')
@app.route('/graph')
def graph(chartID = 'chart_ID', chart_type = 'line', chart_height = 500):
   
    return render_template('index_2D.html', chartID=chartID)
 
@app.route('/')
def index():
    return render_template('layout/index_2D.html')

@app.route('/', methods=['POST'])
def my_form_post():

    text = request.form['text']

    df=pd.read_csv(text)
    print "danish sodhi"
    print df.columns[0]
    xx=df.Time.tolist()
    yy=df.Output.tolist()
    rng = pd.date_range('1/1/2011', periods=7500, freq='H')
    ts = pd.Series(np.random.randn(len(rng)), index=rng)

    graphs = [
        dict(
            data=[
                dict(
                    x=xx,
                    y=yy,
                    type='scatter'
                ),
            ],
            layout=dict(
                title='Timeseries'
            )
        )
    ]

    # Add "ids" to each of the graphs to pass up to the client
    # for templating
    ids = ['graph-{}'.format(i) for i, _ in enumerate(graphs)]

    print "asshole"
    # Convert the figures to JSON
    # PlotlyJSONEncoder appropriately converts pandas, datetime, etc
    # objects to their JSON equivalents
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('layout/index_2D.html',
                           ids=ids,
                           graphJSON=graphJSON)



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
