import click
from executors import FacenetEncoder, RemoveBadDocs
from jina import Document, DocumentArray, Flow
from jina.types.document.generators import from_files
from helper import dinger as ding

MAX_DOCS = 4000
from_file = "query.jpg"


flow = (
    Flow()
    .add(uses=FacenetEncoder, name="encoder")
    .add(
        uses=RemoveBadDocs, name="bad_doc_remover"
    )  # Sometimes embeddings are malformed. idk why
    .add(
        uses="jinahub+docker://SimpleIndexer",
        name="indexer",
        uses_with={"index_file_name": "index"},
        uses_metas={"workspace": "workspace"},
        volumes="./workspace:/workspace/workspace",
    )
)


def index(num_docs):
    with flow:
        docs = DocumentArray(
            from_files("./data/**/*.jpg", recursive=True, size=num_docs)
        )
        flow.index(inputs=docs, show_progress=True)
        flow.index(inputs=docs)


def query(filepath=from_file):
    query_doc = Document(uri=filepath)

    with flow:
        response = flow.search(inputs=query_doc, return_results=True)

    matches = response[0].data.docs[0].matches

    for match in matches:
        print(match.uri)


def query_restful():
    with flow:
        flow.port_expose = 12345
        flow.protocol = "http"
        flow.block()


@click.command()
@click.option(
    "--task",
    "-t",
    type=click.Choice(["index", "query", "query_restful"], case_sensitive=False),
)
@click.option("--num_docs", "-n", default=MAX_DOCS)
@click.option("--from_file", "-f", default=from_file)
def main(task, num_docs, from_file):
    if task == "index":
        index(num_docs=num_docs)

    elif task == "query":
        query(from_file)

    elif task == "query_restful":
        query_restful()


if __name__ == "__main__":
    main()
