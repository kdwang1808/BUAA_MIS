"""passed test in Python 3.7
"""

import json
import time
from config import es, ES_INDEX_NAME, ES_INDEX_DOC_TYPE


def query_by_keyword():
    query_body = {
        "query":{
            "match": { "title": "中国"} # 新闻标题中包含中国关键词
        },
        "size": 10000
    }

    tb = time.time()
    results = es.search(index=ES_INDEX_NAME, doc_type=ES_INDEX_DOC_TYPE, body=query_body)["hits"]["hits"]

    ff = open("search_results.txt", "w", encoding="UTF-8")
    for item in results:
        data = item["_source"]
        ff.write("%s|.|%s|.|%s|.|%s\n" % (data["url"], data["date"], data["title"], data["content"]))
    ff.close()
    tb1 = time.time()
    print ("ES search data time (seconds): ", tb1 - tb)


if __name__ == "__main__":
    query_by_keyword()

