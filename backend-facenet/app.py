from executor import FacenetEncoder
from jina import Document, DocumentArray, Flow

docs = DocumentArray(
    [
        Document(uri="data/alex.jpg"),
        Document(uri="data/idris.jpg"),
        Document(uri="data/han.jpg"),
    ]
)

flow = (
    Flow()
    .add(uses=FacenetEncoder, name="encoder")
    .add(
        uses="jinahub+docker://SimpleIndexer/old",
        name="indexer",
        uses_with={"index_file_name": "index"},
        uses_metas={"workspace": "workspace"},
        volumes="./workspace:/workspace/workspace",
    )
)

with flow:
    flow.index(inputs=docs)

query_doc = Document(uri="data/cristian.jpg")

with flow:
    response = flow.search(inputs=query_doc, return_results=True)

print(response)
