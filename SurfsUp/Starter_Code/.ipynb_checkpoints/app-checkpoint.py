# Import the dependencies.
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
Base.prepare(autoload_with=engine)

# reflect the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Save references to each table
measurement_table = Measurement
station_table = Station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

# Start at the homepage.
# List all the available routes.
@app.route("/")
def Homepage():
    return (
        f"Welcome to the Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"
    )



# Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) 
# to a dictionary using date as the key and prcp as the value.
# Return the JSON representation of your dictionary.

# While the code is already written in a Jupyter Notebook, you need to adapt and integrate that code 
# into your Flask application to create the API endpoints.
# Think of Jupyter Notebook as a place where you've experimented and developed your logic, and your app.py 
# file as the place where you formalize that logic into a web application with specific routes and endpoints. 
# You're essentially transferring your code from the Jupyter Notebook to your Flask application to make it accessible through the API routes.
@app.route("/api/v1.0/precipitation")
def precipitation():
    
    # Calculate the date one year from the most recent date in the dataset
    most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    one_year_ago = (pd.to_datetime(most_recent_date[0]) - pd.DateOffset(days=365)).date()

    # Perform a query to retrieve the precipitation data for the last 12 months
    precipitation_data = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= one_year_ago).all()

    
    # Convert the query results to a dictionary using date as the key and prcp as the value
    # For each tuple in the precipitation_data list, the loop iterates through and assigns the date value as the key 
    # and the prcp value as the corresponding value in the dictionary. This process is repeated for each tuple in 
    # the list, effectively creating a dictionary where each date is paired with its respective precipitation value.
    precipitation_dict = {date: prcp for date, prcp in precipitation_data}

    # Return the JSON representation of the dictionary
    return jsonify(precipitation_dict)


# Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    
    # Query the list of unique station names from the measurement table
    station_list = session.query(Measurement.station).distinct().all()
    
    # Convert the list of tuples to a list of station names
    stations = [station[0] for station in station_list]
    
    
    return jsonify(stations)



# Query the dates and temperature observations of the most-active station for the previous year of data.
# Return a JSON list of temperature observations for the previous year.
@app.route("/api/v1.0/tobs")
def tobs():
    
    # Calculate the date one year from the most recent date in the dataset
    most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    one_year_ago = (pd.to_datetime(most_recent_date[0]) - pd.DateOffset(days=365)).date()

    # Define the columns to select and join the Measurement and Station tables
    sel = [Measurement.date, Measurement.tobs]
    tobs_query = session.query(*sel).\
        join(Station, Measurement.station == Station.station).\
        filter(Measurement.date >= one_year_ago).\
        filter(Station.station == "USC00519281").all()

    tobs_data = [{"date": date, "tobs": tobs} for date, tobs in tobs_query]


    
    return jsonify(tobs_data)



# Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature 
# for a specified start or start-end range.
# For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
@app.route("/api/v1.0/<start>")
def start_date(start):
    # Convert the input start date to a datetime object
    start_date = pd.to_datetime(start)

    # Query to calculate TMIN, TAVG, and TMAX for dates greater than or equal to the start date
    temp_stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()


    # Create a dictionary to store the temperature statistics
    temp_dict = [{
        "TMIN": temp_stats[0][0],
        "TAVG": temp_stats[0][1],
        "TMAX": temp_stats[0][2]
    }]

    return jsonify(temp_dict)



# For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
@app.route('/api/v1.0/<start>/<end>')
def start_end_date(start, end):
    
    # Convert the input start and end dates to datetime objects
    start_date = pd.to_datetime(start)
    end_date = pd.to_datetime(end)

    # Query to calculate TMIN, TAVG, and TMAX for dates between start date and end date (inclusive)
    temp_stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date, Measurement.date <= end_date).all()
        
    # Create a dictionary to store the temperature statistics
    temp_data = [{
        "TMIN": temp_stats[0][0],
        "TAVG": temp_stats[0][1],
        "TMAX": temp_stats[0][2]
    }]

    # Return the JSON representation of the temperature statistics
    return jsonify(temp_dict)

if __name__ == "__main__":
    app.run(debug=True)



