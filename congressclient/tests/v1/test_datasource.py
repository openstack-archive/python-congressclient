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

from congressclient.osc.v1 import datasource
from congressclient.tests import common


class TestListDatasources(common.TestCongressBase):
    def test_list_datasource(self):
        datasource_name = 'neutron'
        arglist = [
        ]
        verifylist = [
        ]
        response = {
            "results": [{"id": datasource_name,
                         "owner_id": "system",
                         "enabled": "True",
                         "type": "None",
                         "config": "None"}]
        }
        lister = mock.Mock(return_value=response)
        self.app.client_manager.congressclient.list_datasources = lister
        cmd = datasource.ListDatasources(self.app, self.namespace)

        parsed_args = self.check_parser(cmd, arglist, verifylist)
        result = cmd.take_action(parsed_args)

        lister.assert_called_with()
        self.assertEqual(['id', 'owner_id', 'enabled', 'type', 'config'],
                         result[0])


class TestListDatasourceTables(common.TestCongressBase):
    def test_list_datasource_tables(self):
        datasource_name = 'neutron'
        arglist = [
            datasource_name
        ]
        verifylist = [
            ('datasource_name', datasource_name)
        ]
        response = {
            "results": [{"id": "ports"},
                        {"id": "networks"}]
        }
        lister = mock.Mock(return_value=response)
        self.app.client_manager.congressclient.list_datasource_tables = lister
        cmd = datasource.ListDatasourceTables(self.app, self.namespace)

        parsed_args = self.check_parser(cmd, arglist, verifylist)
        result = cmd.take_action(parsed_args)

        lister.assert_called_with(datasource_name)
        self.assertEqual(['id'], result[0])


class TestListDatasourceRows(common.TestCongressBase):

    def test_list_datasource_row(self):
        datasource_name = 'neutron'
        table_name = 'ports'
        arglist = [
            datasource_name, table_name
        ]
        verifylist = [
            ('datasource_name', datasource_name),
            ('table', table_name)
        ]
        response = {
            "results": [{"data": ["69abc88b-c950-4625-801b-542e84381509",
                                  "default"]}]
        }

        lister = mock.Mock(return_value=response)
        self.app.client_manager.congressclient.list_datasource_rows = lister
        cmd = datasource.ListDatasourceRows(self.app, self.namespace)

        parsed_args = self.check_parser(cmd, arglist, verifylist)
        result = cmd.take_action(parsed_args)

        lister.assert_called_with(datasource_name, table_name)
        self.assertEqual(['Col0', 'Col1'], result[0])
