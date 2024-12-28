from utils import database
from os import getenv
from dotenv import load_dotenv
from json import load, dumps

load_dotenv()

from algoliasearch.search.client import SearchClientSync

algolia_client = SearchClientSync(getenv("ALGOLIA_APP_ID"), getenv("ALGOLIA_API_KEY"))

records = []

def agg(record):
    for rec in  record.to_dict()["hits"]:
        if rec.get("body") == None: continue
        records.append(rec["body"]["objectID"])

algolia_client.browse_objects(index_name="products", aggregator=agg, request_options={
   "timeouts": {
            "read": 100_000,
            "connect": 100_000,
            "write": 100_000
        },
})

products = database["indexed_products"].find()

to_upload= []

for index, product in enumerate(products):
    if str(product["_id"]) in records:
        continue

    product["objectID"] = str(product["_id"])

    del product["_id"]

    to_upload.append({"action": "addObject", "body": product})

    print(f"{index}) {product.get('name')}")

print(f"{len(to_upload)} to upload")

for index, product in enumerate(to_upload):
    
    print(f"{index}) {product["body"].get('name')}")
    
    try:

        resp = algolia_client.save_object(index_name="products", body=product)

    except Exception as e:
        print(e)


