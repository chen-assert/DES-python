# encoding: utf-8
from data import *
import numpy as np
import math
import eel


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


def to_binary_text(text_plain):
    # bin(int("中".encode().hex(), 16)='0b111001001011100010101101'
    # -2是为了删掉"0b"
    re = ''.join(
        '{{0:0{}b}}'.format(math.ceil((len(bin(int(x.encode().hex(), 16))) - 2) / 8) * 8).format(
            int(x.encode().hex(), 16)) for x in text_plain)
    return re
    # yep, full of rubbish!


def to_binary_hex(hex_text):
    # the first format is to construct the string that indicate the format length
    re = '{{0:0{}b}}'.format(len(hex_text) * 4).format(int(hex_text, 16), 'b')
    return re


def create_subkey(key_text):
    bkey = to_binary_text(key_text)
    assert len(bkey) >= 64
    bkey = bkey[:64]
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


def listXOR(a, b):
    assert len(a) == len(b)
    c = [None] * len(a)
    for i in range(len(a)):
        if a[i] == None or b[i] == None:
            continue
        c[i] = a[i] ^ b[i]
    return c


def f(r, k):
    e = transfer(r, E_BIT)
    eXORk = listXOR(e, k)
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


@eel.expose
def encrypt(message: str, key_text, padding=True) -> str:
    try:
        key = create_subkey(key_text)
    except Exception:
        return "Create subkey fail, its length may not enough(>=8 bytes)"
    if padding == True and utf8len(message) % 8 != 0:
        # need padding
        pad_len = 8 - (utf8len(message) % 8)
        message += (bytes([pad_len]) * pad_len).decode()
    # now this part is full of redundancy, need further optimize
    encrypted = ""
    assert utf8len(message) % 8 == 0
    message_binary = to_binary_text(message)
    for i in range(len(message_binary) // 64):
        encrypted += encrypt_block(message_binary[i * 64:i * 64 + 64], key)
    return encrypted


@eel.expose
def decrypt(ciphermessage: str, key_text, padding=True) -> str:
    try:
        key = create_subkey(key_text)
    except Exception:
        return "Create subkey fail, its length may not enough(>=8 bytes)"
    decrypted_hex: str = ""
    try:
        assert utf8len(ciphermessage) % 16 == 0
    except Exception:
        return "Sth went wrong, maybe your input data is illegal"
    ciphermessage_binary = to_binary_hex(ciphermessage)
    for i in range(len(ciphermessage_binary) // 64):
        decrypted_hex += decrypt_block(ciphermessage_binary[i * 64:i * 64 + 64], key)
    try:
        decrypted = bytes.fromhex(decrypted_hex).decode('utf-8')
    except Exception:
        return "Sth went wrong, maybe your key is wrong"
    if padding == True:
        last = ord(decrypted[-1])
        if last < 8:
            for i in range(last):
                if decrypted[-1 - i] != decrypted[-1]:
                    # not conformity with padding rule
                    return decrypted
            return decrypted[:-last]
    return decrypted


def encrypt_block(block: str, key):
    assert len(block) == 64
    # message2 = to_binary(message)
    block2 = [None] + list(map(int, block))
    block3 = transfer(block2, IP)
    l, r = list(), list()
    l.append(block3[0:len(block3) // 2 + 1])
    r.append([None] + block3[len(block3) // 2 + 1:])
    for i in range(1, 16 + 1):
        l.append(r[i - 1])
        r.append(listXOR(l[i - 1], f(r[i - 1], key[i])))
    RL16 = r[16] + l[16][1:]
    encrypted = transfer(RL16, IP_1)
    encrypted2 = ''.join(str(e) for e in encrypted[1:])
    # encrypted3 = hex(int(encrypted2, 2))[2:]
    encrypted3 = "{0:016x}".format(int(encrypted2, 2))
    return encrypted3


def decrypt_block(cipherblock: str, key, decode=False):
    # assert len(cipherblock) == 64
    # cipherblock = to_binary_hex(cipherblock)
    ciphertext3 = [None] + list(map(int, cipherblock))
    ciphertext4 = transfer(ciphertext3, IP)
    l, r = list(), list()
    l.append(ciphertext4[0:math.ceil(len(ciphertext4) / 2)])
    r.append([None] + ciphertext4[len(ciphertext4) // 2 + 1:])
    try:
        for i in range(1, 16 + 1):  # [1-16]
            l.append(r[i - 1])
            r.append(listXOR(l[i - 1], f(r[i - 1], key[17 - i])))
    except:
        pass
    RL16 = r[16] + l[16][1:]
    decrypted = transfer(RL16, IP_1)
    decrypted_binary: str = ''.join(str(e) for e in decrypted[1:])
    decrypted_hex: str = hex(int(decrypted_binary, 2))[2:]
    if decode is False: return decrypted_hex
    decrypted_decode: str = bytes.fromhex(decrypted_hex).decode('utf-8')
    return decrypted_decode


class DesKey(object):
    pass


def index_convert(IP, num=8):
    print('IP = (\n0,')
    n = 0
    for i in IP:
        n += 1
        print("%d, " % (i + 1), end='')
        if n % num == 0: print()
    print(')')


def utf8len(s):
    return len(s.encode('utf-8'))
