from myDes import *
import des
import importlib

# again I wrote a no comment code
key = "some key"
encrypted = encrypt("加密测试test", key)
print(encrypted)
decrypted = decrypt(encrypted, key)
print(decrypted)
