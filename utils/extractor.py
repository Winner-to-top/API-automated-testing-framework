import logging
import allure
import jsonpath
from utils.send_request import send_jdbc_request


def json_extractor(case, all, res):
    if case["jsonExData"]:
        with allure.step("4.JSON提取"):
            # 首先要把 jsonExData 的 key, value 拆开
            for key, value in eval(case["jsonExData"]).items():
                value = jsonpath.jsonpath(res.json(), value)[0]
                # print(key)
                # print(value)
                all[key] = value
                # print(all)
            logging.info(f"4.JSON提取, 根据{case["jsonExData"]}提取数据, 此时全局变量为: {all}")


def jdbc_extractor(case, all):
    if case["sqlExData"]:
        with allure.step("4.JDBC提取"):
            for key, value in eval(case["sqlExData"]).items():
                # print(key)
                # print(value)
                value = send_jdbc_request(value)
                # print(value)
                all[key] = value
                # print(all)
            logging.info(f"4.JDBC提取, 根据{case["sqlExData"]}提取数据, 此时全局变量为: {all}")
