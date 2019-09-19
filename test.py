from des import DesKey
import pyDes
key0 = DesKey(b"some key")                  # for DES
key1 = DesKey(b"a key for TRIPLE")          # for 3DES, same as "a key for TRIPLEa key fo"
key2 = DesKey(b"a 24-byte key for TRIPLE")  # for 3DES
key3 = DesKey(b"1234567812345678REAL_KEY")  # for DES, same as "REAL_KEY"
key0.is_single()  # -> True
key1.is_triple()  # -> True
key2.is_single()  # -> False
key3.is_triple()  # -> False
key0.encrypt(b"any long message")  # -> b"\x14\xfa\xc2 '\x00{\xa9\xdc;\x9dq\xcbr\x87Q"
key0.encrypt(b"any long message", initial=0)        # -> b"\x14\xfa\xc2 '\x00{\xa9\xb2\xa5\xa7\xfb#\x86\xc5\x9b"
key0.encrypt(b"any long message", initial=b"\0"*8)  # same as above
key0.encrypt(b"abc", padding=True)  # -> b"%\xd1KU\x8b_A\xa6"
key0.decrypt(b"%\xd1KU\x8b_A\xa6", padding=True)  # -> b"abc"
key0.decrypt(b"\x14\xfa\xc2 '\x00{\xa9\xdc;\x9dq\xcbr\x87Q")  # -> b"abc"