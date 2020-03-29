import flask
from flask import jsonify
import os
import mysql.connector

application = flask.Flask(__name__)

 #WHEN URL IS http://nameofwebsite.com/ DO THIS
@application.route('/')
def main():
    return flask.render_template('index.html')
# ^^^ RETURNS index.html AFTER HAVING PROCESSED IT USING THE render_template() FUNCTION

@application.route('/queue')
def queue():
    return flask.render_template('queue.html')

@application.route('/request',methods=['GET'])
def request():
    if flask.request.method == 'GET':
        list = []
        db = mysql.connector.connect(host="localhost", user="root", passwd="root", db="hackathon")
        cur = db.cursor()
        cur.execute("SELECT * FROM inStore")
        for i in cur:
            list.append(i)
        return jsonify(list)


#ONLY RUNS THE FLASK APPLICATION IF THE APP.PY IS BEING USED AS THE DRIVER
if __name__ == '__main__':
    application.run()
