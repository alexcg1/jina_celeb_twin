from jina import Executor, Document, DocumentArray, requests
from facenet_pytorch import MTCNN, InceptionResnetV1
from PIL import Image
import numpy as np


class FacenetEncoder(Executor):
    @requests
    def get_face_embeddings(self, docs, **kwargs):
        print(kwargs)
        resnet = InceptionResnetV1(
            pretrained="vggface2"
        ).eval()  # Create an inception resnet (in eval mode):
        mtcnn = MTCNN(
            image_size=160, margin=20
        )  # If required, create a face detection pipeline using MTCNN:
        bad_docs = []  # Sometimes doc embedding has issues

        for idx, doc in enumerate(docs):
            # if hasattr(doc, "uri"):
            # elif hasattr(doc, "blob"):
            # pass # add later

            try:
                img = Image.open(doc.uri)
                img_cropped = mtcnn(img)  # Crop to face
                img_embedding = resnet(
                    img_cropped.unsqueeze(0)
                )  # Calculate embedding (unsqueeze to add batch dimension)
                ndarray = img_embedding.detach().numpy()
                doc.embedding = ndarray.squeeze()  # Squeeze to 1d array
            except:
                bad_docs.append(idx)
            # print("---")
            # print(doc.uri)
            # print(type(doc.embedding))
            # print(doc.embedding.shape)
                # print(f"{doc.uri} failed")
                # print(doc.uri)
                # import sys
                # sys.exit()
            # assert doc.embedding.shape == (512,)

        for idx in bad_docs:
            print(f"=== Encoder: Removing {docs[idx].uri}")
            del docs[idx]

# class DocPrinter(Executor):
    # @requests
    # def print_doc(self, docs, **kwargs):
        # for doc in docs:
            # print(doc.uri)
            # print(doc.embedding)


class RemoveBadDocs(Executor):
    @requests(on="/index")
    def remove_bad_docs(self, docs, **kwargs):
        bad_docs = []  # Bads docs == docs with no embedding
        for idx, doc in enumerate(docs):
            # print(f"Checking {doc.uri}")
            try:
                assert type(doc.embedding) is not None
                assert isinstance(doc.embedding, np.ndarray)
                assert doc.embedding.shape == (512,)
            except:
                print(f"=== Killer: Removing {doc.uri}")
                bad_docs.append(idx)
            # if not hasattr(doc, "embedding"):
                # bad_docs.append(idx)
                # print(f"=== {doc.uri} has no embedding")
            # else:
                # if doc.embedding.shape != (512,):
                    # bad_docs.append(idx)
                    # print(f"{doc.uri} had malformed embedding")

        bad_docs.reverse()
        for idx in bad_docs:
            del docs[idx]
