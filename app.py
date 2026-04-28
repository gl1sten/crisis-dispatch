from flask import Flask, request, jsonify, send_from_directory
import math
import random
import os

app = Flask(__name__)

incidents = []
responders = []

MAX_RADIUS = 5  # km

# -----------------------------
# Generate location near user
# -----------------------------
def random_nearby(lat, lng, radius_km=5):
    radius_deg = radius_km / 111
    return {
        "lat": lat + random.uniform(-radius_deg, radius_deg),
        "lng": lng + random.uniform(-radius_deg, radius_deg)
    }

# -----------------------------
# Serve frontend
# -----------------------------
@app.route("/")
def serve():
    return send_from_directory(".", "index.html")

@app.route("/responder")
def responder_page():
    return send_from_directory(".", "responder.html")

# -----------------------------
# Distance (Haversine)
# -----------------------------
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
# Get responders
# -----------------------------
@app.route("/responders")
def get_responders():
    return jsonify(responders)

# -----------------------------
# SOS
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
        "type": data.get("type"),
        "lat": data.get("lat"),
        "lng": data.get("lng"),
        "assigned": False,
        "priority": priority_map.get(data.get("type"), "C1"),
        "responder_id": None,
        "status": "waiting",
        "distance_km": None
    }

    incidents.append(incident)

    global responders

    if len(responders) == 0:
        need_spawn = True
    else:
        avg_dist = sum(
            distance(r["lat"], r["lng"], data["lat"], data["lng"])
            for r in responders
        ) / len(responders)

        need_spawn = avg_dist > 5

    if need_spawn:
        responders.clear()

        for i in range(5):
            loc = random_nearby(data["lat"], data["lng"])

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
# Incidents + Assignment
# -----------------------------
@app.route("/incidents")
def get_incidents():

    incidents.sort(key=lambda x: x["priority"])

    for incident in incidents:
        if not incident["assigned"]:

            nearest = None
            min_dist = float("inf")

            for r in responders:
                if not r["busy"]:
                    d = distance(
                        r["lat"], r["lng"],
                        incident["lat"], incident["lng"]
                    )

                    if d < min_dist and d <= MAX_RADIUS:
                        min_dist = d
                        nearest = r

            if nearest:
                nearest["busy"] = True
                incident["assigned"] = True
                incident["responder_id"] = nearest["id"]
                incident["status"] = "assigned"
                incident["distance_km"] = round(min_dist, 2)
            else:
                incident["status"] = "no_responder_available"

    return jsonify(incidents)

# -----------------------------
# Resolve
# -----------------------------
@app.route("/resolve", methods=["POST"])
def resolve():
    data = request.json
    incident_id = data.get("id")

    for incident in incidents[:]:
        if incident["id"] == incident_id:

            responder_id = incident.get("responder_id")

            for r in responders:
                if r["id"] == responder_id:
                    r["busy"] = False
                    break

            incidents.remove(incident)
            break

    return jsonify({"status": "resolved"})

# -----------------------------
# Update responder location
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
# Manual responder accept/deny
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
                incident["assigned"] = True
                incident["responder_id"] = responder_id
                incident["status"] = "assigned"

                for r in responders:
                    if r["id"] == responder_id:
                        r["busy"] = True
                        break

            elif action == "deny":
                incident["status"] = "denied"

            return jsonify({"msg": "done"})

    return jsonify({"msg": "incident not found"})

# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))