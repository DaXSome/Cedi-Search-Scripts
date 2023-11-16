from dotenv import load_dotenv
from arango.client import ArangoClient
from os import getenv

load_dotenv()

client = ArangoClient(hosts=str(getenv("DB_CONNECTION_STRING")))

database = client.db("cedi_search", username=str(getenv(
    "DB_USERNAME")), password=str(getenv("DB_PASSWORD")))
