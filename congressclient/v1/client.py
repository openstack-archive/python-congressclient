#   Copyright 2014 VMWare.
#
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

from keystoneclient import adapter


class Client(object):
    policy_rules_path = '/policies/%s/rules'
    policy_rules_paths = '/policies/%s/rules/%s'
    policy_rows = '/policies/%s/tables/%s/rows'
    policy_rules = '/policies/%s/rules'
    policies = '/policies'

    def __init__(self, **kwargs):
        super(Client, self).__init__()

        kwargs.setdefault('user_agent', 'python-congressclient')
        self.httpclient = adapter.LegacyJsonAdapter(**kwargs)

    def create_policy_rule(self, policy_name, body=None):
        resp, body = self.httpclient.post(
            self.policy_rules_path % policy_name, body=body)
        return body

    def delete_policy_rule(self, policy_name, rule_id):
        resp, body = self.httpclient.delete(
            self.policy_rules_paths % (policy_name, rule_id))
        return body

    def get_policy_rows(self, policy_name, table):
        resp, body = self.httpclient.get(self.policy_rows % (policy_name,
                                                             table))
        return body

    def list_policy_rules(self, policy_name):
        resp, body = self.httpclient.get(self.policy_rules % (policy_name))
        return body

    def list_policy(self):
        resp, body = self.httpclient.get(self.policies)
        return body
