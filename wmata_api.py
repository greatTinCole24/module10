import json
import requests
from flask import Flask
 
# API endpoint URL's and access keys
WMATA_API_KEY = "f9fd0e28e99a4edba7731a913bb19e3e"
INCIDENTS_URL = "https://api.wmata.com/Incidents.svc/json/ElevatorIncidents"
headers = {"api_key": WMATA_API_KEY, "Accept": "*/*"}

app = Flask(__name__)

@app.route("/incidents/<unit_type>", methods=["GET"])
def get_incidents(unit_type):
    incidents = []

    # Use Requests to pull api with header and url
    response = requests.get(INCIDENTS_URL, headers=headers)
    data = response.json()

    # only accept valid unit types
    if unit_type not in ["elevators", "escalators"]:
        return json.dumps([])
    # Uses slice to pull expected from the unit_type
    expected_type = unit_type[:-1].upper()   

    # Loop and filter manually to add in filter
    for incident in data.get("ElevatorIncidents", []):
        type = incident.get("UnitType", "").upper()

        if type != expected_type:
            continue

        incidents.append({
            "StationCode": incident.get("StationCode", ""),
            "StationName": incident.get("StationName", ""),
            "UnitName": incident.get("UnitName", ""),
            "UnitType": incident.get("UnitType", "")
        })

    return json.dumps(incidents, indent=2)


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False) ## added use_reloader because kept getting weird error