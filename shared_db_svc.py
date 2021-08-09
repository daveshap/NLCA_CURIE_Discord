import sqlite3
import flask
import json
from flask import request
import logging
from time import sleep, time
from random import seed, uniform


log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)
app = flask.Flask("shared DB")
dbfile = "shared_db.sqlite"


def start_db(dbcon, dbcur):
    dbcur.execute("CREATE TABLE IF NOT EXISTS shared (type text, time real, content text, last_access real, access_count real, uuid text, parent text);")
    dbcur.execute("CREATE INDEX IF NOT EXISTS content_idx ON shared(content);")
    dbcon.commit()
    dbcon.close()


def get_db_cursor_safe():
    while True:
        try:
            dbcon = sqlite3.connect(dbfile)
            dbcur = dbcon.cursor()
            return dbcon, dbcur
        except Exception as oops:
            print("error getting DB connection or cursor:", oops)
            sleep(uniform(0.05, 0.25))  # sleep a fraction of a second and then try again


@app.route("/save", methods=["POST"])
def save():
    payload = request.json
    dbcon, dbcur = get_db_cursor_safe()
    value = (payload["type"], payload["time"], payload["content"], 0, 0, payload["uuid"], payload["parent"])
    result = dbcur.execute("INSERT OR IGNORE INTO shared VALUES (?,?,?,?,?,?,?);", value)
    dbcon.commit()
    dbcon.close()
    return flask.Response(json.dumps(result), mimetype="application/json")


@app.route("/search", methods=["GET"])
def search():
    payload = request.json
    dbcon, dbcur = get_db_cursor_safe()
    command = "SELECT * FROM shared WHERE content like %s;" % "%"+query+"%"
    print('SEARCH:', command)
    result = dbcur.execute(command)
    results = result.fetchall()
    dbcon.close()
    records = [{"type": i[0], "time": i[1], "content": i[2], "last_access": i[3], "access_count": i[4], "uuid": i[5], "parent": i[6]} for i in results]
    return flask.Response(json.dumps(records), mimetype="application/json")


@app.route("/increment", methods=["POST"])
def increment():
    payload = request.json
    dbcon, dbcur = get_db_cursor_safe()
    command = "UPDATE shared SET access_count = access_count + 1 WHERE uuid = '%s';" % payload["uuid"]
    print('INCREMENT:', command)
    result = dbcur.execute(command)
    command = "UPDATE shared SET last_access = '%s' WHERE uuid = '%s';" % (time(), payload["uuid"])
    print('INCREMENT:', command)
    result = dbcur.execute(command)
    dbcon.commit()
    dbcon.close()
    return flask.Response(json.dumps(result), mimetype="application/json")


@app.route("/select", methods=["GET"])
def select():
    payload = request.json
    dbcon, dbcur = get_db_cursor_safe()
    #print(payload)
    command = "SELECT * FROM shared WHERE type LIKE '%s' ORDER BY %s %s LIMIT %s;" % (payload['type'], payload['orderby'], payload['orderdir'], payload['limit'])
    print('SELECT:', command)
    result = dbcur.execute(command)
    results = result.fetchall()
    dbcon.close()
    records = [{"type": i[0], "time": i[1], "content": i[2], "last_access": i[3], "access_count": i[4], "uuid": i[5], "parent": i[6]} for i in results]
    return flask.Response(json.dumps(records), mimetype="application/json")


if __name__ == "__main__":
    print("Starting Shared Database")
    seed()
    dbcon, dbcur = get_db_cursor_safe()
    start_db(dbcon, dbcur)
    app.run(host="0.0.0.0", port=8888)