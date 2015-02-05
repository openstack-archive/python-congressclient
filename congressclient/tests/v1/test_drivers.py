#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#

import mock

from congressclient.osc.v1 import driver
from congressclient.tests import common


class TestListDrivers(common.TestCongressBase):

    def test_list_drivers(self):
        arglist = [
        ]
        verifylist = [
        ]
        response = {
            "results": [{"id": "neutronv2",
                         "description": "this does blah.."}]
        }
        lister = mock.Mock(return_value=response)
        self.app.client_manager.congressclient.list_drivers = lister
        cmd = driver.ListDrivers(self.app, self.namespace)

        parsed_args = self.check_parser(cmd, arglist, verifylist)
        result = cmd.take_action(parsed_args)

        lister.assert_called_with()
        self.assertEqual(['id', 'description'], result[0])


class TestShowDriverSchema(common.TestCongressBase):

    def test_show_driver_shema(self):
        arglist = [
            "neutronv2"
        ]
        verifylist = [
            ('driver', "neutronv2")
        ]

        response = {
            "tables":
                [{'table_id': 'ports',
                  'columns': [{"name": "name", "description": "None"},
                              {"name": "status", "description": "None"},
                              {"name": "id", "description": "None"}]},
                 {'table_id': 'routers',
                  'columns': [{"name": "name", "description": "None"},
                              {"name": "floating_ip", "description": "None"},
                              {"name": "id", "description": "None"}]}]
        }
        lister = mock.Mock(return_value=response)
        self.app.client_manager.congressclient.show_driver = lister
        cmd = driver.ShowDriverSchema(self.app, self.namespace)

        parsed_args = self.check_parser(cmd, arglist, verifylist)
        result = cmd.take_action(parsed_args)

        lister.assert_called_with("neutronv2")
        self.assertEqual(['table', 'columns'], result[0])


class TestShowDriverConfig(common.TestCongressBase):

    def test_show_driver_config(self):
        arglist = [
            "neutronv2"
        ]
        verifylist = [
            ('driver', "neutronv2")
        ]

        response = {
            "tables": [],
            'id': 'aabbcc',
            'description': 'foobar',
            'config': {'password': 'password'},
        }
        mocker = mock.Mock(return_value=response)
        self.app.client_manager.congressclient.show_driver = mocker
        cmd = driver.ShowDriverConfig(self.app, self.namespace)

        parsed_args = self.check_parser(cmd, arglist, verifylist)
        result = list(cmd.take_action(parsed_args))

        mocker.assert_called_with("neutronv2")
        filtered = [('config', 'description', 'id'),
                    (response['config'], response['description'],
                     response['id'])]
        self.assertEqual(filtered, result)
