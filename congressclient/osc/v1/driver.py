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

"""Driver action implemenations"""

from cliff import lister
from cliff import show
from oslo_log import log as logging
import six

from congressclient.common import utils


class ListDrivers(lister.Lister):
    """List drivers."""

    log = logging.getLogger(__name__ + '.ListDrivers')

    def get_parser(self, prog_name):
        parser = super(ListDrivers, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.congressclient
        data = client.list_drivers()['results']
        columns = ['id', 'description']
        formatters = {'Drivers': utils.format_list}
        return (columns,
                (utils.get_dict_properties(s, columns,
                                           formatters=formatters)
                 for s in data))


class ShowDriverConfig(show.ShowOne):
    """List driver tables."""

    log = logging.getLogger(__name__ + '.ShowDriverConfig')

    def get_parser(self, prog_name):
        parser = super(ShowDriverConfig, self).get_parser(prog_name)
        parser.add_argument(
            'driver',
            metavar="<datasource-driver>",
            help="Name of the datasource driver")
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)' % parsed_args)
        client = self.app.client_manager.congressclient
        data = client.show_driver(
            parsed_args.driver)
        # remove table schema info from displaying
        del data['tables']
        return zip(*sorted(six.iteritems(data)))
        columns = ['id']
        formatters = {'DriverTables': utils.format_list}
        return (columns,
                (utils.get_dict_properties(s, columns,
                                           formatters=formatters)
                 for s in data))


class ShowDriverSchema(lister.Lister):
    """List datasource tables."""

    log = logging.getLogger(__name__ + '.ShowDriverSchema')

    def get_parser(self, prog_name):
        parser = super(ShowDriverSchema, self).get_parser(prog_name)
        parser.add_argument(
            'driver',
            metavar="<datasource-driver>",
            help="Name of the datasource driver")
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)' % parsed_args)
        client = self.app.client_manager.congressclient
        data = client.show_driver(
            parsed_args.driver)
        formatters = {'columns': utils.format_long_dict_list}
        newdata = [{'table': x['table_id'],
                    'columns': x['columns']}
                   for x in data['tables']]
        columns = ['table', 'columns']
        return (columns,
                (utils.get_dict_properties(s, columns,
                                           formatters=formatters)
                 for s in newdata))
