import os

import pytest

from utils.db import LongTengServer
from utils.data import load_yaml
from utils.path import DATA_DIR
from .api import Api


@pytest.fixture(scope='session')
def db():
    db = LongTengServer()  # 建立数据库连接
    yield db
    # db.conn.rollback()
    db.close()  # 关闭数据库


@pytest.fixture(scope='session')
def api(base_url='http://115.28.108.130:8080'):
    yield Api(base_url)


@pytest.fixture(scope='session')
def data():
    yield load_yaml('data.yaml')


@pytest.fixture(scope='session', autouse=True)
def check_data_source_id(db):
    assert db.check_data_source_id('lts')


@pytest.fixture(scope='session', autouse=True)
def setup_teardown_sql(db):
    setup_sql_file = os.path.join(DATA_DIR, 'setup.sql')
    teardown_sql_file = os.path.join(DATA_DIR, 'teardown.sql')

    db.execute_file(teardown_sql_file)
    db.execute_file(setup_sql_file)
    yield
    # db.execute_file(teardown_sql_file)
