from jina import Client, Document
from jina.types.request import Response
from dynaconf import settings


port = settings.JINA.port
metric = settings.JINA.metric
protocol = settings.JINA.protocol


def query(data, distance=True):
    c = Client(protocol=protocol, port_expose=port)
    value = c.post("/search", Document(embedding=data), return_results=distance)
    return value[0].docs[0].matches
