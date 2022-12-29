#from flask import Flask
#app = Flask(__name__)
#@app.route('/')
#def hello_world():
    #return 'Hello World'

# Set Up the Flask Weather App

# Set all the dependencies

import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Set Up the Database

engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect the database into classes

Base = automap_base()

# Write the python Flask Function to reflect the tables

Base.prepare(engine, reflect=True)

# We'll create a variable for each of the classes so that we can reference them later, as shown below.

Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session link from Python to our database

session = Session(engine)

# Set Up Flask

app = Flask(__name__)

# Welcome route

@app.route("/")
def Welcome():
    return(
        '''
    Welcome to the Climate Analysis API!.\
    Available Routes:.\
    /api/v1.0/precipitation.\
    /api/v1.0/stations.\
    /api/v1.0/tobs.\
    /api/v1.0/temp/start/end.\
    ''')

# Precipitation route

@app.route("/api/v1.0/precipitation")
# Next, we will create the precipitation() function
def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)

# Station route

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

# Temperature Observations Route

@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)
   
# Statistics Route

# this route is different from the previous ones 
# in that we will have to provide both a starting and ending date

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)


