from myDes import *
key = "some key"
encrypted = encrypt("加密测试test", key)
print(encrypted)
encrypted = encrypt("加密测试tesv", key)
print(encrypted)
decrypted = decrypt(encrypted, key)
print(decrypted)
