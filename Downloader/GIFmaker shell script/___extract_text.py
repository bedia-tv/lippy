import re
import sys


with open(sys.argv[1]) as f:
    data = f.read()

# for k, v in rep1.items():
#     data = re.sub(k, v, data)

data = re.sub(r'\d+\n\d\d:\d\d:\d\d,\d\d\d[^\n]+\n', r'', data)
data = re.sub(r'\n+', r' ', data)

# name = "" + sys.argv[1].split('\')[-1]

with open(sys.argv[2], 'w') as f:
    f.write(data)

# print(name)
