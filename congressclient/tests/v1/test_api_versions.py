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

import mock

from congressclient.osc.v1 import api_versions
from congressclient.tests import common


class TestAPIVersions(common.TestCongressBase):

    def test_list_api_versions(self):
        fake_response = {
            "versions": [
                {
                    "status": "CURRENT",
                    "updated": "2015-08-12T17:42:13Z",
                    "id": "v2",
                    "links": [
                        {
                            "href": "http://localhost:1789/v2/",
                            "rel": "self"
                        }
                    ]
                },
                {
                    "status": "SUPPORTED",
                    "updated": "2013-08-12T17:42:13Z",
                    "id": "v1",
                    "links": [
                        {
                            "href": "http://localhost:1789/v1/",
                            "rel": "self"
                        }
                    ]
                }
            ]
        }

        with mock.patch.object(self.app.client_manager.congressclient,
                               'list_api_versions',
                               return_value=fake_response) as lister:

            cmd = api_versions.ListAPIVersions(self.app, self.namespace)
            parsed_args = self.check_parser(cmd, [], [])
            result = cmd.take_action(parsed_args)

            lister.assert_called_once_with()
            self.assertEqual(['id', 'status', 'updated'], result[0])
            self.assertEqual(('v1', 'SUPPORTED', '2013-08-12T17:42:13Z'),
                             next(result[1]))
            self.assertEqual(('v2', 'CURRENT', '2015-08-12T17:42:13Z'),
                             next(result[1]))
