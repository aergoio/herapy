# -*- coding: utf-8 -*-

import decimal

from ..errors.conversion_exception import ConversionException
from ..utils.converter import bigint_to_bytes

UNITS_SIZE = {
    'aergo': 18,
    'gaer': 9,
    'aer': 0
}
AERGO_UNIT_PRECISION = UNITS_SIZE['aergo']


class Aer:
    """Return Aergo Unit, AER(/ˈɛəɹ/)."""
    def __init__(self, value='0 aer'):
        if isinstance(value, bytes):
            value = int.from_bytes(value, byteorder='big')
        self.__aer = self._parsing_value(value)

    def _parsing_value(self, v):
        try:
            decimal.Decimal(v)
            v = self._decimal_to_str(v) + ' aer'
        except decimal.InvalidOperation:
            v = v.strip().lower()

        unit = ''
        size = -1
        for u, s in UNITS_SIZE.items():
            if v.endswith(u):
                unit = u
                size = s
                break

        if size < 0:
            raise ConversionException('cannot recognize aergo unit: ' + v)

        v = v[:len(v) - len(unit)].strip()
        if not '.' in v:
            zero_padding = UNITS_SIZE[unit]
        else:
            number, below = v.split('.')
            if len(below) > UNITS_SIZE[unit]:
                raise ConversionException('too small value below decimal point: ' + v)

            v = number + below
            zero_padding = UNITS_SIZE[unit] - len(below)

        v = v + '0' * zero_padding

        try:
            decimal.getcontext().prec = AERGO_UNIT_PRECISION
            v = decimal.Decimal(v)
        except decimal.InvalidOperation:
            raise ConversionException('cannot recognize value: ' + v)

        return v

    @staticmethod
    def _decimal_to_str(d):
        s = str(d).lower()
        if 'e' in s:
            digits, exp = s.split('e')

            exp = int(exp)
            if exp > 0 and '.' in digits:
                exp = exp - len(digits.split('.')[1]) + 1

            digits = digits.replace('.', '').replace('-', '')

            zero_padding = '0' * (abs(exp) - 1)  # minus 1 for decimal point in the sci notation
            sign = '-' if d < 0 else ''

            if exp > 0:
                s = '{}{}{}'.format(sign, digits, zero_padding)
            else:
                s = '{}0.{}{}'.format(sign, zero_padding, digits)
        return s

    @property
    def aer(self):
        return self._decimal_to_str(self.__aer) + ' aer'

    @property
    def gaer(self):
        with decimal.localcontext() as ctx:
            ctx.prec = len(str(self.__aer))
            v = self.__aer / decimal.Decimal(10 ** UNITS_SIZE['gaer'])
            s = self._decimal_to_str(v) + ' gaer'
        return s

    @property
    def aergo(self):
        with decimal.localcontext() as ctx:
            ctx.prec = len(str(self.__aer))
            v = self.__aer / decimal.Decimal(10 ** UNITS_SIZE['aergo'])
            s = self._decimal_to_str(v) + ' aergo'
        return s

    @property
    def dec(self):
        return self.__aer

    @dec.setter
    def dec(self, v):
        self.__aer = self._parsing_value(v)

    def __str__(self):
        return self.aer

    def __int__(self):
        return int(self.dec)

    def __bytes__(self):
        return bigint_to_bytes(int(self))

    def __add__(self, other):
        with decimal.localcontext():
            decimal.setcontext(decimal.DefaultContext)
            v = self.dec + other.dec
        return Aer(str(v))

    def __sub__(self, other):
        with decimal.localcontext():
            decimal.setcontext(decimal.DefaultContext)
            v = self.dec - other.dec
        return Aer(str(v))

    def __mul__(self, other):
        with decimal.localcontext() as ctx:
            ctx.prec = decimal.MAX_PREC
            v = self.dec * other.dec
        return Aer(str(v))

    def __floordiv__(self, other):
        with decimal.localcontext():
            decimal.setcontext(decimal.DefaultContext)
            v = self.dec // other.dec
        return Aer(str(v))

    def __truediv__(self, other):
        with decimal.localcontext():
            decimal.setcontext(decimal.DefaultContext)
            v = self.dec / other.dec
        return Aer(str(v))

