
import pytest
import pytest_check as check


def test_query_fuel_card(db, api, data):
    user_name = data['BIND_USER'][0]
    user_id = db.get_user_id(user_name)
    card_number = data['BLANK_CARD']  # 无消费、重置记录
    res = api.query_fuel_card(user_id, card_number)

    check.equal(200, res['code'])
    check.equal('成功返回', res['msg'])
    check.is_true(res['success'])

    result = res['result']
    check.equal(card_number, result['cardNumber'])
    check.equal('已经被绑定,正常使用中', result['cardStatus'])
    check.equal(db.get_balance(card_number), result['cardBalance'])
    check.equal([], result['consumptionDetails'])
    check.equal([], result['rechargeDetails'])


def test_query_fuel_card_with_recharge_consume_records(db, api, data):
    user_name = data['USER_WITH_TWO_CARDS'][0]
    user_id = db.get_user_id(user_name)

    card_number = data['USED_CARD']  # 既有消费又有充值记录
    res = api.query_fuel_card(user_id, card_number)

    check.equal(200, res['code'])
    check.equal('成功返回', res['msg'])
    check.is_true(res['success'])

    result = res['result']
    check.equal(card_number, result['cardNumber'])
    check.equal('已经被绑定,正常使用中', result['cardStatus'])
    check.equal(db.get_balance(card_number), result['cardBalance'])
    db_consume_records = db.get_consume_details(card_number)
    db_recharge_records = db.get_recharge_details(card_number)
    if len(db_consume_records) > 3:
        db_consume_records = db_consume_records[:3]
    if len(db_recharge_records) > 3:
        db_recharge_records = db_recharge_records[:3]

    check.equal(db_consume_records, result['consumptionDetails'])
    check.equal(db_recharge_records, result['rechargeDetails'])


@pytest.mark.negetive
def test_query_fuel_card_not_exist(db, api, data):
    user_name = data['BIND_USER'][0]
    user_id = db.get_user_id(user_name)

    card_number = data['CARD_NOT_EXIST']
    res = api.query_fuel_card(user_id, card_number)

    check.equal(400, res['code'])
    check.equal('无查询信息', res['msg'])
    check.is_false(res['success'])


@pytest.mark.negetive
def test_query_fuel_card_user_not_exist(db, api, data):
    user_id = data['USER_ID_NOT_EXIST']
    card_number = 'hzc_123456'
    res = api.query_fuel_card(user_id, card_number)

    check.equal(400, res['code'])
    check.equal('无查询信息', res['msg'])
    check.is_false(res['success'])


@pytest.mark.xfail(reason='已知bug: dataSourceId不对也能查询到结果')
@pytest.mark.negetive
def test_query_fuel_card_data_source_id_not_exist(db, api, data):
    user_name = data['BIND_USER'][0]
    user_id = db.get_user_id(user_name)
    card_number = data['BLANK_CARD']  # 无消费、重置记录
    data_source_id = data['INVALID_DATA_SOURCE_ID']
    params = {'dataSourceId': data_source_id, 'userId': user_id, 'cardNumber': card_number, 'methodId': '02A'}
    res = api.get(params=params).json()

    check.equal(400, res['code'])
    check.equal('无查询信息', res['msg'])
    check.is_false(res['success'])
