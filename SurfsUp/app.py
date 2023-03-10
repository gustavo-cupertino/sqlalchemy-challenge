import numpy as np
import datetime as dt


import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


from flask import Flask, jsonify


# Database Setup

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model

Base = automap_base()

# reflect the tables

Base.prepare(autoload_with=engine)
Base.classes.keys()

# Save a reference to the measurement and station tables

Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup

app = Flask(__name__)

# Flask Routes

@app.route("/")
def home():
    return (
        f"Welcome to the Home Page!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session from Python to the DB
    session = Session(engine)

    # Query results from precipitation analysis
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= "2016-08-23").all() 

    session.close()

    # Convert list of tuples into normal list

    prcp_scores = []
    for dates, prcp in results:
        precipitation_dict = {}
        precipitation_dict[dates] = prcp
        prcp_scores.append(precipitation_dict)

    return jsonify(prcp_scores)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query results for station analysis
    results2 = session.query(Station.station, Station.name).all() 

    session.close()

    # Convert list of tuples into normal list

    station_list = []
    for station, name in results2:
        station_dict = {}
        station_dict[station] = name
        station_list.append(station_dict)

    return jsonify(station_list)



@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query results from precipitation analysis

    results3 = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
                        filter(Measurement.station == 'USC00519281').\
                        filter(Measurement.date >= "2016-08-18").all()
    

    session.close()

    # Convert list of tuples into normal list

    temp_list = []
    for station, date, tobs in results3:
        temp_dict = {}
        temp_dict["station"] = station
        temp_dict["date"] = date
        temp_dict["temperature"] = tobs
        temp_list.append(temp_dict)

    return jsonify(temp_list)



@app.route("/api/v1.0/<start>")
def start_date(start):

    # Create our session (link) from Python to the DB
    session = Session(engine)


    # define date format to be passed on the search

    start == dt.datetime.strptime(start, "%Y-%m-%d")

    # Query results from measurements table

    sel = [func.min(Measurement.tobs),\
            func.avg(Measurement.tobs),\
                func.max(Measurement.tobs)]

    results4 = session.query(*sel).filter(Measurement.date >= start).all()


    session.close()

    # Convert list of tuples into normal list

    temps = list(np.ravel(results4))

    return jsonify(temps)





@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
# def end_date(end):

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # define date format to be passed on the search
    start == dt.datetime.strptime(start, "%Y-%m-%d")
    end == dt.datetime.strptime(end, "%Y-%m-%d")

    # Query results from measurements table

    sel = [func.min(Measurement.tobs),\
            func.avg(Measurement.tobs),\
                func.max(Measurement.tobs)]

    results5 = session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end).all()


    session.close()

    # Convert list of tuples into normal list

    temps2 = list(np.ravel(results5))

    return jsonify(temps2)



if __name__ == '__main__':
    app.run(debug=True)




