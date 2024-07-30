import functions_framework
import sqlalchemy
import pg8000
import os
from google.cloud.sql.connector import Connector, IPTypes

@functions_framework.http
def get_restaurants_by_zipcode_pricerange(request):
    request_json = request.get_json()

    zip_code = request_json["zipcode"]
    price_range = request_json["pricerange"]
    
    stmt = sqlalchemy.text("select name from restaurant_9 where zip_code=:zip and price_range=:pricerange limit 10")

    text = "Here is a list of restaurants: "

    with connect_with_connector().connect() as db_conn:
        # read from database
        rows = db_conn.execute(stmt, parameters={"zip": zip_code, "pricerange": price_range}).fetchall()

        for row in rows:
            text = text + "\n" + row[0]
        text = text + "\n"
    
        res = {"fulfillment_response": {"messages": [{"text": {"text": [text]}}]}}

        if db_conn is not None:
            db_conn.close()

    # Returns json
    return res

def connect_with_connector() -> sqlalchemy.engine.base.Engine:
    # Cloud Secret Manager secrets exposed as environment variables
    db_user = os.environ["DB_USER"]
    db_pass = os.environ["DB_PASS"] 
    db_name = os.environ["DB_NAME"]
    instance_connection_name = os.environ["INSTANCE_CONNECTION_NAME"]

    # initialize Cloud SQL Python Connector object
    connector = Connector()

    def getconn() -> pg8000.dbapi.Connection:
        conn: pg8000.dbapi.Connection = connector.connect(
            instance_connection_name,
            "pg8000",
            user=db_user,
            password=db_pass,
            db=db_name,
            ip_type=IPTypes.PUBLIC,
        )
        return conn

    # The Cloud SQL Python Connector can be used with SQLAlchemy
    # using the 'creator' argument to 'create_engine'
    pool = sqlalchemy.create_engine(
        "postgresql+pg8000://",
        creator=getconn,
        # ...
    )
    return pool

