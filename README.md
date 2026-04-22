# Crisis Dispatch System

> A real-time, map-based emergency dispatch prototype with live GPS tracking, road-based routing, and intelligent responder allocation.

---

## Overview

Crisis Dispatch started as a basic grid-based simulation and has evolved into a fully functional emergency dispatch system featuring real-world routing, live ETA tracking, and a complete responder lifecycle.

The system simulates how modern emergency services can be optimized using:

- **Real-time location tracking**
- **Intelligent nearest-responder allocation**
- **Road-based navigation**
- **Dynamic incident resolution**

---

## Current Features

| Feature | Status |
|---|---|
| SOS-based emergency triggering (Fire / Medical / Crime) | Done |
| Real-time GPS location detection | Done |
| Live map via Leaflet & OpenStreetMap | Done |
| Automatic nearest-responder assignment | Done |
| Road-based routing via OSRM | Done |
| Smooth responder movement along real roads | Done |
| Live incident tracking on map | Done |
| Responder status tracking (available / busy) | Done |
| Return-to-base after task completion | Done |
| Base locations displayed on map | Done |
| Live ETA tracking (scaled to simulation speed) | Done |
| Path fading to show movement progress | Done |
| Added radius limit to the responder spawn and changed UI|

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/gl1sten/crisis-dispatch.git
cd crisis-dispatch
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the app

```bash
python app.py
```

### 4. Open in browser

```
http://127.0.0.1:5000
```

---

## How to Use

1. **Allow location access** when prompted by your browser
2. **Click an emergency button** to trigger an SOS:
   - Fire
   - Medical
   - Crime
3. Watch responders get **automatically dispatched**, navigate via real roads, and **return to base** after resolution.

---

## Map Legend

| Color | Meaning |
|---|---|
| Red | Active incident |
| Blue | Available responder |
| Purple | Busy responder |
| Grey | Responder base location |
| Cyan | Route to incident |
| Green | Return route to base |

---

## Responder Lifecycle

Each incident follows a full lifecycle:

```
SOS Triggered → Nearest Responder Assigned → Route Generated (OSRM)
      → Live Movement + ETA Display → Incident Resolved → Return to Base
```

---

## Limitations

- Uses **simulated responders** — not connected to real emergency services
- ETA does **not** account for real-time traffic conditions
- Simulation speed is **scaled** for demonstration purposes
- Uses the **public OSRM service** (may have latency)
- **No database** — data resets on every restart

---

## Future Scope

- [ ] Priority-based dispatch (A1 incidents handled first)
- [ ] Traffic-aware ETA calculations
- [ ] Heatmap for crisis-prone areas
- [ ] Multi-dispatcher coordination system
- [ ] Real-time communication between services
- [ ] AI-based incident prioritization
- [ ] Mobile application version

---

## Team

| Name |
|---|
| Ajitesh Rajput |
| Ananya Soni |
| Pranit Arora |

---

## Vision

> To build a scalable emergency response system that reduces response time and improves coordination using real-time data and intelligent dispatching.
