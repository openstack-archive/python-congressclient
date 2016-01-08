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

from congressclient.common import utils
from congressclient.osc.v1 import policy
from congressclient.tests import common


class TestCreatePolicy(common.TestCongressBase):

    def test_create_policy(self):
        policy_name = 'test1'
        policy_id = "e531f2b3-3d97-42c0-b3b5-b7b6ab532018"
        response = {"description": "",
                    "id": policy_id,
                    "name": policy_name,
                    "kind": "nonrecursive",
                    "owner": "system",
                    "abbreviation": "test1"}

        arglist = [policy_name]
        verifylist = [
            ('policy_name', policy_name),
        ]

        mocker = mock.Mock(return_value=response)
        self.app.client_manager.congressclient.create_policy = mocker
        cmd = policy.CreatePolicy(self.app, self.namespace)
        parsed_args = self.check_parser(cmd, arglist, verifylist)
        result = list(cmd.take_action(parsed_args))
        filtered = [('abbreviation', 'description', 'id', 'kind', 'name',
                     'owner'),
                    (policy_name, '', policy_id, 'nonrecursive',
                     policy_name, 'system')]
        self.assertEqual(filtered, result)


class TestShowPolicy(common.TestCongressBase):
    def test_show_policy(self):
        policy_id = "14f2897a-155a-4c9d-b3de-ef85c0a171d8"
        policy_name = "test1"
        arglist = [policy_id]
        verifylist = [
            ('policy_name', policy_id),
        ]
        response = {"description": "",
                    "id": policy_id,
                    "name": policy_name,
                    "kind": "nonrecursive",
                    "owner": "system",
                    "abbreviation": "test1"}

        mocker = mock.Mock(return_value=response)
        self.app.client_manager.congressclient.show_policy = mocker
        self.app.client_manager.congressclient.list_policy = mock.Mock()
        cmd = policy.ShowPolicy(self.app, self.namespace)
        parsed_args = self.check_parser(cmd, arglist, verifylist)
        with mock.patch.object(utils, "get_resource_id_from_name",
                               return_value="name"):
            result = list(cmd.take_action(parsed_args))
        filtered = [('abbreviation', 'description', 'id', 'kind', 'name',
                     'owner'),
                    (policy_name, '', policy_id, 'nonrecursive',
                     policy_name, 'system')]
        self.assertEqual(filtered, result)


class TestDeletePolicy(common.TestCongressBase):
    def test_delete_policy(self):
        policy_id = 'e531f2b3-3d97-42c0-b3b5-b7b6ab532018'
        arglist = [
            policy_id
        ]
        verifylist = [
            ('policy', policy_id)
        ]
        mocker = mock.Mock(return_value=None)
        self.app.client_manager.congressclient.delete_policy = mocker
        self.app.client_manager.congressclient.list_policy = mock.Mock()
        cmd = policy.DeletePolicy(self.app, self.namespace)

        parsed_args = self.check_parser(cmd, arglist, verifylist)
        with mock.patch.object(utils, "get_resource_id_from_name",
                               return_value="id"):
            result = cmd.take_action(parsed_args)

        mocker.assert_called_with(policy_id)
        self.assertIsNone(result)


class TestCreatePolicyRule(common.TestCongressBase):

    def test_create_policy_rule(self):
        policy_name = 'classification'
        rule = "p(x) :- q(x)"
        response = {"comment": "Comment",
                    "id": "e531f2b3-3d97-42c0-b3b5-b7b6ab532018",
                    "rule": rule}

        arglist = [policy_name, rule]
        verifylist = [
            ('policy_name', policy_name),
            ('rule', rule),
        ]

        mocker = mock.Mock(return_value=response)
        self.app.client_manager.congressclient.create_policy_rule = mocker
        cmd = policy.CreatePolicyRule(self.app, self.namespace)
        parsed_args = self.check_parser(cmd, arglist, verifylist)
        result = list(cmd.take_action(parsed_args))
        filtered = [('comment', 'id', 'rule'),
                    ('Comment', 'e531f2b3-3d97-42c0-b3b5-b7b6ab532018', rule)]
        self.assertEqual(filtered, result)

    def test_create_policy_rule_with_name(self):
        policy_name = "classification"
        rule = "p(x) :- q(x)"
        rule_name = "classification_rule"
        response = {"comment": "None",
                    "id": "e531f2b3-3d97-42c0-b3b5-b7b6ab532018",
                    "rule": rule,
                    "name": rule_name}

        arglist = ["--name", rule_name, policy_name, rule]
        verifylist = [
            ('policy_name', policy_name),
            ('rule', rule),
            ("rule_name", rule_name)
        ]

        mocker = mock.Mock(return_value=response)
        self.app.client_manager.congressclient.create_policy_rule = mocker
        cmd = policy.CreatePolicyRule(self.app, self.namespace)
        parsed_args = self.check_parser(cmd, arglist, verifylist)
        result = list(cmd.take_action(parsed_args))
        filtered = [('comment', 'id', 'name', 'rule'),
                    ('None', 'e531f2b3-3d97-42c0-b3b5-b7b6ab532018', rule_name,
                     rule)]
        self.assertEqual(filtered, result)


class TestDeletePolicyRule(common.TestCongressBase):
    def test_delete_policy_rule(self):
        policy_name = 'classification'
        rule_id = 'e531f2b3-3d97-42c0-b3b5-b7b6ab532018'
        arglist = [
            policy_name, rule_id
        ]
        verifylist = [
            ('policy_name', policy_name),
            ('rule_id', rule_id)
        ]
        mocker = mock.Mock(return_value=None)
        self.app.client_manager.congressclient.delete_policy_rule = mocker
        self.app.client_manager.congressclient.list_policy_rules = mock.Mock()
        cmd = policy.DeletePolicyRule(self.app, self.namespace)

        parsed_args = self.check_parser(cmd, arglist, verifylist)
        with mock.patch.object(utils, "get_resource_id_from_name",
                               return_value=rule_id):
            result = cmd.take_action(parsed_args)

        mocker.assert_called_with(policy_name, rule_id)
        self.assertIsNone(result)


class TestListPolicyRules(common.TestCongressBase):
    def test_list_policy_rules(self):
        policy_name = 'classification'
        rule_id = 'e531f2b3-3d97-42c0-b3b5-b7b6ab532018'
        arglist = [
            policy_name
        ]
        verifylist = [
            ('policy_name', policy_name)
        ]
        response = {
            "results": [{"comment": "None",
                         "id": rule_id,
                         "rule": "security_group(port, security_group_name)"
                         }]
        }
        lister = mock.Mock(return_value=response)
        self.app.client_manager.congressclient.list_policy_rules = lister
        cmd = policy.ListPolicyRules(self.app, self.namespace)

        parsed_args = self.check_parser(cmd, arglist, verifylist)
        cmd.take_action(parsed_args)

        lister.assert_called_with(policy_name)


class TestListPolicy(common.TestCongressBase):
    def test_list_policy_rules(self):
        policy_name = 'classification'
        policy_id = 'e531f2b3-3d97-42c0-b3b5-b7b6ab532018'
        arglist = [
        ]
        verifylist = [
        ]
        response = {
            "results": [{"id": policy_id,
                         "owner_id": "system",
                         "name": policy_name,
                         "kind": "nonrecursive",
                         "description": "my description"
                         }]}
        lister = mock.Mock(return_value=response)
        self.app.client_manager.congressclient.list_policy = lister
        cmd = policy.ListPolicy(self.app, self.namespace)

        parsed_args = self.check_parser(cmd, arglist, verifylist)
        result = cmd.take_action(parsed_args)

        lister.assert_called_with()
        self.assertEqual(['id', 'name', 'owner_id', 'kind', 'description'],
                         result[0])


class TestListPolicyTables(common.TestCongressBase):
    def test_list_policy_tables(self):
        policy_name = 'classification'
        arglist = [
            policy_name
        ]
        verifylist = [
            ('policy_name', policy_name)
        ]
        response = {
            "results": [{"id": "ports"},
                        {"id": "virtual_machines"}]
        }
        lister = mock.Mock(return_value=response)
        self.app.client_manager.congressclient.list_policy_tables = lister
        cmd = policy.ListPolicyTables(self.app, self.namespace)

        parsed_args = self.check_parser(cmd, arglist, verifylist)
        result = cmd.take_action(parsed_args)

        lister.assert_called_with(policy_name)
        self.assertEqual(['id'], result[0])


class TestListPolicyRows(common.TestCongressBase):

    def test_list_policy_rules(self):
        policy_name = 'classification'
        table_name = 'port_security_group'
        arglist = [
            policy_name, table_name
        ]
        verifylist = [
            ('policy_name', policy_name),
            ('table', table_name)
        ]
        response = {"results":
                    [{"data": ["69abc88b-c950-4625-801b-542e84381509",
                               "default"]}]}

        lister = mock.Mock(return_value=response)
        self.app.client_manager.congressclient.list_policy_rows = lister
        cmd = policy.ListPolicyRows(self.app, self.namespace)

        parsed_args = self.check_parser(cmd, arglist, verifylist)
        cmd.take_action(parsed_args)

        lister.assert_called_with(policy_name, table_name, False)

    def test_list_policy_rules_trace(self):
        policy_name = 'classification'
        table_name = 'p'
        arglist = [
            policy_name, table_name, "--trace"
        ]
        verifylist = [
            ('policy_name', policy_name),
            ('table', table_name)
        ]
        response = {"results":
                    [{"data": ["69abc88b-c950-4625-801b-542e84381509",
                               "default"]}],
                    "trace": "Call p(x, y)\n "
                             "Exit p('69abc88b-c950-4625-801b-542e84381509', "
                             "'default')\n"}

        lister = mock.Mock(return_value=response)
        self.app.client_manager.congressclient.list_policy_rows = lister
        cmd = policy.ListPolicyRows(self.app, self.namespace)

        parsed_args = self.check_parser(cmd, arglist, verifylist)
        cmd.take_action(parsed_args)

        lister.assert_called_with(policy_name, table_name, True)


class TestSimulatePolicy(common.TestCongressBase):

    def test_simulate_policy(self):
        policy_name = 'classification'
        action_name = 'action'
        sequence = 'q(1)'
        query = 'error(x)'
        arglist = [
            policy_name, query, sequence, action_name
        ]
        verifylist = [
            ('policy', policy_name),
            ('action_policy', action_name),
            ('sequence', sequence),
            ('query', query),
            ('delta', False)
        ]
        response = {'result': ['error(1)', 'error(2)']}

        lister = mock.Mock(return_value=response)
        self.app.client_manager.congressclient.execute_policy_action = lister
        cmd = policy.SimulatePolicy(self.app, self.namespace)

        parsed_args = self.check_parser(cmd, arglist, verifylist)
        cmd.take_action(parsed_args)

        body = {'action_policy': action_name,
                'sequence': sequence,
                'query': query}
        lister.assert_called_with(policy_name=policy_name,
                                  action='simulate',
                                  trace=False,
                                  delta=False,
                                  body=body)

    def test_simulate_policy_delta(self):
        policy_name = 'classification'
        action_name = 'action'
        sequence = 'q(1)'
        query = 'error(x)'
        arglist = [
            policy_name, query, sequence, action_name, "--delta"
        ]
        verifylist = [
            ('policy', policy_name),
            ('action_policy', action_name),
            ('sequence', sequence),
            ('query', query),
            ('delta', True)
        ]
        response = {'result': ['error(1)', 'error(2)']}

        lister = mock.Mock(return_value=response)
        self.app.client_manager.congressclient.execute_policy_action = lister
        cmd = policy.SimulatePolicy(self.app, self.namespace)

        parsed_args = self.check_parser(cmd, arglist, verifylist)
        cmd.take_action(parsed_args)

        body = {'action_policy': action_name,
                'sequence': sequence,
                'query': query}
        lister.assert_called_with(policy_name=policy_name,
                                  action='simulate',
                                  trace=False,
                                  delta=True,
                                  body=body)

    def test_simulate_policy_trace(self):
        policy_name = 'classification'
        action_name = 'action'
        sequence = 'q(1)'
        query = 'error(x)'
        arglist = [
            policy_name, query, sequence, action_name, "--trace"
        ]
        verifylist = [
            ('policy', policy_name),
            ('action_policy', action_name),
            ('sequence', sequence),
            ('query', query),
            ('trace', True)
        ]
        response = {'result': ['error(1)', 'error(2)'], 'trace': 'Call'}

        lister = mock.Mock(return_value=response)
        self.app.client_manager.congressclient.execute_policy_action = lister
        cmd = policy.SimulatePolicy(self.app, self.namespace)

        parsed_args = self.check_parser(cmd, arglist, verifylist)
        cmd.take_action(parsed_args)

        body = {'action_policy': action_name,
                'sequence': sequence,
                'query': query}
        lister.assert_called_with(policy_name=policy_name,
                                  action='simulate',
                                  trace=True,
                                  delta=False,
                                  body=body)


class TestGet(common.TestCongressBase):

    def test_create_policy_rule(self):
        policy_name = 'classification'
        rule = "p(x) :- q(x)"
        id = "e531f2b3-3d97-42c0-b3b5-b7b6ab532018"
        response = {"comment": "None",
                    "id": id,
                    "rule": rule}

        arglist = [policy_name, id]
        verifylist = [
            ('policy_name', policy_name),
            ('rule_id', id),
        ]

        mocker = mock.Mock(return_value=response)
        self.app.client_manager.congressclient.show_policy_rule = mocker
        self.app.client_manager.congressclient.list_policy_rules = mock.Mock()
        cmd = policy.ShowPolicyRule(self.app, self.namespace)
        parsed_args = self.check_parser(cmd, arglist, verifylist)
        with mock.patch.object(utils, "get_resource_id_from_name",
                               return_value="id"):
            result = list(cmd.take_action(parsed_args))
        filtered = [('comment', 'id', 'rule'),
                    ('None', id, rule)]
        self.assertEqual(filtered, result)
