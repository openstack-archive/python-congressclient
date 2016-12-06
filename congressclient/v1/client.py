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

from keystoneauth1 import adapter


class Client(object):
    """Client for the Congress v1 API.

    Example::
        from keystoneauth1.identity import v2
        from keystoneauth1 import session
        from congressclient.v1 import client
        auth = v2.Password(auth_url=AUTH_URL, username=USERNAME,
                           password=PASSWORD, tenant_name=TENANT_NAME)
        sess = session.Session(auth=auth)
        congress = client.Client(session=sess,
                                 auth=None,
                                 interface='publicURL',
                                 service_type='policy',
                                 region_name='RegionOne')
        congress.create_policy_rule(..)

    """
    policy = '/v1/policies'
    policy_path = '/v1/policies/%s'
    policy_rules = '/v1/policies/%s/rules'
    policy_rules_path = '/v1/policies/%s/rules/%s'
    policy_tables = '/v1/policies/%s/tables'
    policy_table_path = '/v1/policies/%s/tables/%s'
    policy_rows = '/v1/policies/%s/tables/%s/rows'
    policy_rows_trace = '/v1/policies/%s/tables/%s/rows?trace=True'
    policies = '/v1/policies'
    policy_action = '/v1/policies/%s?%s'
    datasources = '/v1/data-sources'
    datasource_path = '/v1/data-sources/%s'
    datasource_tables = '/v1/data-sources/%s/tables'
    datasource_table_path = '/v1/data-sources/%s/tables/%s'
    datasource_status = '/v1/data-sources/%s/status'
    datasource_actions = '/v1/data-sources/%s/actions'
    datasource_schema = '/v1/data-sources/%s/schema'
    datasource_table_schema = '/v1/data-sources/%s/tables/%s/spec'
    datasource_rows = '/v1/data-sources/%s/tables/%s/rows'
    driver = '/v1/system/drivers'
    driver_path = '/v1/system/drivers/%s'
    policy_api_versions = '/'

    def __init__(self, **kwargs):
        super(Client, self).__init__()

        kwargs.setdefault('user_agent', 'python-congressclient')
        self.httpclient = adapter.LegacyJsonAdapter(**kwargs)

    def create_policy(self, body):
        resp, body = self.httpclient.post(
            self.policy, body=body)
        return body

    def delete_policy(self, policy):
        resp, body = self.httpclient.delete(
            self.policy_path % policy)
        return body

    def show_policy(self, policy):
        resp, body = self.httpclient.get(
            self.policy_path % policy)
        return body

    def create_policy_rule(self, policy_name, body=None):
        resp, body = self.httpclient.post(
            self.policy_rules % policy_name, body=body)
        return body

    def delete_policy_rule(self, policy_name, rule_id):
        resp, body = self.httpclient.delete(
            self.policy_rules_path % (policy_name, rule_id))
        return body

    def show_policy_rule(self, policy_name, rule_id):
        resp, body = self.httpclient.get(
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

    def execute_policy_action(self, policy_name, action, trace, delta, body):
        uri = "?action=%s&trace=%s&delta=%s" % (action, trace, delta)
        resp, body = self.httpclient.post(
            (self.policy_path % policy_name) + str(uri), body=body)
        return body

    def show_policy_table(self, policy_name, table_id):
        resp, body = self.httpclient.get(self.policy_table_path %
                                         (policy_name, table_id))
        return body

    def list_datasources(self):
        resp, body = self.httpclient.get(self.datasources)
        return body

    def show_datasource(self, datasource_name):
        """Get a single datasource

        Intended for use by Horizon. Not available in CLI
        """
        resp, body = self.httpclient.get(self.datasource_path %
                                         (datasource_name))
        return body

    def list_datasource_tables(self, datasource_name):
        resp, body = self.httpclient.get(self.datasource_tables %
                                         (datasource_name))
        return body

    def list_datasource_rows(self, datasource_name, table_name):
        resp, body = self.httpclient.get(self.datasource_rows %
                                         (datasource_name, table_name))
        return body

    def update_datasource_rows(self, datasource_name, table_name, body=None):
        """Update rows in a table of a datasource.

        Args:
            datasource_name: Name or id of the datasource
            table_name: Table name for updating
            body: Rows for update.
        """
        resp, body = self.httpclient.put(self.datasource_rows %
                                         (datasource_name, table_name),
                                         body=body)
        return body

    def list_datasource_status(self, datasource_name):
        resp, body = self.httpclient.get(self.datasource_status %
                                         datasource_name)
        return body

    def list_datasource_actions(self, datasource_name):
        resp, body = self.httpclient.get(self.datasource_actions %
                                         datasource_name)
        return body

    def show_datasource_schema(self, datasource_name):
        resp, body = self.httpclient.get(self.datasource_schema %
                                         datasource_name)
        return body

    def show_datasource_table_schema(self, datasource_name, table_name):
        resp, body = self.httpclient.get(self.datasource_table_schema %
                                         (datasource_name, table_name))
        return body

    def show_datasource_table(self, datasource_name, table_id):
        resp, body = self.httpclient.get(self.datasource_table_path %
                                         (datasource_name, table_id))
        return body

    def create_datasource(self, body=None):
        resp, body = self.httpclient.post(
            self.datasources, body=body)
        return body

    def delete_datasource(self, datasource):
        resp, body = self.httpclient.delete(
            self.datasource_path % datasource)
        return body

    def execute_datasource_action(self, service_name, action, body):
        uri = "?action=%s" % (action)
        resp, body = self.httpclient.post(
            (self.datasource_path % service_name) + str(uri), body=body)
        return body

    def list_drivers(self):
        resp, body = self.httpclient.get(self.driver)
        return body

    def show_driver(self, driver):
        resp, body = self.httpclient.get(self.driver_path %
                                         (driver))
        return body

    def request_refresh(self, driver, body=None):
        resp, body = self.httpclient.post(self.datasource_path %
                                          (driver) + "?action=request-refresh",
                                          body=body)
        return body

    def list_api_versions(self):
        resp, body = self.httpclient.get(self.policy_api_versions)
        return body
