import os

# TODO: Pass file to convert as command line arg
# TODO: Write to new file, basename-new.extension

with open(os.path.join(os.path.dirname(__file__), "test.txt"), "r") as f:
        lines_to_write = ["{" + "{".join(line.split("{")[1:]) for line in f.readlines() if "Measurement" in line]
        # NOTE: readlines does not rstrip()
    # Add jsonification step
    with open(os.path.join(os.path.dirname(__file__), "test.txt"), "w") as f:
        for line in lines_to_write:
            f.write(line)
    return "Finished!"
