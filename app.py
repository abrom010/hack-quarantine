import flask
from flask import jsonify
import os
import mysql.connector

application = flask.Flask(__name__)
db = mysql.connector.connect(host="localhost", user="root", passwd="root", db="hackathon")

 #WHEN URL IS http://nameofwebsite.com/ DO THIS
@application.route('/')
def main():
    return flask.render_template('index.html')
# ^^^ RETURNS index.html AFTER HAVING PROCESSED IT USING THE render_template() FUNCTION

@application.route('/store')
def store():
    return flask.render_template('storepage.html')

@application.route('/addresses',methods=['GET'])
def addresses():
    if flask.request.method == 'GET':
        add = []
        cur = db.cursor()
        cur.execute("SELECT CONCAT(address, ', ', city, ', ', state, ', ', zip_code) AS FullAddress FROM groceryStores;")
        for i in cur:
            add.append(i[0])
    return jsonify(add)

# @application.route('/queue')
# def queue():
#     return flask.redirect('/store', code=302)

@application.route('/request',methods=['GET'])
def request():
    if flask.request.method == 'GET':
        list = []
        cur = db.cursor()
        cur.execute("SELECT grocery_id FROM groceryStores WHERE zip_code='27560';")
        for i in cur:
            list.append(i)
        return jsonify(list)


#ONLY RUNS THE FLASK APPLICATION IF THE APP.PY IS BEING USED AS THE DRIVER
if __name__ == '__main__':
    application.run()
