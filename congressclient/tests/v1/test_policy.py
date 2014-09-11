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

from congressclient.osc.v1 import policy
from congressclient.tests import common


class TestCreatePolicyRule(common.TestCongressBase):

    def test_create_policy_rule(self):
        policy_name = 'classification'
        rule = ("port_security_group(port, security_group_name) :-"
                "neutron:ports(addr_pairs, security_groups, extra_dhcp_opts,"
                "binding_cap, status, name, admin_state_up, network_id, "
                "tenant_id, binding_vif, device_owner, mac_address, "
                "fixed_ips, port, device_id, binding_host_id1), "
                "neutron:ports.security_groups(security_groups, "
                "security_group_id), neutron:security_groups(tenant_id2, "
                "security_group_name, desc2, security_group_id)")

        response = {"comment": "None",
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
                    ('None', 'e531f2b3-3d97-42c0-b3b5-b7b6ab532018', rule)]
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
        cmd = policy.DeletePolicyRule(self.app, self.namespace)

        parsed_args = self.check_parser(cmd, arglist, verifylist)
        result = cmd.take_action(parsed_args)

        mocker.assert_called_with(policy_name, rule_id)
        self.assertEqual(None, result)


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
        arglist = [
        ]
        verifylist = [
        ]
        response = {
            "results": [{"id": policy_name,
                         "owner": "system"
                         }]}
        lister = mock.Mock(return_value=response)
        self.app.client_manager.congressclient.list_policy = lister
        cmd = policy.ListPolicy(self.app, self.namespace)

        parsed_args = self.check_parser(cmd, arglist, verifylist)
        result = cmd.take_action(parsed_args)

        lister.assert_called_with()
        self.assertEqual(['id', 'owner_id'], result[0])


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
