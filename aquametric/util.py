import os
import json
import datetime
import pytz

# ------------------ Sensor Config -----------------

def get_sensor_list(sensor_config):
    with open(sensor_config, "r") as f:
        sensors = json.load(f)
    return sensors.keys()

def get_sensor_info(sensor_id, sensor_config):
    with open(sensor_config, "r") as f:
        sensors = json.load(f)
    return sensors[sensor_id]

# ------------------ JSON Parsing ------------------

def swap_quotes(input_str):

    singleq_indices = [i for i, char in enumerate(input_str) if char == "'"]
    doubleq_indices = [i for i, char in enumerate(input_str) if char == '"']

    str_list = list(input_str)

    for i in singleq_indices:
        str_list[i] = '"'
    for i in doubleq_indices:
        str_list[i] = "'"
    
    return "".join(str_list)

def load_json(json_str):
    try:
        json_data = json.loads(json_str)
        print("JSON parsed without quote swap!")
    except:
        if "'" in json_str:
            if '"' in json_str:
                if json_str.index("'") < json_str.index('"'):
                    json_str = swap_quotes(json_str)
            else:
                json_str = swap_quotes(json_str)
        json_data = json.loads(json_str)
        print("JSON parsed using quote swap!")
    return json_data

# -------------------- Log Files -------------------

def get_logfile_path(data_dir, sensor_id):
    return os.path.join(data_dir, "{}.txt".format(sensor_id))

def get_json(logfile, latest=False, listform=False):

    with open(logfile, "r") as f:
        json_dumps = [json.loads(line) for line in f.readlines() if line.rstrip() != ""]
    
    if latest:
        return json_dumps[-1]
    if listform:
        return json_dumps
    else:
        return {snippet.pop('published_at'): snippet for snippet in json_dumps}

# -------------- Datetime Conversions --------------

date_format = '%Y-%m-%dT%H:%M:%S.%f%z'
my_timezone = 'US/Eastern'

def get_local_datetime(date_str):
    date = datetime.datetime.strptime(date_str, date_format)
    return date.astimezone(pytz.timezone(my_timezone))

# ---------------- Data Conversions ----------------

plot_formats = {
    "battery": "go-",
    "stage": "bo-",
    "temp": "ro-",
    "turbidity": "ko-",
    "conductivity": "co-"
}

data_units = {
    "battery": ("Battery Voltage", "V"),
    "stage": ("Stage Height", "cm"),
    "temp": ("Temperature", "degrees C"),
    "turbidity": ("Turbidity", "Turbids"),
    "conductivity": ("Conductivity", "Siemens/Meter")
}

def convert_stage(base_height, current_stage):
    pass

def plot(dates, values, field):

    import time
    while os.path.isfile("/tmp/mplock"):
        time.sleep(1)

    with open("/tmp/mplock", "w") as f:
        f.write("")

    import matplotlib.pyplot as plt
    from io import BytesIO

    fig, ax = plt.subplots(figsize=(13, 3))
    
    ax.plot(dates, values, plot_formats[field])
    ax.set_title("{} vs. Time".format(data_units[field][0]))
    ax.set_xlabel("Time")
    ax.set_ylabel("{} ({})".format(*data_units[field]))
    ax.grid()

    ax.margins(x=0.01, y=0.15) # Margins are percentages
    fig.tight_layout()

    bg_color = "#ededed"
    fig.patch.set_facecolor(bg_color)
    ax.patch.set_facecolor(bg_color)

    img_io = BytesIO()
    plt.savefig(img_io, format='png', facecolor=fig.get_facecolor())
    img_io.seek(0)

    plt.close()

    os.remove("/tmp/mplock")

    return img_io
