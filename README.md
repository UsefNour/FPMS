# FPMS — Fighter Performance Management System

A combat sports training platform built with Flask. Covers camp planning, weight tracking, sparring partner matching, social features, and event management.

---

## Requirements

- Python 3.10 or higher
- pip

---

## Setup & Run

**1. Clone the repository**

```bash
git clone https://github.com/UsefNour/FPMS.git
cd FPMS
```

**2. Create and activate a virtual environment**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python -m venv venv
source venv/bin/activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Run the application**

```bash
python app.py
```

The app will start at **http://127.0.0.1:5000**

---

## First-time use

- Go to `http://127.0.0.1:5000/signup` to create an account
- The SQLite database (`fpms.db`) is created automatically on first run
- To pre-populate the fighters database, run:

```bash
python populate_fighters.py
```

---

## Project Structure

```
FPMS/
├── app.py                  # Application entry point
├── models.py               # SQLAlchemy database models (14 models)
├── extensions.py           # Shared extensions (LoginManager, SocketIO)
├── forms.py                # WTForms form definitions
├── requirements.txt
├── routes/
│   ├── auth.py             # Login, signup, logout
│   ├── main.py             # Dashboard, index
│   ├── training.py         # Camp planner, game plan, weight tracker
│   ├── social.py           # Friends, chat, messaging
│   ├── fighters.py         # Fighter database, comparisons
│   ├── sparring.py         # Sparring profiles and matching
│   └── events.py           # Events, registration, admin panel
├── templates/              # Jinja2 HTML templates
├── static/                 # CSS, JS, images
├── report/
│   └── FPMS_Report.docx    # Final year project report
└── poster/
    └── poster.png          # Degree show poster
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Flask 2.3, Python 3.x |
| Database | SQLite via SQLAlchemy |
| Auth | Flask-Login + bcrypt |
| Real-time | Flask-SocketIO (WebSocket) |
| Forms | WTForms + Flask-WTF (CSRF) |
| Frontend | Jinja2 templates + Bootstrap 5 |

---

## Submission

**Student:** Yousef Nour — Student ID: 23019868  
**Module:** UFCFFF-30 — Software Engineering for Business  
**Institution:** UWE Bristol, Faculty of Environment and Technology  
**Year:** 2025–26  
**Supervisor:** Steve Battle
