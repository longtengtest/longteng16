import requests


class Api(object):
    def __init__(self, base_url):
        self.url = f'{base_url}/gasStation/process'
        self.session = requests.session()

    def get(self, **kwargs):
        res = self.session.get(self.url, **kwargs)
        print(f'响应报文: {res.json()}')
        return res

    def post(self, **kwargs):
        res = self.session.post(self.url, **kwargs)
        print(f'响应报文: {res.json()}')
        return res

    def add_fuel_card(self, card_number):
        data = {
            "dataSourceId": "bHRz",
            "methodId": "00A",
            "CardInfo": {
                "cardNumber": card_number
            }
        }

        return self.post(json=data).json()

    def bind_fuel_card(self, user_name, id_number, card_number, id_type="1", email=None, gender=None):
        data = {
                "dataSourceId": "bHRz",
                "methodId": "01A",
                "CardUser": {
                    "userName": user_name,
                    "idType": id_type,
                    "idNumber": id_number,
                    "email": email,
                    "gender": gender
                },
                "CardInfo": {
                    "cardNumber": card_number
                }
            }
        return self.post(json=data).json()

    def query_fuel_card(self, user_id, card_number):
        params = {'dataSourceId': "bHRz", 'userId': user_id, 'cardNumber': card_number, 'methodId': '02A'}
        res = self.session.get(self.url, params=params).json()
        print(f'响应报文: {res}')
        return res

    def recharge_fuel_card(self, card_number, balance):
        data = {
             "dataSourceId": "bHRz",
             "methodId": "03A",
             "CardInfo": {
              "cardNumber": card_number,
              "cardBalance": str(balance)
             }}
        return self.post(json=data).json()

    def consume_fuel_card(self, user_id, card_number, balance):
        data = {
             "dataSourceId": "bHRz",
             "methodId": "04A",
             "CardUser": {
              "userId": user_id
             },
             "CardInfo": {
              "cardNumber": card_number,
              "cardBalance": str(balance)
             }
            }
        return self.post(json=data).json()
