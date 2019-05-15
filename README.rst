========================
Team and repository tags
========================

.. image:: https://governance.openstack.org/tc/badges/python-congressclient.svg
    :target: https://governance.openstack.org/tc/reference/tags/index.html

.. Change things from this point on

===============================
python-congressclient
===============================

Client for Congress

* Free software: Apache license
* Documentation: https://docs.openstack.org/python-congressclient/latest/
* Source: https://opendev.org/openstack/python-congressclient
* Bugs: https://bugs.launchpad.net/python-congressclient


Client for Standalone Congress
------------------------------
Install the Congress CLI by cloning the repository and running the setup file.
The master repository always contains the latest source code, so if you are
installing and testing a specific branch of Congress, clone the matching branch
of the python-congressclient.

To execute CLI commands to standalone Congress installed with noauth:

* Install python-openstackclient::

    $ pip install python-openstackclient

* Clone master repository & install python-congressclient::

    $ git clone https://github.com/openstack/python-congressclient.git
    $ cd python-congressclient
    $ python setup.py install

* (Optional) Clone a branch; for example, if you are using the Ocata version of OpenStack and Congress::

    $ git clone -b stable/ocata https://github.com/openstack/python-congressclient.git
    $ cd python-congressclient
    $ python setup.py install

* Read the HTML documentation. Install python-sphinx and the oslosphinx extension if missing::

  $ sudo pip install sphinx
  $ sudo pip install oslosphinx

  Build the docs
  $ make docs

  Open doc/html/index.html in a browser

* To execute CLI commands::

    $ cd python-congressclient

    For example:
    $ export CONGRESS_URL="http://127.0.0.1:1789"
    $ openstack --os-token foo --os-url $CONGRESS_URL
    (openstack) congress policy create test_policy
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

    (openstack) congress policy rule create test_policy "p(5)"
    +---------+--------------------------------------+
    | Field   | Value                                |
    +---------+--------------------------------------+
    | comment | None                                 |
    | id      | 5ce7fb18-a227-447e-bec8-93e99c0052a5 |
    | name    | None                                 |
    | rule    | p(5)                                 |
    +---------+--------------------------------------+

    (openstack) congress policy rule list test_policy
    // ID: 5ce7fb18-a227-447e-bec8-93e99c0052a5
    // Name: None
    p(5)

    (openstack) exit
    $

Features
--------

* TODO
