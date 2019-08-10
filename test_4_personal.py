import unittest
from interface.interface_personal import InterfacePersonal
from interface.interface_login import InterfaceLogin
from common.get_result_easy import get_result_for_keyword
from common.operationexcel import OperationExcel
import os
import ddt
import json

BASE_PATH = os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]
data_file = os.path.join(BASE_PATH, "data", "address_data.xlsx")
oper_excel = OperationExcel(data_file)
test_data = oper_excel.get_data_for_dict()


@ddt.ddt
class TestPersonal(unittest.TestCase):
    """
    个人中心测试用例
    """

    def setUp(self) -> None:
        # 登录
        self.method = "post"
        url = "http://ecshop.itsoso.cn/ECMobile/?url=/user/signin"
        data = {"name": "u123", "password": "123456"}
        response = InterfaceLogin.login(method=self.method, url=url, data=data)
        self.sid = get_result_for_keyword(response, "sid")  # 获取登录返回值的sid
        self.uid = get_result_for_keyword(response, "uid")  # 获取登录返回值的uid

    def test_1_waite_pay(self):
        """待付款"""
        url = "http://ecshop.itsoso.cn/ECMobile/?url=/order/list"
        data = {"session": {"uid": f"{self.uid}", "sid": f"{self.sid}"}, "type": "await_pay",
                "pagination": {"count": 10, "page": 1}}
        response = InterfacePersonal.waite_pay(method=self.method, url=url, data=data)
        succeed = InterfacePersonal.succeed_value(method=self.method, url=url, data=data)  # 获取待付款返回值succeed
        self.assertEqual(succeed, 1)  # 断言succeed
        self.count_pay = get_result_for_keyword(response, "count")  # 获取待付款返回值商品数量count
        if self.count_pay > 0:  # 判断有商品
            self.order_id_pay = get_result_for_keyword(response, "order_id")  # 获取商品order_id

    @unittest.skip
    def test_2_cell_order(self):
        """取消订单"""
        url = "http://ecshop.itsoso.cn/ECMobile/?url=/order/cancel"
        data = {"session": {"uid": f"{self.uid}", "sid": f"{self.sid}"}, "order_id": self.order_id_pay}
        succeed = InterfacePersonal.succeed_value(method=self.method, url=url, data=data)
        self.assertEqual(succeed, 1)

    def test_3_waite_ship(self):
        """待发货"""
        url = "http://ecshop.itsoso.cn/ECMobile/?url=/order/list"
        data = {"session": {"uid": f"{self.uid}", "sid": f"{self.sid}"}, "type": "await_ship",
                "pagination": {"count": 10, "page": 1}}
        succeed = InterfacePersonal.succeed_value(method=self.method, url=url, data=data)
        self.assertEqual(succeed, 1)

    def test_4_waite_received(self):
        """待收货"""
        url = "http://ecshop.itsoso.cn/ECMobile/?url=/order/list"
        data = {"session": {"uid": f"{self.uid}", "sid": f"{self.sid}"}, "type": "shipped",
                "pagination": {"count": 10, "page": 1}}
        succeed = InterfacePersonal.succeed_value(method=self.method, url=url, data=data)
        self.assertEqual(succeed, 1)
        response = InterfacePersonal.waite_pay(method=self.method, url=url, data=data)
        self.count_received = get_result_for_keyword(response, "count")  # 获取待付款返回值商品数量count
        if self.count_received > 0:  # 判断有商品
            self.order_id_received = get_result_for_keyword(response, "order_id")  # 获取商品order_id

    @unittest.skip
    def test_5_view_logistics(self):
        """查看物流"""
        url = "http://ecshop.itsoso.cn/ECMobile/?url=/order/express"
        data = {"session": {"uid": f"{self.uid}", "sid": f"{self.sid}"}, "order_id": f"{self.order_id_received}",
                "app_key": "xxx"}
        succeed = InterfacePersonal.succeed_value(method=self.method, url=url, data=data)
        self.assertEqual(succeed, 1)

    @unittest.skip
    def test_6_confirm_receipt(self):
        """确认收货"""
        url = "http://ecshop.itsoso.cn/ECMobile/?url=/order/affirmReceived"
        data = {"session": {"uid": f"{self.uid}", "sid": f"{self.sid}"}, "order_id": self.order_id_received}
        succeed = InterfacePersonal.succeed_value(method=self.method, url=url, data=data)
        self.assertEqual(succeed, 1)

    def test_7_his_order(self):
        """历史订单"""
        url = "http://ecshop.itsoso.cn/ECMobile/?url=/order/list"
        data = {"session": {"uid": f"{self.uid}", "sid": f"{self.sid}"}, "type": "finished",
                "pagination": {"count": 10, "page": 1}}
        succeed = InterfacePersonal.succeed_value(method=self.method, url=url, data=data)
        self.assertEqual(succeed, 1)

    def test_8_1_add_coll(self):
        """添加收藏"""
        url = "http://ecshop.itsoso.cn/ECMobile/?url=/user/collect/create"
        data = {"session": {"uid": f"{self.uid}", "sid": f"{self.sid}"}, "goods_id": 68}
        InterfacePersonal.add_coll(method=self.method, url=url, data=data)
        data = InterfacePersonal.coll_goods_id()
        print(data)
        self.assertTrue(68 in data)

    def test_8_2_look_coll(self):
        """查看收藏"""
        url = "http://ecshop.itsoso.cn/ECMobile/?url=/user/collect/list"
        data = {"session": {"uid": f"{self.uid}", "sid": f"{self.sid}"}, "pagination": {"count": 10, "page": 1},
                "rec_id": 0}
        succeed = InterfacePersonal.succeed_value(method=self.method, url=url, data=data)
        self.assertEqual(succeed, 1)

    def test_8_3_del_coll(self):
        """移除收藏"""
        url = "http://ecshop.itsoso.cn/ECMobile/?url=/user/collect/delete"
        try:
            rec_id = InterfacePersonal.coll_rec_id()  # 获取rec_id
            data = {"session": {"uid": f"{self.uid}", "sid": f"{self.sid}"}, "rec_id": rec_id}
            InterfacePersonal.del_coll(method=self.method, url=url, data=data)
            rec_ids = InterfacePersonal.coll_rec_id()
            self.assertTrue(rec_id not in rec_ids)
        except:
            print("没有收藏商品")

    def test_9_1_look_address(self):
        """查看收货地址"""
        url = "http://ecshop.itsoso.cn/ECMobile/?url=/address/list"
        data = {"session": {"uid": f"{self.uid}", "sid": f"{self.sid}"}}
        succeed = InterfacePersonal.succeed_value(method=self.method, url=url, data=data)
        self.assertEqual(succeed, 1)

    @ddt.data(*test_data)
    def test_9_2_add_address(self, data):
        """新增收货地址"""
        url = "http://ecshop.itsoso.cn/ECMobile/?url=/address/add"
        add_data = {
            "address": {"default_address": 0, "consignee": data["username"], "tel": data["tel"], "zipcode": "621000",
                        "country": "4044", "city": "", "id": 0, "email": data["mail"], "address": data["address"],
                        "province": "", "district": "", "mobile": ""},
            "session": {"uid": f"{self.uid}", "sid": f"{self.sid}"}}
        response = InterfacePersonal.add_address(method=self.method, url=url, data=add_data)
        status = get_result_for_keyword(response, "succeed")
        self.assertEqual(status, data["except"])

    @ddt.data(*test_data)
    def test_9_3_upd_address(self, data):
        """修改收货地址"""
        url = "http://ecshop.itsoso.cn/ECMobile/?url=/address/update"
        upd_data = {"address": {"default_address": 0, "consignee": data["username"], "tel": data["new_tel"],
                                "zipcode": "621000",
                                "country": "4044", "city": "0", "id": 0, "email": data["new_mail"],
                                "address": data["new_address"], "province": "0", "district": "0", "mobile": ""},
                    "address_id": "2515", "session": {"uid": f"{self.uid}", "sid": f"{self.sid}"}}
        response = InterfacePersonal.upd_address(method=self.method, url=url, data=upd_data)
        print(response)
        status = get_result_for_keyword(response, "succeed")
        self.assertEqual(status, data["except"])

    def test_9_4_del_address(self):
        """删除收货地址"""
        address_ids = InterfacePersonal.address_id()
        url = "http://ecshop.itsoso.cn/ECMobile/?url=/address/delete"
        data = {"address_id": f"{address_ids[len(address_ids) - 1]}",
                "session": {"uid": f"{self.uid}", "sid": f"{self.sid}"}}
        InterfacePersonal.del_address(method=self.method, url=url, data=data)
        address_id = InterfacePersonal.address_id()
        self.assertTrue(address_ids[len(address_ids) - 1] not in address_id)


if __name__ == '__main__':
    unittest.main()
