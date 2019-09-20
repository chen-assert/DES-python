from myDes import *
import importlib
#again I wrote a no comment code
key = create_subkey("some key")
encrypted=encrypy_block("中文12", key)
print(encrypted)
decrypted=decrypt_block(encrypted, key)
print(decrypted)
