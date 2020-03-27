"""passed test in Python 3.7
"""

from elasticsearch import Elasticsearch

# ES config
ES_HOST = 'localhost'
ES_PORT = 9200
ES_TIME_OUT = 600
ES_INDEX_NAME = "test"
ES_INDEX_DOC_TYPE = "news"

es = Elasticsearch("%s:%s" % (ES_HOST, ES_PORT), timeout=ES_TIME_OUT)

# MySQL config
MYSQL_USERNAME = "root"
MYSQL_PASSWORD = "zgdbsfdxfszx"  # 需要改成安装MySQL时设置的root用户的密码
MYSQL_HOST = "localhost"
MYSQL_DB = "test"
MYSQL_TABLE = "news"
