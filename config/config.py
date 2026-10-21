# 环境基准地址
BASE_URL = "http://127.0.0.1:8888/api/private/v1"

# excel格式的测试用例文件配置
EXCEL_FILE = "./data/测试用例完整版.xlsx"
SHEET_NAME = "Sheet1"

# mysql配置
DB_HOST = "127.0.0.1"
DB_PORT = 3306
DB_NAME = "mydb"
DB_USER = "root"
DB_PASSWORD = "123456"

# mysql资源销毁
SQL1 = 'delete from sp_category where cat_name = "大码服装"'
SQL2 = 'delete from sp_attribute where attr_name = "VIP尺码"'
SQL3 = 'delete from sp_goods where goods_name = "大码牛仔裤+"'

