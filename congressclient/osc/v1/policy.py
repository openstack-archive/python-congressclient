#   Copyright 2012-2013 OpenStack, LLC.
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

"""Policy action implemenations"""

import sys

from cliff import command
from cliff import lister
from cliff import show
from keystoneauth1 import exceptions
from oslo_log import log as logging
from oslo_serialization import jsonutils
import six
import yaml

from congressclient.common import utils


def _format_rule(rule):
    """Break up rule string so it fits on screen."""

    rule_split = jsonutils.dumps(rule).split(":-")
    formatted_string = rule_split[0] + ":-\n"
    for rule in rule_split[1].split("), "):
        formatted_string += rule + '\n'
    return formatted_string


def get_rule_id_from_name(client, parsed_args):
    results = client.list_policy_rules(parsed_args.policy_name)['results']
    rule_id = None
    for result in results:
        if result.get('name') == parsed_args.rule_id:
            if rule_id is None:
                rule_id = result.get('id')
            else:
                raise exceptions.Conflict(
                    "[Multiple rules with same name: %s]" %
                    parsed_args.rule_id)
    if rule_id is None:
        raise exceptions.NotFound(
            "[No rule found with name: %s]" % parsed_args.rule_id)
    return rule_id


class CreatePolicyRule(show.ShowOne):
    """Create a policy rule."""

    log = logging.getLogger(__name__ + '.CreatePolicyRule')

    def get_parser(self, prog_name):
        parser = super(CreatePolicyRule, self).get_parser(prog_name)
        parser.add_argument(
            'policy_name',
            metavar="<policy-name>",
            help="Name or identifier of the policy")
        parser.add_argument(
            'rule',
            metavar="<rule>",
            help="Policy rule")
        parser.add_argument(
            '--name', dest="rule_name",
            help="Name of the policy rule")
        parser.add_argument(
            '--comment', dest="comment",
            help="Comment about policy rule")
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)' % parsed_args)
        # set default max-width
        if parsed_args.max_width == 0:
            parsed_args.max_width = 80
        client = self.app.client_manager.congressclient
        body = {'rule': parsed_args.rule}
        if parsed_args.rule_name:
            body['name'] = parsed_args.rule_name
        if parsed_args.comment:
            body['comment'] = parsed_args.comment
        data = client.create_policy_rule(parsed_args.policy_name, body)
        return zip(*sorted(six.iteritems(data)))


class DeletePolicyRule(command.Command):
    """Delete a policy rule."""

    log = logging.getLogger(__name__ + '.DeletePolicyRule')

    def get_parser(self, prog_name):
        parser = super(DeletePolicyRule, self).get_parser(prog_name)
        parser.add_argument(
            'policy_name',
            metavar="<policy-name>",
            help="Name of the policy to delete")
        parser.add_argument(
            'rule_id',
            metavar="<rule-id/rule-name>",
            help="ID/Name of the policy rule to delete")
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)' % parsed_args)
        client = self.app.client_manager.congressclient
        results = client.list_policy_rules(parsed_args.policy_name)
        rule_id = utils.get_resource_id_from_name(
            parsed_args.rule_id, results)
        client.delete_policy_rule(parsed_args.policy_name, rule_id)


class ListPolicyRules(command.Command):
    """List policy rules."""

    log = logging.getLogger(__name__ + '.ListPolicyRules')

    def get_parser(self, prog_name):
        parser = super(ListPolicyRules, self).get_parser(prog_name)
        parser.add_argument(
            'policy_name',
            metavar="<policy-name>",
            help="Name of the policy")
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)' % parsed_args)
        client = self.app.client_manager.congressclient
        results = client.list_policy_rules(parsed_args.policy_name)['results']
        for result in results:
            print("// ID: %s" % str(result['id']))
            print("// Name: %s" % str(result.get('name')))
            if result['comment'] != "None" and result['comment']:
                print("// %s" % str(result['comment']))
            print(result['rule'])
            print('')
        return 0


class SimulatePolicy(command.Command):
    """Show the result of simulation."""

    log = logging.getLogger(__name__ + '.SimulatePolicy')

    def get_parser(self, prog_name):
        parser = super(SimulatePolicy, self).get_parser(prog_name)
        parser.add_argument(
            'policy',
            metavar="<policy>",
            help="Name of the policy")
        parser.add_argument(
            'query',
            metavar="<query>",
            help="String representing query (policy rule or literal)")
        parser.add_argument(
            'sequence',
            metavar="<sequence>",
            help="String representing sequence of updates/actions")
        parser.add_argument(
            'action_policy',
            metavar="<action_policy>",
            help="Name of the policy with actions",
            default=None)
        parser.add_argument(
            '--delta',
            action='store_true',
            default=False,
            help="Return difference in query caused by update sequence")
        parser.add_argument(
            '--trace',
            action='store_true',
            default=False,
            help="Include trace describing computation")
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)' % parsed_args)
        client = self.app.client_manager.congressclient
        args = {}
        args['query'] = parsed_args.query
        args['sequence'] = parsed_args.sequence
        if parsed_args.action_policy is not None:
            args['action_policy'] = parsed_args.action_policy
        if parsed_args.delta:
            args['delta'] = parsed_args.delta
        if parsed_args.trace:
            args['trace'] = parsed_args.trace

        body = {'query': parsed_args.query,
                'sequence': parsed_args.sequence,
                'action_policy': parsed_args.action_policy}

        results = client.execute_policy_action(
            policy_name=parsed_args.policy,
            action="simulate",
            trace=parsed_args.trace,
            delta=parsed_args.delta,
            body=body)
        for result in results['result']:
            print(result)
        if 'trace' in results:
            print(results['trace'])
        return 0


class ListPolicyTables(lister.Lister):
    """List policy tables."""

    log = logging.getLogger(__name__ + '.ListPolicyTables')

    def get_parser(self, prog_name):
        parser = super(ListPolicyTables, self).get_parser(prog_name)
        parser.add_argument(
            'policy_name',
            metavar="<policy-name>",
            help="Name of the policy")
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)' % parsed_args)
        # set default max-width
        if parsed_args.max_width == 0:
            parsed_args.max_width = 80
        client = self.app.client_manager.congressclient
        data = client.list_policy_tables(parsed_args.policy_name)['results']
        columns = ['id']
        formatters = {'PolicyTables': utils.format_list}
        return (columns,
                (utils.get_dict_properties(s, columns,
                                           formatters=formatters)
                 for s in data))


class ListPolicy(lister.Lister):
    """List Policy."""

    log = logging.getLogger(__name__ + '.ListPolicy')

    def get_parser(self, prog_name):
        parser = super(ListPolicy, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        # set default max-width
        if parsed_args.max_width == 0:
            parsed_args.max_width = 80
        client = self.app.client_manager.congressclient
        data = client.list_policy()['results']
        columns = ['id', 'name', 'owner_id', 'kind', 'description']
        formatters = {'Policies': utils.format_list}
        return (columns,
                (utils.get_dict_properties(s, columns,
                                           formatters=formatters)
                 for s in data))


class CreatePolicy(show.ShowOne):
    """Create a policy."""

    log = logging.getLogger(__name__ + '.CreatePolicy')

    def get_parser(self, prog_name):
        parser = super(CreatePolicy, self).get_parser(prog_name)
        parser.add_argument(
            'policy_name',
            metavar="<policy_name>",
            help="Name of the policy")
        parser.add_argument(
            '--description',
            metavar="<description>",
            help="Policy description")
        parser.add_argument(
            '--abbreviation',
            metavar="<abbreviation>",
            help="Policy abbreviation (used in traces). The length of the "
                 "string must be equal to or less than 5 characters. Defaults "
                 "to the first five characters of policy_name if not set.")
        parser.add_argument(
            '--kind',
            metavar="<kind>",
            choices=['nonrecursive', 'database', 'action', 'materialized',
                     'z3'],
            help="Kind of policy: "
                 "{nonrecursive, database, action, materialized, z3}")
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)' % parsed_args)
        # set default max-width
        if parsed_args.max_width == 0:
            parsed_args.max_width = 80
        client = self.app.client_manager.congressclient
        body = {'name': parsed_args.policy_name,
                'description': parsed_args.description,
                'abbreviation': parsed_args.abbreviation,
                'kind': parsed_args.kind}
        data = client.create_policy(body)
        return zip(*sorted(six.iteritems(data)))


class CreatePolicyFromFile(show.ShowOne):
    """Create a policy."""

    log = logging.getLogger(__name__ + '.CreatePolicy')

    def get_parser(self, prog_name):
        parser = super(CreatePolicyFromFile, self).get_parser(prog_name)
        parser.add_argument(
            'policy_file_path',
            metavar="<policy_file_path>",
            help="Path to policy file")
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)' % parsed_args)
        # set default max-width
        if parsed_args.max_width == 0:
            parsed_args.max_width = 80
        client = self.app.client_manager.congressclient
        with open(parsed_args.policy_file_path, "r") as stream:
            policies = yaml.load_all(stream)
            try:
                body = next(policies)
            except StopIteration:
                raise Exception('No policy found in file.')
            try:
                body = next(policies)
                raise Exception(
                    'More than one policy found in file. None imported.')
            except StopIteration:
                pass
        data = client.create_policy(body)

        def rule_dict_to_string(rules):
            rule_str_list = [rule['rule'] for rule in rules]
            return "\n".join(rule_str_list)

        data['rules'] = rule_dict_to_string(data['rules'])
        return zip(*sorted(six.iteritems(data)))


class DeletePolicy(command.Command):
    """Delete a policy."""

    log = logging.getLogger(__name__ + '.DeletePolicy')

    def get_parser(self, prog_name):
        parser = super(DeletePolicy, self).get_parser(prog_name)
        parser.add_argument(
            'policy',
            metavar="<policy>",
            help="ID or name of the policy to delete")
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)' % parsed_args)
        client = self.app.client_manager.congressclient

        client.delete_policy(parsed_args.policy)


class ListPolicyRows(lister.Lister):
    """List policy rows."""

    log = logging.getLogger(__name__ + '.ListPolicyRows')

    def get_parser(self, prog_name):
        parser = super(ListPolicyRows, self).get_parser(prog_name)
        parser.add_argument(
            'policy_name',
            metavar="<policy-name>",
            help="Name of the policy to show")
        parser.add_argument(
            'table',
            metavar="<table>",
            help="Table to get the policy rows from")
        parser.add_argument(
            '--trace',
            action='store_true',
            default=False,
            help="Display explanation of result")
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)' % parsed_args)
        # set default max-width
        if parsed_args.max_width == 0:
            parsed_args.max_width = 80
        client = self.app.client_manager.congressclient
        answer = client.list_policy_rows(parsed_args.policy_name,
                                         parsed_args.table,
                                         parsed_args.trace)

        if 'trace' in answer:
            sys.stdout.write(answer['trace'] + '\n')
        results = answer['results']
        columns = []
        if results:
            columns = ['Col%s' % (i)
                       for i in range(0, len(results[0]['data']))]
        self.log.debug("Columns: " + str(columns))
        return (columns, (x['data'] for x in results))


class ShowPolicyRule(show.ShowOne):
    """Show a policy rule."""

    log = logging.getLogger(__name__ + '.ShowPolicyRule')

    def get_parser(self, prog_name):
        parser = super(ShowPolicyRule, self).get_parser(prog_name)
        parser.add_argument(
            'policy_name',
            metavar="<policy-name>",
            help="Name or identifier of the policy")
        parser.add_argument(
            'rule_id',
            metavar="<rule-id/rule-name>",
            help="Policy rule id or rule name")

        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)' % parsed_args)
        # set default max-width
        if parsed_args.max_width == 0:
            parsed_args.max_width = 80
        client = self.app.client_manager.congressclient
        results = client.list_policy_rules(parsed_args.policy_name)
        rule_id = utils.get_resource_id_from_name(
            parsed_args.rule_id, results)
        data = client.show_policy_rule(parsed_args.policy_name, rule_id)
        return zip(*sorted(six.iteritems(data)))


class ShowPolicyTable(show.ShowOne):
    """Show policy table properties."""

    log = logging.getLogger(__name__ + '.ShowPolicyTable')

    def get_parser(self, prog_name):
        parser = super(ShowPolicyTable, self).get_parser(prog_name)
        parser.add_argument(
            'policy_name',
            metavar='<policy-name>',
            help="Name of policy")
        parser.add_argument(
            'table_id',
            metavar='<table-id>',
            help="Table id")

        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)' % parsed_args)
        # set default max-width
        if parsed_args.max_width == 0:
            parsed_args.max_width = 80
        client = self.app.client_manager.congressclient
        data = client.show_policy_table(parsed_args.policy_name,
                                        parsed_args.table_id)
        return zip(*sorted(six.iteritems(data)))


class ShowPolicy(show.ShowOne):
    """Show policy properties."""

    log = logging.getLogger(__name__ + '.ShowPolicy')

    def get_parser(self, prog_name):
        parser = super(ShowPolicy, self).get_parser(prog_name)
        parser.add_argument(
            'policy_name',
            metavar='<policy-name>',
            help="Name of policy")

        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)' % parsed_args)
        # set default max-width
        if parsed_args.max_width == 0:
            parsed_args.max_width = 80
        client = self.app.client_manager.congressclient
        results = client.list_policy()
        policy_id = utils.get_resource_id_from_name(
            parsed_args.policy_name, results)
        data = client.show_policy(policy_id)
        return zip(*sorted(six.iteritems(data)))
