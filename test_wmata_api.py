from wmata_api import app
import json
import unittest

class WMATATest(unittest.TestCase):
    # ensure both endpoints return a 200 HTTP code
    def test_http_success(self):
        escalator_response = app.test_client().get('/incidents/escalators').status_code
        # assert that the response code of 'incidents/escalators returns a 200 code
        self.assertEqual(escalator_response, 200)
        elevator_response = app.test_client().get('/incidents/elevators').status_code
        self.assertEqual(elevator_response, 200)
################################################################################

    # ensure all returned incidents have the 4 required fields
    def test_required_fields(self):
        required_fields = ["StationCode", "StationName", "UnitType", "UnitName"]

        response = app.test_client().get('/incidents/escalators')
        json_response = json.loads(response.data.decode())
        
        # for loop to check the outputs from json_response == 4 required fields
        for i in json_response:
            self.assertTrue("StationCode" in i)
            self.assertTrue("StationName" in i)
            self.assertTrue("UnitType" in i)
            self.assertTrue("UnitName" in i)

################################################################################

    # ensure all entries returned by the /escalators endpoint have a UnitType of "ESCALATOR"
    def test_escalators(self):
        response = app.test_client().get('/incidents/escalators')
        json_response = json.loads(response.data.decode())

        for i in json_response:
            self.assertEqual(i.get("UnitType", ""), "ESCALATOR")

################################################################################

    # ensure all entries returned by the /elevators endpoint have a UnitType of "ELEVATOR"
    def test_elevators(self):
        response = app.test_client().get('/incidents/elevators')
        json_response = json.loads(response.data.decode())
        
        for i in json_response:
            self.assertEqual(i.get("UnitType", ""), "ELEVATOR")
        # for each incident in the JSON response, assert that the 'UnitType' is "ELEVATOR"

################################################################################

if __name__ == "__main__":
    unittest.main()