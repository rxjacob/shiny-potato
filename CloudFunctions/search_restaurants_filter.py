import functions_framework
import requests
import os


@functions_framework.http
def search_restaurants_filter(request):

    request_json = request.get_json()

    # Session ID
    sess = request_json["sessionInfo"]["session"]
    # Parameters
    params = request_json["sessionInfo"]["parameters"]

    if 'zipcode' in params:
        zip_code = params["zipcode"]

    if 'cuisine' in params:
        cuisine = params["cuisine"]

    if 'pricerange' in params:
        pricerange = params["pricerange"]
        
 
    project_id = os.environ.get("CLOUD_PROJECT")
    region = os.environ.get("CLOUD_REGION")

    base_url = "https://"+ region + "-" + project_id + ".cloudfunctions.net/"

    # Send an HTTP POST request
    response = requests.post(base_url + "fetch_restaurants_by_zipcode_func", json=params)
    text = response.text


    msgs = {"text": {"text": [text]}}
    res = {"fulfillment_response": {"messages": [msgs]}, "sessionInfo": {"session": sess, "parameters":params}}

    # Returns json
    return res

