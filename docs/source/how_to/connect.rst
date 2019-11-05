
.. _Aergo: http://github.com/aergoio/aergo
.. _HeraPy: http://github.com/aergoio/herapy
.. _SDKs: https://docs.aergo.io/en/latest/sdks/index.html

Connecting to Node
==================

HeraPy_ is one of the SDKs_ for interacting with the Aergo_ blockchain. For interacting, a client-side should connect to one of the nodes of a blockchain obviously. After connecting to the node, through HeraPy_, there are many :ref:`features<what_is_herapy>` that can do.

Connecting to the node is following Aergo API usage based on gRPC of `aergo-protobuf <https://github.com/aergoio/aergo-protobuf>`_.


*Connect*
  :py:meth:`aergo.herapy.Aergo.connect`

  This is the method in the :py:class:`aergo.herapy.Aergo` to :ref:`connect to the target node<how_to_connect_target_node>`.

*Disconnect*
  :py:meth:`aergo.herapy.Aergo.diconnect`
  This is the method in the :py:class:`aergo.herapy.Aergo` to disconnect the connection.


.. _how_to_connect_target_node:

How To Connect to the Target Node
+++++++++++++++++++++++++++++++++

*Target*
  This is the property by a combination of IP and Port. And, the delimiter is *:* between values.

.. code-block:: python
   :linenos:

    aergo.connect('localhost:7845')


.. _how_to_disconnect_target_node:

How To Disconnect the Connection
++++++++++++++++++++++++++++++++

.. code-block:: python
   :linenos:

    aergo.disconnect()


Example
+++++++

.. code-block:: python
   :linenos:

    import aergo.herapy as herapy

    aergo = herapy.Aergo()
    aergo.connect('localhost:7845')

    print(aergo.get_chain_info())

    aergo.disconnect()

