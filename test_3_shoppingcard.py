'''
购物车的增/查/改/删  流程
购物车单商品最多加购99件.

author:llj
'''
import unittest
from time import sleep

from common.get_result_easy import get_result_for_keyword, get_results_for_keyword,get_results_for_label_keyword
from interface.interface_login import InterfaceLogin
from interface.interface_shoppingcart import InterfaceShopping
import random

rec_id = None
class TestSCard(unittest.TestCase):

    def setUp(self) -> None:
        """
        登录个人账户
        :return:
        """
        self.method = "post"
        url = "http://ecshop.itsoso.cn/ECMobile/?url=/user/signin"
        data = {"name": "test", "password": "123123"}

        response = InterfaceLogin.login(method=self.method, url=url, data=data)
        self.sid = get_result_for_keyword(response, "sid")  # 获取登录返回值的sid
        self.uid = get_result_for_keyword(response, "uid")  # 获取登录返回值的uid

    def test_1_get_id(self):
        """查询手机类商品id"""
        global goodsid
        url = "http://ecshop.itsoso.cn/ECMobile/?url=/search "
        data = {"pagination": {"count": 50, "page": 1},
                "filter": {"keywords": "", "sort_by": "price_asc", "brand_id": "", "category_id": "25",
                           "price_range": {"price_min": 0, "price_max": 0}}}
        response = InterfaceShopping.get_id(method=self.method, url=url, data=data)  # 发送请求
        # 获取响应的 goods_id
        goods_id = get_results_for_keyword(response, "goods_id")
        # 获取任一 goods_id
        num = random.randint(0, len(goods_id)-1)
        print("索引值",num)
        goodsid = goods_id[num]
        # self.goodsid = goods_id[num]
        print("添加商品id",goodsid)
        # 获取响应succeed 值
        res = get_result_for_keyword(response, "succeed")
        # 断言 succeed=1
        self.assertEqual(res, 1)

    def test_2_get_good(self):
        '''选择商品加购物车--添加商品后清单'''
        global goodsid  #将goodid 变为全局变量操作?
        url = "http://ecshop.itsoso.cn/ECMobile/?url=/cart/create"
        good = {"spec": [],
                "session": {"uid":self.uid, "sid":self.sid},
                "goods_id":goodsid, "number": 1}
        sleep(3)
        response2 = InterfaceShopping.get_good(method=self.method, url=url, goods=good)  # 发送请求
        print(2,response2)
        '''添加商品后清单'''
        global rec_id
        url = "http://ecshop.itsoso.cn/ECMobile/?url=/cart/list"
        data = {"session": {"uid": self.uid, "sid": self.sid}}
        response3 = InterfaceShopping.get_list(method=self.method, url=url, data=data)  # 发送请求
        print(3,response3)
        # global rec_id
        # 获取rec_id
        rec_id = get_results_for_label_keyword(response3,"goods_list", "rec_id")
        print(rec_id)

        # 获取响应succeed 值
        res = get_result_for_keyword(response3, "succeed")
        # 断言 succeed=1
        self.assertEqual(res, 1)


    def test_3_update_num(self):
        '''修改商品数量--正常值'''
        global rec_id
        url = "http://ecshop.itsoso.cn/ECMobile/?url=/cart/update"

        num = random.randint(1, 100)
        data = {"new_number": num,
                "session": {"uid": self.uid, "sid": self.sid}, "rec_id": rec_id}
        response = InterfaceShopping.update_num(method=self.method, url=url, data=data)  # 发送请求
        # 获取响应succeed 值
        res = get_result_for_keyword(response, "succeed")
        # 断言 succeed=1
        self.assertEqual(res, 1)

    def test_4_modify_num(self):
        '''修改商品数量--超上限'''
        global rec_id
        url = "http://ecshop.itsoso.cn/ECMobile/?url=/cart/update"

        num = random.randint(100, 1000)
        data = {"new_number": num,
                "session": {"uid": self.uid, "sid": self.sid}, "rec_id": rec_id}
        response = InterfaceShopping.modify_num(method=self.method, url=url, data=data)  # 发送请求
        # 获取响应succeed 值
        res = get_result_for_keyword(response, "succeed")
        # 断言 succeed=0
        self.assertEqual(res, 0,msg="添加商品超出上限添加成功")

    def test_5_del_goods(self):
        '''删除购物车商品'''
        global rec_id
        url = "http://ecshop.itsoso.cn/ECMobile/?url=/cart/delete "
        data = {"session": {"uid": self.uid, "sid": self.sid}, "rec_id": rec_id}
        response = InterfaceShopping.del_goods(method=self.method, url=url, data=data)  # 发送请求
        # 获取响应succeed 值
        res = get_result_for_keyword(response, "succeed")
        # 断言 succeed=1
        self.assertEqual(res, 1)


if __name__ == '__main__':
    unittest.main()
