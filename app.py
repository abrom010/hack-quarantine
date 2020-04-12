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
db = mysql.connector.connect(host="localhost", user="username", passwd="password", db="database")

# Twilio SID Info
account_sid = 'ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
auth_token = 'your_auth_token'
client = Client(account_sid, auth_token)

# Route to Homepage at initial Launch
@application.route('/')
def main():
    return flask.render_template('index.html')

# Route to the Map Page
@application.route('/map/')
def map():
    return flask.render_template('mappage.html')

# Route main store
@application.route('/mainStore')
def mainstore():
    return flask.render_template('mainstore.html')

# Route to store entry
@application.route('/storeEntry')
def storeEntry():
    return flask.render_template('storeentry.html')

# Posts a store to the database, creates a table for their queue
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
        if test[0]==None:
            currId = 1
        else:
            currId = test[0] + 1
        cur.execute('''INSERT INTO groceryStores (grocery_id, store_name, address, city, state, zip_code) VALUES(%s, %s, %s, %s, %s, %s)''', (currId, storeName, storeAddress, storeCity, storeState, storeZip))
        db.commit()

        cur.execute("CREATE TABLE queue" + str(currId) + ''' ( ticket_id INT AUTO_INCREMENT PRIMARY KEY, \
        cust_name VARCHAR(25) DEFAULT 'Walk-In', \
        position INT NOT NULL, \
        ticket_gen_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, \
        phone_num VARCHAR(12) NOT NULL, \
        authentication VARCHAR(160) DEFAULT NULL );''')
        cur.close()
        return flask.render_template('storesuccesspage.html',id=currId)


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

# Gets an address from grocery id
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

# Gets a name from grocery id
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
@application.route('/getSize',methods=['POST'])
def getSize():
    if flask.request.method == 'POST':
        groceryID = request.form["id"]
        cur = db.cursor()
        cur.execute('''SELECT MAX(position) FROM queue'''+groceryID+";")
        result = cur.fetchone()
        cur.close()
        return jsonify(result)

# Generates the user to database, when they enter Name and Phone number on ticketpage.
# Then texts them the code and sends them to TicketSuccessPage
@application.route('/generateCustomer', methods=['POST','GET'])
def generateCustomer():
    if flask.request.method == 'POST':
        custName = request.form["custName"]
        groceryID = request.form["id"]
        numb = request.form["numb"]
        numb = formatNumb(numb)
        authToken = random.randint(100000, 999999)
        cur = db.cursor()
        cur.execute('''SELECT MAX(ticket_id), MAX(position) FROM queue'''+groceryID+";")
        test = cur.fetchone()
        if (test[0]):
            cur.execute("INSERT INTO queue"+groceryID+" (ticket_id, cust_name, position, phone_num, authentication) VALUES(%s, %s, %s, %s, %s)", (test[0] + 1, custName, test[1] + 1, numb, authToken))
        else:
            cur.execute("INSERT INTO queue"+groceryID+" (ticket_id, cust_name, position, phone_num, authentication) VALUES(%s, %s, %s, %s, %s)", (1, custName, 1, numb, authToken))
        db.commit()
        msg = "Thank you for using Queue Up! Your authentication code is " + str(authToken) + '''. To check your current position in the queue, please visit http://your_domain_name_here/myPosition/''' + str(groceryID) + "/" + str(authToken)
        meesage = client.messages.create(
            body = msg,
            messaging_service_sid = "your_messaging_service_sid",
            to = numb
        )
        cur.close()
        return flask.render_template('TicketSuccessPage.html')
    return flask.render_template('TicketSuccessPage.html')

# Renders myposition.html using id,code,name
@application.route('/myPosition/<string:id>/<string:code>')
def my_position(id,code):
    cur = db.cursor()
    cur.execute('''SELECT store_name FROM grocerySores WHERE grocery_id = '''+id+";")
    name = cur.fetchone()[0]
    cur.close()
    return flask.render_template('myposition.html',id=id,code=code,name=name)

# Gets a position using grocery id and customer authentication
@application.route('/getPosition',methods=['POST'])
def get_position():
    groceryID = request.form["id"]
    code = request.form["code"]
    cur = db.cursor()
    cur.execute("SELECT position FROM queue"+groceryID+" WHERE authentication = "+code)
    position = cur.fetchone()
    print(position)
    return jsonify(position)

# Renders position.html using database info
@application.route('/position/<string:id>',methods=['POST','GET'])
def position(id):
    cur = db.cursor()
    cur.execute("SELECT store_name FROM groceryStores WHERE grocery_id = "+id+";")
    name = cur.fetchone()[0]
    if flask.request.method == 'POST':
        code = request.form["code"]
        if len(code) == 6:
            cur.execute("SELECT position FROM queue"+id+" WHERE authentication = "+code+";")
            lyst = cur.fetchall()
            if len(lyst) == 1:
                position = lyst[0][0]
                cur.execute("DELETE FROM queue"+id+" WHERE authentication = "+code+";")
                db.commit()
                cur.execute("UPDATE queue"+id+" SET position = position-1 WHERE position >= "+str(position)+";")
                db.commit()
                cur.close()
            return flask.render_template('position.html',name=name,id=id)
    return flask.render_template('position.html',name=name,id=id)

# Renders mystore.html
@application.route('/myStore')
def get_id():
    return flask.render_template('mystore.html')

# Returns the customer names using store id
@application.route('/populateNames/<string:id>', methods=['GET'])
def populateNames(id):
    if flask.request.method == 'GET':
        name = []
        cur = db.cursor()
        cur.execute("SELECT cust_name FROM queue"+id)
        for i in cur:
            name.append(i[0])
        cur.close()
        return jsonify(name)

# Returns the authentication codes using store id
@application.route('/populateCodes/<string:id>', methods=['GET'])
def populateCodes(id):
    if flask.request.method == 'GET':
        name = []
        cur = db.cursor()
        cur.execute("SELECT authentication FROM queue"+id)
        for i in cur:
            name.append(i[0])
        cur.close()
        return jsonify(name)

# Format the phone number for Twilio
def formatNumb(num):
    print(num)
    num = re.sub("[^0-9]", "", num)
    newNum = "+1" + num
    return newNum

# ONLY RUNS THE FLASK APPLICATION IF THE APP.PY IS BEING USED AS THE DRIVER
if __name__ == '__main__':
    application.run()
