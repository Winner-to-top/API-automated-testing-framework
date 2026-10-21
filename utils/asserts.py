import logging

import allure
import jsonpath
from utils.send_request import send_jdbc_request


@allure.step("3.HTTP响应断言")
def http_assert(case, res):
    if case["check"]:
        result = jsonpath.jsonpath(res.json(), case["check"])[0]
        logging.info(f"3.HTTP响应断言内容: 实际结果({result}) == 预期结果({case["expected"]})")
        assert result == case["expected"]
    else:
        logging.info(f"3.HTTP响应断言内容: 预期结果({case["expected"]}) in 实际结果({res.text})")
        assert case["expected"] in res.text


def jdbc_assert(case):
    if case["sql_check"] and case["sql_expected"]:
        with allure.step("3.JDBC响应断言"):
            result = send_jdbc_request(case["sql_check"])
            logging.info(f"3.JDBC响应断言内容: 实际结果({result}) == 预期结果({case["sql_expected"]})")
            assert result == case["sql_expected"]
