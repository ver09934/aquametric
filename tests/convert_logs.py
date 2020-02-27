import os

file = "../aquametric/test.txt"

# NOTE: readlines does not rstrip(), and writelines() does not add newlines
# TODO: Gotta actually convert everything to JSON...

with open(file, "r") as f:
    lines_to_write = ["{" + "{".join(line.split("{")[1:]) for line in f.readlines() if all([substr in line for substr in ["001", "Measurement"]])]
with open(file, "w") as f:
    f.writelines()
print("Finished!")
