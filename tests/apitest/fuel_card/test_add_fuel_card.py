import pytest
import requests
import pytest_check as check
from utils.data import load_yaml


@pytest.mark.smoke
@pytest.mark.p0
@pytest.mark.bug
@pytest.mark.parametrize('card_number', load_yaml('data.yaml')['FREE_CARD_NUMBERS'])
def test_add_fuel_card(card_number, db, api):
    db.del_card_if_exist(card_number)  # 环境准备

    res = api.add_fuel_card(card_number)

    check.equal(200, res['code'], "响应code不为200")
    check.equal('添加卡成功', res['msg'], "响应msg非'添加卡成功'")
    check.is_false(res['success'], '响应success不为false')  # bug
    check.is_true(db.check_card(card_number), f'数据库查询卡号{card_number}不存在')  # 数据库断言

    db.del_card_if_exist(card_number)  # 环境清理


@pytest.mark.p1
def test_add_fuel_card_exist(db, api, data):
    card_number = data['FREE_CARD_NUMBERS'][0]
    db.add_card_if_not_exist(card_number)

    res = api.add_fuel_card(card_number)

    check.equal(5000,res['code'])
    check.equal('该卡已添加', res['msg'])
    check.is_false(res['success'])  # bug


@pytest.mark.p4
def test_add_fuel_card_twice(db, api, data):
    card_numbers = data['FREE_CARD_NUMBERS'][:2]
    [db.del_card_if_exist(card_number) for card_number in card_numbers]
    for card_number in card_numbers:
        res = api.add_fuel_card(card_number)

        check.equal(200, res['code'], "响应code不为200")
        check.equal('添加卡成功', res['msg'], "响应msg非'添加卡成功'")
        check.is_false(res['success'], '响应success不为false')   # bug
        check.is_true(db.check_card(card_number), f'数据库查询卡号{card_number}不存在')  # 数据库断言

    [db.del_card_if_exist(card_number) for card_number in card_numbers]


@pytest.mark.p4
def test_add_fuel_card_3times(db, api, data):
    card_numbers = data['FREE_CARD_NUMBERS'][:3]
    [db.del_card_if_exist(card_number) for card_number in card_numbers]
    for card_number in card_numbers:
        res = api.add_fuel_card(card_number)

        check.equal(200, res['code'], "响应code不为200")
        check.equal('添加卡成功', res['msg'], "响应msg非'添加卡成功'")
        check.is_false(res['success'], '响应success不为false')
        check.is_true(db.check_card(card_number), f'数据库查询卡号{card_number}不存在')  # 数据库断言

    [db.del_card_if_exist(card_number) for card_number in card_numbers]


@pytest.mark.negetive
@pytest.mark.p4
def test_add_fuel_card_wrong_request_format(api, data):
    card_number = data['FREE_CARD_NUMBERS'][0]
    data = {"dataSourceId": "bHRz", "methodId": "00A", "CardInfo": {"cardNumber": card_number}}
    res = api.post(data=data).json()
    check.equal(301, res['code'])
    check.is_in('参数类型错误', res['msg'])


@pytest.mark.negetive
@pytest.mark.p4
def test_add_fuel_card_data_source_id_blank(api, data):
    card_number = data['FREE_CARD_NUMBERS'][0]
    data = {"dataSourceId": "", "methodId": "00A", "CardInfo": {"cardNumber": card_number}}
    res = api.post(json=data).json()

    check.equal(301, res['code'])
    check.is_in('第三方平台ID不能为空', res['msg'])


@pytest.mark.negetive
@pytest.mark.p4
def test_add_fuel_card_method_id_blank(api, data):
    card_number = data['FREE_CARD_NUMBERS'][0]
    data = {"dataSourceId": "bHRz", "methodId": "", "CardInfo": {"cardNumber": card_number}}
    res = api.post(json=data).json()

    check.equal(301, res['code'])
    check.is_in('业务ID不能为空', res['msg'])


@pytest.mark.xfail(reason='已知Bug: cardNumber为None时报500报错')
@pytest.mark.bug
@pytest.mark.negetive
@pytest.mark.p4
def test_add_fuel_card_card_number_none(api):
    card_number = None
    data = {"dataSourceId": "bHRz", "methodId": "00A", "CardInfo": {"cardNumber": card_number}}
    res = api.post(json=data)
    check.equal(200, res.status_code)


if __name__ == '__main__':
    pytest.main(['test_add_fuel_card.py::', '-s'])
