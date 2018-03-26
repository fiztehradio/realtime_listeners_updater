import sys
import pymysql
import requests
from time import time, sleep

time_sleep_in_seconds = 60


def get_website_listeners():
    try:
        data = requests.get("http://radio.mipt.ru:8410/status-json.xsl").json()
        return data["icestats"]["source"]["listeners"]
    except:
        return 0


def connect_db():
    connection = pymysql.connect(host='radio.mipt.ru',
                                 user=sys.argv[1],
                                 password=sys.argv[2],
                                 db='radio',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection


if len(sys.argv) < 3:
    print("please give user and password")
    exit()

connection = connect_db()

while True:
    try:
        with connection.cursor() as cursor:
            data_to_send = (get_website_listeners())
            sql = "INSERT INTO website_listeners (listeners) VALUES (%s);"
            cursor.execute(sql, data_to_send)
        connection.commit()

        sleep(time_sleep_in_seconds)
    except:
        connection.close()
        connection = connect_db()
