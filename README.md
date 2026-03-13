# 🏥 MAAUN Clinic Queue Manager 

A Flask web application that manages patient queues at a health clinic. Built for **COS 202 — Assignment 4** at Maryam Abacha American University of Nigeria (MAAUN).

---

## What the App Does

- **Register patients** at the clinic with their name, age, and chief complaint
- **View the live waiting queue** — patients are served in the order they arrived (First-In, First-Out / FIFO)
- **Call the next patient** with one click, moving them from the queue to the "seen" list
- **View today's history** of all patients who have been attended to, including wait times
- **Dashboard stats** show how many patients are waiting, how many have been seen, and the total registered today

---

## Technologies Used

| Layer | Technology |
|-------|-----------|
| Backend | Python 3, Flask |
| OOP | `Patient`, `SeenRecord`, `ClinicQueue` classes in `models.py` |
| Data Structure | `deque` (Queue / FIFO) for the waiting list; `list` as a Stack for seen history |
| Standard API | Python `datetime` module for timestamping registrations and call times |
| Frontend | Jinja2 HTML templates with CSS |

---

## Project Structure

```
clinic_queue/
│
├── app.py          # Flask routes (web layer)
├── models.py       # OOP classes + data structures (logic layer)
├── templates/
│   ├── base.html   # Shared layout / nav bar
│   ├── index.html  # Dashboard (home page)
│   ├── register.html  # Register new patient form
│   └── history.html   # Full seen-patients history
└── README.md
```

---

## How to Run the App Locally (Step-by-Step for Beginners)

### Step 1 — Make sure Python is installed
Open your terminal (Command Prompt on Windows, Terminal on Mac/Linux) and type:
```bash
python --version
```
You should see something like `Python 3.10.x`. If not, download Python from [python.org](https://python.org).

### Step 2 — Download or clone this project
If you have Git:
```bash
git clone https://github.com/YOUR_USERNAME/maaun-clinic-queue.git
cd maaun-clinic-queue
```
Or simply download the ZIP from GitHub and extract it, then open a terminal in that folder.

### Step 3 — Install Flask
```bash
pip install Flask
```

### Step 4 — Run the app
```bash
python app.py
```

### Step 5 — Open your browser
Go to: **http://127.0.0.1:5000**

You should see the clinic dashboard! 🎉

---

## Core Requirements Met

| Requirement | How it's implemented |
|-------------|---------------------|
| **OOP — Class with `__init__` & methods** | `Patient`, `SeenRecord`, and `ClinicQueue` classes in `models.py` |
| **Data Structure — Queue (FIFO)** | `collections.deque` in `ClinicQueue._waiting`; patients served in order of arrival |
| **Data Structure — Stack (LIFO)** | Python `list` used as stack in `ClinicQueue._seen_stack`; most recent seen patient is on top |
| **Standard API — `datetime`** | Every patient registration and call-time is timestamped using `datetime.now()` |
| **Flask — 2+ routes** | `/` (dashboard), `/register`, `/call-next`, `/history` |
| **Forms** | Register page submits via POST to Flask; data flows backend → template via `render_template` |

---

## Author
**[Dawud Munir Aliyu]** — COS 202, MAAUN, 2026
