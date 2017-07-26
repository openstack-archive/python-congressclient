# Copyright 2015 Huawei.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""List API versions implemenations"""

from cliff import lister
from oslo_log import log as logging

from congressclient.common import utils


class ListAPIVersions(lister.Lister):
    """List API Versions."""

    log = logging.getLogger(__name__ + '.ListAPIVersions')

    def get_parser(self, prog_name):
        return super(ListAPIVersions, self).get_parser(prog_name)

    def take_action(self, parsed_args):
        # set default max-width
        if parsed_args.max_width == 0:
            parsed_args.max_width = 80
        client = self.app.client_manager.congressclient
        data = client.list_api_versions()['versions']
        # sort API by id
        data.sort(key=lambda item: item.get('id'))
        columns = ['id', 'status', 'updated']
        return (columns,
                (utils.get_dict_properties(s, columns) for s in data))
