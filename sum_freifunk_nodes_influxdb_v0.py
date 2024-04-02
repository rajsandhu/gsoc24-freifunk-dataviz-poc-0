import os
import json
import requests
from dotenv import load_dotenv
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# Load environment variables from .env file
load_dotenv()

# Access environment variables
url = os.getenv('INFLUXDB_URL')
token = os.getenv('INFLUXDB_TOKEN')
org = os.getenv('INFLUXDB_ORG')
bucket = os.getenv('INFLUXDB_BUCKET')

# Create a client object
client = InfluxDBClient(url=url, token=token, org=org)

# Get a write API instance
write_api = client.write_api(write_options=SYNCHRONOUS)

# URLs of the JSON data
urls = [
    "https://api.freifunk.net/data/history/20240402-12.01.01-ffSummarizedDir.json",
    "https://api.freifunk.net/data/history/20240402-13.01.01-ffSummarizedDir.json",
    "https://api.freifunk.net/data/history/20240402-14.01.01-ffSummarizedDir.json"
]

# Iterate over each URL
for url in urls:
    # Fetch the JSON data from the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        # Extract the date from the URL
        date = url.split('/')[-1].split('-')[1]

        # Iterate over the list of city objects
        for city_name, city_data in data.items():
            total_cities += 1 # Increment the total cities counter
            # Check if 'city_data' is a dictionary and contains 'state' key
            if isinstance(city_data, dict) and 'state' in city_data:
                # Check if 'state' is a dictionary
                if isinstance(city_data['state'], dict):
                    # Check if 'state' contains 'nodes' key
                    if 'nodes' in city_data['state']:
                        point = Point("freifunk_nodes").tag("city", city_name).field("nodes", city_data['state']['nodes']).time(date)
                        write_api.write(bucket, org, point)
                else:
                    print(f"Unexpected structure for city: {city_name}")
            else:
                print(f"Unexpected structure for city: {city_name}")

# Close the client
client.close()

# Query data from InfluxDB using InfluxQL
query_api = client.query_api()
query = 'SELECT * FROM "freifunk_nodes" WHERE time >= now() - 1h'
result = query_api.query(query, org=org)

# Print the query results
for table in result:
    for record in table.records:
        print(record.values)
