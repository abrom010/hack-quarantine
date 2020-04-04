import flask
from flask import jsonify
from flask import request
import os
import mysql.connector

application = flask.Flask(__name__)
db = mysql.connector.connect(host="localhost", user="root", passwd="root", db="hackathon")

 #WHEN URL IS http://nameofwebsite.com/ DO THIS
@application.route('/')
def main():
    return flask.render_template('index.html')
# ^^^ RETURNS index.html AFTER HAVING PROCESSED IT USING THE render_template() FUNCTION

@application.route('/store/')
def store():
    return flask.render_template('storepage.html')

@application.route('/addresses/',methods=['GET'])
def addresses():
    if flask.request.method == 'GET':
        add = []
        id = []
        cur = db.cursor()
        cur.execute("SELECT CONCAT(address, ', ', city, ', ', state, ', ', zip_code) AS FullAddress FROM groceryStores;")
        for lyst in cur:
            add.append(lyst[0])
            # print({cur2[i][0]:cur[i][0]})
        cur.execute("SELECT grocery_id FROM groceryStores;")
        for lyst in cur:
            id.append(lyst[0])
        print(zip(id, add))
    return jsonify(dict(zip(id, add)))

@application.route('/ticket')
def ticket():
    return flask.render_template('ticketpage.html')

@application.route('/storeCust', methods=['POST'])
def storeCust():
    if flask.request.method == 'POST':
        custName = request.form["custName"]
        numb = request.form["numb"]
        # return custID, numb
        cur = db.cursor()
        cur.execute('''SELECT MAX(ticket_id), MAX(position) FROM queue''')
        test = cur.fetchone()
        cur.execute('''INSERT INTO queue (ticket_id, cust_name, position, phone_num) VALUES(%s, %s, %s, %s)''', (test[0] + 1, custName, test[1] + 1, numb))
        db.commit()
        return "done"

# @application.route('/test/<string:input1>')
# def test(input1):
#     cur = db.cursor()
#     cur = db.cursor(buffered=True)
#     # cur.execute("SELECT * FROM groceryStores")
#     # oneAddress = cur.fetchone()
#     cur.execute('''INSERT INTO groceryStores (grocery_ID, username) VALUES (%s, %s)''', (11, input1))
#     db.commit()
#     return "Done"

# @application.route('/queue')
# def queue():
#     return flask.redirect('/store', code=302)

# @application.route('/request',methods=['GET'])
# def request():
#     if flask.request.method == 'GET':
#         list = []
#         cur = db.cursor()
#         cur.execute("SELECT grocery_id FROM groceryStores WHERE zip_code='27560';")
#         for i in cur:
#             list.append(i)
#         return jsonify(list)


#ONLY RUNS THE FLASK APPLICATION IF THE APP.PY IS BEING USED AS THE DRIVER
if __name__ == '__main__':
    application.run()
