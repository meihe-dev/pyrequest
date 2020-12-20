import requests, unittest, hashlib
from time import time
from db_fixture import test_data


class AddEventTest(unittest.TestCase):
    '''添加发布会（签名+时间戳）'''

    # @classmethod
    # def setUpClass(cls):
    #     test_data.init_data()  # 初始化接口测试数据
    #
    # @classmethod
    # def tearDownClass(cls):
    #     test_data.clear_data() # 清空测试数据

    def setUp(self):
        self.base_url = 'http://127.0.0.1:8000/api/sec_add_event/'
        # app_key
        self.api_key = '&Guest-Bugmaster'
        # 当前时间
        now_time = time()
        self.client_time = str(now_time).split('.')[0]
        # sign
        md5 = hashlib.md5()
        sign_str = self.client_time + self.api_key
        sign_bytes_utf8 = sign_str.encode(encoding='utf-8')
        md5.update(sign_bytes_utf8)
        self.sign_md5 = md5.hexdigest()
        self.result = ''

    def tearDown(self):
        print(self.result)

    def test_add_event_request_error(self):
        '''请求方法错误'''
        r = requests.get(self.base_url)
        self.result = r.json()
        self.assertEqual(10011, self.result['status'])
        self.assertEqual('request error', self.result['message'])

    def test_add_event_sign_null(self):
        '''签名参数为空'''
        payload = {'eid': '', '': '', 'limit': '', 'address': '', 'start_time': '', 'time': '', 'sign': ''}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(10012, self.result['status'])
        self.assertEqual('user sign null', self.result['message'])

    def test_add_event_time_out(self):
        '''请求超时'''
        now_time = str(int(self.client_time) - 61)
        payload = {'eid': '', '': '', 'limit': '', 'address': '', 'start_time': '', 'time': now_time, 'sign': 'abc'}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(10013, self.result['status'])
        self.assertEqual('user sign timeout', self.result['message'])

    def test_add_event_sign_error(self):
        '''签名错误'''
        payload = {'eid': 1, '': '', 'limit': '', 'address': '', 'start_time': '', 'time': self.client_time, 'sign': 'abc'}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(10014, self.result['status'])
        self.assertEqual('user sign error', self.result['message'])

    def test_add_event_success(self):
        '''添加成功'''
        # create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # payload = {'eid': 11, 'name': '一加5手机发布会', 'limit': 2000, 'address': '深圳宝体',
        #            'start_time': '2016-08-20 00:25:42', 'create_time': create_time,
        #            'time': self.client_time, 'sign': self.sign_md5}
        payload = {'eid': 12, 'name': '一加5手机发布会', 'limit': 2000, 'address': '深圳宝体',
                   'start_time': '2016-08-20 00:25:42', 'create_time': '2016-08-20 00:25:42',
                   'time': self.client_time, 'sign': self.sign_md5}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(200, self.result['status'])
        self.assertEqual('add event success', self.result['message'])


if __name__ == '__main__':
    unittest.main()
