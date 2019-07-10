import pytest
from utils.page import Page

# @pytest.fixture
# def chrome_options(chrome_options):
#     chrome_options.binary_location = '/path/to/chrome'
#     chrome_options.add_extension('/path/to/extension.crx')
#     chrome_options.add_argument('--kiosk')
#     return chrome_options
#
#
# @pytest.fixture
# def selenium(selenium):
#     selenium.implicitly_wait(10)
#     selenium.maximize_window()
#     return selenium


@pytest.fixture
def login_page(selenium):
    selenium.get('http://39.104.14.232/ecshop/wwwroot/admin/privilege.php?act=login')
    yield Page(selenium, 'login_page.yaml')
