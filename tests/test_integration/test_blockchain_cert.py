import pytest
import aergo.herapy as herapy


def test_blockchain_cert():
    pytest.skip("Fix local enterprise node setup")
    aergo = herapy.Aergo()

    print("------ Connect AERGO -----------")
    aergo.connect('localhost:7845',
                  tls_ca_cert="./cert/rootca.crt",
                  tls_cert="./cert/client.pem",
                  tls_key="./cert/client.key")

    print("------ Get Node Info -----------")
    node_state = aergo.get_node_state()
    print("Node State: {}".format(str(node_state)))
    node_info = aergo.get_node_info()
    print("Node Info: {}".format(str(node_info)))

    print("------ Get Blockchain Info -----------")
    blockchain_info = aergo.get_chain_info()
    print("Blockchain Info: {}".format(str(blockchain_info)))
    blockchain_info = aergo.get_chain_info(with_consensus_info=False)
    print("Blockchain Info: {}".format(str(blockchain_info)))

    print("------ Get Consensus Info -----------")
    consensus_info = aergo.get_consensus_info()
    print("Consensus Info: {}".format(str(consensus_info)))
