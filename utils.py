from os import getenv
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

client = MongoClient(getenv("DB_URI"))

database = client["cedi_search"]
