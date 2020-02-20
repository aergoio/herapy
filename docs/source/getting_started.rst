
.. _Aergo: http://github.com/aergoio/aergo
.. _HeraPy: http://github.com/aergoio/herapy
.. _Aergocli: https://docs.aergo.io/en/latest/tools/aergocli.html
.. _SDKs: https://docs.aergo.io/en/latest/sdks/index.html
.. _running_a_node: https://docs.aergo.io/en/latest/running-node/quickstart.html
.. |running_a_node| replace:: *running your own Aergo node*


Getting Started
===============

Let's find out how to use HeraPy_ quickly with a few examples.


Installation
++++++++++++

* Python3 (>= 3.7)

Setup your environment and install aergo-herapy

.. code-block:: bash

    $ cd my_new_project
    $ virtualenv -p python3 venv
    $ source venv/bin/activate
    $ pip install aergo-herapy

Connecting to Aergo_
++++++++++++++++++++

Connecting to Aergo can be done with a public api like 'testnet-api.aergo.io:7845' or by |running_a_node|_.

.. code-block:: python
   :linenos:

    import aergo.herapy as herapy

    aergo = herapy.Aergo()
    aergo.connect('testnet-api.aergo.io:7845')

    print(aergo.get_chain_info())

    aergo.disconnect()


Creating a new Account
++++++++++++++++++++++

Connecting to Aergo is optional when creating new accounts with the parameter **skip_state=True**.

.. code-block:: python
   :linenos:

    import aergo.herapy as herapy

    aergo = herapy.Aergo()

    # connect to a node to retrieve the account state (nonce, balance...)
    # aergo.connect('testnet-api.aergo.io:7845')
    # aergo.new_account()

    # create a new account offline
    aergo.new_account(skip_state=True)

    # print the address
    print(aergo.get_address())

    # print the address as bytes
    print(bytes(aergo.get_address()))


Exporting/Importing an Account
++++++++++++++++++++++++++++++

For using an account created in various other SDKs_ and Aergocli_, the prefered method is to import an Aergo encrypted keystore file.

Connecting to a node is optional.

.. code-block:: python
   :linenos:

    import aergo.herapy as herapy

    aergo = herapy.Aergo()
    aergo.new_account(skip_state=True)
    exp_account = aergo.export_account_to_keystore("keep-safe")

    aergo2 = herapy.Aergo()
    aergo2.import_account_from_keystore(exp_account, "keep-safe", skip_state=True)


Creating a Transaction
++++++++++++++++++++++

.. code-block:: python
   :linenos:

    import aergo.herapy as herapy

    # connect to a node
    aergo = herapy.Aergo()
    aergo.connect('testnet-api.aergo.io:7845')

    keystore_file_path = "./my/keystore.json"

    # import account from keystore file and get current nonce
    aergo.import_account_from_keystore_file(keystore_file_path, "keep-safe")

    # transfer 1 aergo
    tx, status = aergo.transfer(to_address, 1 * 10**18)

    assert result.status == herapy.CommitStatus.TX_OK

    receipt = aergo.wait_tx_result(tx.tx_hash)

    assert receipt.status == herapy.TxResultStatus.SUCCESS:



Deploying and calling smart contracts
+++++++++++++++++++++++++++++++++++++

.. code-block:: python
   :linenos:

    import aergo.herapy as herapy

    # connect to a node
    aergo = herapy.Aergo()
    aergo.connect('testnet-api.aergo.io:7845')

    keystore_file_path = "./my/keystore.json"

    # import account from keystore file and get current nonce
    aergo.import_account_from_keystore_file(keystore_file_path, "keep-safe")


    # deploy a new contract
    payload = "Compiled contract string"
    tx, result = aergo.deploy_sc(amount=0, payload=payload, args=1234)
    assert result.status == herapy.CommitStatus.TX_OK

    receipt = aergo.wait_tx_result(tx.tx_hash)
    assert receipt.status == herapy.TxResultStatus.CREATED:

    # get address of newly deployed contract
    sc_address = receipt.contract_address

    # send a transaction to a contract (write)
    tx, result = aergo.call_sc(sc_address, "lua function name")
    assert result.status == herapy.CommitStatus.TX_OK

    assert receipt.status == herapy.TxResultStatus.SUCCESS:
    receipt = aergo.wait_tx_result(tx.tx_hash)


    # query a contract function (read-only)
    return_value = aergo.query_sc(sc_address, "lua function name")