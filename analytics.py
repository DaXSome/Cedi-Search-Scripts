import streamlit as st
import pandas as pd
from utils import database
from streamlit_autorefresh import st_autorefresh

st_autorefresh(interval=1000*60)


url_sources = ["Jumia", "Jiji", "Oraimo", "Deus", "Ishtari"]

indexed_products_cursor = database["indexed_products"].find()

indexed_products = 0

sources = {}

for source in url_sources:
    total = database["indexed_products"].count_documents({
        "source": source})

    sources[source] = total

    indexed_products += total

st.write(f"# Total indexed products: {indexed_products}")

st.write("## Sources")

sources_df = pd.DataFrame(sources.items(), columns=["Source", "Count"])
sources_df.set_index("Source", inplace=True)

st.bar_chart(sources_df, y="Count")

url_queues_cursor = database["url_queues"].find()

url_queues = 0

sources = {}

for source in url_sources:
    total = database["url_queues"].count_documents({
        "source": source})

    sources[source] = total

    url_queues += total

st.write(f"# Total url queues: {url_queues}")

st.write("## Sources")

sources_df = pd.DataFrame(sources.items(), columns=["Source", "Count"])
sources_df.set_index("Source", inplace=True)

st.bar_chart(sources_df, y="Count")
