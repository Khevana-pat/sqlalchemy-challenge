 #Import all dependencies: 
import numpy as np
import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify 

# Create connection to Hawaii.sqlite file
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to the measurement and station tables in the database
Measurement = Base.classes.measurement
Station = Base.classes.station

# Initialize Flask
app = Flask(__name__)

# Create  route
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
        f"Note: to access values between a start and end date enter both dates using format: YYYY-mm-dd/YYYY-mm-dd"
    )

app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    #calculate previous year based on the last entry in the table
    prev_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    #calculate precipitation for the previous year
    precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    session.close()
    return jsonify(precip)

app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    #calculate previous year based on the last entry in the table
    prev_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    #calculate precipitation for the previous year
    precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    session.close()
    return jsonify(precip)

@app.route("/api/v1.0/tobs")
def temp_monthly():
     session = Session(engine)
     prev_year = dt.date(2017,8,23) - dt.timedelta(days=365)
     #calculate all the temperature reported at the highest reported station for the previous year
     results = session.query(Measurement.tobs).\
         filter(Measurement.station == 'USC00519281').\
         filter(Measurement.date >= prev_year).all()
     temps = list(np.ravel(results))
     session.close()
     return jsonify(temps=temps)

@app.route("/api/v1.0/<start>/<end>")

# Define function, set start and end dates entered by user as parameters for start_end_date decorator
def Start_end_date(start, end):
    session = Session(engine)

    """Return a list of min, avg and max tobs between start and end dates entered"""
    
    # Create query for minimum, average, and max tobs where query date is greater than or equal to the start date and less than or equal to end date user submits in URL

    start_end_date_tobs_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()

    session.close()
  
    # Create a list of min,max,and average temps that will be appended with dictionary values for min, max, and avg tobs queried above
    start_end_tobs_date_values = []
    for min, avg, max in start_end_date_tobs_results:
        start_end_tobs_date_dict = {}
        start_end_tobs_date_dict["min_temp"] = min
        start_end_tobs_date_dict["avg_temp"] = avg
        start_end_tobs_date_dict["max_temp"] = max
        start_end_tobs_date_values.append(start_end_tobs_date_dict) 
    

    return jsonify(start_end_tobs_date_values)
   
if __name__ == '__main__':
    app.run(debug=True) 
