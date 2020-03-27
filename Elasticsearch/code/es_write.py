"""passed test in Python 3.7
"""

import time
from datetime import datetime

from config import es, ES_INDEX_NAME, ES_INDEX_DOC_TYPE


def write_data(d):
    data = dict()
    data["url"] = d[0]
    data["title"] = d[1]
    data["content"] = d[2]
    data["date"] = d[3]

    es.index(index=ES_INDEX_NAME, doc_type=ES_INDEX_DOC_TYPE, id=data["url"], body=data)


if __name__ == "__main__":
    data_list = []
    with open("news.txt", "r", encoding='UTF-8') as f:
        for line in f:
            url, date, title, content = line.strip().split("|.|")
            data_list.append([url, title, content, date])

    count = 0
    tb = time.time()
    for data in data_list:
        write_data(data)

        count += 1
        
    print ("ES writing %s items need %s seconds" % (count, time.time() - tb))