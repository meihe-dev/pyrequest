import requests
import unittest
from db_fixture import test_data


class GetEventListTest(unittest.TestCase):
    '''查询发布会接口测试'''

    # @classmethod
    # def setUpClass(cls):
    #     test_data.init_data()  # 初始化接口测试数据
    #
    # @classmethod
    # def tearDownClass(cls):
    #     test_data.clear_data()  # 清空测试数据

    def setUp(self):
        self.url = 'http://127.0.0.1:8000/api/get_event_list/'
        self.result = ''

    def tearDown(self):
        print(self.result)

    def test_get_event_null(self):
        '''发布会id为空'''
        r = requests.get(self.url, params={'eid': ''})
        result = r.json()
        self.assertEqual(result['status'], 10021)
        self.assertEqual(result['message'], 'parameter error')

    def test_get_event_error(self):
        '''发布会id不存在'''
        r = requests.get(self.url, params={'eid': '901'})
        result = r.json()
        self.assertEqual(result['status'], 10022)
        self.assertEqual(result['message'], 'query result is empty')

    def test_get_event_success(self):
        '''发布会id为1，查询成功'''
        r = requests.get(self.url, params={'eid': '1'})
        result = r.json()
        self.assertEqual(result['status'], 200)
        self.assertEqual(result['message'], 'success')
        self.assertEqual(result['data']['name'], '红米Pro发布会')
        self.assertEqual(result['data']['address'], '北京会展中心')
        self.assertEqual(result['data']['start_time'], '2016-08-20T00:25:42')

if __name__ == '__main__':
    unittest.main()