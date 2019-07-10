import os

# __file__: 当前文件
# os.path.dirname(): 所在目录
# os.path.abspath(): 当前文件/目录的绝对路径
# os.path.join(): 路径连接

# 项目路径
BASEDIR = os.path.abspath(
    os.path.dirname(
        os.path.dirname(
            __file__)))

# 数据文件目录
DATA_DIR = os.path.join(BASEDIR, "data")
SNAPSHOT_DIR = os.path.join(BASEDIR, "reports")
WEB_PAGES_DIR = os.path.join(BASEDIR, "tests", "webtest", "ecshop", "pages")

