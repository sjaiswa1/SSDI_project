from flask import Flask, jsonify, request, json
from flask_cors import CORS
from flask_mysqldb import MySQL

import Seat_Geek_API as SGE
from Database_Layer.dbController import DBController
import DB_config

app = Flask(__name__)
CORS(
    app
)  # Need this to allow requests between client and server for Cross-origin resource sharing

app.config["MYSQL_HOST"] = DB_config.MYSQL_HOST
app.config["MYSQL_USER"] = DB_config.MYSQL_USER
app.config["MYSQL_PASSWORD"] = DB_config.MYSQL_PASSWORD
app.config["MYSQL_DB"] = DB_config.MYSQL_DB
mysql = MySQL(app)


@app.route(
    "/index", methods=["GET"]
)  # handles route of home page in backend send required data to react
def index():
    events = SGE.Seat_Geek_Api()
    eventsdata = events.getallEvents()
    return eventsdata


@app.route("/getusers/<userid>", methods=["GET"])
def getUsers(userid):
    cursor = mysql.connection.cursor()
    controller = DBController(cursor)
    response = controller.getUser(userid)

    print("db op", response)
    return str(response)


@app.route(
    "/event/<eventId>", methods=["GET"]
)  # handles route of Event page in backend send required data to react
def event(eventId):
    event = SGE.Seat_Geek_Api()
    eventdata = event.getEvent(eventId)
    return eventdata

@app.route('/event/rides/<eventId>', methods=['GET']) #handles route of Event page in backend send required data to react
def rides(eventId):
    eventId = 5075823 #hardcoded as we have data for this few events only
    cursor = mysql.connection.cursor()
    controller = DBController(cursor)
    if 'userId' in request.args and request.args.get('userId') != "": # condition to check if userId is sent in request 
        response = controller.getrides_username(eventId, request.args.get('userId')) #sending offered rides data without his own rides
    else:
        response = controller.getrides_wo_username(eventId) # sending all offered rides data for any given event
    return response


@app.route("/saveRequest", methods=["POST"])
def save_request():
    data = request.get_json(silent=True)
    item = data.get("firstName")
    # print(item)
    # return "Done!"
    # RideID = "124"
    # eventID = "1"
    # userID = "eaimek"
    # status = "pending"
    cursor = mysql.connection.cursor()
    controller = DBController(cursor)
    controller.saveRequest(RideID, eventID, userID, status)
    mysql.connection.commit()


if __name__ == "__main__":
    app.run(host="localhost", debug=True, port=5000)
