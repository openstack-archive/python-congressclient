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
    """Client for the Congress v1 API.

    Example::
        import keystoneclient
        from congressclient.v1 import client
        auth = keystoneclient.auth.identity.v2.Password(
            auth_url=AUTH_URL, username=USERNAME,
            password=PASSWORD, tenant_name=TENANT_NAME)
        session = keystoneclient.session.Session(auth=auth)
        congress = client.Client(session=session,
                                 auth=None,
                                 interface='publicURL',
                                 service_type='policy',
                                 region_name='RegionOne')
        congress.create_policy_rule(..)

    """

    policy_rules = '/v1/policies/%s/rules'
    policy_rules_path = '/v1/policies/%s/rules/%s'
    policy_tables = '/v1/policies/%s/tables'
    policy_rows = '/v1/policies/%s/tables/%s/rows'
    policy_rows_trace = '/v1/policies/%s/tables/%s/rows?trace=True'
    policy_rules = '/v1/policies/%s/rules'
    policies = '/v1/policies'
    datasources = '/v1/data-sources'
    datasource_tables = '/v1/data-sources/%s/tables'
    datasource_rows = '/v1/data-sources/%s/tables/%s/rows'

    def __init__(self, **kwargs):
        super(Client, self).__init__()

        kwargs.setdefault('user_agent', 'python-congressclient')
        self.httpclient = adapter.LegacyJsonAdapter(**kwargs)

    def create_policy_rule(self, policy_name, body=None):
        resp, body = self.httpclient.post(
            self.policy_rules % policy_name, body=body)
        return body

    def delete_policy_rule(self, policy_name, rule_id):
        resp, body = self.httpclient.delete(
            self.policy_rules_path % (policy_name, rule_id))
        return body

    def list_policy_rows(self, policy_name, table, trace=None):
        if trace:
            query = self.policy_rows_trace
        else:
            query = self.policy_rows
        resp, body = self.httpclient.get(query % (policy_name, table))
        return body

    def list_policy_rules(self, policy_name):
        resp, body = self.httpclient.get(self.policy_rules % (policy_name))
        return body

    def list_policy(self):
        resp, body = self.httpclient.get(self.policies)
        return body

    def list_policy_tables(self, policy_name):
        resp, body = self.httpclient.get(self.policy_tables % (policy_name))
        return body

    def list_datasources(self):
        resp, body = self.httpclient.get(self.datasources)
        return body

    def list_datasource_tables(self, datasource_name):
        resp, body = self.httpclient.get(self.datasource_tables %
                                         (datasource_name))
        return body

    def list_datasource_rows(self, datasource_name, table_name):
        resp, body = self.httpclient.get(self.datasource_rows %
                                         (datasource_name, table_name))
        return body
