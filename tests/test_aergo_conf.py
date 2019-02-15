import pytest

import aergo.herapy as herapy


DEFAULT_AERGO_CONFIG = """datadir = "${AERGO_HOME}/data"
dbtype = "badgerdb"
enableprofile = false
profileport = 6060
enabletestmode = false
personal = true
authdir = "${AERGO_HOME}/auth"

[rpc]
netserviceaddr = "127.0.0.1"
netserviceport = 7845
netservicetrace = false
nstls = false
nskey = ""

[p2p]
netprotocoladdr = ""
netprotocolport = 7846
npbindaddr = ""
npbindport = -1
nptls = false
npcert = ""
npkey = ""
npaddpeers = []
npdiscoverpeers = true
npmaxpeers = 100
nppeerpool = 100
npexposeself = true
npusepolaris = true
npaddpolarises = []

[polaris]
allowprivate = false
genesisfile = ""

[blockchain]
maxblocksize = 1048576
coinbaseaccount = ""
maxanchorcount = 20
forceresetheight = 0

[mempool]
showmetrics = false
enablefadeout = false
fadeoutperiod = 12
dumpfilepath = "${AERGO_HOME}/mempool.dump"

[consensus]
enablebp = false
blockinterval = 1

[monitor]
protocol = ""
endpoint = ""

[account]
unlocktimeout = 60
"""


def test_default():
    aergo_conf = herapy.AergoConfig()
    generate_toml = herapy.utils.convert_aergo_conf_to_toml(aergo_conf)
    assert DEFAULT_AERGO_CONFIG == generate_toml
    with pytest.raises(KeyError):
        aergo_conf.rpc_nscert
    with pytest.raises(KeyError):
        aergo_conf.rpc_nsallowcors
    with pytest.raises(KeyError):
        aergo_conf.blockchain_verifiercount
    with pytest.raises(KeyError):
        aergo_conf.mempool_verifiers


TEST_AERGO_CONFIG = """
# aergo TOML Configuration File (https://github.com/toml-lang/toml)
# base configurations
datadir = "/Users/yp/work/blocko/go/src/github.com/aergoio/aergo/bin/alone/data"
enableprofile = false
profileport = 6060
#enablerest = false
enabletestmode = true

[rpc]
netserviceaddr = "127.0.0.1"
netserviceport = 7845
nstls = false
nscert = ""
nskey = ""
nsallowcors = false

#[rest]
#restport = "8080"

[p2p]
netprotocoladdr = "127.0.0.1"
netprotocolport = 7846
nptls = false
npcert = ""
npkey = ""
npaddpeers = [
]
npmaxpeers = "100"
nppeerpool = "100"

[blockchain]
# blockchain configurations
maxblocksize = 1048576

[mempool]
showmetrics = false
dumpfilepath = "/Users/yp/work/blocko/go/src/github.com/aergoio/aergo/bin/alone/mempool.dump"

[consensus]
enablebp = true
blockinterval = 3
"""


def test_success():
    aergo_conf = herapy.utils.convert_toml_to_aergo_conf(TEST_AERGO_CONFIG)
    with pytest.raises(KeyError):
        aergo_conf.add_conf("test", "test")
    with pytest.raises(KeyError):
        aergo_conf.add_conf("test", "test", "test")
    with pytest.raises(KeyError):
        aergo_conf.add_conf("test", "test", "rpc")
    # check base config
    assert aergo_conf.datadir == "/Users/yp/work/blocko/go/src/github.com/aergoio/aergo/bin/alone/data"
    assert aergo_conf.dbtype == herapy.AERGO_DEFAULT_CONF['dbtype']
    assert aergo_conf.enableprofile is False
    assert aergo_conf.profileport == 6060
    with pytest.raises(KeyError):
        herapy.AERGO_DEFAULT_CONF['enablerest']
    assert aergo_conf.enabletestmode is True
    assert aergo_conf.personal is herapy.AERGO_DEFAULT_CONF['personal']
    assert aergo_conf.authdir is herapy.AERGO_DEFAULT_CONF['authdir']
    # check rcp config
    assert aergo_conf.rpc_netserviceaddr == "127.0.0.1"
    assert aergo_conf.rpc_netserviceport == 7845
    assert aergo_conf.rpc_netservicetrace is False
    assert aergo_conf.rpc_nstls is False
    with pytest.raises(KeyError):
        herapy.AERGO_DEFAULT_CONF['rpc']['nscert']
    assert aergo_conf.rpc_nscert == ""
    assert aergo_conf.rpc_nskey == ""
    with pytest.raises(KeyError):
        herapy.AERGO_DEFAULT_CONF['rpc']['nsallowcors']
    assert aergo_conf.rpc_nsallowcors is False
    # check rest config
    #assert aergo_conf.rest_restport == 8080
    # check p2p config
    assert aergo_conf.p2p_netprotocoladdr != herapy.AERGO_DEFAULT_CONF['p2p']['netprotocoladdr']
    assert aergo_conf.p2p_netprotocoladdr == "127.0.0.1"
    assert aergo_conf.p2p_netprotocolport == 7846
    assert aergo_conf.p2p_npbindaddr == herapy.AERGO_DEFAULT_CONF['p2p']['npbindaddr']
    assert aergo_conf.p2p_npbindport == herapy.AERGO_DEFAULT_CONF['p2p']['npbindport']
    assert aergo_conf.p2p_nptls is False
    assert aergo_conf.p2p_npcert == ""
    assert aergo_conf.p2p_npkey == ""
    assert isinstance(aergo_conf.p2p_npaddpeers, list)
    assert 0 == len(aergo_conf.p2p_npaddpeers)
    assert aergo_conf.p2p_npmaxpeers == 100
    assert aergo_conf.p2p_nppeerpool == 100
    # check blockchain config
    assert aergo_conf.blockchain_maxblocksize == 1048576
    assert aergo_conf.blockchain_coinbaseaccount == herapy.AERGO_DEFAULT_CONF['blockchain']['coinbaseaccount']
    assert aergo_conf.blockchain_maxanchorcount == herapy.AERGO_DEFAULT_CONF['blockchain']['maxanchorcount']
    #assert aergo_conf.blockchain_usefastsyncer is herapy.AERGO_DEFAULT_CONF['blockchain']['usefastsyncer']
    assert aergo_conf.blockchain_forceresetheight == herapy.AERGO_DEFAULT_CONF['blockchain']['forceresetheight']
    # check mempool config
    assert aergo_conf.mempool_showmetrics is False
    with pytest.raises(KeyError):
        herapy.AERGO_DEFAULT_CONF['mempool']['verifiers']
    with pytest.raises(KeyError):
        aergo_conf.mempool_verifiers
    assert aergo_conf.mempool_dumpfilepath == "/Users/yp/work/blocko/go/src/github.com/aergoio/aergo/bin/alone/mempool.dump"
    # check consensus config
    assert aergo_conf.consensus_enablebp is True
    assert aergo_conf.consensus_blockinterval == 3
    # check monitor config
    assert aergo_conf.monitor_protocol == herapy.AERGO_DEFAULT_CONF['monitor']['protocol']
    assert aergo_conf.monitor_endpoint == herapy.AERGO_DEFAULT_CONF['monitor']['endpoint']
    # check account config
    assert aergo_conf.account_unlocktimeout == herapy.AERGO_DEFAULT_CONF['account']['unlocktimeout']
