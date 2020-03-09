import pytest
import aergo.herapy as herapy


def test_account_exp_imp(aergo) -> None:

    aergo.new_account()
    new_exp_txt = aergo.export_account(password="1234")
    print("Exported txt is {}".format(new_exp_txt))

    # fail to import with wrong pwd
    with pytest.raises(herapy.errors.GeneralException):
        aergo.import_account(new_exp_txt, password='test')

    # import with correct pwd
    account = aergo.import_account(new_exp_txt, password='1234')
    print("Account private key is {}".format(account.private_key))
    print("Account address is {}".format(account.address))

    # import with exported key
    exported_txt = "47DpVeQt14U834UP6uosqA2ahpg9FPjWNM1vd1LxX1m7MXm" \
                   "AcUy4oqVmcmZgkNVh6AMhHv1CE"
    print("Exported Data is {}".format(exported_txt))
    account = aergo.import_account(exported_txt, password='1234')
    print("Account private key is {}".format(account.private_key))
    print("Account address is {}".format(account.address))

    new_exp_txt = aergo.export_account(password='1234')
    print("Exported txt is {}".format(new_exp_txt))

    assert new_exp_txt == exported_txt, \
        "Exported account should be same as imported one"
