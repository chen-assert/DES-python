from myDes import *
import importlib
key = "some key"
encrypted = encrypt("加密测试test", key)
print(encrypted)
decrypted = decrypt(encrypted, key)
print(decrypted)
