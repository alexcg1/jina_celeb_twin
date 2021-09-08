import click
import pretty_errors
from jina import Flow, DocumentArray
from jina.types.document.generators import from_files
from executors import UriToBlob

NUM_DOCS = 1000
FORMATS = ["jpg", "png", "jpeg"]
DATA_DIR = "data"
WORKSPACE_DIR = "workspace"

flow = (
    Flow()
    .add(uses=UriToBlob, name="celeb_to_blob")  # Embed image in doc, not just filename
    .add(
        uses="jinahub+docker://ImageNormalizer",
        name="celeb_crafter",
        uses_with={"target_size": 96},
    )
    .add(uses="jinahub+docker://CLIPImageEncoder", name="celeb_clip_encoder")
    .add(
        uses="jinahub+docker://SimpleIndexer",
        uses_with={"index_file_name": "index"},
        uses_metas={"workspace": WORKSPACE_DIR},
        name="celeb_indexer",
        volumes=f"./{WORKSPACE_DIR}:/workspace/workspace",
    )
)


def prep_docs(directory, num_docs=NUM_DOCS, formats=FORMATS):
    docs = DocumentArray()
    for format in formats:
        docarray = DocumentArray(
            from_files(f"{directory}/**/*.{format}", size=num_docs)
        )
        docs.extend(docarray)

    return docs[:num_docs]


def index(num_docs=NUM_DOCS):
    docs = prep_docs(DATA_DIR, num_docs)

    with flow:
        flow.index(inputs=docs, show_progress=True)


def query_restful():
    flow.protocol = "http"
    flow.port_expose = 54321

    with flow:
        flow.block()


@click.command()
@click.option(
    "--task",
    "-t",
    type=click.Choice(["index", "query_restful"], case_sensitive=False),
)
@click.option("--num_docs", "-n", default=NUM_DOCS)
def main(task: str, num_docs: int):
    if task == "index":
        index(num_docs=num_docs)
    if task == "query_restful":
        query_restful()


if __name__ == "__main__":
    main()
