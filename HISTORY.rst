=======
History
=======

0.11.0 (2019-02-20)
-------------------

* Change the result type from the 'get_tx_result' function ('SmartContractStatus' --> 'TxResultStatus')
* Separate two function 'send_tx' and 'batch_tx' from the single 'send_tx' function for a single and multiple txs
* Open the 'generate_tx' function for helping a new transaction manually
* Support multiple proof queries with the array of Storage Keys
* Simplify verifying proof as the 'verify_proof' function from 'verify_inclusion' and 'verify_exclusion'

0.9.0 (2018-12-31)
------------------

* Fit for the public Aergo testnet.
* First public release on PyPI.


0.1.0 (2018-11-07)
------------------

* First release on PyPI.
