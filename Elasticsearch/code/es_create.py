"""passed test in Python 3.7
"""

from config import ES_INDEX_NAME, ES_INDEX_DOC_TYPE, es

def create_mapping():
    index_info = {
        'settings':{
            'number_of_replicas': 1,
            'number_of_shards': 5
        },
        'mappings':{
            ES_INDEX_DOC_TYPE:{
                'properties':{
                    "url":{
                        'type': 'string',
                        'index': 'not_analyzed'
                    },
                    "title":{
                        'type': 'string',
                        'index': 'analyzed'
                    },
                    "content":{
                        'type': 'string',
                        'index': 'analyzed'
                    },
                    "date":{
                        'type': 'string',
                        'index': 'not_analyzed'
                    }
                }
            }
        }
    }

    exist_indice = es.indices.exists(index=ES_INDEX_NAME)
    if not exist_indice:
        es.indices.create(index=ES_INDEX_NAME, body=index_info, ignore=400)


if __name__=='__main__':
    create_mapping()
