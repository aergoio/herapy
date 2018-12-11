import pytest

import aergo.herapy as herapy


def test_success():
    with open("./test_aergo_config.toml") as f:
        conf = herapy.utils.aergo_config_to_dict(f.read())
    print(conf.keys())

    aergo_conf = herapy.AergoConfig()

    for k, v in conf.items():
        if isinstance(v, dict):
            print("[{}]".format(k))
            for k2, v2 in v.items():
                print("  Key   =", k2)
                print("  Value =", v2)
                print()
        else:
            print("Key   =", k)
            print("Value =", v)
            print()
    assert type(conf['datadir']) == str
    assert type(conf['enableprofile']) == bool
    assert type(conf['profileport']) == int
    assert type(conf['enablerest']) == bool
    assert type(conf['enabletestmode']) == bool

    # [rpc]
    assert type(conf['rpc']) == dict
    assert type(conf['rpc']['netserviceaddr']) == str
    assert type(conf['rpc']['netserviceport']) == int
    assert type(conf['rpc']['nstls']) == bool
    assert type(conf['rpc']['nscert']) == str
    assert type(conf['rpc']['nskey']) == str
    assert type(conf['rpc']['nsallowcors']) == bool

    # [rest]
    assert type(conf['rest']) == dict
    assert type(conf['rest']['restport']) == str

    # [p2p]
    assert type(conf['p2p']) == dict

    # [blockchain]
    assert type(conf['blockchain']) == dict

    # [mempool]
    assert type(conf['mempool']) == dict

    # [consensus]
    assert type(conf['consensus']) == dict
