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
from oslo_serialization import jsonutils

from congressclient.common import utils
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
                         "name": "my_name",
                         "enabled": "True",
                         "driver": "driver1",
                         "config": None}]
        }
        lister = mock.Mock(return_value=response)
        self.app.client_manager.congressclient.list_datasources = lister
        cmd = datasource.ListDatasources(self.app, self.namespace)

        parsed_args = self.check_parser(cmd, arglist, verifylist)
        result = cmd.take_action(parsed_args)

        lister.assert_called_with()
        self.assertEqual(['id', 'name', 'enabled', 'driver', 'config'],
                         result[0])
        for row in result[1]:
            self.assertEqual(datasource_name, row[0])
            self.assertEqual("my_name", row[1])
            self.assertEqual("True", row[2])
            self.assertEqual("driver1", row[3])
            self.assertEqual("None", row[4])

    def test_list_datasource_output_not_unicode(self):
        # response json string is converted to dict by oslo jsonutils.loads(),
        # so the key and value in the dict should be unicode type.
        response = {
            u"results": [{u"id": u"neutron",
                          u"name": u"my_name",
                          u"enabled": True,
                          u"driver": 'driver1',
                          u"config": {
                              u'username': u'admin',
                              u'project_name': u'admin',
                              u'poll_time': u'10',
                              u'password': u'<hidden>',
                              u'auth_url': u'http://127.0.0.1:5000/v2.0'
                          }}]
        }
        lister = mock.Mock(return_value=response)
        self.app.client_manager.congressclient.list_datasources = lister
        cmd = datasource.ListDatasources(self.app, self.namespace)

        parsed_args = self.check_parser(cmd, [], [])
        result = cmd.take_action(parsed_args)

        lister.assert_called_with()
        self.assertEqual(['id', 'name', 'enabled', 'driver', 'config'],
                         result[0])
        # get 'config' column
        config = list(result[1])[0][-1]
        self.assertIn("'username': 'admin'", config)
        self.assertNotIn("u'username': u'admin'", config)


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


class TestListDatasourceStatus(common.TestCongressBase):
    def test_list_datasource_status(self):
        datasource_name = 'neutron'
        arglist = [
            datasource_name
        ]
        verifylist = [
            ('datasource_name', datasource_name)
        ]
        response = {'last_updated': "now",
                    'last_error': "None"}
        lister = mock.Mock(return_value=response)
        self.app.client_manager.congressclient.list_datasource_status = lister
        cmd = datasource.ShowDatasourceStatus(self.app, self.namespace)

        parsed_args = self.check_parser(cmd, arglist, verifylist)
        result = list(cmd.take_action(parsed_args))

        lister.assert_called_with(datasource_name)
        self.assertEqual([('last_error', 'last_updated'),
                          ('None', 'now')],
                         result)


class TestShowDatasourceActions(common.TestCongressBase):
    def test_show_datasource_actions(self):
        datasource_name = 'fake'
        arglist = [
            datasource_name
        ]
        verifylist = [
            ('datasource_name', datasource_name)
        ]
        response = {
            "results":
                [{'name': 'execute',
                  'args': [{"name": "name", "description": "None"},
                           {"name": "status", "description": "None"},
                           {"name": "id", "description": "None"}],
                  'description': 'execute action'}]
        }
        lister = mock.Mock(return_value=response)
        self.app.client_manager.congressclient.list_datasource_actions = lister
        cmd = datasource.ShowDatasourceActions(self.app, self.namespace)

        parsed_args = self.check_parser(cmd, arglist, verifylist)
        result = cmd.take_action(parsed_args)

        lister.assert_called_once_with(datasource_name)
        self.assertEqual(['action', 'args', 'description'], result[0])


class TestShowDatasourceSchema(common.TestCongressBase):
    def test_show_datasource_schema(self):
        datasource_name = 'neutron'
        arglist = [
            datasource_name
        ]
        verifylist = [
            ('datasource_name', datasource_name)
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
        self.app.client_manager.congressclient.show_datasource_schema = lister
        cmd = datasource.ShowDatasourceSchema(self.app, self.namespace)

        parsed_args = self.check_parser(cmd, arglist, verifylist)
        result = cmd.take_action(parsed_args)

        lister.assert_called_with(datasource_name)
        self.assertEqual(['table', 'columns'], result[0])


class TestShowDatasourceTableSchema(common.TestCongressBase):
    def test_show_datasource_table_schema(self):
        datasource_name = 'neutron'
        table_name = 'ports'
        arglist = [
            datasource_name, table_name
        ]
        verifylist = [
            ('datasource_name', datasource_name),
            ('table_name', table_name)
        ]
        response = {
            'table_id': 'ports',
            'columns': [{"name": "name", "description": "None"},
                        {"name": "status", "description": "None"},
                        {"name": "id", "description": "None"}]
        }
        lister = mock.Mock(return_value=response)
        client = self.app.client_manager.congressclient
        client.show_datasource_table_schema = lister
        cmd = datasource.ShowDatasourceTableSchema(self.app, self.namespace)

        parsed_args = self.check_parser(cmd, arglist, verifylist)
        result = cmd.take_action(parsed_args)

        lister.assert_called_with(datasource_name, table_name)
        self.assertEqual(['name', 'description'], result[0])


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
        schema_response = {
            'table_id': 'ports',
            'columns': [{"name": "ID", "description": "None"},
                        {"name": "name", "description": "None"}]
        }

        client = self.app.client_manager.congressclient
        lister = mock.Mock(return_value=response)
        client.list_datasource_rows = lister
        schema_lister = mock.Mock(return_value=schema_response)
        client.show_datasource_table_schema = schema_lister
        cmd = datasource.ListDatasourceRows(self.app, self.namespace)

        parsed_args = self.check_parser(cmd, arglist, verifylist)
        result = cmd.take_action(parsed_args)

        lister.assert_called_with(datasource_name, table_name)
        self.assertEqual(['ID', 'name'], result[0])


class TestShowDatasourceTable(common.TestCongressBase):
    def test_show_datasource_table(self):
        datasource_name = 'neutron'
        table_id = 'ports'
        arglist = [
            datasource_name, table_id
        ]
        verifylist = [
            ('datasource_name', datasource_name),
            ('table_id', table_id)
        ]
        response = {
            'id': 'ports',
        }
        lister = mock.Mock(return_value=response)
        client = self.app.client_manager.congressclient
        client.show_datasource_table = lister
        cmd = datasource.ShowDatasourceTable(self.app, self.namespace)
        expected_ret = [('id',), ('ports',)]

        parsed_args = self.check_parser(cmd, arglist, verifylist)
        result = list(cmd.take_action(parsed_args))

        self.assertEqual(expected_ret, result)


class TestCreateDatasource(common.TestCongressBase):

    def test_create_datasource(self):
        driver = 'neutronv2'
        name = 'arosen-neutronv2'
        response = {"description": '',
                    "config": {"username": "admin",
                               "project_name": "admin",
                               "password": "password",
                               "auth_url": "http://127.0.0.1:5000/v2.0"},
                    "enabled": True,
                    "owner": "user",
                    "driver": "neutronv2",
                    "type": None,
                    "id": "b72f81a0-32b5-4bf4-a1f6-d69c09c42cec",
                    "name": "arosen-neutronv2"}

        arglist = [driver, name,
                   "--config", "username=admin",
                   "--config", "password=password",
                   "--config", "auth_url=http://1.1.1.1/foo",
                   "--config", "project_name=admin"]
        verifylist = [
            ('driver', driver),
            ('name', name),
            ('config', {'username': 'admin', 'password': 'password',
                        'auth_url': 'http://1.1.1.1/foo',
                        'project_name': 'admin'}),
        ]

        mocker = mock.Mock(return_value=response)
        self.app.client_manager.congressclient.create_datasource = mocker
        cmd = datasource.CreateDatasource(self.app, self.namespace)
        parsed_args = self.check_parser(cmd, arglist, verifylist)
        result = list(cmd.take_action(parsed_args))
        filtered = [('config', 'description',
                     'driver', 'enabled', 'id', 'name',
                     'owner', 'type'),
                    (response['config'], response['description'],
                     response['driver'], response['enabled'],
                     response['id'], response['name'],
                     response['owner'], response['type'])]
        self.assertEqual(filtered, result)


class TestDeleteDatasourceDriver(common.TestCongressBase):

    def test_delete_datasource(self):
        driver = 'neutronv2'

        arglist = [driver]
        verifylist = [('datasource', driver), ]

        mocker = mock.Mock(return_value=None)
        self.app.client_manager.congressclient.delete_datasource = mocker
        cmd = datasource.DeleteDatasource(self.app, self.namespace)
        parsed_args = self.check_parser(cmd, arglist, verifylist)
        result = cmd.take_action(parsed_args)
        mocker.assert_called_with(driver)
        self.assertIsNone(result)


class TestUpdateDatasourceRow(common.TestCongressBase):

    def test_update_datasource_row(self):
        driver = 'push'
        table_name = 'table'
        rows = [["data1", "data2"],
                ["data3", "data4"]]

        arglist = [driver, table_name, jsonutils.dumps(rows)]
        verifylist = [('datasource', driver),
                      ('table', table_name),
                      ('rows', rows)]

        mocker = mock.Mock(return_value=None)
        self.app.client_manager.congressclient.update_datasource_rows = mocker
        self.app.client_manager.congressclient.list_datasources = mock.Mock()

        cmd = datasource.UpdateDatasourceRow(self.app, self.namespace)
        parsed_args = self.check_parser(cmd, arglist, verifylist)
        with mock.patch.object(utils, 'get_resource_id_from_name',
                               return_value="push"):
            cmd.take_action(parsed_args)
        mocker.assert_called_with(driver, table_name, rows)


class TestDatasourceRequestRefresh(common.TestCongressBase):

    def test_datasource_request_refresh(self):
        driver = 'neutronv2'

        arglist = [driver]
        verifylist = [('datasource', driver), ]

        mocker = mock.Mock(return_value=None)
        self.app.client_manager.congressclient.request_refresh = mocker
        self.app.client_manager.congressclient.list_datasources = mock.Mock()
        cmd = datasource.DatasourceRequestRefresh(self.app, self.namespace)
        parsed_args = self.check_parser(cmd, arglist, verifylist)
        with mock.patch.object(utils, "get_resource_id_from_name",
                               return_value="id"):
            result = cmd.take_action(parsed_args)
        mocker.assert_called_with("id", {})
        self.assertIsNone(result)
