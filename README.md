# Crisis Dispatch System (Hackathon Prototype)

**Note from Pranit:**
The project started as a basic grid-based simulation and has now been upgraded to a real map-based system. There are still several features left to build, but the core system is now significantly improved and functional.

---

## Current Status

This project has evolved from a grid-based simulation into a real-time map-based emergency dispatch prototype.

### What is Working:

* SOS-based emergency triggering (Fire / Medical / Crime)
* Real-time GPS location detection
* Live map visualization using Leaflet and OpenStreetMap
* Automatic responder assignment based on proximity
* Smooth responder movement toward incidents
* Live incident tracking on map
* Responder status tracking (available / busy)

The system now behaves like a simplified real-world dispatch system.

---

## Concept

This system simulates how modern emergency services can be optimized using:

* Real-time location tracking
* Intelligent nearest-responder allocation
* Dynamic incident resolution

Each incident:

* Is created via SOS
* Gets assigned to the nearest available responder
* Is tracked live until resolution

---

## Features

* One-tap SOS system
* GPS-based incident location
* Real-time interactive map
* Automatic responder dispatch
* Live movement simulation
* Nearest responder selection
* Clean UI

---

## How to Run

### 1. Clone the repository

```id="a91v2d"
git clone https://github.com/gl1sten/crisis-dispatch.git
cd crisis-dispatch
```

### 2. Install dependencies

```id="7p1xmf"
pip install -r requirements.txt
```

### 3. Run the app

```id="v5u3gh"
python app.py
```

### 4. Open in browser

```id="k3zq8s"
http://127.0.0.1:5000
```

---

## How to Use

1. Allow location access in your browser
2. Click any emergency button:

   * Fire
   * Medical
   * Crime

### Map Legend:

* Red: Incident
* Blue: Available responder
* Purple: Busy responder

Responders will automatically:

* Get assigned
* Move toward the incident
* Resolve it

---

## Limitations

* Uses simulated responders (not connected to real emergency services)
* No integration with official APIs
* Distance calculation is simplified (not road-based)
* No database (data resets on restart)

---

## Future Scope

* Route-based movement using real roads
* ETA calculation
* Heatmap for crisis-prone areas
* Multi-dispatcher system
* Real-time communication between services
* AI-based prioritization
* Mobile application version

---

## Team

Ajitesh Rajput
Ananya Soni
Pranit Arora

---

## Vision

To build a scalable emergency response system that reduces response time and improves coordination using real-time data and intelligent dispatching.
