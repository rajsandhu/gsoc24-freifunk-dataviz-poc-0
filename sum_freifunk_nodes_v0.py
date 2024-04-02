import json
import requests

# URLs of the JSON data
urls = [
    "https://api.freifunk.net/data/history/20240402-12.01.01-ffSummarizedDir.json",
    "https://api.freifunk.net/data/history/20240402-13.01.01-ffSummarizedDir.json",
    "https://api.freifunk.net/data/history/20240402-14.01.01-ffSummarizedDir.json"
]

# Initialize counters for each date
dates_data = {}

# Iterate over each URL
for url in urls:
    # Fetch the JSON data from the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        # Extract the date from the URL
        date = url.split('/')[-1].split('-')[1]
        # Initialize counters for this date
        total_nodes = 0
        zero_nodes = 0
        no_nodes_key = 0
        total_cities = 0

        # Iterate over the list of city objects
        for city_name, city_data in data.items():
            total_cities += 1 # Increment the total cities counter
            # Check if 'city_data' is a dictionary and contains 'state' key
            if isinstance(city_data, dict) and 'state' in city_data:
                # Check if 'state' is a dictionary
                if isinstance(city_data['state'], dict):
                    # Check if 'state' contains 'nodes' key
                    if 'nodes' in city_data['state']:
                        # Add the number of nodes for the current city to the total
                        nodes = city_data['state']['nodes']
                        total_nodes += nodes
                        if nodes == 0:
                            zero_nodes += 1
                    else:
                        no_nodes_key += 1
                else:
                    print(f"Unexpected structure for city: {city_name}")
            else:
                print(f"Unexpected structure for city: {city_name}")

        # Store the data for this date
        dates_data[date] = {
            "total_cities": total_cities,
            "total_nodes": total_nodes,
            "zero_nodes": zero_nodes,
            "no_nodes_key": no_nodes_key
        }
    else:
        print(f"Failed to fetch data from {url}. Status code: {response.status_code}")

# Print the data for each date
for date, data in dates_data.items():
    print(f"Date: {date}")
    print(f"Total number of cities: {data['total_cities']}")
    print(f"Total number of nodes: {data['total_nodes']}")
    print(f"Cities with zero nodes: {data['zero_nodes']}")
    print(f"Cities with no 'nodes' key: {data['no_nodes_key']}")
    print()