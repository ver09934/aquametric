# aquametric

Stream stage monitoring.

## Running (Development)

Create a virtual environment:

```bash
$ python3 -m venv venv
$ . venv/bin/activate
$ pip install -r requirements.txt
```

Run the flask application:

```bash
$ export FLASK_ENV=development
$ export FLASK_APP=aquametric
$ flask run
```

## TODO

* [ ] Figure out how unit configuration is going to work
    * Will the unit list be stored on the server, or will any new unit be allowed to add data to the database, and in doing so be added to the unit list?
* [ ] Create a way to interact with a MySQL or SQLite database
* [ ] Create a way to submit data to the database via an HTTP request
* [ ] Create a unit list page (either list-based or map-based)
* [ ] Create a unit page, with either matplotlib (noninteractive) or javascript (interactive) plots
