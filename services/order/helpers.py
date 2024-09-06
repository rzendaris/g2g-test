from decimal import Decimal

from currency_converter import CurrencyConverter


def point_to_usd_exchange(point):
    return point * 0.01


def usd_to_point_exchange(usd):
    return usd / Decimal(0.01)


def amount_conversion(amount, convert_from, convert_to='USD'):
    c = CurrencyConverter()
    return Decimal(c.convert(amount, convert_from, convert_to))
