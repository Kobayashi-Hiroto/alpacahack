import os
import re
import subprocess

FLAG = os.environ.get("FLAG", "Alpaca{dummy}")

def sanitize(txt:str):
    txt = re.sub(r'[^-0-9]', '', txt)
    return txt[:3]

a = sanitize(input("A> "))
b = sanitize(input("B> "))
c = sanitize(input("C> "))

code = """#include <stdio.h>
#define CUBE(x) (x * x * x)

int main(void)
{
    setbuf(stdin,  NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);

    if ("""+a+""" <= 0 || """+b+""" <= 0 || """+c+""" <= 0) {
        printf("Invalid.\\n");
    }
    else if (CUBE("""+a+""") + CUBE("""+b+""") == CUBE("""+c+""")) {
        printf("Seriously? Flag: """+FLAG+"""\\n");
    }
    else {
        printf("Expected.\\n");
    }

    return 0;
}
"""

open("/app/work/chall.c", "w").write(code)

try:
    subprocess.run(["gcc", "-o", "/app/work/chall", "/app/work/chall.c"], check=True)
    subprocess.run(["/app/work/chall"])
except:
    pass
