# Flask endpoint test cases
import unittest
from unittest.mock import Mock, patch, MagicMock
from flask import Flask
from index import app
from unittest.mock import patch
import json
from Seat_Geek_API import Seat_Geek_Api
from Database_Layer.dbController import DBController

BASE_URL = "http://127.0.0.1:5000"
eventId = {"eventId": "5097856"}  # Hardcoded eventID to test the event page
user = {"username": "ageldartp"}
sga = Seat_Geek_Api()
dbc = DBController


class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.sampleResponse = {
            "title": "Young The Giant with Grouplove",
            "url": "https://seatgeek.com/young-the-giant-with-grouplove-tickets/new-york-new-york-terminal-5-2012-03-09/concert/721901/",
            "datetime_local": "2012-03-09T19:00:00",
            "performers": [
                {
                    "name": "Young The Giant",
                    "short_name": "Young The Giant",
                    "url": "https://seatgeek.com/young-the-giant-tickets/",
                    "image": "https://chairnerd.global.ssl.fastly.net/images/bandshuge/band_8741.jpg",
                    "primary": True,
                    "id": 8741,
                    "score": 6404,
                    "type": "band",
                    "slug": "young-the-giant"
                }
            ],
            "venue": {
                "extended_address": "Baker Street",
                "country": "US",
                "state": "NY",
                "address": "ABC Store",
                "id": 814
            },
            "datetime_utc": "2012-03-10T00:00:00",
            "type": "concert",
            "id": 721901,
            "description": "Sample",
            "status_code": 200,
        }

    # Tests the home page endpoint
    @patch('Seat_Geek_API.requests.get')    
    def test_home(self, mock_get):
        raise_for_status = Mock()        
        mock_get.return_value.raise_for_status= raise_for_status
        mock_get.return_value = self.sampleResponse
        response = self.app.get(BASE_URL + "/index")
        data = json.loads(response.get_data())
        print('checking response code. is: ', response.status_code)
        mock_get.assert_called_once()
        self.assertEqual(response.status_code, 200)  # Testing if endpoint is hitting

    # Tests the event page endpoint function - if the response is return
    @patch("Seat_Geek_API.requests.get")
    def test_eventData(self, mock_get):
        mock_get.return_value.ok = True
        response = sga.getEvent(eventId)
        self.assertIsNotNone(response)
        self.assertIn("status", response)

    # Tests the offered rides data endpoint - data is returning and correct data is present
    # @patch("Seat_Geek_API.requests.get")
    # def test_rides(self):
    #     mock_get.return_value.status_code = 200
    #     dbc.getrides_username = MagicMock(return_value=ridesdata)
    #     print("Get user data: ", response)
    #     self.assertIsNotNone(response)

    # Tests the insert request in database endpoint - data is getting saved
    def test_saveRequest(self):
        # Test data is hitting the aws server directly, need to make a dummy db
        Testdata = {
            "rideId": "125",
            "eventId": "1",
            "userId": "testuser",
            "status": "testpending",
        }
        response = self.app.post(
            BASE_URL + "/saveRequest",
            data=json.dumps(Testdata),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
    
    @patch('Database_Layer.dbController.DBController.enterUser')
    def signup(self, email, password, firstName, lastName, phoneNumber, mockResponse, mock_get):
        testData = {
            "email":email,
            "password":password,
            "firstName":firstName,
            "lastName":lastName,
            "phoneNumber":phoneNumber
        }
        mock_get.return_value = mockResponse
        print('Tetsing signup.....data is', testData)
        return self.app.post(
            "/signup", data=json.dumps(testData), content_type="application/json"
        )

    # Tests the status and response of signup endpoint
    def test_enterUserSuccess(self):
        response = self.signup("testing@test.com", "password123", "XYZ", "ABC", "1234567890", "Success")
        self.assertEqual(response.status_code, 200)
        json_response = response.data
        print('response received is', response.data)
        self.assertIn(b'Success', json_response)
        print('Signup Success test completed!!!')
        print()

    def test_enterUserFailure(self):
        response = self.signup("testing@test.com", "password123", "XYZ", "ABC", "1234567890", "Email already present. Try a new email-id")
        self.assertEqual(response.status_code, 200)
        json_response = response.data
        print('response received is', response.data)
        self.assertIn(b'Email already present', json_response)
        print('Signup Failure test completed!!!')
        print()        

    @patch('Seat_Geek_API.requests.get')
    def test_cityFilter(self, mock_get):
        raise_for_status = Mock()        
        mock_get.return_value.raise_for_status= raise_for_status
        mock_get.return_value = self.sampleResponse
        response = self.app.get(BASE_URL + "/index?filterValue=City&searchValue=Charlotte")
        data = json.loads(response.get_data())
        print('checking response code. is: ', response.status_code)
        mock_get.assert_called_once()
        mock_get.assert_called_with('https://api.seatgeek.com/2/events?venue.city=Charlotte', headers={'Content-Type': 'application/json'}, params={'client_id': 'MTkwMzc2MzB8MTU3MTc4MjA1Ni41Mw'})
        self.assertEqual(response.status_code, 200)  # Testing if endpoint is hitting

    @patch('Seat_Geek_API.requests.get')
    def test_dateFilter(self, mock_get):
        raise_for_status = Mock()        
        mock_get.return_value.raise_for_status= raise_for_status
        mock_get.return_value = self.sampleResponse
        response = self.app.get(BASE_URL + "/index?filterValue=Date&searchValue=2019/11/30")
        data = json.loads(response.get_data())
        print('checking response code. is: ', response.status_code)
        mock_get.assert_called_once()
        mock_get.assert_called_with('https://api.seatgeek.com/2/events?datetime_utc.gte=2019/11/30', headers={'Content-Type': 'application/json'}, params={'client_id': 'MTkwMzc2MzB8MTU3MTc4MjA1Ni41Mw'})
        self.assertEqual(response.status_code, 200)  # Testing if endpoint is hitting

    @patch('Seat_Geek_API.requests.get')
    def test_performerFilter(self, mock_get):
        raise_for_status = Mock()        
        mock_get.return_value.raise_for_status= raise_for_status
        mock_get.return_value = self.sampleResponse
        response = self.app.get(BASE_URL + "/index?filterValue=Performer&searchValue=coachella")
        data = json.loads(response.get_data())
        print('checking response code. is: ', response.status_code)
        mock_get.assert_called_once()
        mock_get.assert_called_with('https://api.seatgeek.com/2/events?performers.slug=coachella', headers={'Content-Type': 'application/json'}, params={'client_id': 'MTkwMzc2MzB8MTU3MTc4MjA1Ni41Mw'})
        self.assertEqual(response.status_code, 200)  # Testing if endpoint is hitting

    @patch('Seat_Geek_API.requests.get')
    def test_noFilter(self, mock_get):
        raise_for_status = Mock()        
        mock_get.return_value.raise_for_status= raise_for_status
        mock_get.return_value = self.sampleResponse
        response = self.app.get(BASE_URL + "/index?filterValue=No%20Filter&searchValue=mets")
        data = json.loads(response.get_data())
        print('checking response code. is: ', response.status_code)
        mock_get.assert_called_once()
        mock_get.assert_called_with('https://api.seatgeek.com/2/events?q=mets', headers={'Content-Type': 'application/json'}, params={'client_id': 'MTkwMzc2MzB8MTU3MTc4MjA1Ni41Mw'})
        self.assertEqual(response.status_code, 200)  # Testing if endpoint is hitting

     # Tests the login functionality and handle exceptions
    def test_successfullogin(self):
         rv = self.login("user@user.com","python123")
         assert b'You were logged in' in rv.data

    def test_loginEmail(self):
        rv = self.login("use@user.com","python123")
        assert b'Invalid email' in rv.data

    def test_loginPassword(self):
         rv = self.login("user@user.com","python123")
         assert b'Invalid password' in rv.data
        
    def test_successfullogout(self):

        rv = self.logout()
        assert b'You were logged out' in rv.data
            
    # # Testing login functionality with DB
    # def test_login(self):
    #     with app.test_db():
    #     rv = self.app.post('/api/auth', json={

        
    #         'email': 'flask@gmail.com', 'password': 'clt@2019'
    #     })
    #     json_data = rv.get_json(email)
    #     assert verify_token(email, json_data['token'])

    # def test_login(self):
    #     with app.test_client():
    #     rv = self.app.post('/api/auth', json={
    #         'email': 'flask@gmail.com', 'password': 'clt@2019'
    #     })
    #     json_data = rv.get_json(firstName)
    #     assert verify_token(firstName, json_data['token'])

    # def test_login(self):
    #     with app.test_client():
    #     rv = self.app.post('/api/auth', json={
    #         'email': 'flask@gmail.com', 'password': 'clt@2019'
    #     })
    #     json_data = rv.get_json(lastName)
    #     assert verify_token(lastName, json_data['token'])

        

        
    

if __name__ == "__main__":
    unittest.main()
