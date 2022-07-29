import requests
import csv
from datetime import datetime


url = 'https://earthquake.usgs.gov/fdsnws/event/1/query?'


def validate_time(type_time):
    while True:        
        try:
            date_value = input(f"Enter the {type_time} in format yyyy-mm-dd (year-month-day): ")
            datetime.strptime(date_value, '%Y-%m-%d')
            print('Tnank you!')
            return date_value
        except ValueError:
            print(f'Parameter {type_time} must be in format yyyy-mm-dd')
            
                       
start_time = validate_time('start time')
end_time = validate_time('end time')


def validate_coordinate(type_coordinate, type_parameter, a, b):        
    while True:
        try:
            coordinate_value = input(f"Enter the {type_coordinate} in decimal {type_parameter} in the range from {a} to {b}: ")
            coordinate_value = float(coordinate_value)
            if  float(a) <= coordinate_value <= float(b):
                print('Tnank you!')
                return coordinate_value
            else:
                print(f'Parameter {type_coordinate} must be in the range from {a} to {b}')   
        except:
            print(f'Parameter {type_coordinate} must be in decimal {type_parameter}')
            
                             
latitude = validate_coordinate('latitude', 'degrees', '-90', '90')
longitude = validate_coordinate('longitude', 'degrees', '-180', '180')
max_radius_km = validate_coordinate('max radius', 'km', '0', '20001.6')


try:
    response = requests.get(url, params={
            'format':'geojson',
            'starttime':start_time,
            'endtime':end_time,
            'latitude':latitude,
            'longitude':longitude,
            'maxradiuskm': max_radius_km
            })
    data = response.json()
except requests.exceptions.Timeout:
    print("The server is not responding. Please try again later.")
    exit()
except requests.exceptions.TooManyRedirects:
    print("Probably wrong address.")
    exit()
except requests.ConnectionError:
    print("No connection to server. Check your internet connection and try again.")
    exit()


earthquake_list = data["features"]


with open('earthquake.csv', 'w', encoding="utf-8", newline='') as file:
	csv_writer = csv.writer(file)
	csv_writer.writerow(['Place', 'Magnitude'])
	for earthquake in earthquake_list:
		place = earthquake['properties'] ['place']
		magnitude = earthquake['properties'] ['mag']
		csv_writer.writerow([place, magnitude])  