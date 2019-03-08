import pytest

import decimal

import aergo.herapy as herapy

from aergo.herapy.obj.aer import AERGO_UNIT_PRECISION


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

    aer1 = herapy.Aer('24999999910000000081000000100000000000000000000000000000000000000000000000000000 aer')
    aer2 = herapy.Aer('24999999910000000081000000100000000000000000000000000000000000 aergo')
    assert aer1.dec == aer2.dec
    assert str(aer1) == str(aer2)
    assert int(aer1) == int(aer2)
    assert bytes(aer1) == bytes(aer2)

    aer3 = herapy.Aer()
    aer3.dec = 24999999910000000081000000100000000000000000000000000000000000000000000000000000
    assert aer1.dec == aer3.dec
    assert str(aer1) == str(aer3)
    assert int(aer1) == int(aer3)
    assert bytes(aer1) == bytes(aer3)

    aer = herapy.Aer(b'test')
    assert 1952805748 == aer.dec
    assert '1952805748 aer' == aer.aer
    assert '1.952805748 gaer' == aer.gaer
    assert '0.000000001952805748 aergo' == aer.aergo

    with pytest.raises(herapy.errors.ConversionException):
        herapy.Aer(0.1)

    aer = herapy.Aer()
    aer.dec = 1
    assert 1 == aer.dec
    assert '1 aer' == aer.aer
    assert '0.000000001 gaer' == aer.gaer
    assert '0.000000000000000001 aergo' == aer.aergo

    with pytest.raises(herapy.errors.ConversionException):
        aer = herapy.Aer()
        aer.dec = 0.1

    with pytest.raises(herapy.errors.ConversionException):
        aer = herapy.Aer()
        aer.dec = 0.0001 / AERGO_UNIT_PRECISION

    aer = herapy.Aer(10000000000000000 / 1)
    assert '1000000000000000 aer' == aer.aer
    assert '1000000 gaer' == aer.gaer
    assert '0.001 aergo' == aer.aergo

    aer = herapy.Aer()
    aer.dec = 10000000000000000 / 1
    assert '1000000000000000 aer' == aer.aer
    assert '1000000 gaer' == aer.gaer
    assert '0.001 aergo' == aer.aergo

    with pytest.raises(herapy.errors.ConversionException):
        aer = herapy.Aer()
        aer.dec = 10000000000000000 / 3

    aer = herapy.Aer(123141000000000000000000 / 10)
    assert '12314100000000000000000 aer' == aer.aer
    assert '12314100000000 gaer' == aer.gaer
    assert '12314.1 aergo' == aer.aergo


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
    assert str(aer1) == str(aer2)
    assert int(aer1) == int(aer2)
    assert bytes(aer1) == bytes(aer2)

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
    assert str(aer1) == str(aer2)
    assert int(aer1) == int(aer2)
    assert bytes(aer1) == bytes(aer2)

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
    assert str(aer1) == str(aer2)
    assert int(aer1) == int(aer2)
    assert bytes(aer1) == bytes(aer2)

    aer = aer1 * aer2
    assert isinstance(aer, herapy.Aer)
    assert aer.aer == str(aer)
    assert 249999999100000000810000000999999998200000000000000001 == aer.dec
    assert '249999999100000000810000000999999998.200000000000000001 aergo' == aer.aergo
    assert '249999999100000000810000000999999998200000000.000000001 gaer' == aer.gaer
    assert '249999999100000000810000000999999998200000000000000001 aer' == aer.aer


def test_op_div():
    aer1 = herapy.Aer('2')
    aer2 = herapy.Aer('10')

    with pytest.raises(herapy.errors.ConversionException):
        aer1 / aer2

    aer = aer2 / aer1
    assert isinstance(aer, herapy.Aer)
    assert aer.aer == str(aer)
    assert 5 == aer.dec
    assert '0.000000000000000005 aergo' == aer.aergo
    assert '0.000000005 gaer' == aer.gaer
    assert '5 aer' == aer.aer

    aer1 = herapy.Aer('499999999100000000000000001 aer')
    aer2 = herapy.Aer('499999999100000000000000001 aer')
    assert str(aer1) == str(aer2)
    assert int(aer1) == int(aer2)
    assert bytes(aer1) == bytes(aer2)

    aer = aer1 // aer2
    assert isinstance(aer, herapy.Aer)
    assert aer.aer == str(aer)
    assert 1 == aer.dec
    assert '0.000000000000000001 aergo' == aer.aergo
    assert '0.000000001 gaer' == aer.gaer
    assert '1 aer' == aer.aer
