from elasticsearch import Elasticsearch

from sheerlike.query import QueryHit


class IndexHelper(object):
    # See "The borg singleton" in "Learning Python Design Patterns"
    _shared_state = {}

    def __new__(cls, *args, **kwargs):
        obj = super(IndexHelper, cls).__new__(cls, *args, **kwargs)
        obj.__dict__ = cls._shared_state
        return obj

    def configure(self, config):
        self.es = Elasticsearch(config["elasticsearch"])
        self.index_name = config['index']

    def get_document(self, doctype, docid):
        raw_results = self.es.get(index=self.index_name,
                                  doc_type=doctype, id=docid)
        return QueryHit(raw_results, es=self.es, es_index=self.index_name)


def process_string_fields(field, callback):
    """Apply a callback function to all strings in a data structure."""
    if isinstance(field, basestring):
        field = callback(field)
    elif isinstance(field, list):
        field = [
            process_string_fields(item, callback=callback)
            for item in field
        ]
    elif isinstance(field, dict):
        field = {
            key: process_string_fields(value, callback=callback)
            for key, value in field.iteritems()
        }

    return field
