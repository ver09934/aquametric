import os
import json
# import datetime

# ------------------ Sensor Config -----------------

def get_sensor_list(sensor_config):
    with open(sensor_config, "r") as f:
        sensors = json.load(f)
    return sensors.keys()

def get_sensor_info(sensor_id, sensor_config):
    with open(sensor_config, "r") as f:
        sensors = json.load(f)
    return sensors[sensor_id]

# -------------------- Log Files -------------------

def get_logfile_path(data_dir, sensor_id):
    return os.path.join(data_dir, "{}.txt".format(sensor_id))

# -------------- Datetime Conversions --------------
