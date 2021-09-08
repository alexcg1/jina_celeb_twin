import requests
import uuid
from PIL import Image
import face_recognition

def check_human(image_uri):
    image = face_recognition.load_image_file(image_uri)
    face_locations = face_recognition.face_locations(image)
    print(face_locations)
    return face_locations

def save_image(image, output_filename=None):
    if not output_filename:
        output_filename = f"uploads/{str(uuid.uuid4())}.jpg"
    im = Image.fromarray(image)
    im.save(output_filename)

    return output_filename


def search_by_file(endpoint, top_k, filename="query.png"):
    """search_by_file.

    :param endpoint:
    :param top_k:
    :param filename:
    """
    filetype = magic.from_file(filename, mime=True)
    filename = os.path.abspath(filename)

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
    matches = content["data"]["docs"][0]["matches"]

    return matches
