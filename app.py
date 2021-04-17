import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from datetime import datetime, timedelta

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save reference to the table
Measurement= Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    return (
        f"Home Page<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/station<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def percipitation():
    session = Session(engine)
    
    results0= session.query(Measurement.date,Measurement.prcp ).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_prcp
    all_prcp = []
    for date2, prcp in results0:
        prcp_dict = {}
        prcp_dict["date"] = date2
        prcp_dict["prcp"] = prcp
        all_prcp.append(prcp_dict)
    return jsonify(all_prcp)

@app.route("/api/v1.0/station")
def stationfunc():
    session = Session(engine)
    results2= session.query(Station.station).all()
    session.close()
    stns = list(np.ravel(results2))

    #return json representation of the list
    return jsonify(stns)
    # # Create a dictionary from the row data and append to a list of stations_list
    # stations_list = []
    # for station in results2:
    #     stations_dict = {}
    #     stations_dict["station"] = station
    #     stations_list.append(stations_dict)

    # return jsonify(stations_list)


@app.route("/api/v1.0/tobs")
def temp():
    session = Session(engine)
    
    results3= session.query(Measurement.date,Measurement.tobs).filter(Measurement.station=='USC00519281',Measurement.date>'2016-08-23').all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_prcp
    all_tobs = []
    for date, tobs in results3:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)


@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def var_temp(start=None, end=None):
    session = Session(engine)
    sel = [func.min(Measurement.tobs), 
       func.max(Measurement.tobs), 
       func.count(Measurement.tobs),
       func.avg(Measurement.tobs)]

    if end != None:
        results4= session.query(*sel).filter(Measurement.date>=start).filter(Measurement.date<=end).all()
    else:
        results4= session.query(*sel).filter(Measurement.date>=start).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_prcp
    all_calcs = []
    for tmin, tmax, tcount, tavg  in results4:
        calcs_dict = {}
        calcs_dict["tmin"] = tmin
        calcs_dict["tmax"] = tmax
        calcs_dict["tcount"] = tcount
        calcs_dict["tavg"] = tavg
        all_calcs.append(calcs_dict)

    return jsonify(all_calcs)





if __name__ == '__main__':
    app.run(debug=True)