from flask import Flask, request, jsonify, send_from_directory
import webbrowser
import math
import random

app = Flask(__name__)

incidents = []
responders = []

MAX_RADIUS = 5  # km

# -----------------------------
# Generate location near user
# -----------------------------
def random_nearby(lat, lng, radius_km=5):
    radius_deg = radius_km / 111  # approx conversion
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

# -----------------------------
# Distance (Haversine)
# -----------------------------
def distance(lat1, lng1, lat2, lng2):
    R = 6371  # Earth radius in km

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
@app.route("/responder")
def responder_page():
    return send_from_directory(".", "responder.html")

# -----------------------------
# SOS (Create incident + spawn responders)
# -----------------------------
@app.route("/sos", methods=["POST"])
def sos():
    data = request.json

    priority_map = {
        "fire": "A1",
        "medical": "A2",
        "crime": "B1"
    }

    # CREATE INCIDENT
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

    # -----------------------------
    # SPAWN / RESPAWN RESPONDERS
    # -----------------------------
    global responders

    if len(responders) == 0:
        need_spawn = True
    else:
        # check avg distance from responders to new incident
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

        print("Responders spawned near incident")

    print("New Incident:", incident)

    return jsonify(incident)

# -----------------------------
# Assign responders (WITH 5KM LIMIT)
# -----------------------------
# @app.route("/incidents")
# def get_incidents():

#     incidents.sort(key=lambda x: x["priority"])

#     for incident in incidents:
#         # if not incident["assigned"]:

#         #     nearest = None
#         #     min_dist = float("inf")

#         #     for r in responders:
#         #         if not r["busy"]:
#         #             d = distance(r["lat"], r["lng"], incident["lat"], incident["lng"])

#         #             if d < min_dist and d <= MAX_RADIUS:
#         #                 min_dist = d
#         #                 nearest = r

#             if nearest:
#                 nearest["busy"] = True
#                 incident["assigned"] = True
#                 incident["responder_id"] = nearest["id"]
#                 incident["status"] = "assigned"
#                 incident["distance_km"] = round(min_dist, 2)

#                 print(f"Responder {nearest['id']} assigned ({incident['distance_km']} km)")

#             else:
#                 incident["status"] = "no_responder_available"

#     return jsonify(incidents)
@app.route("/incidents")
def get_incidents():
    return jsonify(incidents)
# -----------------------------
# Resolve incident
# -----------------------------
@app.route("/resolve", methods=["POST"])
def resolve():
    data = request.json
    incident_id = data.get("id")

    global incidents

    for incident in incidents:
        if incident["id"] == incident_id:

            responder_id = incident.get("responder_id")

            for r in responders:
                if r["id"] == responder_id:
                    r["busy"] = False
                    break

            incidents.remove(incident)
            print(f"Incident {incident_id} resolved")
            break

    return jsonify({"status": "resolved"})

@app.route("/update_location", methods=["POST"])
def update_location():
    data = request.json

    for r in responders:
        if r["id"] == data["id"]:
            r["lat"] = data["lat"]
            r["lng"] = data["lng"]
            break

    return jsonify({"status": "updated"})


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

            elif action == "deny":
                incident["status"] = "denied"

            return jsonify({"msg": "done"})
# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:5000")
    app.run(debug=True, use_reloader=False)