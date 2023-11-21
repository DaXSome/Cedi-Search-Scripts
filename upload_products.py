from json import dumps
import uuid
from database import database
from algoliasearch.search_client import SearchClient
from dotenv import load_dotenv
from os import getenv
from firebase_admin import credentials, initialize_app
from firebase_admin.firestore import client, firestore
from uuid import uuid4
import concurrent.futures


def upload_product(index: int, product: dict) -> None:
    name = product["name"]
    productID = product["product_id"]

    if productID == "":
        productID = str(uuid4())

    _key = product["_key"]

    del product["_key"]

    print(f"[+] {index}) Uploading {name}")

    try:

        algolia_index.save_object(
            {**product,
             "objectID": productID,
             "description": product["description"][:5000]
             }).wait()

        firestore_client.collection(
            "products").document(productID).set(product)

        uploaded_products_collection.insert(product)

        indexed_products_collection.delete(_key)

        print(f"[+] {index}) Uploaded {name}")

    except Exception as e:
        print(f"[!] {index} Couldn't upload {name} because {e}")


load_dotenv()

cred = credentials.Certificate("serviceAccount.json")

initialize_app(cred)

firestore_client = client()

algolia_client = SearchClient.create(
    getenv("ALGOLIA_APP_ID"), getenv("ALGOLIA_API_KEY"))

algolia_index = algolia_client.init_index("products")

uploaded_products_collection = database.collection(name="uploaded_products")
indexed_products_collection = database.collection(name="indexed_products")


cursor = database.aql.execute(
    """
        FOR d IN indexed_products
        RETURN {
            _key: d._key,
            product_id: d.product_id,
            name: d.name,
            price: d.price,
            rating: d.rating,
            description: d.description,
            url: d.url,
            source: d.source,
            images: d.images
        }
    """,
)


if cursor is not None:
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:

        for index, product in enumerate(cursor):

            executor.submit(upload_product, index, product)


cursor = database.aql.execute(
    """
        FOR d IN uploaded_products
        RETURN d.name
    """,
)

with open("index.json", "w") as index_file:
    index_file.write(dumps(list(cursor)))
