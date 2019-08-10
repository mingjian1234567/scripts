# _*_ coding: UTF-8 _*_
# 开发团队  : 测试一组
# 开发人员  : Candy
# 开发时间  : 2019/7/24 19:31
# 文件名称  : test_shiping.PY
# 开发工具  : PyCharm
import unittest
from interface.interface import Interface
from common.sendmethod import SendMethod
from common.get_result_easy import get_result_for_keyword
import json
import time

order_id = None


class TestRegister(unittest.TestCase):
    def setUp(self) -> None:
        # 登录
        self.method = "post"
        url = "http://ecshop.itsoso.cn/ECMobile/?url=/user/signin"
        data = {"name": "test", "password": "123123"}
        response = Interface.common_method(method=self.method, url=url, data=data)
        self.sid = get_result_for_keyword(response, "sid")  # 获取登录返回值的sid
        self.uid = get_result_for_keyword(response, "uid")  # 获取登录返回值的uid

    def test_cart(self):
        """
        添加商品到购物车
        :return:
        """
        url = "http://ecshop.itsoso.cn/ECMobile/?url=/cart/create "
        data = {"spec": [], "session": {"uid": f"{self.uid}", "sid": f"{self.sid}"}, "goods_id": 72, "number": 1}
        response = Interface.common_method(method=self.method, url=url, data=data)
        print(response)

        """购物车清单(列表)"""
        url = "http://ecshop.itsoso.cn/ECMobile/?url=/cart/list"
        data = {"session": {"uid": f"{self.uid}", "sid": f"{self.sid}"}}
        response = Interface.common_method(method=self.method, url=url, data=data)
        # self.rec_id = get_result_for_keyword(response, "rec_id")
        print(response)

        """确认订单 """

        url = "http://ecshop.itsoso.cn/ECMobile/?url=/flow/checkOrder"
        data = {"session": {"uid": f"{self.uid}", "sid": f"{self.sid}"}}
        response = Interface.common_method(method=self.method, url=url, data=data)

        print(response)

        """提交订单"""
        url = "http://ecshop.itsoso.cn/ECMobile/?url=/flow/done "
        data = {"shipping_id": "6", "session": {"uid": f"{self.uid}", "sid": f"{self.sid}"}, "pay_id": "5"}
        response = Interface.common_method(method=self.method, url=url, data=data)
        global order_id
        order_id = get_result_for_keyword(response, "order_id")
        print(order_id)
        print(response)

        """订单支付"""
        url = "http://ecshop.itsoso.cn/ECMobile/?url=/order/pay "
        data = {"session": {"uid": f"{self.uid}", "sid": f"{self.sid}"}, "order_id": f"{order_id}"}
        response = Interface.common_method(method=self.method, url=url, data=data)
        status = Interface.status(response)
        print(response)
        self.assertTrue(status == 1)

    # def test_8_all(self):
    #     pass


if __name__ == '__main__':
    unittest.main()
