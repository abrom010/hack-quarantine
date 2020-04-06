import flask
from flask import jsonify
from flask import request
from flask import flash
import os
import mysql.connector
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import re

# Create Application
application = flask.Flask(__name__)
application.secret_key = 'secret'

# Connect to database
db = mysql.connector.connect(host="localhost", user="root", passwd="root", db="hackathon")

# Twilio SID Info
account_sid = 'ACf50d76cba4344433156557d73e062105'
auth_token = '5fd058e27df16f50cf47db3f4d4ce732'
client = Client(account_sid, auth_token)

# Route to Homepage at initial Launch
@application.route('/')
def main():
    return flask.render_template('index.html')

# Route to the Map Page
@application.route('/store/')
def store():
    return flask.render_template('storepage.html')

# Generates list of addresses for Google Maps API, happens on the storepage HTML
@application.route('/addresses/',methods=['GET'])
def addresses():
    if flask.request.method == 'GET':
        addresses = []
        names = []
        cur = db.cursor()
        cur.execute("SELECT CONCAT(address, ', ', city, ', ', state, ', ', zip_code) AS FullAddress FROM groceryStores;")
        for lyst in cur:
            addresses.append(lyst[0])
            # print({cur2[i][0]:cur[i][0]})
        cur.execute("SELECT store_name FROM groceryStores;")
        for lyst in cur:
            names.append(lyst[0])
        #print(dict(zip(id, add)))
    return jsonify(dict(zip(names, addresses)))

# Route to the ticketpage
@application.route('/ticket')
def ticket():
    return flask.render_template('ticketpage.html')

# Generates the user to database, when they enter Name and Phone number on ticketpage.
# Then texts them the code and returns them to
@application.route('/storeCust', methods=['POST'])
def storeCust():
    if flask.request.method == 'POST':
        custName = request.form["custName"]
        numb = request.form["numb"]
        numb = formatNumb(numb)
        # return custID, numb
        cur = db.cursor()
        cur.execute('''SELECT MAX(ticket_id), MAX(position) FROM queue''')
        test = cur.fetchone()
        if (test[0]):
            cur.execute('''INSERT INTO queue (ticket_id, cust_name, position, phone_num) VALUES(%s, %s, %s, %s)''', (test[0] + 1, custName, test[1] + 1, numb))
        else:
            cur.execute('''INSERT INTO queue (ticket_id, cust_name, position, phone_num) VALUES(%s, %s, %s, %s)''', (1, custName, 1, numb))
        db.commit()
        meesage = client.messages.create(
            body = "https://www.google.com",
            messaging_service_sid = "MGc4338215ff683f8a462df06e206eb8fb",
            to = numb
        )
        flash('Check your phone for your check-in code!')
        # print(numb)
        return flask.render_template('index.html')

# Format the phone number for Twilio
def formatNumb(num):
    print(num)
    num = re.sub("[^0-9]", "", num)
    newNum = "+1" + num
    return newNum

#ONLY RUNS THE FLASK APPLICATION IF THE APP.PY IS BEING USED AS THE DRIVER
if __name__ == '__main__':
    application.run()
