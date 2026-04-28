from flask import Flask, request, jsonify, send_from_directory
import math
import random
import os

app = Flask(__name__)

incidents = []
responders = []

MAX_RADIUS = 8  # km dispatch radius

# -----------------------------
# Helpers
# -----------------------------
def random_nearby(lat, lng, radius_km=8):
    radius_deg = radius_km / 111
    return {
        "lat": lat + random.uniform(-radius_deg, radius_deg),
        "lng": lng + random.uniform(-radius_deg, radius_deg)
    }

def distance(lat1, lng1, lat2, lng2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)

    a = (
        math.sin(dlat / 2) ** 2 +
        math.cos(math.radians(lat1)) *
        math.cos(math.radians(lat2)) *
        math.sin(dlng / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# -----------------------------
# Frontend Pages
# -----------------------------
@app.route("/")
def serve():
    return send_from_directory(".", "index.html")

@app.route("/responder")
def responder_page():
    return send_from_directory(".", "responder.html")

# -----------------------------
# API
# -----------------------------
@app.route("/responders")
def get_responders():
    return jsonify(responders)

@app.route("/incidents")
def get_incidents():
    return jsonify(incidents)

# -----------------------------
# SOS
# -----------------------------
@app.route("/sos", methods=["POST"])
def sos():
    data = request.json

    incident = {
        "id": len(incidents) + 1,
        "type": data.get("type"),
        "lat": data.get("lat"),
        "lng": data.get("lng"),
        "assigned": False,
        "status": "waiting",
        "responder_id": None
    }

    incidents.append(incident)

    global responders

    # FIXED: respawn responders every SOS inside 8km
    responders.clear()

    for i in range(5):
        loc = random_nearby(data["lat"], data["lng"], 8)

        responders.append({
            "id": i + 1,
            "lat": loc["lat"],
            "lng": loc["lng"],
            "base_lat": loc["lat"],
            "base_lng": loc["lng"],
            "busy": False
        })

    return jsonify(incident)

# -----------------------------
# Accept / Deny
# -----------------------------
@app.route("/respond", methods=["POST"])
def respond():
    data = request.json

    incident_id = data["incident_id"]
    responder_id = data["responder_id"]
    action = data["action"]

    for incident in incidents:
        if incident["id"] == incident_id:

            if action == "accept":

                selected = None

                for r in responders:
                    if r["id"] == responder_id:
                        selected = r
                        break

                if selected:

                    d = distance(
                        selected["lat"], selected["lng"],
                        incident["lat"], incident["lng"]
                    )

                    if d <= MAX_RADIUS and not selected["busy"]:
                        incident["assigned"] = True
                        incident["status"] = "assigned"
                        incident["responder_id"] = responder_id
                        selected["busy"] = True
                    else:
                        incident["status"] = "out_of_range"

            elif action == "deny":
                incident["status"] = "denied"

            return jsonify({"msg": "done"})

    return jsonify({"msg": "incident not found"})

# -----------------------------
# Movement sync from frontend
# -----------------------------
@app.route("/update_location", methods=["POST"])
def update_location():
    data = request.json

    for r in responders:
        if r["id"] == data["id"]:
            r["lat"] = data["lat"]
            r["lng"] = data["lng"]
            break

    return jsonify({"status": "updated"})

# -----------------------------
# Resolve incident
# -----------------------------
@app.route("/resolve", methods=["POST"])
def resolve():
    data = request.json
    incident_id = data["id"]

    for incident in incidents[:]:
        if incident["id"] == incident_id:

            responder_id = incident["responder_id"]

            for r in responders:
                if r["id"] == responder_id:
                    r["busy"] = False
                    r["lat"] = r["base_lat"]
                    r["lng"] = r["base_lng"]
                    break

            incidents.remove(incident)
            return jsonify({"status": "resolved"})

    return jsonify({"status": "not found"})

# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))