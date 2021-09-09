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

# Top section
st.markdown(UI.repo_banner, unsafe_allow_html=True)

tabs = ["Search by image", "Search by text", "Dude, this meme search suuuuucks"]
if "tab" in query_params:
    active_tab = query_params["tab"][0]
else:
    active_tab = "Search by image"

if active_tab not in tabs:
    st.experimental_set_query_params(tab="Search by image")
    active_tab = "Search by image"

li_items = "".join(
    f"""
    <li class="nav-item">
        <a class="nav-link{' active' if t==active_tab else ''}" href="/?tab={t}">{t}</a>
    </li>
    """
    for t in tabs
)
tabs_html = f"""
    <ul class="nav nav-tabs mt-4">
    {li_items}
    </ul>
"""

st.markdown(tabs_html, unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

if active_tab == "Search by image":
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

    # Sample image list
    elif active_tab == "Search by text":
        st.header("...or search from an existing meme")
        sample_files = []
        for filename in os.listdir("./samples"):
            sample_files.append(filename)
        sample_cells = st.columns(len(sample_files))

        for cell, filename in zip(sample_cells, sample_files):
            meme_name = filename.split(".")[0]
            cell.image(f"samples/{filename}", width=128)
            if cell.button(f"{meme_name}", key=meme_name):
                matches = search_by_file(image_endpoint, top_k, f"samples/{filename}")
elif active_tab == "Search by text":
    media_type = "Text"
    st.subheader("Search with a meme subject and/or caption...")
    query = st.text_input("Meme subject or caption", key="text_search_box")
    search_fn = search_by_text
    if st.button("Search", key="text_search"):
        matches = search_by_text(query, text_endpoint, top_k)
    st.subheader("...or search from a sample")
    sample_texts = [
        "squidward school",
        "so you're telling me willy wonka",
        "seagull kitkat",
    ]
    for text in sample_texts:
        if st.button(text):
            matches = search_by_text(text, text_endpoint, top_k)
else:
    st.markdown(
        """
### So, why I can't I see <this meme>?

A couple of answers to that question!

1. The [dataset we're using](https://www.kaggle.com/abhishtagatya/imgflipscraped-memes-caption-dataset) only contains so many "meme types"
2. This time round we only indexed 1,000 memes from the shuffled dataset. So there's a chance that even if a meme exists in the dataset, it didn't get picked up in our subset.

Update: Now it's 10,000 memes for text search. Image search still at 1,000 for now.

### So just index more memes, duh!
We didn't expect this to explode so soon. We're doing this as we speak.

### Ugh, just use a better dataset
We use this dataset because it has rich metadata. That lets use use both text search and image search (because the text search searches the JSON metadata that includes the captions)

### My meme search is much better!

Awesome! We threw this together quickly and didn't expect it to blow up. With more time we would use a better image encoder (like CLIP) and probably throw in some OCR too.

### How can I contact you to tell you that you suck to your stupid face?

Go to [Jina's Slack](https://slack.jina.ai) and vent away on #your-meme-search-sucks channel
"""
    )

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
            if media_type == "Text":
                cell.image("http:" + match["tags"]["image_url"])
            else:
                image_uri = str(os.path.join(data_dir_root, match["tags"]["uri"]))
                cell.image(image_uri, use_column_width="auto")
                cell.markdown(score)

# Sidebar
st.sidebar.markdown(UI.text_block, unsafe_allow_html=True)
st.sidebar.markdown(UI.image_repo_block, unsafe_allow_html=True)
