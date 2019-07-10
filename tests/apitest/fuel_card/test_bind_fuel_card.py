
import pytest
import requests
import pytest_check as check


@pytest.mark.smoke
@pytest.mark.p0
def test_bind_fuel_card(db, api, data):
    user_name, id_number = data['FREE_USER']
    card_number = data['FREE_CARD']
    # db.reset_card(card_number)

    res = api.bind_fuel_card(user_name, id_number, card_number)

    check.equal(5010, res['code'])
    check.equal('绑定成功', res['msg'])
    check.is_true(res['success'])

    db.reset_card(card_number)


@pytest.mark.p1
def test_bind_fuel_card_binded(db, api, data):
    user_name, id_number = data['FREE_USER']
    card_number = data['BIND_CARD']

    # db.bind_card(card_number, user_name)

    res = api.bind_fuel_card(user_name, id_number, card_number)

    check.equal(5041, res['code'])
    check.equal('卡已经被绑定,无法绑定', res['msg'])
    check.is_false(res['success'])


@pytest.mark.p1
def test_bind_fuel_card_twice(db, api, data):
    user_name, id_number = data['FREE_USER']
    card_numbers = (data['FREE_CARD'], data['FREE_CARD2'])

    db.reset_user(user_name)
    for card_number in card_numbers:
        res = api.bind_fuel_card(user_name, id_number, card_number)

        check.equal(5010, res['code'])
        check.equal('绑定成功', res['msg'])
        check.is_true(res['success'])
    db.reset_user(user_name)


@pytest.mark.p1
def test_bind_fuel_card_3times(db, api, data):
    user_name, id_number = data['USER_WITH_TWO_CARDS']  # 用户已绑定2张卡
    card_number = data['FREE_CARD']

    res = api.bind_fuel_card(user_name, id_number, card_number)

    check.equal(5014, res['code'])
    check.equal('每个用户只能绑定两张卡', res['msg'])
    check.is_false(res['success'])


@pytest.mark.p1
def test_bind_fuel_card_not_exist(db, api, data):
    user_name, id_number = data['FREE_USER']
    card_number = data['CARD_NOT_EXIST']

    db.del_card_if_exist(card_number)
    res = api.bind_fuel_card(user_name, id_number, card_number)

    check.equal(5013, res['code'])
    check.equal('加油卡号不存在', res['msg'])
    check.is_false(res['success'])


@pytest.mark.p4
def test_bind_method_id_not_valid(api, data):
    user_name, id_number = data['FREE_USER']
    card_number = data['FREE_CARD']

    data = {
            "dataSourceId": "bHRz",
            "methodId": "05A",
            "CardUser": {
                "userName": user_name,
                "idType": "1",
                "idNumber": id_number
            },
            "CardInfo": {
                "cardNumber": card_number
            }
        }
    res = api.post(json=data).json()
    check.equal(199, res['code'])
    check.equal('业务ID无效', res['msg'])
    check.is_false(res['success'])


@pytest.mark.p2
def test_bind_fuel_card_in_blacklist(db, api, data):
    user_name, id_number = data['FREE_USER']
    card_number = data['BLACK_CARD']  # 黑名单状态cardstatus=5011

    res = api.bind_fuel_card(user_name, id_number, card_number)

    check.equal(5011, res['code'])
    check.equal('卡号是否黑名单,无法绑定', res['msg'])
    check.is_false(res['success'])


@pytest.mark.p2
def test_bind_fuel_card_cancelled(db, api, data):
    user_name, id_number = data['FREE_USER']
    card_number = data['OFF_CARD']  # 注销状态cardstatus=5012

    res = api.bind_fuel_card(user_name, id_number, card_number)

    check.equal(5012, res['code'])
    check.equal('卡号已经注销,无法绑定', res['msg'])
    check.is_false(res['success'])


@pytest.mark.p2
def test_bind_fuel_card_unit(db, api, data):
    user_name, id_number = data['FREE_USER']
    card_number = data['UNIT_CARD']  # 单位卡状态cardstatus=5021

    res = api.bind_fuel_card(user_name, id_number, card_number)

    check.equal(5021, res['code'])
    check.equal('单位卡不支持,无法绑定', res['msg'])
    check.is_false(res['success'])
