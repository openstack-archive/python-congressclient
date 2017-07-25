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

import importlib
import os

from congressclient import exceptions


def env(*vars, **kwargs):
    """Search for the first defined of possibly many env vars

    Returns the first environment variable defined in vars, or
    returns the default defined in kwargs.
    """
    for v in vars:
        value = os.environ.get(v, None)
        if value:
            return value
    return kwargs.get('default', '')


def import_class(import_str):
    """Returns a class from a string including module and class

    :param import_str: a string representation of the class name
    :rtype: the requested class
    """
    mod_str, _sep, class_str = import_str.rpartition('.')
    mod = importlib.import_module(mod_str)
    return getattr(mod, class_str)


def get_client_class(api_name, version, version_map):
    """Returns the client class for the requested API version

    :param api_name: the name of the API, e.g. 'compute', 'image', etc
    :param version: the requested API version
    :param version_map: a dict of client classes keyed by version
    :rtype: a client class for the requested API version
    """
    try:
        client_path = version_map[str(version)]
    except (KeyError, ValueError):
        msg = "Invalid %s client version '%s'. must be one of: %s" % (
              (api_name, version, ', '.join(version_map.keys())))
        raise exceptions.UnsupportedVersion(msg)

    return import_class(client_path)


def format_long_dict_list(data):
    """Return a formatted string.

    :param data: a list of dicts
    :rtype: a string formatted to {a:b, c:d}, {e:f, g:h}
    """
    newdata = [str({str(key): str(value) for key, value in d.iteritems()})
               for d in data]
    return ',\n'.join(newdata) + '\n'


def format_dict(data):
    """Return a formatted string.

    :param data: a dict
    :rtype: a string formatted to {a:b, c:d}
    """
    if not isinstance(data, dict):
        return str(data)
    return str({str(key): str(value) for key, value in data.items()})


def format_list(data):
    """Return a formatted strings

    :param data: a list of strings
    :rtype: a string formatted to a,b,c
    """

    return ', '.join(data)


def get_dict_properties(item, fields, mixed_case_fields=[], formatters={}):
    """Return a tuple containing the item properties.

    :param item: a single dict resource
    :param fields: tuple of strings with the desired field names
    :param mixed_case_fields: tuple of field names to preserve case
    :param formatters: dictionary mapping field names to callables
       to format the values
    """
    row = []
    for field in fields:
        if field in mixed_case_fields:
            field_name = field.replace(' ', '_')
        else:
            field_name = field.lower().replace(' ', '_')
        data = item[field_name] if field_name in item else ''
        if field in formatters:
            row.append(formatters[field](data))
        else:
            row.append(data)
    return tuple(row)


def get_resource_id_from_name(name, results):
    # FIXME(arosen): move to common lib and add tests...
    name_match = None
    id_match = None
    double_name_match = False
    for result in results['results']:
        if result['id'] == name:
            id_match = result['id']
        if result['name'] == name:
            if name_match:
                double_name_match = True
            name_match = result['id']
    if not double_name_match and name_match:
        return name_match
    if double_name_match and not id_match:
        # NOTE(arosen): this should only occur is using congress
        # as admin and multiple projects use the same datsource name.
        raise exceptions.Conflict(
            "Multiple resources have this name %s. Please specify id." % name)
    if id_match:
        return id_match

    raise exceptions.NotFound("Resource %s not found" % name)
