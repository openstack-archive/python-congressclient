===============================
python-congressclient
===============================

Client for Congress

* Free software: Apache license
* Documentation: http://docs.openstack.org/developer/python-congressclient
* Source: http://git.openstack.org/cgit/stackforge/python-congressclient
* Bugs: http://bugs.launchpad.net/python-congressclient


Client for Standalone Congress
------------------------------
To execute CLI commands to standalone congress set with noauth:

* Install python-openstackclient::

    $ pip install python-openstackclient

* Clone repository & install python-congressclient::

    $ git clone https://github.com/stackforge/python-congressclient.git
    $ cd python-congressclient
    $ python setup.py install


* Edit congress_noauth and fix CONGRESS_URL to point to correct congress server

* Run script "congress_noauth" to execute CLI commands::

    $ cd python-congressclient

    For example:
    $ ./congress_noauth policy create test_policy
    +--------------+--------------------------------------+
    | Field        | Value                                |
    +--------------+--------------------------------------+
    | abbreviation | test_                                |
    | description  |                                      |
    | id           | 8595f24a-7d74-45ee-8168-0b3e937b8419 |
    | kind         | nonrecursive                         |
    | name         | test_policy                          |
    | owner_id     | user                                 |
    +--------------+--------------------------------------+

    $ ./congress_noauth policy rule create test_policy "p(5)"
    +---------+--------------------------------------+
    | Field   | Value                                |
    +---------+--------------------------------------+
    | comment | None                                 |
    | id      | 5ce7fb18-a227-447e-bec8-93e99c0052a5 |
    | name    | None                                 |
    | rule    | p(5)                                 |
    +---------+--------------------------------------+

    $ ./congress_noauth policy rule list test_policy
    // ID: 5ce7fb18-a227-447e-bec8-93e99c0052a5
    // Name: None
    p(5)


Features
--------

* TODO
