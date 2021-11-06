"""
Columbia's COMS W4111.003 Introduction to Databases

Ruoxi Liu & Yunfan Cai

To run locally:
    python3 rest.py
"""

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response, url_for

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


# record the database uri
DATABASEURI = "postgresql://yc3992:5331@104/196.152.219/proj1part2"
# create a database engine
engine = create_engine(DATABASEURI)

@app.before_request
def before_request():
    """
    This function is runned at the beginning of every web request;
    it will set up a database connection that can be used throughout the request

    g is globally accessible
    """
    try:
        g.conn = engine.connect()
    except:
        print("Uh oh, problem connecting to database")
        import traceback;
        traceback.print_exc()
        g.conn = None


@app.teardown_request
def teardown_request(exception):
    """
    At the end of the web request, this makes sure to close the database connection
    """
    try:
        g.conn.close()
    except Exception as e:
        pass

@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        areas = request.form.get('Areas')
        cuisines = request.form.get('Cuisines')
        dine_types = request.form.get('Dine_Type')
        dine_options = request.form.get('Dine_Option')
        return redirect(url_for('webshow', areas = areas, cuisines = cuisines, dine_types = dine_types, dine_options = dine_options))
    
    area_selection = engine.execute('SELECT * FROM Area').fetchall()
    cuisine_selection = engine.execute('SELECT * FROM').fetchall()
    dine_type_selection = engine.execute('SELECT * FROM').fetchall()
    dine_option_selection = engine.execute('SELECT * FROM').fetchall()
    return render_template('index.html', area_selection, cuisine_selection, dine_option_selection, dine_type_selection)

@app.route('/show_result/?')
def webshow(areas, cuisines, dine_types, dine_options):
    restaurants = engine.execute('select distinct r.restaurant_name, r.rid, a.street_name, g1.grades_name'
                                'from Restaurant r join Rest_Type c on r.rid = c.rid'
                                'join Located_in l on r.rid = l.rid'
                                'join Address a on l.sid = a.sid'
                                'join Restaurant_Dining_Type dt on r.rid = dt.rid'
                                'join Restaurant_Dining_Option do on r.rid = do.rid'
                                'join graded g on r.rid = g.gid'
                                'join Grades g1 on g,gid = g1.gid'
                                'where c.cid = ? and a.aid = ? and dt.tid = ? and do.option_id = ?'
                                'order by g.gid asc',
                                (cuisines, areas, dine_types, dine_options))
    return render_template('webshow.html', restaurants)

if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python server.py

    Show the help text using:

        python server.py --help

    """

    HOST, PORT = host, port
    print("running on %s:%d" % (HOST, PORT))
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)
  run()