# encoding: utf-8
from data import *
import numpy as np
import math


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


def to_binary(text_plain):
    # if it is chinese, there can't be 8
    # int("中".encode().hex(), 16)
    return ''.join(
        '{{0:0{}b}}'.format(math.ceil((len(bin(int(x.encode().hex(), 16))) - 2) / 8) * 8).format(
            int(x.encode().hex(), 16)) for x in text_plain)
    #yep, full of rubbish!


def to_binary_hex(hex_text):
    # what is that?
    # l = len(format(int(hex_text, 16), 'b'))
    re = '{0:064b}'.format(int(hex_text, 16), 'b')
    return re


def create_subkey(key_text):
    # not suitable for chinese
    # assert len(key_text) == 8
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


def f(r, k):
    e = transfer(r, E_BIT)
    eXORk = myXOR(e, k)
    sb1_8 = [None]
    for o in range(8):
        sb1_8 += extract_from_sbox(eXORk[1 + o * 6:7 + o * 6], o)
    f_ = transfer(sb1_8, P32)
    return f_


def extract_from_sbox(bit6, snum):
    assert len(bit6) == 6
    mul = [32, 8, 4, 2, 1, 16]
    bit6 = [mul[i] * bit6[i] for i in range(6)]
    num4 = S_BOX[snum][sum(bit6)]
    bit4 = '{0:04b}'.format(num4)
    bit4 = list(map(int, bit4))
    return bit4


def encrypy_block(message, key):
    # not suitable for chinese
    # assert len(message) == 8
    messgae2 = to_binary(message)
    message3 = [None] + list(map(int, messgae2))
    message4 = transfer(message3, IP)
    l, r = list(), list()
    l.append(message4[0:len(message4) // 2 + 1])
    r.append([None] + message4[len(message4) // 2 + 1:])
    for i in range(1, 16 + 1):
        l.append(r[i - 1])
        r.append(myXOR(l[i - 1], f(r[i - 1], key[i])))
    RL16 = r[16] + l[16][1:]
    encrypted = transfer(RL16, IP_1)
    encrypted2 = ''.join(str(e) for e in encrypted[1:])
    encrypted3 = hex(int(encrypted2, 2))[2:]
    return encrypted3


def decrypt_block(ciphertext, key):
    ciphertext2 = to_binary_hex(ciphertext)
    ciphertext3 = [None] + list(map(int, ciphertext2))
    ciphertext4 = transfer(ciphertext3, IP)
    l, r = list(), list()
    l.append(ciphertext4[0:math.ceil(len(ciphertext4) / 2)])
    r.append([None] + ciphertext4[len(ciphertext4) // 2 + 1:])
    try:
        for i in range(1, 16 + 1):  # [1-16]
            l.append(r[i - 1])
            r.append(myXOR(l[i - 1], f(r[i - 1], key[17 - i])))
    except:
        pass
    RL16 = r[16] + l[16][1:]
    decrypted = transfer(RL16, IP_1)
    decrypted2 = ''.join(str(e) for e in decrypted[1:])
    decrypted3 = hex(int(decrypted2, 2))[2:]
    #return decrypted3
    decrypted4 = bytes.fromhex(decrypted3).decode('utf-8')
    return decrypted4


class DesKey(object):
    pass
