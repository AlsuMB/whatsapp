import base64
import json
import logging

import requests

logging.basicConfig(level=logging.DEBUG)


class Chat:
    def __init__(self):
        APIUrl = 'https://dev.wapp.im/v3/'
        method = 'chat/spare?crm=TEST&domain=test'
        headers = {'Content-type': 'application/json', 'X-Tasktest-Token': 'f62cdf1e83bc324ba23aee3b113c6249'}

        self.chat = requests.get(APIUrl + method, headers=headers).json()
        self.headers = {'X-Tasktest-Token': 'f62cdf1e83bc324ba23aee3b113c6249'}

        # self.chat = {"id": 22, "instanceId": "2a01:4f8:c17:ac8:3::11", "token": "qrtYYGoXkJE145ER",
        #              "chat_id": "2a01:4f8:c17:ac8:3::11", "md": 0, "chat_token": "qrtYYGoXkJE145ER",
        #              "chat_key": "96ae91405d9407ccfc32dcdd0e8187de",
        #              "apikey": "96ae91405d9407ccfc32dcdd0e8187de", "date_add": 1644227374, "date_trial": None,
        #              "date_pay": 0, "date_subscription": 0, "phone": "", "name": "", "platform": "", "status": 0,
        #              "is_premium": 0}

    def get_status_and_save_qr(self):
        url = f'https://dev.wapp.im/v3/instance{self.chat["id"]}/status'
        params = {'full': 1, 'token': {self.chat["token"]}}
        response = requests.get(url, headers=self.headers, params=params)

        map = json.loads(response.content.decode())
        self.__save_qr__(map['qrCode'].split(',')[1])
        return response

    @staticmethod
    def __save_qr__(data):
        imgdata = base64.b64decode(data)
        filename = 'qr_code.jpg'
        with open(filename, 'wb') as f:
            f.write(imgdata)

    def get_name_and_phone(self):
        url = f'https://dev.whatsapp.sipteco.ru/v3/instance{self.chat["id"]}/contact?token={self.chat["token"]}&chatId={self.chat["chat_id"]}&phone'
        headers = {'X-Tasktest-Token': 'f62cdf1e83bc324ba23aee3b113c6249'}

        response = requests.post(url, headers=headers)
        print(response.content)

    def send_message(self):
        url = f'https://dev.whatsapp.sipteco.ru/v3/instance{self.chat["id"]}/sendMessage'
        params = {'token': self.chat["token"]}

        data = {'phone': '89003235143', "body": "текст сообщения", 'sendSeen': "1", 'typeMsg': 'text',
                'footer': 'footer', 'title': 'title'}
        response = requests.post(url, params=params, data=data, headers=self.headers)
        print(response.content)

    def delete(self):
        url = f'https://dev.whatsapp.sipteco.ru/v3/instance{self.chat["id"]}/removeChat'
        params = {'token': self.chat["token"], 'phone': self.chat["chat_id"]}

        response = requests.get(url, headers=self.headers, params=params)
        print(response.content)
