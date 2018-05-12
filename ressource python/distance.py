# coding utf8

from math import radians, cos, sin, asin, sqrt

def haversineDistance(lon1, lat1, lon2, lat2):
    """
    Computes the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    # Radius of earth in kilometers is 6371
    m = 6371000 * c
    return m

def getDistances(df):
    size = df['timestampMs'].size
    distances = []
    for i in range(size - 1):
        distances.append(haversineDistance(
            df["longitude"][i],
            df["latitude"][i],
            df["longitude"][i+1],
            df["latitude"][i+1]))

    distances.append(0)

    return distances

def computeVelocity(dist, t1, t2):
    #Velocity in m/s
    v1 = (dist) / ((float(t2)-float(t1))*pow(10, -3))
    #Velocity in km/h
    v2 = v1 * 3.6
    return v2

def getVelocities(df):
    size = df['timestampMs'].size
    velocities = []
    for i in range(size - 1):
        velocities.append(computeVelocity(
            df["distance"][i],
            df["timestampMs"][i+1],
            df["timestampMs"][i]
        ))

    velocities.append(0)

    return velocities

def getAccelerations(df) :
    size = df['timestampMs'].size
    accelerations = []
    for i in range(size - 1):
        accelerations.append(computeVelocity(
            df["velocity"][i],
            df["timestampMs"][i+1],
            df["timestampMs"][i]
        ))

    accelerations.append(0)

    return accelerations

import pandas as pd
import datetime
import distance

def importJson(filepath, addColumns=True) :

	# Loading data
	raw = pd.io.json.read_json(filepath)
	df = raw['locations'].apply(pd.Series)

	# Create latitude and longitude columns
	df['latitude'] = df['latitudeE7'] * 0.0000001
	df['longitude'] = df['longitudeE7'] * 0.0000001

	# Clean up columns
	columns = ["timestampMs", "latitude", "longitude"]
	for col in list(df) :
		if col not in columns :
			del df[col]

	# Add date column in format 'dd-mm-YY'
	dates = []
	for timestamp in df['timestampMs']:
		dates.append(datetime.datetime.fromtimestamp(int(timestamp) / 1000).strftime('%d-%m-%Y'))
	df['date'] = dates

	# Add time column in format 'HH:MM:SS'
	time = []
	for row in df['timestampMs']:
		time.append(datetime.datetime.fromtimestamp(int(row) / 1000).strftime('%H:%M:%S'))
	df['time'] = time

	if not addColumns :
		return df
	else :
		# Add delay column seconds
		delay = []
		delay.append(0)
		for i in range(df['timestampMs'].size - 1):
			delay.append(int(int(df['timestampMs'][i]) - int(df['timestampMs'][i + 1])) / 1000)
		df['delay'] = delay

		# Add distance, velocity and acceleration 
		df['distance'] = distance.getDistances(df)
		df['velocity'] = distance.getVelocities(df)
		df['acceleration'] = distance.getAccelerations(df)

		return df

def selectDate(date, df) :
	result = df[df['date'] == date]
	return result.reset_index(drop=True) # Reset indices of dataframe
	