# Crisis Dispatch System (Hackathon Prototype)

**Note from Pranit:**  
Bhai itna hee kar paaya kuch college ka assignment bhi karna tha isliye zyaada nahi hua chutti li hai toh din mei poora yahi karunga aur aage ka bhi bnaunga

---

## Current Status

This project is currently a partially complete but fully functional prototype.

The core system has been implemented and is working:
- Incident creation (SOS system)
- Real-time grid simulation
- Automatic responder assignment
- Responder movement and resolution

However, the system is not fully complete yet. Several planned features and refinements are still pending and will be developed further.

In progress / to be added:
- Multi-dispatcher role system
- Service-specific filtered views
- Improved UI and visualization
- Better prioritization logic

---

## Features

- SOS-based incident creation
- Real-time grid-based simulation
- Automatic responder assignment
- Dynamic movement of responders
- Priority-based emergencies (A1, A2, etc.)
- Multi-service dispatch concept

---

## Concept

This system simulates how modern emergency services can be optimized using intelligent dispatching.

Each incident can involve multiple services (fire, medical, police), and responders are automatically assigned based on proximity and availability.

---

## How to Run

### 1. Clone the repository

git clone https://github.com/gl1sten/crisis-dispatch.git

cd crisis-dispatch

---

### 2. Install dependencies

pip install -r requirements.txt

---

### 3. Run the app

python app.py

---

### 4. Open in browser

The app will automatically open in your browser at:

http://127.0.0.1:5000

---

## How to Use

- Click buttons to simulate emergencies  
- Red = Incident  
- Blue = Available responder  
- Purple = Busy responder  

Responders automatically move toward incidents and resolve them.

---

## Future Scope

- Real-time maps integration  
- AI-based priority optimization  
- Multi-dispatcher system  
- Live communication between services  

---

## Team

Ajitesh Rajput  
Ananya Soni  
Pranit Arora
