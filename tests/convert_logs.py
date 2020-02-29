import sys
import os
import argparse
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from aquametric import util

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('logfile', type=str, help='Path to logfile to convert')
    args = parser.parse_args()

    file_path = os.path.expanduser(os.path.abspath(args.logfile))

    file_dir = os.path.dirname(file_path)
    file_basename = os.path.basename(file_path)
    file_name, file_ext = os.path.splitext(file_basename)
    out_path = os.path.join(file_dir, "{}-converted{}".format(file_name, file_ext))

    if not os.path.isfile(file_path):
        print("Path is not a file... exiting!")
        exit(1)
    
    with open(file_path, "r") as f:
        lines_to_write = []
        for line in f.readlines():
            # The "001" is not needed for most files, but one in particular needed it
            # (The line without "001" had unquoted strings in it)
            if all([substr in line for substr in ["data", "id", "published_at", "001"]]):
                json_str = "{" + "{".join(line.split("{")[1:])
                json_data = util.load_json(json_str)
                if "data" in json_data:
                    if isinstance(json_data["data"], str):
                        json_data["data"] = util.load_json(json_data["data"])
                lines_to_write.append(json.dumps(json_data).rstrip() + "\n")

    if os.path.exists(out_path):
        os.remove(out_path)
    with open(out_path, "w") as f:
        f.writelines(lines_to_write)
    
    print("Finished!")

if __name__ == "__main__":    
    main()
