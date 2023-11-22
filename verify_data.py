from utils import database
from utils import algolia_index, firestore_client, database


uploaded_products_collection = database.collection(name="uploaded_products")
url_queues_collection = database.collection(name="url_queues")

urls = []

cursor = database.aql.execute(
    """
        FOR d IN uploaded_products
        RETURN {
            _key: d._key,
            url: d.url,
            id: d.product_id
        }
    """,
)

if cursor is not None:
    for product in cursor:
        if product["url"] not in urls:
            urls.append(product["url"])
        else:
            print(product["url"])
            algolia_index.delete_object(product["id"])
            firestore_client.collection(
                "products").document(product['id']).delete()
            uploaded_products_collection.delete(product["_key"])

urls = []

cursor = database.aql.execute(
    """
        FOR d IN url_queues
        RETURN {
            _key: d._key,
            url: d.url,
            id: d.product_id
        }
    """,
)

if cursor is not None:
    for product in cursor:
        if product["url"] not in urls:
            urls.append(product["url"])
        else:
            print(product["url"])
            url_queues_collection.delete(product["_key"])
