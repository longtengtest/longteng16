import pytest
import pytest_check as check


def test_consume_fuel_card(db, api, data):
    user_name = data['USER_WITH_TWO_CARDS'][0]
    user_id = db.get_user_id(user_name)
    card_number = data['USED_CARD']
    print(f'card_number:{card_number}')
    print(db.execute(f'select cardBalance from cardinfo where cardNumber="{card_number}"'))
    balance = data['AMOUNT']
    print(f'消费:{balance}')
    res = api.consume_fuel_card(user_id, card_number, balance)

    check.equal(200, res['code'])
    check.equal('消费成功!', res['msg'])
    check.is_true(res['success'])


def test_consume_fuel_card_balance_not_enough(db, api, data):
    user_name = data['USER_WITH_TWO_CARDS'][0]
    user_id = db.get_user_id(user_name)
    card_number = data['USED_CARD']
    balance = data['VERY_LARGE_AMOUNT']
    res = api.consume_fuel_card(user_id, card_number, balance)

    check.equal(200, res['code'])
    check.equal('对不起，您的余额不足，请充值!', res['msg'])
    check.is_false(res['success'])


@pytest.mark.xfail(reason='已知bug: 消费金额为负数可以充值成功')
@pytest.mark.bug
def test_consume_fuel_card_balance_negative(db, api, data):
    user_name = data['USER_WITH_TWO_CARDS'][0]
    user_id = db.get_user_id(user_name)
    card_number = data['USED_CARD']
    balance = -int(data['AMOUNT'])
    res = api.consume_fuel_card(user_id, card_number, balance)

    check.not_equal(200, res['code'])
    check.not_equal('消费成功!', res['msg'])
    check.is_false(res['success'])


@pytest.mark.xfail(reason='已知bug: 消费金额不能带小数')
@pytest.mark.bug
def test_consume_fuel_card_balance_float(db, api, data):
    user_name = data['USER_WITH_TWO_CARDS'][0]
    user_id = db.get_user_id(user_name)
    card_number = data['USED_CARD']
    balance = float(data['AMOUNT'])
    res = api.consume_fuel_card(user_id, card_number, balance)

    check.not_equal(200, res['code'])
    check.not_equal('消费成功!', res['msg'])
    check.is_false(res['success'])


def test_consume_fuel_card_card_number_not_exist(db, api, data):
    user_name = data['USER_WITH_TWO_CARDS'][0]
    user_id = db.get_user_id(user_name)
    card_number = data['CARD_NOT_EXIST']
    balance = data['AMOUNT']
    res = api.consume_fuel_card(user_id, card_number, balance)

    check.equal(5013, res['code'])
    check.equal('根据用户ID没有查询到卡号!', res['msg'])
    check.is_false(res['success'])


def test_consume_fuel_card_user_not_exist(db, api, data):
    user_id = data['USER_ID_NOT_EXIST']
    card_number = data['USED_CARD']
    balance = data['AMOUNT']
    res = api.consume_fuel_card(user_id, card_number, balance)

    check.equal(5013, res['code'])
    check.equal('根据用户ID没有查询到卡号!', res['msg'])
    check.is_false(res['success'])

