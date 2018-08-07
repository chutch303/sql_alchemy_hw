from flask import Flask, jsonify

from dbsetup import session, Measurement, Station, engine

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World'

# Query for the dates and temperature observations from the last year.
# Convert the query results to a Dictionary using date as the key and tobs as the value.
# Return the JSON representation of your dictionary.

@app.route('/api/v1.0/precipitation/')
def precipv1():
    weather_rows = engine.execute("""
    SELECT m.date, avg(m.tobs) as temp
    from Measurement m
    WHERE strftime('%Y', m.date) = "2017"
    GROUP BY 1
    ORDER BY 1
    """).fetchall()

    vals = {k:v for k,v in weather_rows}   
    return jsonify(vals)

#Return a JSON list of stations from the dataset.

@app.route('/api/v1.0/stations/')
def stationsv1():
    station_list = {}
    station_list['data'] = []

    for row in session.query(Station):
        station_list['data'].append(
                {'id': row.id,
                'station': row.station,
                'lat': row.latitude,
                'lng' : row.longitude,
                'elev' : row.elevation})
        return jsonify(station_list)

app.run(debug=True)