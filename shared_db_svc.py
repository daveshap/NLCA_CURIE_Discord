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
    try:
        payload = request.json
        dbcon, dbcur = get_db_cursor_safe()
        value = (payload["type"], payload["time"], payload["content"], 0, 0, payload["uuid"], payload["parent"])
        result = dbcur.execute("INSERT OR IGNORE INTO shared VALUES (?,?,?,?,?,?,?);", value)
        dbcon.commit()
        dbcon.close()
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
    except Exception as oops:
        print('error in save:', oops)
        return json.dumps({'success':False, 'message': oops}), 500, {'ContentType':'application/json'} 


@app.route("/search", methods=["GET"])
def search():
    try:
        payload = request.json
        dbcon, dbcur = get_db_cursor_safe()
        print(payload)
        command = "SELECT * FROM shared WHERE content LIKE '%{}%';".format(payload['query'].replace("'",''))  # TODO handle if query has apostrophe
        print('SEARCH:', command)
        result = dbcur.execute(command)
        results = result.fetchall()
        dbcon.close()
        records = [{"type": i[0], "time": i[1], "content": i[2], "last_access": i[3], "access_count": i[4], "uuid": i[5], "parent": i[6]} for i in results]
        return flask.Response(json.dumps(records), mimetype="application/json")
    except Exception as oops:
        print('error in search:', oops)
        return json.dumps({'success':False, 'message': oops}), 500, {'ContentType':'application/json'} 


@app.route("/increment", methods=["POST"])
def increment():
    try:
        payload = request.json
        dbcon, dbcur = get_db_cursor_safe()
        command = "UPDATE shared SET access_count = access_count + 1 WHERE uuid = '{}';".format(payload["uuid"])
        print('INCREMENT:', command)
        result = dbcur.execute(command)
        command = "UPDATE shared SET last_access = '{}' WHERE uuid = '{}';".format(time(), payload["uuid"])
        print('INCREMENT:', command)
        result = dbcur.execute(command)
        dbcon.commit()
        dbcon.close()
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
    except Exception as oops:
        print('error in increment:', oops)
        return json.dumps({'success':False, 'message': oops}), 500, {'ContentType':'application/json'} 


@app.route("/select", methods=["GET"])
def select():
    try:
        payload = request.json
        dbcon, dbcur = get_db_cursor_safe()
        #print(payload)
        command = "SELECT * FROM shared WHERE type LIKE '{}' ORDER BY {} {} LIMIT {};".format(payload['type'], payload['orderby'], payload['orderdir'], payload['limit'])
        print('SELECT:', command)
        result = dbcur.execute(command)
        results = result.fetchall()
        dbcon.close()
        records = [{"type": i[0], "time": i[1], "content": i[2], "last_access": i[3], "access_count": i[4], "uuid": i[5], "parent": i[6]} for i in results]
        return flask.Response(json.dumps(records), mimetype="application/json")
    except Exception as oops:
        print('error in select:', oops)
        return json.dumps({'success':False, 'message': oops}), 500, {'ContentType':'application/json'} 



if __name__ == "__main__":
    print("Starting Shared Database")
    seed()
    dbcon, dbcur = get_db_cursor_safe()
    start_db(dbcon, dbcur)
    app.run(host="0.0.0.0", port=8888)