# _*_ coding: UTF-8 _*_
# 开发团队  : 测试一组
# 开发人员  : Candy
# 开发时间  : 2019/7/23 15:22
# 文件名称  : test_register.PY
# 开发工具  : PyCharm
import json
import unittest
from interface.interface import Interface
from common.get_result_easy import get_result_for_keyword
from common.operationexcel import OperationExcel
from common.database import Database
import ddt
import os

BASE_PATH = os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]
data_file = os.path.join(BASE_PATH, "data", "register_data.xlsx")
oper_excel = OperationExcel(data_file)
test_data = oper_excel.get_data_for_dict()


@ddt.ddt
class TestRegister(unittest.TestCase):
    def setUp(self) -> None:
        self.url = "http://ecshop.itsoso.cn/ECMobile/?url=/user/signup "
        self.method = "post"

    @ddt.data(*test_data)
    def test_register(self, data):
        req_data = {"field": [{"id": 5, "value": data['mobile']}],
                                "email": data['email'],
                                "name": data['name'],
                                "password": data['password']
        }
        response = Interface.common_method(method=self.method, url=self.url, data=req_data)
        print(response)
        status = get_result_for_keyword(response, "succeed")
        # db = Database(password="ecshop", database="ecshop")
        # sql = "select * from ecs_users where user_name = %s"
        # cont = data["name"]
        # args = [cont]
        # content = db.one(sql, args)
        # res = content["user_name"]
        self.assertEqual(status, data['expect'])
        # self.assertEqual(res,cont,"未添加到数据库中")


if __name__ == '__main__':
    unittest.main()

