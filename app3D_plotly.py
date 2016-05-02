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
    return render_template('test.html')
@app.route('/graph')
def graph(chartID = 'chart_ID', chart_type = 'line', chart_height = 500):
   
    return render_template('index_plotly3D.html', chartID=chartID)
 
@app.route('/')
def index():
    return render_template('layout/index_plotly3D.html')

@app.route('/', methods=['POST'])
def my_form_post():

    text = request.form['text']
    colnames = ['xaxis', 'yaxis','zaxis']
    df=pd.read_csv(text,names=colnames)

    xx=df.xaxis.tolist()
    yy=df.yaxis.tolist()
    zz=xx+yy
    print xx

    import sys
    import os
    from plotly import session, tools, utils
    import uuid
    import json


    def get_plotlyjs():
        path = os.path.join('offline', 'plotly.min.js')
        plotlyjs = resource_string('plotly', path).decode('utf-8')
        return plotlyjs


    def js_convert(figure_or_data,outfilename, show_link=False, link_text='Export to plot.ly',
              validate=True):

        figure = tools.return_figure_from_figure_or_data(figure_or_data, validate)

        width = figure.get('layout', {}).get('width', '100%')
        height = figure.get('layout', {}).get('height', 525)
        try:
            float(width)
        except (ValueError, TypeError):
            pass
        else:
            width = str(width) + 'px'

        try:
            float(width)
        except (ValueError, TypeError):
            pass
        else:
            width = str(width) + 'px'

        plotdivid = uuid.uuid4()
        jdata = json.dumps(figure.get('data', []), cls=utils.PlotlyJSONEncoder)
        jlayout = json.dumps(figure.get('layout', {}), cls=utils.PlotlyJSONEncoder)

        config = {}
        config['showLink'] = show_link
        config['linkText'] = link_text
        config["displaylogo"]=False
        config["modeBarButtonsToRemove"]= ['sendDataToCloud']
        jconfig = json.dumps(config)

        plotly_platform_url = session.get_session_config().get('plotly_domain',
                                                               'https://plot.ly')
        if (plotly_platform_url != 'https://plot.ly' and
                link_text == 'Export to plot.ly'):

            link_domain = plotly_platform_url\
                .replace('https://', '')\
                .replace('http://', '')
            link_text = link_text.replace('plot.ly', link_domain)


        script = '\n'.join([
            'Plotly.plot("{id}", {data}, {layout}, {config}).then(function() {{',
            '    $(".{id}.loading").remove();',
            '}})'
        ]).format(id=plotdivid,
                  data=jdata,
                  layout=jlayout,
                  config=jconfig)

        html="""<div class="{id} loading" style="color: rgb(50,50,50);">
                     Drawing...</div>
                     <div id="{id}" style="height: {height}; width: {width};" 
                     class="plotly-graph-div">
                     </div>
                     <script type="text/javascript">
                     {script}
                     </script>
                     """.format(id=plotdivid, script=script,
                               height=height, width=width)

        #html =  html.replace('\n', '')
        with open(outfilename, 'wb') as out:
            out.write(r'<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>')
            for line in html.split('\n'):
                out.write(line)

            out.close()   
        print ('JS Conversion Complete')


    import numpy as np
    xx=[1,1,7,6,19,14,21,28,29,11]
    yy=[8,4,45,12,4,8,11,1,6,27]

    zz=[5,7,8,15,25,1,0,8,3,17]
    print xx
    x=xx
    y=yy
    z=zz
    trace1 = dict(
        type = 'scatter3d',
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
    layout = dict(
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=0
        )
    )
    fig = dict(data = [trace1], layout = layout)
    js_convert(fig, 'templates/test.html')

    return render_template('layout/index_plotly3D.html',
                           graphJSON='test.html')



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
