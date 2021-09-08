import gradio as gr
import pretty_errors
import numpy as np
from helper import save_image, check_human
from PIL import Image
import magic
import os
import requests

if not os.path.exists("uploads"):
    os.makedirs("uploads")

matches = []
score_filter = 1
headers = {"Content-Type": "application/json"}
message = gr.outputs.HTML("")

def search_by_file(image, endpoint="http://0.0.0.0:12345/search", top_k=1):
    """search_by_file.

    :param endpoint:
    :param top_k:
    :param image: image sent from gradio
    """
    image_file = save_image(image)
    filetype = magic.from_file(image_file, mime=True)
    filename = os.path.abspath(image_file)

    if not check_human(filename):
        image = Image.open("no_human.jpg")
        image_np_array = np.array(image)
        return image_np_array

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


iface = gr.Interface(
    fn=search_by_file,
    inputs=gr.inputs.Image(source="webcam", tool=None),
    outputs="image",
    server_port=7860,
    title="Find your celebrity twin",
    description="Take a selfie to find a celebrity who looks like you!",
    article="This toy uses the publicly available <a href='https://mmlab.ie.cuhk.edu.hk/projects/CelebA.html'>CelebA dataset</a>. Unfortunately this doesn\'t come with names or any other metadata, so if you don\'t recognize your twin then there\'s not much we can do 😅<br><br>Know a better dataset? Ping us on <a href='https://slack.jina/ai'>Slack</a> or <a href='https://twitter.com/alexcg'>drop me a line on Twitter</a>",
    allow_flagging=False,
    theme="huggingface"
)

iface.test_launch()
if __name__ == "__main__":
    iface.launch(share=True)
