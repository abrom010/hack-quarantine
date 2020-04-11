import flask
from flask import jsonify
from flask import request
from flask import flash
import random
import os
import mysql.connector
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import re

# Create Application
application = flask.Flask(__name__)
application.secret_key = 'secret'

# Connect to database
db = mysql.connector.connect(host="35.225.208.225", user="Aaron", passwd="1AsrzsrGJk0l1uEa", db="hackathon")
#db = mysql.connector.connect(host="localhost", user="root", passwd="root", db="hackathon")

# Twilio SID Info
account_sid = 'ACf50d76cba4344433156557d73e062105'
auth_token = '5fd058e27df16f50cf47db3f4d4ce732'
client = Client(account_sid, auth_token)

# Route to Homepage at initial Launch
@application.route('/')
def main():
    return flask.render_template('index.html')

# Route to the Map Page
@application.route('/map/')
def map():
    return flask.render_template('mappage.html')

@application.route('/mainStore')
def mainstore():
    return flask.render_template('mainstore.html')

@application.route('/storeEntry')
def storeEntry():
    return flask.render_template('storeentry.html')

@application.route('/generateStore',methods=['POST'])
def generateStore():
    if flask.request.method == 'POST':
        storeName = request.form["storeName"]
        storeAddress = request.form["storeAddress"]
        storeCity = request.form["storeCity"]
        storeState = request.form["storeState"]
        storeZip = request.form["storeZip"]
        cur = db.cursor()
        cur.execute('''SELECT MAX(grocery_id) FROM groceryStores;''')
        test = cur.fetchone()
        currId = test[0] + 1
        if (test[0]):
            cur.execute('''INSERT INTO groceryStores (grocery_id, store_name, address, city, state, zip_code) VALUES(%s, %s, %s, %s, %s, %s)''', (currId, storeName, storeAddress, storeCity, storeState, storeZip))
        else:
            cur.execute('''INSERT INTO groceryStores (grocery_id, store_name, address, city, state, zip_code) VALUES(%s, %s, %s, %s, %s, %s)''', (1, storeName, storeAddress, storeCity, storeState, storeZip))
        db.commit()

        cur.execute("CREATE TABLE queue" + str(currId) + ''' ( ticket_id INT AUTO_INCREMENT PRIMARY KEY, \
        cust_name VARCHAR(25) DEFAULT 'Walk-In', \
        position INT NOT NULL, \
        ticket_gen_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, \
        phone_num VARCHAR(12) NOT NULL, \
        authentication VARCHAR(160) DEFAULT NULL );''')
        cur.close()
        return flask.render_template('storesuccesspage.html')


# Generates list of addresses for Google Maps API, happens on the storepage HTML
@application.route('/ids/',methods=['GET'])
def addresses():
    if flask.request.method == 'GET':
        ids = []
        cur = db.cursor()
        cur.execute("SELECT grocery_id FROM groceryStores;")
        for lyst in cur:
            ids.append(lyst[0])
        cur.close()
        return jsonify(ids)

@application.route('/address', methods=['POST'])
def storeAddress():
    if flask.request.method == 'POST':
        groceryID = request.form["groceryID"]
        print(groceryID)
        cur = db.cursor()
        query = "SELECT CONCAT(address, ', ', city, ', ', state, ', ', zip_code) AS FullAddress FROM groceryStores WHERE grocery_id = "+groceryID+";"
        cur.execute(query)
        address = cur.fetchone()[0]
        print(address)
        cur.close()
        return jsonify(address)

@application.route('/name', methods=['POST'])
def storeName():
    if flask.request.method == 'POST':
        groceryID = request.form["groceryID"]
        cur = db.cursor()
        query = "SELECT store_name FROM groceryStores WHERE grocery_id = "+groceryID+";"
        cur.execute(query)
        name = cur.fetchone()[0]
        print(name)
        cur.close()
        return jsonify(name)

# Route to the ticketpage
@application.route('/ticket/<string:id>')
def ticket(id):
    return flask.render_template('ticketpage.html', id=id)

# Get store name, add, csz to populate ticketpage.html
@application.route('/getData',methods=['POST'])
def getData():
    if flask.request.method == 'POST':
        groceryID = request.form["id"]
        result = []
        query = '''SELECT store_name, address, city, state, zip_code FROM groceryStores WHERE grocery_id = '''+groceryID+";"
        cur = db.cursor()
        cur.execute(query)
        for i in cur:
            result.append(i)
        cur.close()
        return jsonify(result)

# Get queue size to populate ticketpage.html
@application.route('/getSize')
def getSize():
    if flask.request.method == 'GET':
        cur = db.cursor()
        cur.execute('''SELECT MAX(position) FROM queue''')
        result = cur.fetchone()
        cur.close()
        return jsonify(result)

# Generates the user to database, when they enter Name and Phone number on ticketpage.
# Then texts them the code and sends them to TicketSuccessPage
@application.route('/generateCustomer', methods=['POST'])
def generateCustomer():
    if flask.request.method == 'POST':
        custName = request.form["custName"]
        numb = request.form["numb"]
        numb = formatNumb(numb)
        authToken = random.randint(100000, 999999)
        cur = db.cursor()
        cur.execute('''SELECT MAX(ticket_id), MAX(position) FROM queue''')
        test = cur.fetchone()
        if (test[0]):
            cur.execute('''INSERT INTO queue (ticket_id, cust_name, position, phone_num, authentication) VALUES(%s, %s, %s, %s, %s)''', (test[0] + 1, custName, test[1] + 1, numb, authToken))
        else:
            cur.execute('''INSERT INTO queue (ticket_id, cust_name, position, phone_num, authentication) VALUES(%s, %s, %s, %s, %s)''', (1, custName, 1, numb, authToken))
        db.commit()
        meesage = client.messages.create(
            body = authToken,
            messaging_service_sid = "MGc4338215ff683f8a462df06e206eb8fb",
            to = numb
        )
        flash('Check your phone for your check-in code!')
        cur.close()
        return flask.render_template('TicketSuccessPage.html')

@application.route('/position',methods=['POST','GET'])
def position():
    if flask.request.method == 'POST':
        code = request.form["code"]
        if len(code) == 6:
            cur = db.cursor()
            cur.execute("SELECT position FROM queue WHERE authentication = "+code+";")
            lyst = cur.fetchall()
            if len(lyst) == 1:
                position = lyst[0][0]
                cur.execute("DELETE FROM queue WHERE authentication = "+code+";")
                db.commit()
                cur.execute("UPDATE queue SET position = position-1 WHERE position >= "+str(position)+";")
                db.commit()
                cur.close()
            return flask.render_template('position.html')
    return flask.render_template('position.html')

# @application.route('/enter',methods=['POST'])
# def enter():
#     if flask.request.method == 'POST':
#         code = request.form["code"]
#         cur = db.cursor()
#         cur.execute("SELECT position FROM queue WHERE authentication = "+code+";")
#         lyst = cur.fetchall()
#         if len(lyst) == 1:
#             position = lyst[0][0]
#             cur.execute("DELETE FROM queue WHERE authentication = "+code+";")
#             db.commit()
#             cur.execute("UPDATE queue SET position = position-1 WHERE position >= "+str(position)+";")
#             db.commit()
#         return flask.render_template('position.html')

@application.route('/populateTable', methods=['GET'])
def populateTable():
    if flask.request.method == 'GET':
        name = []
        cur = db.cursor()
        cur.execute('''SELECT cust_name FROM queue''')
        for i in cur:
            name.append(i[0])
        return jsonify(name)

# Format the phone number for Twilio
def formatNumb(num):
    print(num)
    num = re.sub("[^0-9]", "", num)
    newNum = "+1" + num
    return newNum

#ONLY RUNS THE FLASK APPLICATION IF THE APP.PY IS BEING USED AS THE DRIVER
if __name__ == '__main__':
    application.run()
