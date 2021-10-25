import click
from executors import FacenetEncoder, RemoveBadDocs
from jina import Document, DocumentArray, Flow
from jina.types.document.generators import from_files
from helper import dinger as ding

MAX_DOCS = 4000


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


def query():
    query_doc = Document(uri="data.old/idris.jpg")

    with flow:
        response = flow.search(inputs=query_doc, return_results=True)

    matches = response[0].data.docs[0].matches

    for match in matches:
        print(match.uri)


@click.command()
@click.option(
    "--task",
    "-t",
    type=click.Choice(["index", "query_restful"], case_sensitive=False),
)
@click.option("--num_docs", "-n", default=MAX_DOCS)
def main(task, num_docs):
    if task == "index":
        index(num_docs=num_docs)

    if task == "query":
        query()


if __name__ == "__main__":
    main()
