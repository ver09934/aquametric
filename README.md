# aquametric

Stream stage monitoring.

## TODO

* [ ] Get submission to separate unit files working
    * Based off ID specified in post request (remember to convert to int first!)
    * Don't break the server (write a separate submit function and swap once working)
* [ ] Add unit configuration file for maps code to read
* [ ] Add URL args for sensor ID to sensor and plot pages
    * [ ] Graphs will also need an arg for metric to plot
    * [ ] Add logfile conversion to CSV (on-the-fly)
        * [ ] Add data download links on unit pages
    * [ ] Plots will need to parse time strings into `datetime`s
* [ ] Improve log conversion and submit tests
    * [ ] Run the log conversion on the server
    * [ ] Pass file to convert as command line arg
    * [ ] Write to new file, `"{}-new.{}".format(basename, extension)`
* [ ] Add configuration based off environment variables
* [ ] Add "about" page (as linked-to on currently deployed sensor)

## Setup

* Add config through environment variables (TODO: Describe)
* Add unit list `JSON` file (TODO: Describe)
* Deploy a sensor unit (TODO: Get sensor code into version control)

## Running (Development)

```bash
$ chmod +x run.sh
$ ./run.sh
```

## Apache Adventures

I suspect that the problem was just the virtualhost configuration, but here are all the steps that were taken:

* `sudo apt install apache2-dev`
* install `mod_wsgi` in `venv`
* `sudo adduser $USER www-data`
* `sudo chown -R flask-project-dir www-data:www-data` and `sudo chmod -R g+rw flask-project-dir`
* Make dirs/files in code absolute using `os.path.join()` and `os.path.dirname(__file__)`
    * See <https://modwsgi.readthedocs.io/en/develop/user-guides/application-issues.html#application-working-directory>
    * See <https://modwsgi.readthedocs.io/en/develop/user-guides/application-issues.html#access-rights-of-apache-user>

## Python `JSON` Notes

* Hello, `json.dumps`!
