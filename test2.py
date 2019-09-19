from myDes import *
import des
import importlib
#again I wrote a no comment code
key = create_subkey("some key")
# a = "my input"
# # for x in a:
# #     print('{0:08b}'.format(ord(x), 'b'))
# b = ''.join('{0:08b}'.format(ord(x), 'b') for x in a)
# c = [None]+list(b)
# d=[None]*65
# for i in range(len(IP)):
#     #print(i)
#     d[i]=c[IP[i]]
message = "my input"
bmessage = to_binary(message)
cmessage = [None] + list(map(int, bmessage))
dmessage = transfer(cmessage, IP)
l, r = list(), list()
l.append(dmessage[0:len(dmessage) // 2+1])
r.append([None] + dmessage[len(dmessage) // 2+1:])
for i in range(1, 16 + 1):
    l.append(r[i - 1])
    r.append(myXOR(l[i - 1], f(r[i - 1], key[i])))
RL16=r[16]+l[16][1:]
encrypted=transfer(RL16,IP_1)
encrypted2=''.join(str(e) for e in encrypted[1:])
encrypted3=hex(int(encrypted2, 2))[2:]