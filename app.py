# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#################################################
# Database Setup
#################################################

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def climate(): 
    return(f"/api/v1.0/percipitation<br/>" f"/api/v1.0/stations<br/>" f"/api/v1.0/tobs<br/>" 
          f"/api/v1.0/ start<br/>" f"/api/v1.0/start/end<br/>") 
@app.route("/api/v1.0/percipitation")
def percipitation(): 
    session = Session(engine)
    last_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= last_date).all()
    ##() generally means calling a function, when calling function parameters go into parantheses
    ##example dt.function(2017, 8, 23) 
    ## set is in parantheses, different from list because immutable, cannot change what's in it 
    
    ##{} dictionary, dictionary has key value pairs unlike list 
    ##example key is a name of a column and values are names within column 
    
    ##[] a list, in python can be different types of objects, also used to set key in dict
    
    ##tuples shows with parantheses, a tuple is one variable with multiple objects inside like a list 
    ##tuples stores collection of variables like a list
    ##different from list because immutable, cannot change what's in it
    ##also ordered 
    ##key value pair because want value = percipitation and key = date 
    ##i is value and x is percipitation 
    ##calling on object and jsonifying object
    results_dict = {}
    for i, x in results: 
        results_dict[i] = x  
        session.close()
    return(jsonify(results_dict))
    ##object is a unit of code that computer understands, computer understands c
    ##jsonify converts into object computer understands, similar to translation tool

    ##/api/v1.0/stations
@app.route("/api/v1.0/stations")
def stations(): 
    session = Session(engine)
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    session.close()
    return(jsonify(stations))

    ##/api/v1.0/tobs
@app.route("/api/v1.0/tobs")
def tobs(): 
    session = Session(engine)
    last_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).filter(Measurement.station=="USC00519281").filter(Measurement.date>=last_date).all()
    stations = list(np.ravel(results))
    session.close()
    return(jsonify(stations))
    
    
##runs the app(variable created substantiating flask)
##dynamic route means that user can choose 
##dynamic route means based on user input

##m, d y allows user to input date and year, uppercase year is full year, lowercase is last two digits
@app.route ("/api/v1.0/<start>") 
@app.route ("/api/v1.0/<start>/<end>")
def stats(start = None, end = None):
    session = Session(engine)
    if not end: 
        start = dt.datetime.strptime(start, "%m-%d-%Y") 
        results = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.station == "USC00519281").filter(Measurement.date >= start).all()    
        session.close()
        return(jsonify(list(np.ravel(results)))) 
    
    start = dt.datetime.strptime(start, "%m-%d-%Y") 
    end = dt.datetime.strptime(end, "%m-%d-%Y")
    results = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.station == "USC00519281").filter(Measurement.date >= start).filter(Measurement.date <= end).all()  
    session.close()
    return(jsonify(list(np.ravel(results)))) 

if __name__ == "__main__": 
    app.run(debug=True)
    

    

    