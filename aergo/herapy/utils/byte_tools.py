# -*- coding: utf-8 -*-

def bit_is_set(bits, i):
    return bits[int(i/8)]&(1<<(7-i%8)) != 0
