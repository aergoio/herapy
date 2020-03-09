import pytest
import aergo.herapy as herapy


@pytest.fixture(scope="session")
def aergo() -> herapy.Aergo:
    setup_ok = True
    aergo = herapy.Aergo()
    try:
        aergo.connect('localhost:7845')
    except herapy.errors.exception.CommunicationException:
        setup_ok = False
    if not setup_ok:
        pytest.fail("Integration tests require a localhost:7845 testnet. "
                    "Use `make local_testnet`")
    return aergo
