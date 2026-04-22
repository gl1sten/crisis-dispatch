from flask import Flask, request, jsonify, send_from_directory
import random
import webbrowser

app = Flask(__name__)

incidents = []

responders = [
    {"id": 1, "x": 0, "y": 0, "busy": False},
    {"id": 2, "x": 9, "y": 9, "busy": False}
]

# Serve frontend
@app.route("/")
def serve():
    return send_from_directory(".", "index.html")

# Get responders
@app.route("/responders", methods=["GET"])
def get_responders():
    return jsonify(responders)

# SOS route (create incident)
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
        "x": random.randint(0, 9),
        "y": random.randint(0, 9),
        "assigned": False,
        "priority": priority_map.get(data.get("type"), "C1")
    }

    incidents.append(incident)

    return jsonify(incident)

# Core logic: assign + move responders
@app.route("/incidents", methods=["GET"])
def get_incidents():

    # Assign responders
    for incident in incidents:
        if not incident.get("assigned"):

            nearest = None
            min_dist = 999

            for r in responders:
                if not r["busy"]:
                    dist = abs(r["x"] - incident["x"]) + abs(r["y"] - incident["y"])
                    if dist < min_dist:
                        min_dist = dist
                        nearest = r

            if nearest:
                nearest["busy"] = True
                incident["assigned"] = True
                incident["responder_id"] = nearest["id"]

    # Move responders
    for r in responders:
        for incident in incidents[:]:  # safe removal
            if incident.get("responder_id") == r["id"]:

                # move step-by-step
                if r["x"] < incident["x"]:
                    r["x"] += 1
                elif r["x"] > incident["x"]:
                    r["x"] -= 1

                if r["y"] < incident["y"]:
                    r["y"] += 1
                elif r["y"] > incident["y"]:
                    r["y"] -= 1

                # reached destination
                if r["x"] == incident["x"] and r["y"] == incident["y"]:
                    r["busy"] = False
                    incidents.remove(incident)

    return jsonify(incidents)

if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:5000")
    app.run(debug=True)
