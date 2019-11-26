# import unittest
# from unittest.mock import patch
# import sys
# from flask import Flask
# from flask_mysqldb import MySQL
# from Database_Layer.dbController import DBController
# import DB_config


# app = Flask('__main__')
# app.config['TESTING'] = True
# app.config["MYSQL_HOST"] = DB_config.MYSQL_HOST
# app.config["MYSQL_USER"] = DB_config.MYSQL_USER
# app.config["MYSQL_PASSWORD"] = DB_config.MYSQL_PASSWORD
# app.config["MYSQL_DB"] = DB_config.MYSQL_DB_TEST
# app.config["CORS_HEADERS"] = DB_config.CORS_HEADERS
# app.config["MYSQL_CURSORCLASS"] = DB_config.MYSQL_CURSORCLASS
#  @patch('Seat_Geek_API.requests.get')
# def test_home(self, mock_get):
#     raise_for_status = Mock()
#     mock_get.return_value.raise_for_status= raise_for_status
#     mock_get.return_value = self.sampleResponse
#     response = self.app.get(BASE_URL + "/index")
#     data = json.loads(response.get_data())
#     print('checking response code. is: ', response.status_code)
#     mock_get.assert_called_once()
#     self.assertEqual(response.status_code, 200)  # Testing if endpoint is hitting


import MySQLdb
import unittest
import DB_config
from unittest.mock import patch
from Database_Layer.dbController import DBController


class TestDBController(unittest.TestCase):
    def setUp(self):
        self.db = MySQLdb.connect(
            host=DB_config.MYSQL_HOST,  # your host, usually localhost
            user=DB_config.MYSQL_USER,  # your username
            passwd=DB_config.MYSQL_PASSWORD,  # your password
            db=DB_config.MYSQL_DB_TEST,
        )
        self.db.autocommit = "false"
        self.cur = self.db.cursor()
        self.controller = DBController(self.cur, self.db)
        self.username = "rakgunti26"
        self.ride_id = 181
        self.event_id = "5096273"
        self.request_id = 52
        self.status = "accepted"
        self.offerData = {
            "eventId": "5026583",
            "username": "audenv",
            "carModel": "BMW",
            "noOfSeats": "2",
            "startTime": "2019-11-18 01:52:40",
            "address1": "3456 test lane",
            "address2": "",
            "city": "Charlotte",
            "state": "NC",
            "zipCode": "28243",
            "eventDate": "2019-11-18 01:52:40",
        }

    def tearDown(self):
        self.cur.close()
        self.db.close()

    def test_getUserData(self):
        result = self.controller.getUser(self.username)
        self.cur.execute(
            """ SELECT RIDE_ID, EVENT_ID, USERNAME, STATUS FROM RIDES_REQUESTED WHERE RIDE_ID=%s AND EVENT_ID=%s AND USERNAME=%s""",
            (self.ride_id, self.event_id, self.username),
        )
        result = self.cur.fetchall()[0]
        self.assertEqual(result[0], self.ride_id)
        self.assertEqual(result[1], self.event_id)
        self.assertEqual(result[2], self.username)
        self.assertEqual(result[3], self.status)
        self.cur.execute(
            """ DELETE FROM RIDES_REQUESTED WHERE RIDE_ID=%s AND EVENT_ID=%s AND USERNAME=%s""",
            (self.ride_id, self.event_id, self.username),
        )
        self.db.commit()

    def test_saveRequest(self):
        self.controller.saveRequest(self.offerData)
        self.cur.execute(
            """ SELECT WHERE RIDE_ID=%s AND EVENT_ID=%s AND USERNAME=%s""",
            (self.ride_id, self.event_id, self.username),
        )
        result = self.cur.fetchall()[0]
        self.assertEqual(result[0], self.ride_id)
        self.assertEqual(result[1], self.event_id)
        self.assertEqual(result[2], self.username)
        self.assertEqual(result[3], self.status)
        # To check count of the table given details in where clause
        self.cur.execute(
            """ SELECT COUNT(*) FROM RIDES_REQUESTED WHERE RIDE_ID=%s AND EVENT_ID=%s AND USERNAME=%s""",
            (self.ride_id, self.event_id, self.username),
        )
        result = self.cur.fetchall()[0]
        self.assertEqual(result[0], 1)
        # To delete inserted data
        self.cur.execute(
            """ DELETE FROM RIDES_REQUESTED WHERE RIDE_ID=%s AND EVENT_ID=%s AND USERNAME=%s""",
            (self.ride_id, self.event_id, self.username),
        )
        self.db.commit()

    def test_updateRequest(self):
        self.cur.execute(
            """ SELECT STATUS FROM RIDES_REQUESTED WHERE REQUEST_ID=%s""",
            (self.request_id),
        )
        before_status = self.cur.fetchall()[0][0]
        self.assertEqual(self.status, before_status)

        self.controller.saveRequest(self.request_id, self.status)

        self.cur.execute(
            """ SELECT REQUEST_ID, STATUS FROM RIDES_REQUESTED WHERE REQUEST_ID=%s AND STATUS=%s""",
            (self.request_id, self.status),
        )
        result = self.cur.fetchall()[0]
        self.assertEqual(result[0], self.request_id)
        self.assertEqual(result[1], self.status)
        self.assertEqual(before_status, result)

        # To check count of the table given details in where clause
        self.cur.execute(
            """ SELECT COUNT(*) FROM RIDES_REQUESTED WHERE REQUEST_ID=%s AND STATUS=%s """,
            (self.request_id, self.status),
        )
        result = self.cur.fetchall()[0]
        self.assertEqual(result[0], 1)

        # To delete inserted data
        self.cur.execute(
            """ DELETE FROM RIDES_REQUESTED WHERE REQUEST_ID=%s AND STATUS=%s""",
            (self.request_id, self.status),
        )
        self.db.commit()

    def test_saveOfferRide(self):
        self.controller.saveOfferRide(self.offerData)
        self.cur.execute(
            """SELECT * FROM RIDES_OFFERED WHERE EVENT_ID=%s AND USERNAME=%s""",
            (self.offerData["EVENT_ID"], self.offerData["USERNAME"]),
        )
        result = self.cur.fetchall()[0]
        print("result is:", result)
        self.assertEqual(result[0], self.offerData["EVENT_ID"])
        self.assertEqual(result[2], self.offerData["USERNAME"])
        self.assertEqual(result[3], self.offerData["CAR_MODEL"])
        self.assertEqual(result[4], self.offerData["NO_OF_SEATS"])
        self.assertEqual(result[5], self.offerData["START_TIME"])
        self.assertEqual(result[6], self.offerData["START_ADDRESS_LINE1"])
        self.assertEqual(result[7], self.offerData["START_ADDRESS_LINE2"])
        self.assertEqual(result[8], self.offerData["START_CITY"])
        self.assertEqual(result[9], self.offerData["START_STATE"])
        self.assertEqual(result[10], self.offerData["START_ZIP_CODE"])

        # To delete inserted data
        self.cur.execute(
            """ DELETE FROM RIDES_OFFERED WHERE WHERE EVENT_ID=%s AND USERNAME=%s""",
            (self.offerData["EVENT_ID"], self.offerData["USERNAME"]),
        )
        self.db.commit()


if __name__ == "__main__":
    unittest.main()
