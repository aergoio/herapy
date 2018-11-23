
======
herapy
======

.. image:: https://codecov.io/gh/aergoio/herapy/branch/accounts/graph/badge.svg?token=JylbPsDrDB
  :target: https://codecov.io/gh/aergoio/herapy

.. image:: https://img.shields.io/pypi/v/aergo-herapy.svg
        :target: https://pypi.python.org/pypi/aergo-herapy

.. image:: https://travis-ci.com/aergoio/herapy.svg?token=bxpJA7kPFExuJMq3sBNb&branch=master
    :target: https://travis-ci.com/aergoio/herapy

.. image:: https://readthedocs.org/projects/herapy/badge/?version=latest
        :target: https://herapy.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/aergoio/herapy/shield.svg
     :target: https://pyup.io/repos/github/aergoio/herapy/
     :alt: Updates

HeraPy is a Python package for AERGO that provides the features below.


Features
--------

* Communication with a node
* Getting a metadata
* Managing an account
* Making and sending a transaction
* Making and sending a smart contract

Install
-------

.. code-block::

   pip install aergo-herapy


Build
-----

.. code-block::

  git clone git@github.com:aergoio/herapy.git
  cd herapy
  pip install -r requirements.txt
  make protoc
  make install


Releases and Contributing
-------------------------

HeraPy follows a major release cycle of AERGO.
A minor release such as fixing bugs and errors are occasionally patched.
Please let us know if you encounter a bug by `filling an issue <https://github.com/aergoio/herapy/issues>`_.

If you are planning to contribute a new feature, class, or function,
please `open an issue <https://github.com/aergoio/herapy/issues>`_ and discuss with us.

We appreciate all contributions.


License
-------

HeraPy is MIT license as found in the LICENSE file.
* Documentation: https://herapy.readthedocs.io.


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
