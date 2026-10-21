import logging

import allure
import pymysql
import requests
from config.config import *


@allure.step("2.发送HTTP请求")
def send_http_request(**request_data):
    res = requests.request(**request_data)
    logging.info(f"2.发送HTTP请求, 响应文本为: {res.text}")
    return res


def send_jdbc_request(sql, index=0):
    conn = pymysql.Connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        charset="utf8"
    )
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result[index]
