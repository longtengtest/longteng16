import pytest
import pytest_check as check


def test_recharge_fuel_card(db, api, data):
    user_name = data['USER_WITH_TWO_CARDS'][0]
    user_id = db.get_user_id(user_name)
    card_number = data['USED_CARD']
    balance = data['AMOUNT']

    balance_before = db.get_balance(card_number)

    res = api.recharge_fuel_card(card_number, balance)
    check.equal(200, res['code'])
    check.equal('充值成功', res['msg'])
    check.is_true(res['success'])

    result = res['result']
    check.equal(card_number, result['cardNumber'])
    check.equal(5010, result['cardStatus'])
    check.equal(user_id, result['userId'])

    balance_after = str(int(balance) + int(balance_before))
    check.equal(balance_after, result['cardBalance'])


@pytest.mark.negative
def test_recharge_fuel_card_method_id_blank(api, data):
    card_number = data['USED_CARD']
    balance = data['AMOUNT']
    data = {
         "dataSourceId": "bHRz",
         "methodId": "",
         "CardInfo": {
          "cardNumber": card_number,
          "cardBalance": str(balance)
     }}

    res = api.post(json=data).json()

    check.equal(301, res['code'])
    check.equal('业务ID不能为空!', res['msg'])
    check.is_false(res['success'])


@pytest.mark.negative
def test_recharge_fuel_card_data_source_id_blank(api, data):
    card_number = data['USED_CARD']
    balance = data['AMOUNT']
    data = {
         "dataSourceId": "",
         "methodId": "03A",
         "CardInfo": {
          "cardNumber": card_number,
          "cardBalance": str(balance)
     }}

    res = api.post(json=data).json()

    check.equal(301, res['code'])
    check.equal('第三方平台ID不能为空!', res['msg'])
    check.is_false(res['success'])


@pytest.mark.negative
def test_recharge_fuel_card_card_number_blank(api, data):
    card_number = ''  # 不存在空这个卡号
    balance = data['AMOUNT']

    res = api.recharge_fuel_card(card_number, balance)

    check.equal(5013, res['code'])
    check.equal('加油卡号不存在', res['msg'])
    check.is_false(res['success'])


@pytest.mark.negative
def test_recharge_fuel_card_balance_blank(api, data):
    card_number = data['USED_CARD']
    balance = ''

    res = api.recharge_fuel_card(card_number, balance)

    check.equal(300, res['code'])
    check.equal('金额不能为空', res['msg'])
    check.is_false(res['success'])


@pytest.mark.negative
def test_recharge_fuel_card_method_id_wrong(api, data):
    card_number = data['USED_CARD']
    balance = data['AMOUNT']

    data = {
        "dataSourceId": "bHRz",
        "methodId": data['METHOD_ID_NOT_EXIST'],
        "CardInfo": {
            "cardNumber": card_number,
            "cardBalance": str(balance)
        }}

    res = api.post(json=data).json()

    check.equal(199, res['code'])
    check.equal('业务ID无效', res['msg'])
    check.is_false(res['success'])


@pytest.mark.negative
def test_recharge_fuel_card_data_source_id_wrong(api, data):
    card_number = data['USED_CARD']
    balance = data['AMOUNT']

    data = {
        "dataSourceId": data['INVALID_DATA_SOURCE_ID'],  # 当dataSourceId为'bHRz2'时有bug
        "methodId": "03A",
        "CardInfo": {
            "cardNumber": card_number,
            "cardBalance": str(balance)
        }}

    res = api.post(json=data).json()

    check.equal(100, res['code'])
    check.equal('对不起,您的第三方机构无权限访问该接口', res['msg'])
    check.is_false(res['success'])


@pytest.mark.negative
def test_recharge_fuel_card_card_number_not_exist(api, data):
    card_number = data['CARD_NOT_EXIST']
    balance = data['AMOUNT']

    res = api.recharge_fuel_card(card_number, balance)

    check.equal(5013, res['code'])
    check.equal('加油卡号不存在', res['msg'])
    check.is_false(res['success'])


@pytest.mark.negative
def test_recharge_fuel_card_balance_negative(api, data):
    card_number = data['USED_CARD']
    balance = -int(data['AMOUNT'])

    res = api.recharge_fuel_card(card_number, balance)

    check.equal(300, res['code'])
    check.equal('金额需为整数', res['msg'])
    check.is_false(res['success'])
