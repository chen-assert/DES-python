# encoding: utf-8
from data import *
import numpy as np

def shift(block28, len, contain_none=True):
    # why I persist in the 0-None?
    newblock = [None] + block28[len + 1:] + block28[1:len + 1]
    # print(newblock)
    return newblock


def transfer(oldlist, t):
    newlist = [None] * len(t)
    for i in range(len(t)):
        newlist[i] = oldlist[t[i]]
    return newlist


def to_binary(text):
    return ''.join('{0:08b}'.format(ord(x), 'b') for x in text)


def create_subkey(key_text):
    assert len(key_text) == 8
    bkey = to_binary(key_text)
    ckey = [None] + list(map(int, bkey))
    dkey = transfer(ckey, PC1)
    c, d = list(), list()
    c.append(dkey[0:29])
    d.append([None] + dkey[29:])
    for i in range(1, 16 + 1):
        c.append(shift(c[i - 1], SHIFT[i]))
        d.append(shift(d[i - 1], SHIFT[i]))
    k = list()
    for i in range(16 + 1):
        k.append(transfer(c[i] + d[i][1:], PC2))
    return k


def pla_convert(IP, num=8):
    print('IP = (\n0,')
    n = 0
    for i in IP:
        n += 1
        print("%d, " % (i + 1), end='')
        if n % num == 0: print()
    print(')')


def myXOR(a, b):
    assert len(a) == len(b)
    c = [None] * len(a)
    for i in range(len(a)):
        if a[i] == None or b[i] == None:
            continue
        c[i] = a[i] ^ b[i]
    return c


def f(r,k):
    e = transfer(r, E_BIT)
    eXORk = myXOR(e, k)
    sb1_8 = [None]
    for o in range(8):
        sb1_8 += extract_from_sbox(eXORk[1 + o * 6:7 + o * 6], o)
    f_ = transfer(sb1_8, P32)
    return f_


def extract_from_sbox(bit6, snum):
    assert len(bit6) == 6
    mul=[32,8,4,2,1,16]
    bit6=[mul[i]*bit6[i] for i in range(6)]
    num4=S_BOX[snum][sum(bit6)]
    bit4='{0:04b}'.format(num4)
    bit4=list(map(int, bit4))
    return bit4

class DesKey(object):
    pass
