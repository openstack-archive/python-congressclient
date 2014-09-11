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

"""Datasource action implemenations"""

import logging

from cliff import lister

from congressclient.common import utils


class ListDatasources(lister.Lister):
    """List Datasources."""

    log = logging.getLogger(__name__ + '.ListDatasources')

    def get_parser(self, prog_name):
        parser = super(ListDatasources, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.congressclient
        data = client.list_datasources()['results']
        columns = ['id', 'owner_id', 'enabled', 'type', 'config']
        formatters = {'Datasources': utils.format_list}
        return (columns,
                (utils.get_dict_properties(s, columns,
                                           formatters=formatters)
                 for s in data))


class ListDatasourceTables(lister.Lister):
    """List datasource tables."""

    log = logging.getLogger(__name__ + '.ListDatasourceTables')

    def get_parser(self, prog_name):
        parser = super(ListDatasourceTables, self).get_parser(prog_name)
        parser.add_argument(
            'datasource_name',
            metavar="<datasource-name>",
            help="Name of the datasource")
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)' % parsed_args)
        client = self.app.client_manager.congressclient
        data = client.list_datasource_tables(
            parsed_args.datasource_name)['results']
        columns = ['id']
        formatters = {'DatasourceTables': utils.format_list}
        return (columns,
                (utils.get_dict_properties(s, columns,
                                           formatters=formatters)
                 for s in data))


class ListDatasourceRows(lister.Lister):
    """List datasource rows."""

    log = logging.getLogger(__name__ + '.ListDatasourceRows')

    def get_parser(self, prog_name):
        parser = super(ListDatasourceRows, self).get_parser(prog_name)
        parser.add_argument(
            'datasource_name',
            metavar="<datasource-name>",
            help="Name of the datasource to show")
        parser.add_argument(
            'table',
            metavar="<table>",
            help="Table to get the datasource rows from")
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)' % parsed_args)
        client = self.app.client_manager.congressclient
        results = client.list_datasource_rows(parsed_args.datasource_name,
                                              parsed_args.table)['results']

        if results:
            columns = ['Col%s' % (i)
                       for i in xrange(0, len(results[0]['data']))]
        else:
            columns = ['data']
        return (columns, (x['data'] for x in results))
