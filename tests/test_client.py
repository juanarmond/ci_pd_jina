import numpy as np
from dynaconf import settings
from jina import Document, DocumentArray, Flow
from app.client import query
from app.server import Indexer


def test_client():
    port = settings.JINA.port
    protocol = settings.JINA.protocol

    data = np.array(
        [
            [{"sentence": "a"}, np.array([0.1, 0.2, 0.3])],
            [{"sentence": "b"}, np.array([0.3, 0.2, 0.1])],
            [{"sentence": "c"}, np.array([0.1, 0.1, 0.1])],
        ]
    ,dtype=object)

    f = Flow(port_expose=port, protocol=protocol, cors=True).add(uses=Indexer)
    with f:
        f.post(
            "/index",
            (DocumentArray([Document(tags=vec[0], embedding=vec[1]) for vec in data])),
        )
        query_vector = np.array([0.1, 0.2, 0.3])
        values = query(query_vector)
        values = [f'{sentence.tags["sentence"]}' for sentence in values]
        test_values = ["a", "c", "b"]
        assert values == test_values
