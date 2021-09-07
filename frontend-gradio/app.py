import gradio as gr
import pretty_errors
import numpy as np
from helper import save_image
from PIL import Image
import magic
import os
import requests

if not os.path.exists("uploads"):
    os.makedirs("uploads")

matches = []
score_filter = 0.25
headers = {"Content-Type": "application/json"}

def search_by_file(image, endpoint="http://0.0.0.0:12345/search", top_k=1):
    """search_by_file.

    :param endpoint:
    :param top_k:
    :param image: image sent from gradio
    """
    image_file = save_image(image)
    filetype = magic.from_file(image_file, mime=True)
    filename = os.path.abspath(image_file)
    print(f"Searching for {filename}")

    data = (
        '{"parameters": {"top_k": '
        + str(top_k)
        + '}, "mode": "search",  "data": [{"uri": "'
        + filename
        + '", "mime_type": "'
        + filetype
        + '"}]}'
    )
    response = requests.post(endpoint, headers=headers, data=data)
    content = response.json()
    match = content["data"]["docs"][0]["matches"][0]
    match_uri = match["tags"]["uri_absolute"]
    match_score = match["scores"]["cosine"]["value"]

    os.remove(filename)

    if match_score < score_filter:
        image = Image.open(match_uri)
        image_np_array = np.array(image)
        return image_np_array


iface = gr.Interface(search_by_file, gr.inputs.Image(source="webcam", tool=None), "image")

iface.test_launch()
if __name__ == "__main__":
    iface.launch()
