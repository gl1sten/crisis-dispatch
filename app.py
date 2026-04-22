from flask import Flask, request, jsonify, send_from_directory
import webbrowser
import math
import random

app = Flask(__name__)

incidents = []

# Example responder locations (Delhi)
responders = [
    {"id": 1, "lat": 28.6139, "lng": 77.2090, "busy": False},
    {"id": 2, "lat": 28.6145, "lng": 77.2100, "busy": False},
    {"id": 3, "lat": 28.6150, "lng": 77.2080, "busy": False}
]

# -----------------------------
# Serve frontend
# -----------------------------
@app.route("/")
def serve():
    return send_from_directory(".", "index.html")


def random_location():
    # Delhi bounding box (you can tweak)
    return {
        "lat": 28.50 + random.random() * 0.2,
        "lng": 77.10 + random.random() * 0.2
    }


# -----------------------------
# Get responders
# -----------------------------
@app.route("/responders", methods=["GET"])
def get_responders():
    return jsonify(responders)


# -----------------------------
# Distance function
# -----------------------------
def distance(lat1, lng1, lat2, lng2):
    return math.sqrt((lat1 - lat2)**2 + (lng1 - lng2)**2)


# -----------------------------
# SOS route
# -----------------------------
@app.route("/sos", methods=["POST"])
def sos():
    data = request.json

    priority_map = {
        "fire": "A1",
        "medical": "A2",
        "crime": "B1"
    }

    incident = {
        "id": len(incidents) + 1,
        "type": data.get("type", "unknown"),
        "lat": data.get("lat"),
        "lng": data.get("lng"),
        "assigned": False,
        "priority": priority_map.get(data.get("type"), "C1")
    }

    incidents.append(incident)

    print("New Incident:", incident)

    return jsonify(incident)


# -----------------------------
# Assign responders ONLY
# -----------------------------
@app.route("/incidents", methods=["GET"])
def get_incidents():

    for incident in incidents:
        if not incident.get("assigned"):

            nearest = None
            min_dist = float("inf")

            for r in responders:
                if not r["busy"]:
                    dist = distance(
                        r["lat"], r["lng"],
                        incident["lat"], incident["lng"]
                    )

                    if dist < min_dist:
                        min_dist = dist
                        nearest = r

            if nearest:
                nearest["busy"] = True
                incident["assigned"] = True
                incident["responder_id"] = nearest["id"]

                print(f"Responder {nearest['id']} assigned to Incident {incident['id']}")

    return jsonify(incidents)

@app.route("/resolve", methods=["POST"])
def resolve():
    data = request.json
    incident_id = data.get("id")

    global incidents

    for incident in incidents:
        if incident["id"] == incident_id:

            # FREE THE RESPONDER 
            responder_id = incident.get("responder_id")

            for r in responders:
                if r["id"] == responder_id:
                    r["busy"] = False
                    break

            incidents.remove(incident)
            break

    return jsonify({"status": "resolved"})


responders = []

for i in range(5):  # number of responders
    loc = random_location()
    responders.append({
        "id": i+1,
        "lat": loc["lat"],
        "lng": loc["lng"],
        "base_lat": loc["lat"],   # IMPORTANT
        "base_lng": loc["lng"],
        "busy": False
    })



# -----------------------------
# Run app
# -----------------------------
if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:5000")
    app.run(debug=True, use_reloader=False)