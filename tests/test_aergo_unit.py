import pytest

import decimal

import aergo.herapy as herapy


def test_success():
    aer = herapy.Aer('1aergo')
    assert isinstance(aer, herapy.Aer)
    assert aer.aer == str(aer)
    assert 1000000000000000000 == aer.dec
    assert '1 aergo' == aer.aergo
    assert '1000000000 gaer' == aer.gaer
    assert '1000000000000000000 aer' == aer.aer

    aer = herapy.Aer('1 gaer')
    assert isinstance(aer, herapy.Aer)
    assert aer.aer == str(aer)
    assert 1000000000 == aer.dec
    assert '0.000000001 aergo' == aer.aergo
    assert '1 gaer' == aer.gaer
    assert '1000000000 aer' == aer.aer

    aer = herapy.Aer('1')
    assert isinstance(aer, herapy.Aer)
    assert aer.aer == str(aer)
    assert 1 == aer.dec
    assert '0.000000000000000001 aergo' == aer.aergo
    assert '0.000000001 gaer' == aer.gaer
    assert '1 aer' == aer.aer

    aer = herapy.Aer('1.01 aergo')
    assert isinstance(aer, herapy.Aer)
    assert aer.aer == str(aer)
    assert 1010000000000000000 == aer.dec
    assert '1.01 aergo' == aer.aergo
    assert '1010000000 gaer' == aer.gaer
    assert '1010000000000000000 aer' == aer.aer

    aer = herapy.Aer('1.01gaer')
    assert isinstance(aer, herapy.Aer)
    assert aer.aer == str(aer)
    assert 1010000000 == aer.dec
    assert '0.00000000101 aergo' == aer.aergo
    assert '1.01 gaer' == aer.gaer
    assert '1010000000 aer' == aer.aer

    aer = herapy.Aer('1 aer')
    assert isinstance(aer, herapy.Aer)
    assert aer.aer == str(aer)
    assert 1 == aer.dec
    assert '0.000000000000000001 aergo' == aer.aergo
    assert '0.000000001 gaer' == aer.gaer
    assert '1 aer' == aer.aer

    aer = herapy.Aer('0.123456789012345678 aergo')
    assert isinstance(aer, herapy.Aer)
    assert aer.aer == str(aer)
    assert 123456789012345678 == aer.dec
    assert '0.123456789012345678 aergo' == aer.aergo
    assert '123456789.012345678 gaer' == aer.gaer
    assert '123456789012345678 aer' == aer.aer

    # max length of decimal
    aer = herapy.Aer('0.100000000000000001 aergo')
    assert isinstance(aer, herapy.Aer)
    assert aer.aer == str(aer)
    assert 100000000000000001 == aer.dec
    assert '0.100000000000000001 aergo' == aer.aergo
    assert '100000000.000000001 gaer' == aer.gaer
    assert '100000000000000001 aer' == aer.aer

    # max length of decimal
    aer = herapy.Aer('499999999.100000000000000001 aergo')
    assert isinstance(aer, herapy.Aer)
    assert aer.aer == str(aer)
    assert 499999999100000000000000001 == aer.dec
    assert '499999999.100000000000000001 aergo' == aer.aergo
    assert '499999999100000000.000000001 gaer' == aer.gaer
    assert '499999999100000000000000001 aer' == aer.aer

    # max length of decimal
    aer = herapy.Aer('499999999100000000000000001 aer')
    assert isinstance(aer, herapy.Aer)
    assert aer.aer == str(aer)
    assert 499999999100000000000000001 == aer.dec
    assert '499999999.100000000000000001 aergo' == aer.aergo
    assert '499999999100000000.000000001 gaer' == aer.gaer
    assert '499999999100000000000000001 aer' == aer.aer

    aer = herapy.Aer('24999999910000000081000000100000000000000000000000000000000000.0 aergo')
    assert isinstance(aer, herapy.Aer)
    assert aer.aer == str(aer)
    assert decimal.Decimal('24999999910000000081000000100000000000000000000000000000000000000000000000000000') == aer.dec
    assert '24999999910000000081000000100000000000000000000000000000000000 aergo' == aer.aergo
    assert '24999999910000000081000000100000000000000000000000000000000000000000000 gaer' == aer.gaer
    assert '24999999910000000081000000100000000000000000000000000000000000000000000000000000 aer' == aer.aer


def test_fail():
    with pytest.raises(herapy.errors.ConversionException):
        herapy.Aer('1 aergogo')
    with pytest.raises(herapy.errors.ConversionException):
        herapy.Aer('1gaergogo')
    with pytest.raises(herapy.errors.ConversionException):
        herapy.Aer('1.01')
    with pytest.raises(herapy.errors.ConversionException):
        herapy.Aer('1.01.0')
    with pytest.raises(herapy.errors.ConversionException):
        herapy.Aer('1.01 aer')
    with pytest.raises(herapy.errors.ConversionException):
        herapy.Aer('0.0000000000000000001 aergo')
    with pytest.raises(herapy.errors.ConversionException):
        herapy.Aer('499999999100000000000000001.1 aer')
    with pytest.raises(herapy.errors.ConversionException):
        herapy.Aer('abc.abc aergo')
    with pytest.raises(herapy.errors.ConversionException):
        herapy.Aer('')


def test_op_add():
    aer1 = herapy.Aer('1')
    aer2 = herapy.Aer('10')
    aer = aer1 + aer2
    assert isinstance(aer, herapy.Aer)
    assert aer.aer == str(aer)
    assert 11 == aer.dec
    assert '0.000000000000000011 aergo' == aer.aergo
    assert '0.000000011 gaer' == aer.gaer
    assert '11 aer' == aer.aer

    aer1 = herapy.Aer('499999999100000000000000001 aer')
    aer2 = herapy.Aer('499999999100000000000000001 aer')
    aer = aer1 + aer2
    assert isinstance(aer, herapy.Aer)
    assert aer.aer == str(aer)
    assert 999999998200000000000000002 == aer.dec
    assert '999999998.200000000000000002 aergo' == aer.aergo
    assert '999999998200000000.000000002 gaer' == aer.gaer
    assert '999999998200000000000000002 aer' == aer.aer


def test_op_sub():
    aer1 = herapy.Aer('1')
    aer2 = herapy.Aer('10')
    aer = aer1 - aer2
    assert isinstance(aer, herapy.Aer)
    assert aer.aer == str(aer)
    assert -9 == aer.dec
    assert '-0.000000000000000009 aergo' == aer.aergo
    assert '-0.000000009 gaer' == aer.gaer
    assert '-9 aer' == aer.aer

    aer1 = herapy.Aer('499999999100000000000000001 aer')
    aer2 = herapy.Aer('499999999100000000000000001 aer')
    aer = aer1 - aer2
    assert isinstance(aer, herapy.Aer)
    assert aer.aer == str(aer)
    assert 0 == aer.dec
    assert '0 aergo' == aer.aergo
    assert '0 gaer' == aer.gaer
    assert '0 aer' == aer.aer


def test_op_mul():
    aer1 = herapy.Aer('1')
    aer2 = herapy.Aer('10')
    aer = aer1 * aer2
    assert isinstance(aer, herapy.Aer)
    assert aer.aer == str(aer)
    assert 10 == aer.dec
    assert '0.00000000000000001 aergo' == aer.aergo
    assert '0.00000001 gaer' == aer.gaer
    assert '10 aer' == aer.aer

    aer1 = herapy.Aer('499999999100000000000000001 aer')
    aer2 = herapy.Aer('499999999100000000000000001 aer')
    aer = aer1 * aer2
    assert isinstance(aer, herapy.Aer)
    assert aer.aer == str(aer)
    assert 249999999100000000810000000999999998200000000000000001 == aer.dec
    assert '249999999100000000810000000999999998.200000000000000001 aergo' == aer.aergo
    assert '249999999100000000810000000999999998200000000.000000001 gaer' == aer.gaer
    assert '249999999100000000810000000999999998200000000000000001 aer' == aer.aer
