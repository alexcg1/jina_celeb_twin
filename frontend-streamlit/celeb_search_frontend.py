import streamlit as st
import random
import os
from config import image_endpoint, top_k, score_filter, data_dir_root
from helper import search_by_file, search_by_text, UI, create_temp_file

endpoint = image_endpoint
matches = []

# Layout
st.set_page_config(page_title="Jina meme search")
st.markdown(
    body=UI.css,
    unsafe_allow_html=True,
)

st.markdown(
    '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css" integrity="sha384-TX8t27EcRE3e/ihU7zmQxVncDAy5uIKz4rEkgIXeMed4M0jlfIDPvg6uqKI2xXr2" crossorigin="anonymous">',
    unsafe_allow_html=True,
)
query_params = st.experimental_get_query_params()

media_type = "Image"
st.header("Search from your own image...")
upload_cell, preview_cell = st.columns([12, 1])
query = upload_cell.file_uploader("Upload file")
if query:
    uploaded_image = create_temp_file(query)
    preview_cell.image(uploaded_image)
    if st.button(label="Search"):
        if not query:
            st.markdown("Please enter a query")
        else:
            matches = search_by_file(image_endpoint, top_k, "/tmp/query.png")

# Check for quality of top result (if top is bad, others bad too)
if matches:
    score = matches[0]['scores']['cosine']['value']
    if score > score_filter:
        print("Bad match!foo")
        st.markdown("## No matches found")
    else:

        # Results area
        cell1, cell2, cell3 = st.columns(3)
        cell4, cell5, cell6 = st.columns(3)
        cell7, cell8, cell9 = st.columns(3)
        all_cells = [cell1, cell2, cell3, cell4, cell5, cell6, cell7, cell8, cell9]

        for cell, match in zip(all_cells, matches):
            score = match['scores']['cosine']['value']
            image_uri = str(os.path.join(data_dir_root, match["tags"]["uri"]))
            cell.image(image_uri, use_column_width="auto")
            cell.markdown(score)

# Sidebar
st.sidebar.markdown(UI.text_block, unsafe_allow_html=True)
st.sidebar.markdown(UI.image_repo_block, unsafe_allow_html=True)
