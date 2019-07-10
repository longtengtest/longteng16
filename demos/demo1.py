import pytest



@pytest.fixture(scope='session')
def setup():
    print('setup')



@pytest.fixture(scope='session')
def teardown():
    print('teardown')

@pytest.fixture(scope='session', autouse=True)
def setup_teardown(setup, teardown):
    yield
    teardown()


def test_1():
    print('test_1')
