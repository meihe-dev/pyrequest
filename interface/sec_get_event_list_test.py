import requests, unittest, hashlib
from time import time
from db_fixture import test_data


class GetEventListTest(unittest.TestCase):
    '''查询发布会信息（带用户认证）'''

    # @classmethod
    # def setUpClass(cls):
    #     test_data.init_data()  # 初始化接口测试数据
    #
    # @classmethod
    # def tearDownClass(cls):
    #     test_data.clear_data()  # 清空测试数据

    def setUp(self):
        self.base_url = 'http://127.0.0.1:8000/api/sec_get_event_list/'
        self.result = ''

    def tearDown(self):
        print(self.result)

    def test_get_event_list_auth_null(self):
        '''auth为空'''
        r = requests.get(self.base_url, params={'eid': 1})
        self.result = r.json()
        self.assertEqual(self.result['status'], 10011)
        self.assertEqual(self.result['message'], 'user auth null')

    def test_get_event_list_auth_error(self):
        '''auth错误'''
        auth_user = ('abc', '123')
        r = requests.get(self.base_url, auth=auth_user, params={'eid': 1})
        self.result = r.json()
        self.assertEqual(self.result['status'], 10012)
        self.assertEqual(self.result['message'], 'user auth fail')

    def test_get_event_list_eid_null(self):
        '''eid参数为空'''
        auth_user = ('admin', 'passw0rddjango')
        # eid为‘’而不是为‘ ’
        r = requests.get(self.base_url, auth=auth_user, params={'eid': ''})
        self.result = r.json()
        self.assertEqual(self.result['status'], 10021)
        self.assertEqual(self.result['message'], 'parameter error')

    def test_get_event_list_eid_success(self):
        '''根据eid查询结果成功'''
        auth_user = ('admin', 'passw0rddjango')
        r = requests.get(self.base_url, auth=auth_user, params={'eid': 1})
        self.result = r.json()
        self.assertEqual(self.result['status'], 200)
        self.assertEqual(self.result['message'], 'success')
        self.assertEqual(self.result['data']['name'], u'红米Pro发布会')
        self.assertEqual(self.result['data']['address'], u'北京会展中心')


if __name__ == '__main__':
    unittest.main()
