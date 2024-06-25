import streamlit as st
import pandas as pd
from utils import database

indexed_products_cursor = database["indexed_products"].find()

indexed_products = []

sources = {}

for item in indexed_products_cursor:
    indexed_products.append(item)

    source = item.get("source")

    if source in sources:
        sources[source] += 1
    else:
        sources[source] = 1


st.write(f"# Total indexed products: {len(indexed_products)}")

st.write("## Sources")

sources_df = pd.DataFrame(sources.items(), columns=["Source", "Count"])
sources_df.set_index("Source", inplace=True)

st.bar_chart(sources_df, y="Count")

url_queues_cursor = database["url_queues"].find()

url_queues = []

sources = {}

for items in url_queues_cursor:
    url_queues.append(item)

    source = item.get("source")

    if source in sources:
        sources[source] += 1
    else:
        sources[source] = 1


st.write(f"# Total url queues: {len(url_queues)}")

st.write("## Sources")

sources_df = pd.DataFrame(sources.items(), columns=["Source", "Count"])
sources_df.set_index("Source", inplace=True)

st.bar_chart(sources_df, y="Count")
