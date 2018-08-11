import numpy as np

import datetime as dt

import json

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the precipitation per date as json"""
    end = dt.date(2017,8,23)
    start = end - dt.timedelta(days=365)
    
    prcp_query = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= start).filter(Measurement.date <= end).order_by(Measurement.date.desc()).all()
    #daterains = []
    #for i in prcp_query:
    #    date=(i[0])
    #    prcp=(i[1])
    #    daterain = {"date":date, "prcp":prcp}
    #    daterains.append(daterain)
    
    #dump=json.dumps(daterains)
    #dump=jsonify(dump)
    
    
    return jsonify(prcp_query)

@app.route("/api/v1.0/stations")
def stations():
    Stations = session.query(Measurement.station, Station.name).filter(Measurement.station==Station.station).group_by(Measurement.station).all()
    
    return jsonify(Stations)
    

@app.route("/api/v1.0/tobs")
def tobs():
    end = dt.date(2017,8,23)
    start = end - dt.timedelta(days=365)
    twelve_month_temp = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    return jsonify(twelve_month_temp)


@app.route("/api/v1.0/<start>")
def start_day(start):
    Start_temps = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).group_by(Measurement.date).all()
        
    return jsonify(Start_temps)

@app.route("/api/v1.0/<start>/<end>")
def trip_length(start, end):
    Trip_temps = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date <= end).filter(Measurement.date >= start).group_by(Measurement.date).all()
    
    return jsonify(Trip_temps)

if __name__ == "__main__":
    app.run(debug=True)