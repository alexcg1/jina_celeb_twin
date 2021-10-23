from jina import Executor, Document, DocumentArray, requests
from facenet_pytorch import MTCNN, InceptionResnetV1
from PIL import Image

class FacenetEncoder(Executor):

    @requests
    def get_face_embeddings(self, docs, **kwargs):
        print(kwargs)
        # Create an inception resnet (in eval mode):
        resnet = InceptionResnetV1(pretrained='vggface2').eval()
        # If required, create a face detection pipeline using MTCNN:
        mtcnn = MTCNN(image_size=160, margin=20)

        for doc in docs:
            if hasattr(doc, "uri"):
                img = Image.open(doc.uri)
            elif hasattr(doc, "blob"):
                pass # add later

            # Get cropped and prewhitened image tensor
            img_cropped = mtcnn(img)

            # Calculate embedding (unsqueeze to add batch dimension)
            img_embedding = resnet(img_cropped.unsqueeze(0))

            # ndarray = img_embedding.numpy()
            ndarray = img_embedding.detach().numpy()

            doc.embedding = ndarray

            # Or, if using for VGGFace2 classification
            # resnet.classify = True
            # img_probs = resnet(img_cropped.unsqueeze(0))

            # print(img_probs)
            print(doc.uri)
            print(doc.embedding)
            print(doc.embedding.shape)
