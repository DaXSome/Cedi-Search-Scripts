from dotenv import load_dotenv
from arango.client import ArangoClient
from os import getenv
from dotenv import load_dotenv
from os import getenv
from firebase_admin import credentials, initialize_app
from firebase_admin.firestore import client
from algoliasearch.search_client import SearchClient
from firebase_admin.firestore import client


load_dotenv()

arango_client = ArangoClient(hosts=str(getenv("DB_CONNECTION_STRING")))

database = arango_client.db("cedi_search", username=str(getenv(
    "DB_USERNAME")), password=str(getenv("DB_PASSWORD")))


cred = credentials.Certificate("serviceAccount.json")

initialize_app(cred)

firestore_client = client()

algolia_client = SearchClient.create(
    getenv("ALGOLIA_APP_ID"), getenv("ALGOLIA_API_KEY"))

algolia_index = algolia_client.init_index("products")
