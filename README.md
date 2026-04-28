# Crisis Dispatch System

> A hackathon prototype simulating a modern emergency response network with real-time mapping, dispatcher approval workflow, and live responder movement.

---

## Overview

Crisis Dispatch System demonstrates how emergency incidents can be reported, reviewed, assigned, and resolved through a dual-interface platform. It combines operational visibility, proximity-based response logic, and live route simulation.

---

## Current Status

This project has evolved from an early grid-based simulation into a fully map-based dispatch prototype with separate caller and dispatcher interfaces.

### Working Features

- **Dual interface system** — Caller/SOS interface and Dispatcher/Responder terminal
- **Emergency request generation** — Fire, Medical, Crime
- **Live GPS-based SOS generation**
- **Real-time map visualization** using Leaflet.js, OpenStreetMap, and Carto Dark Theme
- **Dispatcher approval workflow** — Accept or Deny incoming requests
- **Dynamic responder spawning** within operational radius
- **Live responder movement** toward incident along real roads
- **Road-based route visualization** using OSRM
- **Incident resolution flow**
- **Responder return-to-base logic**
- **Real-time operational dashboard UI**

---

## System Flow

### Caller Side

1. User opens the command page
2. User sends an SOS request
3. Incident is generated on the live map

### Dispatcher Side

1. Incoming alert appears in the terminal
2. Dispatcher reviews the request
3. Accept or Deny decision is made

### If Accepted

1. Nearest available responder is dispatched
2. Route is generated using real roads
3. Both interfaces update in real time
4. Incident resolves on arrival

---

## Technology Stack

| Layer | Technologies |
|---|---|
| Backend | Python, Flask |
| Frontend | HTML, CSS, JavaScript |
| Maps / Routing | Leaflet.js, OpenStreetMap, OSRM |

---

## How to Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/gl1sten/crisis-dispatch.git
cd crisis-dispatch
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the server

```bash
python app.py
```

### 4. Open the interfaces

**Caller Interface**
```
http://127.0.0.1:5000
```

**Dispatcher Interface**
```
http://127.0.0.1:5000/responder
```

---

## File Structure

```
crisis-dispatch/
├── app.py
├── index.html
├── responder.html
├── requirements.txt
└── README.md
```

---

## Key Highlights

- Real-time emergency workflow simulation
- Manual dispatcher approval logic
- Smart responder deployment system
- Interactive tactical dashboard
- Two synchronized interfaces
- Modern dark UI design
- Ready for future scaling

---

## Future Scope

- [ ] Multi-responder dispatch logic
- [ ] Hospital and fire station datasets
- [ ] AI-based incident prioritization
- [ ] Heatmaps for high-risk zones
- [ ] Authentication system
- [ ] Live communications module
- [ ] Mobile application
- [ ] Analytics dashboard

---

## Team

| Name |
|---|
| Ajitesh Rajput |
| Ananya Soni |
| Pranit Arora |

---

## Vision

> To create a scalable emergency coordination platform that improves response time, situational awareness, and dispatch efficiency using real-time technology.
