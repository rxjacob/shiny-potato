import functions_framework
import requests
import os


@functions_framework.http
def search_restaurants(request):

    request_json = request.get_json()

    # Session ID
    sess = request_json["sessionInfo"]["session"]
    # Parameters
    params = request_json["sessionInfo"]["parameters"]
        
    project_id = os.environ.get("CLOUD_PROJECT")
    region = os.environ.get("CLOUD_REGION")

    base_url = "https://"+ region + "-" + project_id + ".cloudfunctions.net/"

    if 'zipcode' in params:
        # Send an HTTP POST request
        response = requests.post(base_url + "fetch_restaurants_by_zipcode_func", json=params)
        text = response.text
    else:
        text = "Unavailable to display restaurants without a zip code."


    msgs = {"text": {"text": [text]}}
    res = {"fulfillment_response": {"messages": [msgs]}, "sessionInfo": {"session": sess, "parameters":params}}

    # Returns json
    return res

