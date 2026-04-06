<div align="center">

# 🎯 CrowdPulse

### Real-Time Audience Engagement Detector

![Demo](assets/demo.gif)

> *"A system that watches people watching something — and tells you whether they're actually seeing it."*

![Python](https://img.shields.io/badge/Python-3.10-3776AB?style=flat-square&logo=python&logoColor=white)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10-FF6F00?style=flat-square)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-27338e?style=flat-square&logo=opencv&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.x-000000?style=flat-square&logo=flask&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

</div>

---

## 📌 What Is CrowdPulse?

CrowdPulse is a **real-time computer vision system** that monitors an audience through a webcam and tells you — live — whether each person is engaged or zoned out.

Place a laptop at the back of a classroom, meeting room, or presentation hall. The system watches the audience and gives the presenter a live engagement score — updated every second.

**No cloud. No internet. No special hardware. Just Python running locally on any laptop.**

---

## 🎬 Live Demo

<div align="center">

**Engaged Detection**
![Engaged](https://raw.githubusercontent.com/suhaib1202/CrowdPulse/main/assets/engaged.png)

**Zoned Out / Looking Down**
![Disengaged](https://raw.githubusercontent.com/suhaib1202/CrowdPulse/main/assets/disengaged.png)

**Looking Sideways**
![Sideways1](https://raw.githubusercontent.com/suhaib1202/CrowdPulse/main/assets/sideways1.png)
![Sideways2](https://raw.githubusercontent.com/suhaib1202/CrowdPulse/main/assets/sideways2.png)

**Yawning Detection**
![Yawning](https://raw.githubusercontent.com/suhaib1202/CrowdPulse/main/assets/yanning.png)

**Full Dashboard**
![Dashboard](https://raw.githubusercontent.com/suhaib1202/CrowdPulse/main/assets/dashboard.png)

</div>

---

## 🧠 How It Works

CrowdPulse analyses **4 behavioural signals** per face on every frame:

| Signal | Landmark Used | What It Detects |
|--------|--------------|-----------------|
| 📐 Head Pitch | Nose vs Ear Y-position | Looking down at phone |
| 🔄 Head Yaw | Left ear vs Right ear gap | Head turned sideways |
| 👁️ Iris Gaze | Iris position in eye socket | Eyes glancing away |
| 😮 Mouth Ratio | Top lip vs Bottom lip gap | Yawning |

All 4 signals must pass the threshold → face marked **Engaged** ✅  
Final Score = `(Engaged Faces ÷ Total Faces) × 100`

---

## 🖥️ Dashboard Features

- **Live webcam feed** with coloured dot overlays per face
  - 🟢 Green dot = Engaged
  - 🔴 Red dot = Zoned Out
- **Live engagement % score** — colour shifts green → yellow → red
- **Real-time line graph** — engagement history like a stock ticker
- **Alert banner** — fires when score drops below 40%

---

## 🔗 Real-World Application

>In classrooms, lecture halls, in orientation programs and sessions, the teachers need to know who all are engaged and are the audience active. Hence, CrowdPulse helps them in getting to know about this. 

> At the FIFA World Cup and the Olympics, broadcast directors need to know in real time — which moment made the crowd erupt? Which goal caused the biggest emotional spike in the stadium?

> The core pipeline in CrowdPulse is identical — tracking multiple faces in a live video feed, extracting behavioural signals frame by frame, and producing a real-time score. The technology underneath is exactly what crowd-facing cameras at a stadium need.

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.8 – 3.11 (not 3.12)
- A working webcam
- ~50MB disk space

### Step 1 — Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/CrowdPulse.git
cd CrowdPulse
```

### Step 2 — Create virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac / Linux
python -m venv venv
source venv/bin/activate
```

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Run
```bash
python app.py
```

### Step 5 — Open browser

http://127.0.0.1:5000
> The face landmarker model (~1MB) downloads automatically on first run. No manual setup needed.

---

## 📁 Project Structure
```
CrowdPulse/
├── app.py                  # Flask server — video streaming + API endpoints
├── detector.py             # Core engine — MediaPipe face analysis
├── requirements.txt        # Python dependencies
├── .gitignore
│
├── templates/
│   └── index.html          # Live dashboard UI + Chart.js graph
│
├── static/
│   └── style.css           # Dark theme styling
│
└── assets/                 # Screenshots and demo GIF
    ├── demo.gif
    ├── dashboard.png
    ├── engaged.png
    ├── disengaged.png
    └── sideways.png
```
---

## 🔧 Tuning the Detection

Open `detector.py` and adjust these thresholds based on your room setup:
```python
pitch       < 0.08   # Raise to 0.10 if head-down not catching
yaw         > 0.10   # Lower to 0.08 if sideways not catching
0.30 < gaze < 0.70   # Narrow to 0.35–0.65 for stricter gaze
mouth_ratio < 0.25   # Raise to 0.30 if yawn not catching
```

Watch the terminal while running — every frame prints live values:
pitch=0.031 | yaw=0.142 | gaze=0.51 | mouth=0.04 | ✅ ENGAGED
pitch=0.134 | yaw=0.138 | gaze=0.48 | mouth=0.04 | ❌ ZONED OUT


## 📦 Dependencies

mediapipe==0.10.33
opencv-python
flask
numpy

---

## 🗺️ Roadmap

- [ ] Multi-person tracking with individual face IDs
- [ ] Session recording — export engagement timeline as CSV
- [ ] Nodding detection (active agreement signal)
- [ ] Mobile camera support via IP webcam

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

<div align="center">
