from jina import Document, DocumentArray, Executor, Flow, requests
from dynaconf import settings
from sentence_transformers import SentenceTransformer
from app.client import query


class Indexer(Executor):
    metric = settings.JINA.metric

    _docs = DocumentArray()  # for storing all documents in memory

    @requests(on="/index")
    def index(self, docs: DocumentArray, **kwargs):
        self._docs.extend(docs)  # extend stored `docs`

    @requests(on="/search")
    def search(self, docs: DocumentArray, **kwargs):
        docs.match(self._docs, metric=self.metric, is_distance=True)


path = settings.MODEL.path
model = SentenceTransformer(path)


def create_flow(port, protocol, data):
    f = Flow(port_expose=port, protocol=protocol, cors=True).add(uses=Indexer)
    with f:
        f.post(
            "/index",
            (DocumentArray([Document(tags=vec[0], embedding=vec[1]) for vec in data])),
        )
        f.block()


def calculate_embedding(event):
    sentence = event["query"]
    embedding = model.encode([sentence])
    return embedding[0]


def handler(event, context):
    embedding = calculate_embedding(event)
    nearest_sentences = query(embedding)
    # print(nearest_sentences)
    return {"sentences": nearest_sentences}
