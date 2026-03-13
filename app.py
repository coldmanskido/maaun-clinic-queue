# app.py - Flask web app routes for MAAUN Clinic Queue Manager
from flask import Flask, render_template, request, redirect, url_for, flash
from models import clinic

app = Flask(__name__)
app.secret_key = "clinic-secret-key-2026"


# ── Route 1: Home / Dashboard ─────────────────────────────────────────────────
# Home route - shows dashboard with live queue and today's stats
@app.route("/")
def index():
    waiting = clinic.get_waiting_list()
    recently_seen = clinic.get_last_seen(5)
    return render_template(
        "index.html",
        waiting=waiting,
        recently_seen=recently_seen,
        waiting_count=clinic.waiting_count(),
        seen_today=clinic.seen_today_count(),
        total_today=clinic.total_patients_today(),
    )


# ── Route 2: Register a New Patient ──────────────────────────────────────────
# Register route - GET shows form, POST adds new patient to queue
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        age = request.form.get("age", "").strip()
        complaint = request.form.get("complaint", "").strip()

        if not name or not age or not complaint:
            flash("Please fill in all fields.", "error")
            return redirect(url_for("register"))

        try:
            age = int(age)
            if age <= 0 or age > 120:
                raise ValueError
        except ValueError:
            flash("Please enter a valid age.", "error")
            return redirect(url_for("register"))

        patient = clinic.register_patient(name, age, complaint)
        flash(
            f"✅ {patient.name} registered! Ticket #{patient.ticket_number}. "
            f"Position in queue: {clinic.waiting_count()}",
            "success",
        )
        return redirect(url_for("index"))

    return render_template("register.html")


# ── Route 3: Call Next Patient (action) ──────────────────────────────────────
# Call next - pops first patient from queue using FIFO (deque.popleft)
@app.route("/call-next", methods=["POST"])
def call_next():
    record = clinic.call_next_patient()
    if record:
        flash(
            f"🔔 Now seeing: {record.name} (Ticket #{record.ticket}). "
            f"Waited {record.get_total_wait()} min.",
            "info",
        )
    else:
        flash("No patients in the queue.", "warning")
    return redirect(url_for("index"))


# ── Route 4: Seen Patients History ───────────────────────────────────────────
# History route - displays all patients seen today from the stack
@app.route("/history")
def history():
    all_seen = clinic.get_last_seen(50)
    return render_template(
        "history.html",
        seen=all_seen,
        seen_today=clinic.seen_today_count(),
    )


if __name__ == "__main__":
    app.run(debug=True)
