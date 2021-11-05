"""
Columbia's COMS W4111.003 Introduction to Databases

Ruoxi Liu & Yunfan Cai

To run locally:
    python3 rest.py
"""

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

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

@app.route('/')
def index():
    area_selection = engine.execute('SELECT * FROM Area').fetchall()
    cuisine_selection = engine.execute('SELECT * FROM').fetchall()
    dine_type_selection = engine.execute('SELECT * FROM').fetchall()
    dine_option_selection = engine.execute('SELECT * FROM').fetchall()
    return render_template('index.html', area_selection, cuisine_selection, dine_option_selection, dine_type_selection)