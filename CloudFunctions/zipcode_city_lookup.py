import functions_framework
import requests
import json
import os

# entry function
@functions_framework.http
def city_lookup(request):
    request_json = request.get_json()

    # Extract parameter from the request
    zip_code = request_json["text"]
    sess = request_json["sessionInfo"]["session"]


    # Replace with the actual API URL
    url = "https://maps.googleapis.com/maps/api/geocode/json"+ \
        "?sensor=true"+ \
        "&key="+ os.environ["MAP_API_KEY"] + \
        "&address=" + zip_code

    # Send a GET request
    maps_response = requests.get(url)

    text = "I wasn't able to get your location"

    if maps_response.status_code == 200:
        data = json.loads(maps_response.text)
        for result in data["results"]:
            text = "Your location is set to " + result["formatted_address"]

    msgs = {"text": {"text": [text]}}
    params = {"zipcode": zip_code}
    res = {"fulfillment_response": {"messages": [msgs]}, "sessionInfo": {"session": sess, "parameters":params}}

    # Returns json
    return res
