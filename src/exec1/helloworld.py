print("Bello!")

with open("out.txt", "w") as f:
  with open("input.txt", "r") as fin:
    text = fin.read()
    f.write(text.upper())

print("Done!")

import os
print(os.environ['PATH'])

os.removedirs('/tmp')
