import os
import argparse
import json

# NOTE: readlines does not rstrip(), and writelines() does not add newlines

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
            if all([substr in line for substr in ["001", "Measurement"]]):
                
                json_str = "{" + "{".join(line.split("{")[1:])

                # TODO: Further clean the diry JSON

                '''
                # json_data = json.loads(json_str)
                if isinstance(json_data['data'], str):
                    json_data['data'] = json.loads(json_data['data'])
                lines_to_write.append(json.dumps(json_data))
                '''
    
    print(lines_to_write)
    
    with open(out_path, "w") as f:
        f.writelines(lines_to_write)
    
    print("Finished!")

if __name__ == "__main__":    
    main()
