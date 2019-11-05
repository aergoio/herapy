
.. _Aergo: http://github.com/aergoio/aergo
.. _HeraPy: http://github.com/aergoio/herapy
.. _Aergocli: https://docs.aergo.io/en/latest/tools/aergocli.html
.. _SDKs: https://docs.aergo.io/en/latest/sdks/index.html
.. _running_a_node: https://docs.aergo.io/en/latest/running-node/quickstart.html
.. |running_a_node| replace:: *running a Aergo node*


Getting Started
===============

Let's find out how to use HeraPy_ quickly within examples.


Preparation
+++++++++++

Depedencies
-----------

* Python3 (>= 3.7)


Download HeraPy
---------------

::

    pip install aergo-herapy

Connecting Aergo_
+++++++++++++++++

*Need* |running_a_node|_.

.. code-block:: python
   :linenos:

    import aergo.herapy as herapy

    aergo = herapy.Aergo()
    aergo.connect('localhost:7845')

    print(aergo.get_chain_info())

    aergo.disconnect()


Creating Account
++++++++++++++++

*No need* |running_a_node|_ *, but, in that case, need to be set a parameter* **skip_state=True** *in the method* :py:meth:`aergo.herapy.Aergo.new_account`.

.. code-block:: python
   :linenos:

    import aergo.herapy as herapy

    aergo = herapy.Aergo()
    aergo.new_account(skip_state=True)

    # if with connection, remove the comment of 2 lines in below.
    #aergo.connect('localhost:7845')
    #aergo.new_account()

    # print the address
    print(aergo.get_address())

    # print the address as bytes
    print(bytes(aergo.get_address()))


Exporting/Importing Account
+++++++++++++++++++++++++++

For using the account created in various other SDKs_ and Aergocli_, the account should be exported and imported in them.

*No need* |running_a_node|_.

.. code-block:: python
   :linenos:

    import aergo.herapy as herapy

    aergo = herapy.Aergo()
    aergo.new_account(skip_state=True)
    exp_account = aergo.export_account(password="keep-safe")

    aergo2 = herapy.Aergo()
    aergo2.import_account(exp_account, password="keep-safe")


Exporting/Importing Account
+++++++++++++++++++++++++++

*No need* |running_a_node|_.

.. code-block:: python
   :linenos:

    import aergo.herapy as herapy

    aergo = herapy.Aergo()
    aergo.new_account(skip_state=True)
    exp_account = aergo.export_account(password="keep-safe")

    aergo2 = herapy.Aergo()
    aergo2.import_account(exp_account, password="keep-safe")


Create Transaction
++++++++++++++++++

*No need* |running_a_node|_ *before sending it.*

.. code-block:: python
   :linenos:

    import aergo.herapy as herapy

    aergo = herapy.Aergo()
    aergo.new_account(skip_state=True)

