
import streamlit as st
import pandas as pd
from utils import database


cursor = database.aql.execute(
    'FOR i IN indexed_products RETURN i.source',
)

indexed_products = []

sources = {}

if cursor is not None:
    for source in cursor:
        indexed_products.append(source)

        if source in sources:
            sources[source] += 1
        else:
            sources[source] = 1


st.write(f"# Total indexed products: {len(indexed_products)}")

st.write("## Sources")

sources_df = pd.DataFrame(sources.items(), columns=["Source", "Count"])
sources_df.set_index("Source", inplace=True)

st.bar_chart(sources_df, y="Count")


cursor = database.aql.execute(
    'FOR i IN uploaded_products RETURN i.source',
)

uploaded_products = []

sources = {}

if cursor is not None:
    for source in cursor:
        uploaded_products.append(source)

        if source in sources:
            sources[source] += 1
        else:
            sources[source] = 1


st.write(f"# Total uploaded products: {len(uploaded_products)}")

st.write("## Sources")

sources_df = pd.DataFrame(sources.items(), columns=["Source", "Count"])
sources_df.set_index("Source", inplace=True)

st.bar_chart(sources_df, y="Count")


cursor = database.aql.execute(
    'FOR i IN url_queues RETURN i.source',
)

url_queues = []

sources = {}

if cursor is not None:
    for source in cursor:
        url_queues.append(source)

        if source in sources:
            sources[source] += 1
        else:
            sources[source] = 1


st.write(f"# Total url queues: {len(url_queues)}")

st.write("## Sources")

sources_df = pd.DataFrame(sources.items(), columns=["Source", "Count"])
sources_df.set_index("Source", inplace=True)

st.bar_chart(sources_df, y="Count")


cursor = database.aql.execute(
    'FOR i IN crawled_pages RETURN i.source',
)

crawled_pages = []

sources = {}

if cursor is not None:
    for source in cursor:
        crawled_pages.append(source)

        if source in sources:
            sources[source] += 1
        else:
            sources[source] = 1


st.write(f"# Total crawled pages: {len(crawled_pages)}")

st.write("## Sources")

sources_df = pd.DataFrame(sources.items(), columns=["Source", "Count"])
sources_df.set_index("Source", inplace=True)

st.bar_chart(sources_df, y="Count")
