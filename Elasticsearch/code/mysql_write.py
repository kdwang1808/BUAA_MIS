"""passed test in Python 3.7
"""

import time
import pymysql.cursors

from config import MYSQL_HOST, MYSQL_USERNAME, MYSQL_PASSWORD, MYSQL_DB, MYSQL_TABLE


# read data from txt
data_list = []
with open("news.txt", "r", encoding='UTF-8') as f:
    for line in f:
        url, date, title, content = line.strip().split("|.|")
        data_list.append((url, url, title, content, date))

# Connect to the database
connection = pymysql.connect(host=MYSQL_HOST,
                             user=MYSQL_USERNAME,
                             password=MYSQL_PASSWORD,
                             db=MYSQL_DB,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

# write data
count = 0
tb = time.time()
with connection.cursor() as cursor:
    for data in data_list:
        # Create a new record
        sql = "INSERT INTO `" + MYSQL_TABLE + "` (`id`, `url`, `title`, `content`, `datestr`) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, data)
        
        # connection is not autocommit by default. So you must commit to save your changes.
        connection.commit()
        count += 1

print ("MySQL writing %s items need %s seconds" % (count, time.time() - tb))
