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

"""OpenStackClient plugin for Governance service."""

from oslo_log import log as logging

from congressclient.common import utils

LOG = logging.getLogger(__name__)

DEFAULT_POLICY_API_VERSION = '1'
API_VERSION_OPTION = 'os_policy_api_version'
API_NAME = 'congressclient'
API_VERSIONS = {
    '1': 'congressclient.v1.client.Client',
}


def make_client(instance):
    """Returns a congress service client."""
    congress_client = utils.get_client_class(
        API_NAME,
        instance._api_version[API_NAME],
        API_VERSIONS)
    LOG.debug('instantiating congress client: %s', congress_client)
    return congress_client(session=instance.session,
                           auth=None,
                           interface='publicURL',
                           service_type='policy',
                           region_name=instance._region_name)


def build_option_parser(parser):
    """Hook to add global options."""
    parser.add_argument(
        '--os-policy-api-version',
        metavar='<policy-api-version>',
        default=utils.env(
            'OS_POLICY_API_VERSION',
            default=DEFAULT_POLICY_API_VERSION),
        help=('Policy API version, default=%s (Env: OS_POLICY_API_VERSION)' %
              DEFAULT_POLICY_API_VERSION))
    return parser
