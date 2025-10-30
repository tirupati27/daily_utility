import sys
'''
Usage: python encode.py <string to encode in a CLI command>
'''
if len(sys.argv)!=2:
    print(f"Usage: python {sys.argv[0]} <string-to-encode>")
    sys.exit(1)

string='''\033[1;35m'''+sys.argv[1]+'''\033[0m'''

data="""python -c "print(bytes(["""
for i in list(bytes(string, "utf-8")):
    data+=str(i)+","
print("\033[1;32mCopy the following command, and run it to get the original string\033[0m")
print()
print(data+''']).decode())"''')
print()