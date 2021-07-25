import numpy as np
from dynaconf import settings
from jina import Document, DocumentArray, Flow
from app.client import query
from app.server import Indexer
from skhubness.neighbors import HNSW
from pytest import approx


metric = settings.JINA.metric


def get_jina_results(data_sentence, query_vector):
    port = settings.JINA.port
    protocol = settings.JINA.protocol

    f = Flow(port_expose=port, protocol=protocol, cors=True).add(uses=Indexer)
    with f:
        f.post(
            "/index",
            (
                DocumentArray(
                    [Document(tags=vec[0], embedding=vec[1]) for vec in data_sentence]
                )
            ),
        )
        values = query(query_vector)
        result = [{f'{d.tags["sentence"]}': 1 - d.scores[metric].value} for d in values]
        values = [1 - d.scores[metric].value for d in values]
        return values


def get_hnsw_results(
    data_sentence, data, query_vector, n_candidates, return_distance=False
):
    hnsw = HNSW(
        n_candidates=n_candidates,
        metric=metric,
        method="hnsw",
        post_processing=2,
        n_jobs=1,
        verbose=0,
    )
    hnsw.fit(X=data)
    values = hnsw.kneighbors(X=np.array(query_vector), return_distance=return_distance)
    if return_distance:
        return values[0][0]
    hnsw_values = [data_sentence[i][0]["sentence"] for i in values[0]]
    return hnsw_values


data_sentence = np.array(
    [
        [{"sentence": "a"}, np.array([0.1, 0.2, 0.3])],
        [{"sentence": "b"}, np.array([0.3, 0.2, 0.1])],
        [{"sentence": "c"}, np.array([0.1, 0.1, 0.1])],
    ]
,dtype=object)

data = np.array([[0.1, 0.2, 0.3], [0.3, 0.2, 0.1], [0.1, 0.1, 0.1]])
query_vector = np.array([[0.1, 0.2, 0.3]])


def test_certainty():
    jina_results = get_jina_results(data_sentence, query_vector[0])
    hnsw_results = get_hnsw_results(data_sentence, data, query_vector, 3, True)
    assert approx(jina_results) == hnsw_results
