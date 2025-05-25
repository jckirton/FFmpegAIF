import os
from sys import path

programDir = path[0]
tempDir = f"{programDir}/temp"
os.system(f"mkdir {tempDir}")

with open(f"{tempDir}/test.txt", "w") as f:
    f.write("test")
