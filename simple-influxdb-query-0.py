import os
from dotenv import load_dotenv
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# Load environment variables from .env file
load_dotenv()

# Access environment variables to set up the connection parameters
url = os.getenv('INFLUXDB_URL')
token = os.getenv('INFLUXDB_TOKEN')
org = os.getenv('INFLUXDB_ORG')
bucket = os.getenv('INFLUXDB_BUCKET')

# Create a client object
client = InfluxDBClient(url=url, token=token, org=org)

# Get a write API instance
write_api = client.write_api(write_options=SYNCHRONOUS)

# Write data
data = "mem,host=host1 used_percent=23.43234543"
write_api.write(bucket, org, data)

# Query data
query_api = client.query_api()
query = 'from(bucket:"' + bucket + '") |> range(start: -1h)'
result = query_api.query(query, org=org)

# Print the result
print("Query Result:")
print(result)

# Close the client
client.close()
