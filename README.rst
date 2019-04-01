
======
herapy
======

.. image:: https://codecov.io/gh/aergoio/herapy/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/aergoio/herapy

.. image:: https://img.shields.io/pypi/v/aergo-herapy.svg
        :target: https://pypi.python.org/pypi/aergo-herapy

.. image:: https://travis-ci.com/aergoio/herapy.svg?token=bxpJA7kPFExuJMq3sBNb&branch=master
    :target: https://travis-ci.com/aergoio/herapy

.. image:: https://readthedocs.org/projects/aergo-herapy/badge/?version=latest
        :target: https://aergo-herapy.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/aergoio/herapy/shield.svg
     :target: https://pyup.io/repos/github/aergoio/herapy/
     :alt: Updates

HeraPy is a Python package for AERGO that provides the features below.

--------
Features
--------

* Communication with AERGO node
* Getting AERGO blockchain information
* Creating/Exporting/Importing an account
* Making and sending a transaction
* Deploying/Calling/Querying a smart contract
* Querying and prooving contract/account states

-------
Install
-------

Install the latest version in `the Python Package Index <https://pypi.org/project/aergo-herapy/>`_

.. code-block::

    pip install aergo-herapy

or, install locally

.. code-block::

    git clone git@github.com:aergoio/herapy.git
    cd herapy
    make install

------------
Run examples
------------

After installing aergo-herapy, you can run examples

.. code-block::

    make ex

The examples in the 'examples' directory connect the public Aergo testnet.

-----
Build
-----

Downloading HeraPy
==================

Download HeraPy from this repository

.. code-block::

    git clone git@github.com:aergoio/herapy.git

Installing Dependencies
=======================

.. code-block::

    pip install -r requirements.txt

But, we recommend to use a virtual environment below.

Virtual Environment (Pipenv)
----------------------------

Using Pipenv, all dependencies will be installed automatically.

.. code-block::

    pipenv shell

If you cleaned up and setup again,

.. code-block::

    pipenv install

If you want to test or contribute, then do not forget '--dev' option

.. code-block::

    pipenv install --dev
    make test

Updating Protocol
=================

If need to upgrade a protocol,

.. code-block::

    make protoc

After this command, all protocol related source files will be generated if it's different.

Updating Aergo Configurations
=============================

If need to upgrade Aergo Configurations,

.. code-block::

    make aergo-types

After this command, 'aergo/herapy/obj/aergo_conf.py' will be generated if it's different.

If occur the error message below

.. code-block::

    ERROR: Cannot find 'AERGO_TYPES_SRC'

, find the source code 'aergo/config/types.go' and make this file path as an environment variable of 'AERGO_TYPES_SRC'

.. code-block::

    export AERGO_TYPES_SRC=`find ~ -path '*/aergo/config/types.go' 2>/dev/null`
    make aergo-types


-------------------------
Releases and Contributing
-------------------------

HeraPy follows a major release cycle of AERGO.
A minor release such as fixing bugs and errors are occasionally patched.
Please let us know if you encounter a bug by `filling an issue <https://github.com/aergoio/herapy/issues>`_.

If you are planning to contribute a new feature, class, or function,
please `open an issue <https://github.com/aergoio/herapy/issues>`_ and discuss with us.

We appreciate all contributions.


-------------
Documentation
-------------

https://aergo-herapy.readthedocs.io


-------
License
-------

HeraPy is MIT license as found in the LICENSE file.


-------
Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
