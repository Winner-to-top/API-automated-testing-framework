# 电商后台管理系统 API 自动化测试框架

基于 **Python + pytest + requests + Allure** 搭建的接口自动化测试框架，采用 **Excel 数据驱动** 的方式管理测试用例，支持 HTTP 接口断言、数据库断言、JSON/数据库数据提取与跨用例参数传递。

框架以电商后台管理系统（`/api/private/v1`）为被测对象，覆盖登录、用户、角色、权限、商品分类、分类参数、商品、图片上传、订单、数据统计等核心业务模块。

---

## ✨ 特性

- **数据驱动**：测试用例集中在 Excel 中维护，新增/修改用例无需改动代码
- **模板变量**：使用 Jinja2 语法 `{{变量名}}` 在用例间传递 token、ID 等动态数据
- **多维度断言**：支持 JSONPath 响应断言、响应文本包含断言、MySQL 数据库断言
- **双通道提取**：支持从 HTTP 响应（JSONPath）和数据库查询结果中提取变量
- **Allure 报告**：自动生成可视化测试报告，按 Feature / Story 分层展示，步骤与请求数据可追溯
- **环境清理**：会话结束后自动删除测试过程中产生的脏数据

---

## 🛠 技术栈

| 组件 | 版本 | 用途 |
| --- | --- | --- |
| Python | 3.8+ | 运行环境（代码使用 f-string 嵌套引号，推荐 3.12+） |
| pytest | 8.3.2 | 测试框架与用例调度 |
| requests | 2.32.3 | HTTP 接口请求 |
| PyMySQL | 1.1.1 | MySQL 数据库断言与数据提取 |
| jsonpath | 0.82.2 | JSON 响应数据提取 |
| openpyxl | 3.1.5 | Excel 测试用例读取 |
| allure-pytest | 2.13.5 | Allure 测试报告集成 |
| Jinja2 | 3.1.4 | 用例模板变量渲染 |

---

## 📁 目录结构

```text
jkzdh5.20/
├── config/
│   └── config.py            # 环境地址、Excel 配置、数据库配置、清理 SQL
├── data/
│   ├── 测试用例.xlsx         # 示例用例（部分）
│   └── 测试用例完整版.xlsx    # 完整用例（38 条启用用例）
├── file/
│   └── 1.jpg                # 图片上传接口使用的测试文件
├── testcases/
│   └── test_runner.py       # 统一测试执行入口（数据驱动核心）
├── utils/
│   ├── allure_utils.py      # Allure 报告初始化（feature/story/title）
│   ├── analyse_case.py      # 解析用例中的请求参数
│   ├── asserts.py           # HTTP 断言与数据库断言
│   ├── excel_utils.py       # Excel 用例读取
│   ├── extractor.py         # JSON / 数据库变量提取
│   └── send_request.py      # HTTP 请求与 JDBC 查询封装
├── conftest.py              # 会话级 fixture：测试后清理数据库数据
├── pytest.ini               # pytest 日志配置
├── requirements.txt         # 依赖清单
├── run.py                   # 一键执行并生成 Allure 报告
└── README.md
```

---

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

> 生成 HTML 报告还需要安装 [Allure 命令行工具](https://allurereport.org/docs/install/)，并配置环境变量。

### 2. 修改配置

编辑 `config/config.py`，按实际环境修改：

```python
# 被测服务地址
BASE_URL = "http://127.0.0.1:8888/api/private/v1"

# 测试用例文件与工作表
EXCEL_FILE = "./data/测试用例完整版.xlsx"
SHEET_NAME = "Sheet1"

# MySQL 连接配置（用于数据库断言/提取与数据清理）
DB_HOST = "127.0.0.1"
DB_PORT = 3306
DB_NAME = "mydb"
DB_USER = "root"
DB_PASSWORD = "123456"
```

### 3. 准备被测环境

- 启动被测的电商后台管理系统服务，确保 `BASE_URL` 可访问
- 初始化数据库并按需准备基础数据（管理员账号 `admin / 123456`、分类、订单等）
- 数据库需存在 `sp_manager`、`sp_category`、`sp_attribute`、`sp_goods` 等表（用于断言、提取及清理）

### 4. 执行测试

方式一：一键执行并生成报告（推荐）

```bash
python run.py
```

方式二：直接使用 pytest

```bash
pytest ./testcases/test_runner.py -vs
```

指定用例、生成 Allure 原始数据：

```bash
pytest ./testcases/test_runner.py -vs --alluredir=./report/json_report --clean-alluredir
allure generate ./report/json_report -o ./report/html_report --clean
allure open ./report/html_report
```

运行日志默认输出到 `./log/test.log`，同时在控制台实时打印。

---

## 🔄 执行流程

```mermaid
flowchart LR
    A[读取 Excel 用例] --> B[过滤 is_true 为 True 的用例]
    B --> C[Jinja2 渲染 {{变量}}]
    C --> D[Allure 初始化 feature/story/title]
    D --> E[解析请求参数]
    E --> F[发送 HTTP 请求]
    F --> G[HTTP / 数据库断言]
    G --> H[JSON / 数据库提取变量]
    H --> I[写入全局变量池, 供后续用例使用]
    I --> C
```

单个用例的核心执行逻辑位于 `testcases/test_runner.py`：

1. **渲染用例**：用此前提取的全局变量渲染 `{{TOKEN}}`、`{{USER_ID}}` 等占位符
2. **初始化报告**：写入 Allure 的 feature / story / title
3. **解析请求**：拼接 `BASE_URL + path`，反序列化 headers / params / data / json / files
4. **发送请求**：通过 `requests.request` 发起 HTTP 调用
5. **执行断言**：JSONPath 断言或文本包含断言 + 可选的数据库断言
6. **提取变量**：将响应或数据库中的值存入全局字典，供后续用例引用

---

## 📊 Excel 测试用例说明

用例文件采用 **两行表头**：

- **第 1 行**：中文字段说明
- **第 2 行**：程序读取使用的英文字段名
- **第 3 行起**：测试数据

### 字段定义

| 字段 | 中文含义 | 说明 |
| --- | --- | --- |
| `id` | 用例编号 | 唯一标识，报告中展示 |
| `feature` | 模块 | Allure Feature，如「用户管理」 |
| `story` | 场景 | Allure Story，如「新增成功」 |
| `title` | 用例标题 | Allure 报告标题 |
| `method` | 请求方式 | `get` / `post` / `put` / `delete` |
| `path` | 接口路径 | 与 `BASE_URL` 拼接，可含模板变量 |
| `headers` | 请求头 | Python 字典字符串，如 `{"Authorization": "{{TOKEN}}"}` |
| `params` | URL 参数 | Python 字典字符串 |
| `data` | 表单参数 | Python 字典字符串 |
| `json` | JSON 参数 | Python 字典字符串 |
| `files` | 文件参数 | Python 元组字符串，如 `{"file": ("1.jpg", open("./file/1.jpg", "rb"), "jpg")}` |
| `check` | 响应断言表达式 | JSONPath 表达式，如 `$..msg`；为空时改为文本包含断言 |
| `expected` | 预期结果 | 与 `check` 提取值比较；`check` 为空时判断是否包含在响应文本中 |
| `sql_check` | 数据库断言 SQL | 查询结果与 `sql_expected` 比较 |
| `sql_expected` | 数据库预期结果 | 数据库断言预期值 |
| `jsonExData` | JSON 提取 | Python 字典字符串，`{"变量名": "JSONPath"}` |
| `sqlExData` | 数据库提取 | Python 字典字符串，`{"变量名": "SQL 语句"}` |
| `is_true` | 是否执行 | `TRUE` 时执行，空值或 `FALSE` 时跳过 |

### 变量传递示例

```text
用例 100（登录）      jsonExData: {"TOKEN": "$..token"}
        ↓ 提取 token 写入全局变量池
用例 101（查询用户）  headers: {"Authorization": "{{TOKEN}}"}
        ↓ 新增用户后提取 ID
用例 102（新增用户）  jsonExData: {"JAY_ID": "$..id"}
        ↓
用例 103（修改状态）  path: /users/{{JAY_ID}}/state/true
```

### 新增用例

1. 在 Excel 第 3 行之后追加一行，填写第 2 行对应的英文字段
2. 需要被后续用例引用的数据，在 `jsonExData` 或 `sqlExData` 中定义变量名
3. 将 `is_true` 设为 `TRUE`
4. 无需修改任何代码，重新执行即可

---

## ✅ 断言与提取能力

### 断言

- **JSONPath 断言**（`check` 非空）

  ```python
  jsonpath.jsonpath(res.json(), "$..msg")[0] == expected
  ```

- **文本包含断言**（`check` 为空）

  ```python
  expected in res.text
  ```

- **数据库断言**（`sql_check` 与 `sql_expected` 均非空）

  ```python
  send_jdbc_request(sql_check) == sql_expected
  ```

### 提取

- **JSON 提取**：`{"TOKEN": "$..token"}`
- **数据库提取**：`{"ADMIN_NAME": "select mg_name from sp_manager where mg_name = 'admin'"}`

所有提取结果统一写入 `TestRunner.all` 全局字典，并由 Jinja2 在后续用例渲染时替换。

---

## 🧹 测试数据清理

`conftest.py` 定义了会话级、自动执行的 `destroy_data` fixture：全部用例执行完成后，连接数据库并依次执行 `config.py` 中的 `SQL1`、`SQL2`、`SQL3`，删除测试过程中创建的分类、参数与商品数据。

```python
SQL1 = 'delete from sp_category where cat_name = "大码服装"'
SQL2 = 'delete from sp_attribute where attr_name = "VIP尺码"'
SQL3 = 'delete from sp_goods where goods_name = "大码牛仔裤+"'
```

如新增用例会产生持久化数据，请同步补充对应的清理 SQL。

---

## 📈 测试报告

执行 `python run.py` 后生成：

| 路径 | 内容 |
| --- | --- |
| `report/json_report/` | Allure 原始结果数据 |
| `report/html_report/` | Allure HTML 报告 |

报告按 **Feature（模块）→ Story（场景）→ Title（用例）** 分层展示，每个用例包含：

- 解析后的请求数据（Allure 附件）
- HTTP 请求 / 断言 / 提取等步骤
- 失败时的断言差异信息

---

## 📝 注意事项

1. **配置需按环境修改**：`config/config.py` 中的服务地址与数据库账号密码为本地示例值，请勿直接用于生产环境。
2. **Python 版本**：代码大量使用 f-string 内嵌同类引号，建议使用 **Python 3.12+**；低版本可能触发语法错误。
3. **`eval` 的使用**：用例中的 headers / params / data / json / files 及提取配置通过 `eval` 反序列化，仅适用于可信的本地测试数据，请勿加载来源不明的用例文件。
4. **用例执行顺序**：存在依赖关系的用例（登录 → 提取 Token → 后续操作）依赖 Excel 行顺序与 `pytest` 收集顺序，请勿随意打乱。
5. **数据库依赖**：数据库断言、数据库提取及数据清理均需要可访问的 MySQL 服务，否则相关用例会失败。
6. **文件上传路径**：`files` 字段中的相对路径以项目根目录为基准（`./file/1.jpg`），请从根目录执行测试。

---

## 📄 License

本项目仅用于学习与接口自动化测试实践。
