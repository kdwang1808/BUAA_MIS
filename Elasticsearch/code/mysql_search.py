"""passed test in Python 3.7
"""

import time
import pymysql.cursors

from config import MYSQL_HOST, MYSQL_USERNAME, MYSQL_PASSWORD, MYSQL_DB, MYSQL_TABLE


# Connect to the database
connection = pymysql.connect(host=MYSQL_HOST,
                             user=MYSQL_USERNAME,
                             password=MYSQL_PASSWORD,
                             db=MYSQL_DB,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

tb = time.time()

with connection.cursor() as cursor:
    # Read a single record
    sql = "SELECT * FROM `" + MYSQL_TABLE + "` WHERE `title` like %s"
    cursor.execute(sql, ("%中国%",))
    result = cursor.fetchall()

    ff = open("search_results.txt", "w", encoding="UTF-8")
    for r in result:
        ff.write("%s|.|%s|.|%s|.|%s\n" % (r["url"], r["datestr"], r["title"], r["content"]))
    ff.close()
tb1 = time.time()
print ("MySQL search data time (seconds): ", tb1 - tb)