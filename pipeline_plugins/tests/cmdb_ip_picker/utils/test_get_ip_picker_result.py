# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云PaaS平台社区版 (BlueKing PaaS Community
Edition) available.
Copyright (C) 2017-2021 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""

from mock import patch

from django.test import TestCase

from pipeline_plugins.cmdb_ip_picker.utils import get_ip_picker_result


class MockCMDBReturnEmpty(object):
    @staticmethod
    def get_business_host_topo(*args, **kwargs):
        return []


class MockCMDB(object):
    @staticmethod
    def get_business_host_topo(*args, **kwargs):
        return [
            {
                "host": {
                    "bk_host_innerip": "1.1.1.1",
                    "bk_host_outerip": "1.1.1.1",
                    "bk_host_name": "1.1.1.1",
                    "bk_host_id": 1,
                    "bk_cloud_id": 0,
                },
                "module": [{"bk_module_id": 3, "bk_module_name": "空闲机"}],
            },
            {
                "host": {
                    "bk_host_innerip": "2.2.2.2",
                    "bk_host_outerip": "2.2.2.2",
                    "bk_host_name": "2.2.2.2",
                    "bk_host_id": 2,
                    "bk_cloud_id": 0,
                },
                "module": [{"bk_module_id": 5, "bk_module_name": "test1"}],
            },
            {
                "host": {
                    "bk_host_innerip": "3.3.3.3",
                    "bk_host_outerip": "3.3.3.3",
                    "bk_host_name": "3.3.3.3",
                    "bk_host_id": 3,
                    "bk_cloud_id": 0,
                },
                "module": [{"bk_module_id": 8, "bk_module_name": "test1"}],
            },
        ]

    @staticmethod
    def get_dynamic_group_host_list(*args, **kwargs):
        dynamic_group_data = {
            "group1": [
                {
                    "bk_host_innerip": "1.1.1.1",
                    "bk_host_outerip": "1.1.1.1",
                    "bk_host_name": "1.1.1.1",
                    "bk_host_id": 1,
                    "bk_cloud_id": 0,
                    "host_modules_id": [3],
                },
                {
                    "bk_host_innerip": "2.2.2.2",
                    "bk_host_outerip": "2.2.2.2",
                    "bk_host_name": "2.2.2.2",
                    "bk_host_id": 2,
                    "bk_cloud_id": 0,
                    "host_modules_id": [5],
                },
            ],
            "group2": [
                {
                    "bk_host_innerip": "2.2.2.2",
                    "bk_host_outerip": "2.2.2.2",
                    "bk_host_name": "2.2.2.2",
                    "bk_host_id": 2,
                    "bk_cloud_id": 0,
                    "host_modules_id": [5],
                },
                {
                    "bk_host_innerip": "3.3.3.3",
                    "bk_host_outerip": "3.3.3.3",
                    "bk_host_name": "3.3.3.3",
                    "bk_host_id": 3,
                    "bk_cloud_id": 0,
                    "host_modules_id": [8],
                },
            ],
        }
        return True, {"code": 0, "message": "success", "data": dynamic_group_data[args[-2]]}


def mock_cc_get_ips_info_by_str(username, bk_biz_id, ip_str):
    return {
        "result": True,
        "ip_count": 2,
        "ip_result": [
            {
                "ModuleID": 8,
                "HostID": 3,
                "InnerIP": "3.3.3.3",
                "SetID": 4,
                "Sets": [{"bk_set_id": 4}],
                "Modules": [{"bk_module_id": 8}],
                "Source": 0,
            },
            {
                "ModuleID": 5,
                "HostID": 2,
                "InnerIP": "2.2.2.2",
                "SetID": 3,
                "Sets": [{"bk_set_id": 3}],
                "Modules": [{"bk_module_id": 5}],
                "Source": 0,
            },
        ],
        "invalid_ip": [],
    }


def mock_get_client_by_user(username):
    class MockCC(object):
        def __init__(self, success):
            self.success = success

        def search_biz_inst_topo(self, kwargs):
            return {
                "result": self.success,
                "data": [
                    {
                        "default": 0,
                        "bk_obj_name": "业务",
                        "bk_obj_id": "biz",
                        "child": [
                            {
                                "bk_bj_name": "middle_layer",
                                "bk_obj_id": "layer",
                                "bk_inst_id": 1,
                                "bk_inst_name": "中间层",
                                "child": [
                                    {
                                        "default": 0,
                                        "bk_obj_name": "集群",
                                        "bk_obj_id": "set",
                                        "child": [
                                            {
                                                "default": 0,
                                                "bk_obj_name": "模块",
                                                "bk_obj_id": "module",
                                                "bk_inst_id": 5,
                                                "bk_inst_name": "test1",
                                            },
                                            {
                                                "default": 0,
                                                "bk_obj_name": "模块",
                                                "bk_obj_id": "module",
                                                "bk_inst_id": 6,
                                                "bk_inst_name": "test2",
                                            },
                                            {
                                                "default": 0,
                                                "bk_obj_name": "模块",
                                                "bk_obj_id": "module",
                                                "bk_inst_id": 7,
                                                "bk_inst_name": "test3",
                                            },
                                        ],
                                        "bk_inst_id": 3,
                                        "bk_inst_name": "set2",
                                    },
                                    {
                                        "default": 0,
                                        "bk_obj_name": "集群",
                                        "bk_obj_id": "set",
                                        "child": [
                                            {
                                                "default": 0,
                                                "bk_obj_name": "模块",
                                                "bk_obj_id": "module",
                                                "bk_inst_id": 8,
                                                "bk_inst_name": "test1",
                                            },
                                            {
                                                "default": 0,
                                                "bk_obj_name": "模块",
                                                "bk_obj_id": "module",
                                                "bk_inst_id": 9,
                                                "bk_inst_name": "test2",
                                            },
                                        ],
                                        "bk_inst_id": 4,
                                        "bk_inst_name": "set3",
                                    },
                                ],
                            },
                        ],
                        "bk_inst_id": 2,
                        "bk_inst_name": "蓝鲸",
                    }
                ],
                "message": "error",
            }

        def search_dynamic_group(self, page, **kwargs):
            return {
                "result": True,
                "data": {
                    "count": 1,
                    "info": [
                        {"id": "group1", "bk_obj_id": "host", "name": "group1-name"},
                        {"id": "group2", "bk_obj_id": "host", "name": "group2-name"},
                    ],
                },
            }

        def get_biz_internal_module(self, kwargs):
            return {
                "result": self.success,
                "data": {
                    "bk_set_id": 2,
                    "bk_set_name": "空闲机池",
                    "module": [
                        {
                            "default": 1,
                            "bk_obj_id": "module",
                            "bk_module_id": 3,
                            "bk_obj_name": "模块",
                            "bk_module_name": "空闲机",
                        },
                        {
                            "default": 1,
                            "bk_obj_id": "module",
                            "bk_module_id": 4,
                            "bk_obj_name": "模块",
                            "bk_module_name": "故障机",
                        },
                    ],
                },
                "message": "error",
            }

    class MockClient(object):
        def __init__(self, success):
            self.cc = MockCC(success)

    return MockClient(mock_get_client_by_user.success)


class GetIPPickerResultTestCase(TestCase):
    def setUp(self):
        self.username = "admin"
        self.bk_biz_id = "2"
        self.bk_supplier_account = 0

    @patch("pipeline_plugins.cmdb_ip_picker.utils.cmdb", MockCMDBReturnEmpty)
    @patch("pipeline_plugins.cmdb_ip_picker.utils.get_client_by_user", mock_get_client_by_user)
    def test__get_business_host_topo_return_empty(self):
        mock_get_client_by_user.success = True
        topo_kwargs = {
            "bk_biz_id": self.bk_biz_id,
            "selectors": ["topo"],
            "topo": [],
            "ip": [],
            "filters": [],
            "excludes": [],
        }
        self.assertFalse(
            get_ip_picker_result(self.username, self.bk_biz_id, self.bk_supplier_account, topo_kwargs)["result"]
        )

    @patch("pipeline_plugins.cmdb_ip_picker.utils.cmdb", MockCMDB)
    @patch("pipeline_plugins.cmdb_ip_picker.utils.get_client_by_user", mock_get_client_by_user)
    @patch("pipeline_plugins.cmdb_ip_picker.utils.cc_get_ips_info_by_str", mock_cc_get_ips_info_by_str)
    def test__manual_selector_ip(self):
        mock_get_client_by_user.success = True
        ip_kwargs = {
            "bk_biz_id": self.bk_biz_id,
            "selectors": ["manual"],
            "topo": [],
            "manual_input": {"type": "ip", "value": "2.2.2.2,3.3.3.3"},
            "ip": [],
            "filters": [],
            "excludes": [],
        }
        ip_data = get_ip_picker_result(self.username, self.bk_biz_id, self.bk_supplier_account, ip_kwargs)["data"]
        ip = [host["bk_host_innerip"] for host in ip_data]
        self.assertEqual(ip, ["2.2.2.2", "3.3.3.3"])

    @patch("pipeline_plugins.cmdb_ip_picker.utils.cmdb", MockCMDB)
    @patch("pipeline_plugins.cmdb_ip_picker.utils.get_client_by_user", mock_get_client_by_user)
    def test__manual_selector_topo(self):
        mock_get_client_by_user.success = True
        topo_kwargs = {
            "bk_biz_id": self.bk_biz_id,
            "selectors": ["manual"],
            "topo": [],
            "manual_input": {"type": "topo", "value": "蓝鲸>中间层>set2,蓝鲸>中间层>set2>test1,蓝鲸>中间层>set3>test1"},
            "ip": [],
            "filters": [],
            "excludes": [],
        }
        ip_data = get_ip_picker_result(self.username, self.bk_biz_id, self.bk_supplier_account, topo_kwargs)["data"]
        ip = [host["bk_host_innerip"] for host in ip_data]
        self.assertEqual(ip, ["2.2.2.2", "3.3.3.3"])

    @patch("pipeline_plugins.cmdb_ip_picker.utils.cmdb", MockCMDB)
    @patch("pipeline_plugins.cmdb_ip_picker.utils.get_client_by_user", mock_get_client_by_user)
    def test__selector_topo(self):
        mock_get_client_by_user.success = True
        topo_kwargs = {
            "bk_biz_id": self.bk_biz_id,
            "selectors": ["topo"],
            "topo": [{"bk_obj_id": "set", "bk_inst_id": 2}],
            "ip": [],
            "filters": [],
            "excludes": [],
        }
        ip_data = get_ip_picker_result(self.username, self.bk_biz_id, self.bk_supplier_account, topo_kwargs)["data"]
        ip = [host["bk_host_innerip"] for host in ip_data]
        self.assertEqual(ip, ["1.1.1.1"])

        topo_kwargs = {
            "bk_biz_id": self.bk_biz_id,
            "selectors": ["topo"],
            "topo": [{"bk_obj_id": "set", "bk_inst_id": 3}, {"bk_obj_id": "module", "bk_inst_id": 5}],
            "ip": [],
            "filters": [],
            "excludes": [],
        }
        ip_data = get_ip_picker_result(self.username, self.bk_biz_id, self.bk_supplier_account, topo_kwargs)["data"]
        ip = [host["bk_host_innerip"] for host in ip_data]
        self.assertEqual(ip, ["2.2.2.2"])

        topo_kwargs = {
            "bk_biz_id": self.bk_biz_id,
            "selectors": ["topo"],
            "topo": [{"bk_obj_id": "biz", "bk_inst_id": 2}],
            "ip": [],
            "filters": [],
            "excludes": [],
        }
        ip_data = get_ip_picker_result(self.username, self.bk_biz_id, self.bk_supplier_account, topo_kwargs)["data"]
        ip = [host["bk_host_innerip"] for host in ip_data]
        self.assertEqual(ip, ["1.1.1.1", "2.2.2.2", "3.3.3.3"])

    @patch("pipeline_plugins.cmdb_ip_picker.utils.cmdb", MockCMDB)
    @patch("pipeline_plugins.cmdb_ip_picker.utils.get_client_by_user", mock_get_client_by_user)
    def test__manual_selector_group(self):
        mock_get_client_by_user.success = True
        group_kwargs = {
            "bk_biz_id": self.bk_biz_id,
            "selectors": ["manual"],
            "topo": [],
            "ip": [],
            "group": [{"id": "group_to_be_replaced"}],
            "manual_input": {"type": "group", "value": "group1-name,group2-name"},
            "filters": [],
            "excludes": [],
        }
        ip_data = get_ip_picker_result(self.username, self.bk_biz_id, self.bk_supplier_account, group_kwargs)["data"]
        ip = [host["bk_host_innerip"] for host in ip_data]
        self.assertEqual(ip, ["1.1.1.1", "2.2.2.2", "3.3.3.3"])

    @patch("pipeline_plugins.cmdb_ip_picker.utils.cmdb", MockCMDB)
    @patch("pipeline_plugins.cmdb_ip_picker.utils.get_client_by_user", mock_get_client_by_user)
    def test__selector_group(self):
        mock_get_client_by_user.success = True
        group_kwargs = {
            "bk_biz_id": self.bk_biz_id,
            "selectors": ["group"],
            "topo": [],
            "ip": [],
            "group": [{"id": "group1"}],
            "filters": [],
            "excludes": [],
        }
        ip_data = get_ip_picker_result(self.username, self.bk_biz_id, self.bk_supplier_account, group_kwargs)["data"]
        ip = [host["bk_host_innerip"] for host in ip_data]
        self.assertEqual(ip, ["1.1.1.1", "2.2.2.2"])

        group_kwargs = {
            "bk_biz_id": self.bk_biz_id,
            "selectors": ["group"],
            "topo": [],
            "group": [{"id": "group1"}, {"id": "group2"}],
            "ip": [],
            "filters": [],
            "excludes": [],
        }
        ip_data = get_ip_picker_result(self.username, self.bk_biz_id, self.bk_supplier_account, group_kwargs)["data"]
        ip = [host["bk_host_innerip"] for host in ip_data]
        self.assertEqual(ip, ["1.1.1.1", "2.2.2.2", "3.3.3.3"])

    @patch("pipeline_plugins.cmdb_ip_picker.utils.cmdb", MockCMDB)
    @patch("pipeline_plugins.cmdb_ip_picker.utils.get_client_by_user", mock_get_client_by_user)
    def test__filter_ip_in_group(self):
        mock_get_client_by_user.success = True
        group_kwargs = {
            "bk_biz_id": self.bk_biz_id,
            "selectors": ["group"],
            "topo": [],
            "ip": [],
            "group": [{"id": "group1"}],
            "filters": [{"field": "set", "value": ["set2"]}],
            "excludes": [],
        }
        ip_data = get_ip_picker_result(self.username, self.bk_biz_id, self.bk_supplier_account, group_kwargs)["data"]
        ip = [host["bk_host_innerip"] for host in ip_data]
        self.assertEqual(ip, ["2.2.2.2"])

    @patch("pipeline_plugins.cmdb_ip_picker.utils.cmdb", MockCMDB)
    @patch("pipeline_plugins.cmdb_ip_picker.utils.get_client_by_user", mock_get_client_by_user)
    def test__select_topo_with_diff_layer(self):
        mock_get_client_by_user.success = True
        topo_kwargs = {
            "bk_biz_id": self.bk_biz_id,
            "selectors": ["topo"],
            "topo": [{"bk_obj_id": "set", "bk_inst_id": 2}, {"bk_obj_id": "module", "bk_inst_id": 5}],
            "ip": [],
            "filters": [],
            "excludes": [],
        }
        ip_data = get_ip_picker_result(self.username, self.bk_biz_id, self.bk_supplier_account, topo_kwargs)["data"]
        ip = [host["bk_host_innerip"] for host in ip_data]
        self.assertEqual(ip, ["1.1.1.1", "2.2.2.2"])

        topo_kwargs = {
            "bk_biz_id": self.bk_biz_id,
            "selectors": ["topo"],
            "topo": [
                {"bk_obj_id": "set", "bk_inst_id": 2},
                {"bk_obj_id": "module", "bk_inst_id": 5},
                {"bk_obj_id": "module", "bk_inst_id": 8},
            ],
            "ip": [],
            "filters": [],
            "excludes": [],
        }
        ip_data = get_ip_picker_result(self.username, self.bk_biz_id, self.bk_supplier_account, topo_kwargs)["data"]
        ip = [host["bk_host_innerip"] for host in ip_data]
        self.assertEqual(ip, ["1.1.1.1", "2.2.2.2", "3.3.3.3"])

    @patch("pipeline_plugins.cmdb_ip_picker.utils.cmdb", MockCMDB)
    @patch("pipeline_plugins.cmdb_ip_picker.utils.get_client_by_user", mock_get_client_by_user)
    def test__selector_ip(self):
        mock_get_client_by_user.success = True
        topo_kwargs = {
            "bk_biz_id": self.bk_biz_id,
            "selectors": ["ip"],
            "topo": [],
            "ip": [
                {
                    "bk_host_name": "host1",
                    "bk_host_id": 2,
                    "agent": 1,
                    "cloud": [
                        {
                            "bk_obj_name": "",
                            "id": "0",
                            "bk_obj_id": "plat",
                            "bk_obj_icon": "",
                            "bk_inst_id": 0,
                            "bk_inst_name": "default area",
                        }
                    ],
                    "bk_host_innerip": "1.1.1.1",
                },
                {
                    "bk_host_name": "host2",
                    "bk_host_id": 2,
                    "agent": 1,
                    "cloud": [
                        {
                            "bk_obj_name": "",
                            "id": "0",
                            "bk_obj_id": "plat",
                            "bk_obj_icon": "",
                            "bk_inst_id": 0,
                            "bk_inst_name": "default area",
                        }
                    ],
                    "bk_host_innerip": "2.2.2.2",
                },
            ],
            "filters": [],
            "excludes": [],
        }
        ip_data = get_ip_picker_result(self.username, self.bk_biz_id, self.bk_supplier_account, topo_kwargs)["data"]
        ip = [host["bk_host_innerip"] for host in ip_data]
        self.assertEqual(ip, ["1.1.1.1", "2.2.2.2"])

    @patch("pipeline_plugins.cmdb_ip_picker.utils.cmdb", MockCMDB)
    @patch("pipeline_plugins.cmdb_ip_picker.utils.get_client_by_user", mock_get_client_by_user)
    def test__filters_topo_in_topo(self):
        mock_get_client_by_user.success = True
        topo_kwargs = {
            "bk_biz_id": self.bk_biz_id,
            "selectors": ["topo"],
            "topo": [{"bk_obj_id": "biz", "bk_inst_id": 2}],
            "ip": [],
            "filters": [{"field": "set", "value": ["set2"]}],
            "excludes": [],
        }
        ip_data = get_ip_picker_result(self.username, self.bk_biz_id, self.bk_supplier_account, topo_kwargs)["data"]
        ip = [host["bk_host_innerip"] for host in ip_data]
        self.assertEqual(ip, ["2.2.2.2"])

    @patch("pipeline_plugins.cmdb_ip_picker.utils.cmdb", MockCMDB)
    @patch("pipeline_plugins.cmdb_ip_picker.utils.get_client_by_user", mock_get_client_by_user)
    def test__excludes_topo_in_topo(self):
        mock_get_client_by_user.success = True
        topo_kwargs = {
            "bk_biz_id": self.bk_biz_id,
            "selectors": ["topo"],
            "topo": [{"bk_obj_id": "biz", "bk_inst_id": 2}],
            "ip": [],
            "filters": [],
            "excludes": [{"field": "set", "value": ["set2"]}],
        }
        ip_data = get_ip_picker_result(self.username, self.bk_biz_id, self.bk_supplier_account, topo_kwargs)["data"]
        ip = [host["bk_host_innerip"] for host in ip_data]
        self.assertEqual(ip, ["1.1.1.1", "3.3.3.3"])

    @patch("pipeline_plugins.cmdb_ip_picker.utils.cmdb", MockCMDB)
    @patch("pipeline_plugins.cmdb_ip_picker.utils.get_client_by_user", mock_get_client_by_user)
    def test__filters_and_excludes_topo_in_topo(self):
        mock_get_client_by_user.success = True
        topo_kwargs = {
            "bk_biz_id": self.bk_biz_id,
            "selectors": ["topo"],
            "topo": [{"bk_obj_id": "biz", "bk_inst_id": 2}],
            "ip": [],
            "filters": [{"field": "set", "value": ["set2"]}, {"field": "set", "value": ["set3"]}],
            "excludes": [{"field": "set", "value": ["set3"]}],
        }
        ip_data = get_ip_picker_result(self.username, self.bk_biz_id, self.bk_supplier_account, topo_kwargs)["data"]
        ip = [host["bk_host_innerip"] for host in ip_data]
        self.assertEqual(ip, ["2.2.2.2"])

    @patch("pipeline_plugins.cmdb_ip_picker.utils.cmdb", MockCMDB)
    @patch("pipeline_plugins.cmdb_ip_picker.utils.get_client_by_user", mock_get_client_by_user)
    def test__filters_middle_layer_in_topo(self):
        mock_get_client_by_user.success = True
        topo_kwargs = {
            "bk_biz_id": self.bk_biz_id,
            "selectors": ["topo"],
            "topo": [{"bk_obj_id": "biz", "bk_inst_id": 2}],
            "ip": [],
            "filters": [{"field": "layer", "value": ["中间层"]}],
            "excludes": [],
        }
        ip_data = get_ip_picker_result(self.username, self.bk_biz_id, self.bk_supplier_account, topo_kwargs)["data"]
        ip = [host["bk_host_innerip"] for host in ip_data]
        self.assertEqual(ip, ["2.2.2.2", "3.3.3.3"])

    @patch("pipeline_plugins.cmdb_ip_picker.utils.cmdb", MockCMDB)
    @patch("pipeline_plugins.cmdb_ip_picker.utils.get_client_by_user", mock_get_client_by_user)
    def test__filters_and_excludes_middle_layer_in_topo(self):
        mock_get_client_by_user.success = True
        topo_kwargs = {
            "bk_biz_id": self.bk_biz_id,
            "selectors": ["topo"],
            "topo": [{"bk_obj_id": "biz", "bk_inst_id": 2}],
            "ip": [],
            "filters": [{"field": "layer", "value": ["中间层"]}],
            "excludes": [{"field": "set", "value": ["set2"]}],
        }
        ip_data = get_ip_picker_result(self.username, self.bk_biz_id, self.bk_supplier_account, topo_kwargs)["data"]
        ip = [host["bk_host_innerip"] for host in ip_data]
        self.assertEqual(ip, ["3.3.3.3"])

    @patch("pipeline_plugins.cmdb_ip_picker.utils.cmdb", MockCMDB)
    @patch("pipeline_plugins.cmdb_ip_picker.utils.get_client_by_user", mock_get_client_by_user)
    def test__filter_ip_in_topo(self):
        mock_get_client_by_user.success = True
        topo_kwargs = {
            "bk_biz_id": self.bk_biz_id,
            "selectors": ["topo"],
            "topo": [{"bk_obj_id": "biz", "bk_inst_id": 2}],
            "ip": [],
            "filters": [{"field": "host", "value": ["1.1.1.1", "2.2.2.2"]}],
            "excludes": [],
        }
        ip_data = get_ip_picker_result(self.username, self.bk_biz_id, self.bk_supplier_account, topo_kwargs)["data"]
        ip = [host["bk_host_innerip"] for host in ip_data]
        self.assertEqual(ip, ["1.1.1.1", "2.2.2.2"])

    @patch("pipeline_plugins.cmdb_ip_picker.utils.cmdb", MockCMDB)
    @patch("pipeline_plugins.cmdb_ip_picker.utils.get_client_by_user", mock_get_client_by_user)
    def test__filter_ip_in_hosts(self):
        mock_get_client_by_user.success = True
        topo_kwargs = {
            "bk_biz_id": self.bk_biz_id,
            "selectors": ["ip"],
            "topo": [],
            "ip": [
                {"bk_host_innerip": "1.1.1.1", "cloud": [{"id": 0}]},
                {"bk_host_innerip": "2.2.2.2", "cloud": [{"id": 0}]},
                {"bk_host_innerip": "3.3.3.3", "cloud": [{"id": 0}]},
            ],
            "filters": [{"field": "host", "value": ["1.1.1.1", "2.2.2.2"]}],
            "excludes": [],
        }
        ip_data = get_ip_picker_result(self.username, self.bk_biz_id, self.bk_supplier_account, topo_kwargs)["data"]
        ip = [host["bk_host_innerip"] for host in ip_data]
        self.assertEqual(ip, ["1.1.1.1", "2.2.2.2"])

    @patch("pipeline_plugins.cmdb_ip_picker.utils.cmdb", MockCMDB)
    @patch("pipeline_plugins.cmdb_ip_picker.utils.get_client_by_user", mock_get_client_by_user)
    def test__exclude_ip_in_topo(self):
        mock_get_client_by_user.success = True
        topo_kwargs = {
            "bk_biz_id": self.bk_biz_id,
            "selectors": ["topo"],
            "topo": [{"bk_obj_id": "biz", "bk_inst_id": 2}],
            "ip": [],
            "excludes": [{"field": "host", "value": ["1.1.1.1", "2.2.2.2"]}],
            "filters": [],
        }
        ip_data = get_ip_picker_result(self.username, self.bk_biz_id, self.bk_supplier_account, topo_kwargs)["data"]
        ip = [host["bk_host_innerip"] for host in ip_data]
        self.assertEqual(ip, ["3.3.3.3"])

    @patch("pipeline_plugins.cmdb_ip_picker.utils.cmdb", MockCMDB)
    @patch("pipeline_plugins.cmdb_ip_picker.utils.get_client_by_user", mock_get_client_by_user)
    def test__exclude_ip_in_hosts(self):
        mock_get_client_by_user.success = True
        topo_kwargs = {
            "bk_biz_id": self.bk_biz_id,
            "selectors": ["ip"],
            "topo": [],
            "ip": [
                {"bk_host_innerip": "1.1.1.1", "cloud": [{"id": 0}]},
                {"bk_host_innerip": "2.2.2.2", "cloud": [{"id": 0}]},
                {"bk_host_innerip": "3.3.3.3", "cloud": [{"id": 0}]},
            ],
            "excludes": [{"field": "host", "value": ["1.1.1.1", "2.2.2.2"]}],
            "filters": [],
        }
        ip_data = get_ip_picker_result(self.username, self.bk_biz_id, self.bk_supplier_account, topo_kwargs)["data"]
        ip = [host["bk_host_innerip"] for host in ip_data]
        self.assertEqual(ip, ["3.3.3.3"])

    @patch("pipeline_plugins.cmdb_ip_picker.utils.cmdb", MockCMDB)
    @patch("pipeline_plugins.cmdb_ip_picker.utils.get_client_by_user", mock_get_client_by_user)
    def test__exclude_ip_in_group(self):
        mock_get_client_by_user.success = True
        group_kwargs = {
            "bk_biz_id": self.bk_biz_id,
            "selectors": ["group"],
            "topo": [],
            "group": [{"id": "group1"}, {"id": "group2"}],
            "ip": [],
            "excludes": [{"field": "host", "value": ["1.1.1.1", "2.2.2.2"]}],
            "filters": [],
        }
        ip_data = get_ip_picker_result(self.username, self.bk_biz_id, self.bk_supplier_account, group_kwargs)["data"]
        ip = [host["bk_host_innerip"] for host in ip_data]
        self.assertEqual(ip, ["3.3.3.3"])

    @patch("pipeline_plugins.cmdb_ip_picker.utils.cmdb", MockCMDB)
    @patch("pipeline_plugins.cmdb_ip_picker.utils.get_client_by_user", mock_get_client_by_user)
    def test__filters_topo_and_excludes_ip_in_topo(self):
        mock_get_client_by_user.success = True
        topo_kwargs = {
            "bk_biz_id": self.bk_biz_id,
            "selectors": ["topo"],
            "topo": [{"bk_obj_id": "biz", "bk_inst_id": 2}],
            "ip": [],
            "filters": [{"field": "set", "value": ["set2"]}, {"field": "set", "value": ["set3"]}],
            "excludes": [{"field": "host", "value": ["2.2.2.2"]}],
        }
        ip_data = get_ip_picker_result(self.username, self.bk_biz_id, self.bk_supplier_account, topo_kwargs)["data"]
        ip = [host["bk_host_innerip"] for host in ip_data]
        self.assertEqual(ip, ["3.3.3.3"])

    @patch("pipeline_plugins.cmdb_ip_picker.utils.cmdb", MockCMDB)
    @patch("pipeline_plugins.cmdb_ip_picker.utils.get_client_by_user", mock_get_client_by_user)
    def test__filters_ip_and_excludes_topo_in_topo(self):
        mock_get_client_by_user.success = True
        topo_kwargs = {
            "bk_biz_id": self.bk_biz_id,
            "selectors": ["topo"],
            "topo": [{"bk_obj_id": "biz", "bk_inst_id": 2}],
            "ip": [],
            "excludes": [{"field": "set", "value": ["set2"]}],
            "filters": [{"field": "host", "value": ["2.2.2.2", "3.3.3.3"]}],
        }
        ip_data = get_ip_picker_result(self.username, self.bk_biz_id, self.bk_supplier_account, topo_kwargs)["data"]
        ip = [host["bk_host_innerip"] for host in ip_data]
        self.assertEqual(ip, ["3.3.3.3"])
