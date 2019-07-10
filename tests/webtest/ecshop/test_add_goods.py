import pytest


def test_login(login_page):
    login_page.username_ipt.send_keys('admin')
    login_page.password_ipt.send_keys('123456')
    login_page.login_btn.click()
