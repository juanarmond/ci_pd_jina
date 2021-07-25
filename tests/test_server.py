import numpy as np
import numpy.testing as npt
from dynaconf import settings
from jina import Document, DocumentArray, Flow
from app import handler
from app.server import Indexer, calculate_embedding, model


def test_calculate_embedding():
    value = calculate_embedding({"query": "test"})
    test_values = np.array([-0.06, 0.23, -0.05])
    npt.assert_almost_equal(value[:3], test_values, decimal=2)


def test_handler():
    port = settings.JINA.port
    protocol = settings.JINA.protocol

    # data = np.array([[0.1, 0.2, 0.3], [0.3, 0.2, 0.1], [0.1, 0.1, 0.1]])

    data = np.array(
        [
            [{"sentence": "a"}, model.encode(["a"])[0]],
            [{"sentence": "b"}, model.encode(["a"])[0]],
            [{"sentence": "c"}, model.encode(["a"])[0]],
        ],
        dtype=object,
    )

    f = Flow(port_expose=port, protocol=protocol, cors=True).add(uses=Indexer)
    with f:
        f.post(
            "/index",
            (DocumentArray([Document(tags=vec[0], embedding=vec[1]) for vec in data])),
        )
        values = handler({"query": "a"}, "")
        value = {
            "sentences": [
                {"sentence": sentence.tags["sentence"]}
                for sentence in values["sentences"]
            ]
        }
        assert value == {
            "sentences": [{"sentence": "a"}, {"sentence": "b"}, {"sentence": "c"}]
        }
