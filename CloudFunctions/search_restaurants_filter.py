import functions_framework
import requests
import os
import vertexai
import json
from vertexai.generative_models import (
    Content,
    FunctionDeclaration,
    GenerationConfig,
    GenerativeModel,
    Part,
    Tool,
)

@functions_framework.http
def search_restaurants_filter(request):

  
    request_json = request.get_json()

    # Session ID
    sess = request_json["sessionInfo"]["session"]
    # Parameters
    params = request_json["sessionInfo"]["parameters"]

    zip_code = None
    if 'zipcode' in params:
        zip_code = params["zipcode"]

    cuisine = None
    if 'cuisine' in request_json["intentInfo"]["parameters"]:
        cuisine = request_json["intentInfo"]["parameters"]["cuisine"]["resolvedValue"]
        params["cuisine"]=cuisine
    elif 'cuisine' in params:
        cuisine = params["cuisine"]

    price_range = None
    if 'price' in request_json["intentInfo"]["parameters"]:
        price_range = request_json["intentInfo"]["parameters"]["price"]["resolvedValue"]
        params["pricerange"]=price_range
    elif 'pricerange' in params:
        price_range = params["pricerange"]
        

    fetch_restaurants_by_zipcode_func = FunctionDeclaration(
        name="fetch_restaurants_by_zipcode_func",
        description="Get a list of restaurants based on zip code",
        parameters={
            "type": "object",
            "properties": {
                "zip_code": {"type": "string", "description": "Zip code"},
            },
        },
    )

    fetch_restaurants_by_zipcode_cuisine = FunctionDeclaration(
        name="fetch_restaurants_by_zipcode_cuisine",
        description="Get a list of restaurants based on cuisine and zip code",
        parameters={
            "type": "object",
            "properties": {
                "zip_code": {"type": "string", "description": "Zip code"},
                "cuisine": {"type": "string", "description": "Cuisine"},
            },
        },
    )

    fetch_restaurants_by_zipcode_pricerange = FunctionDeclaration(
        name="fetch_restaurants_by_zipcode_pricerange",
        description="Get a list of restaurants based on zip code and price range (low, medium, high)",
        parameters={
            "type": "object",
            "properties": {
                "zip_code": {"type": "string", "description": "Zip code"},
                "price_range": {"type": "string", "description": "Price Range"},
            },
        },
    )

    fetch_restaurants_by_zipcode_cuisine_pricerange = FunctionDeclaration(
        name="fetch_restaurants_by_zipcode_cuisine_pricerange",
        description="Get a list of restaurants based on zip code, cuisine and price range (low, medium, high)",
        parameters={
            "type": "object",
            "properties": {
                "zip_code": {"type": "string", "description": "Zip code"},
                "cuisine": {"type": "string", "description": "Cuisine"},
                "price_range": {"type": "string", "description": "Price Range"},
            },
        },
    )


    retail_tool = Tool(
        function_declarations=[
            fetch_restaurants_by_zipcode_func,
            fetch_restaurants_by_zipcode_cuisine,
            fetch_restaurants_by_zipcode_pricerange,
            fetch_restaurants_by_zipcode_cuisine_pricerange,
        ],
    )

    model = GenerativeModel(
        "gemini-1.5-pro-001",
        generation_config=GenerationConfig(temperature=0),
        tools=[retail_tool],
    )
    chat = model.start_chat()

    prompt = "find restaurants " + request_json["text"]
    if zip_code is not None:
        prompt += " zip code " + zip_code
    if price_range is not None:
        prompt += " price range " + price_range
    if cuisine is not None:
        prompt += " cuisine " + cuisine

    project_id = os.environ.get("CLOUD_PROJECT")
    region = os.environ.get("CLOUD_REGION")

    base_url = "https://"+ region + "-" + project_id + ".cloudfunctions.net/"

    gem_response = chat.send_message(prompt)
    part = gem_response.candidates[0].content.parts[0]            

    x = gem_response.candidates[0].content.parts[0].function_call.args
    p = '{'
    for i in x:
        p += '"' + i + '"'
        p += ":"
        p += '"' + x[i] + '"'
        p += ","
    p = p[:-1]+'}'

    # Send an HTTP POST request
    response = requests.post(base_url + part.function_call.name, json=json.loads(p))


    text = response.text
    msgs = {"text": {"text": [text]}}
    res = {"fulfillment_response": {"messages": [msgs]}, "sessionInfo": {"session": sess, "parameters":params}}

    # Returns json
    return res

