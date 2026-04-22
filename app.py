from flask import Flask, request, jsonify, send_from_directory
import math

app = Flask(__name__)

incidents = []

# Example responders (Delhi region)
responders = [
    {"id": 1, "lat": 28.6139, "lng": 77.2090, "busy": False},
    {"id": 2, "lat": 28.7041, "lng": 77.1025, "busy": False}
]

# Serve frontend
@app.route("/")
def serve():
    return send_from_directory(".", "index.html")

# Distance function
def distance(lat1, lng1, lat2, lng2):
    return math.sqrt((lat1-lat2)**2 + (lng1-lng2)**2)

# Get responders
@app.route("/responders")
def get_responders():
    return jsonify(responders)

# SOS endpoint
@app.route("/sos", methods=["POST"])
def sos():
    data = request.json

    incident = {
        "id": len(incidents) + 1,
        "type": data["type"],
        "lat": data["lat"],
        "lng": data["lng"],
        "assigned": False,
        "status": "waiting"
    }

    incidents.append(incident)
    return jsonify(incident)

# Main logic
@app.route("/incidents")
def get_incidents():

    # Assign nearest responder
    for incident in incidents:
        if not incident["assigned"]:

            nearest = None
            min_dist = float("inf")

            for r in responders:
                if not r["busy"]:
                    d = distance(r["lat"], r["lng"], incident["lat"], incident["lng"])
                    if d < min_dist:
                        min_dist = d
                        nearest = r

            if nearest:
                nearest["busy"] = True
                incident["assigned"] = True
                incident["responder_id"] = nearest["id"]
                incident["status"] = "assigned"

    # Move responders smoothly
    for r in responders:
        for incident in incidents[:]:
            if incident.get("responder_id") == r["id"]:

                r["lat"] += (incident["lat"] - r["lat"]) * 0.05
                r["lng"] += (incident["lng"] - r["lng"]) * 0.05

                # If reached
                if distance(r["lat"], r["lng"], incident["lat"], incident["lng"]) < 0.0005:
                    r["busy"] = False
                    incidents.remove(incident)

    return jsonify(incidents)


if __name__ == "__main__":
    app.run(debug=True)