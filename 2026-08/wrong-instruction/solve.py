encoded = b'x\253\267\260\272\300\342\303\337\344\372\364\366\f\f#\037.+B6@YTVbh{\203\204\213\216\230\255\273\270\204\303\320\342\330\362\372\364\004\001\023(\0263,2?MP`ldz\214'

flag = ''

for i, c in enumerate(encoded):
    f = (c - 8 * i - 0x37) % 256
    print(f, chr(f))
    flag += chr(f)

print(flag)
