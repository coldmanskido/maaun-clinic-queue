# models.py - Contains all OOP classes for the Clinic Queue App
from datetime import datetime
from collections import deque


class Patient:
    """Represents a patient registered at the clinic."""

    def __init__(self, name, age, complaint):
        self.name = name
        self.age = age
        self.complaint = complaint
        self.registered_at = datetime.now()
        self.ticket_number = None  # Assigned by the clinic

    def get_wait_duration(self):
        """Returns how long the patient has been waiting (in minutes)."""
        delta = datetime.now() - self.registered_at
        return int(delta.total_seconds() // 60)

    def to_dict(self):
        """Returns a dictionary representation for the template."""
        return {
            "ticket": self.ticket_number,
            "name": self.name,
            "age": self.age,
            "complaint": self.complaint,
            "registered_at": self.registered_at.strftime("%I:%M %p"),
            "waiting_minutes": self.get_wait_duration(),
        }

    def __repr__(self):
        return f"<Patient #{self.ticket_number} - {self.name}>"


class SeenRecord:
    """Represents a patient who has already been attended to."""

    def __init__(self, patient, seen_at=None):
        self.name = patient.name
        self.age = patient.age
        self.complaint = patient.complaint
        self.ticket_number = patient.ticket_number
        self.registered_at = patient.registered_at
        self.seen_at = seen_at or datetime.now()

    def get_total_wait(self):
        """Total wait time from registration to being seen."""
        delta = self.seen_at - self.registered_at
        return int(delta.total_seconds() // 60)

    def to_dict(self):
        return {
            "ticket": self.ticket_number,
            "name": self.name,
            "age": self.age,
            "complaint": self.complaint,
            "registered_at": self.registered_at.strftime("%I:%M %p"),
            "seen_at": self.seen_at.strftime("%I:%M %p"),
            "total_wait_minutes": self.get_total_wait(),
        }


class ClinicQueue:
    """
    Manages the clinic's patient queue using a FIFO Queue (deque).
    Also maintains a stack-based 'recently removed' undo feature.
    """

    def __init__(self):
        # QUEUE (FIFO) — patients waiting to be seen
        self._waiting: deque[Patient] = deque()
        # STACK (LIFO) — patients already seen today (last seen on top)
        self._seen_stack: list[SeenRecord] = []
        self._ticket_counter = 1

    # ── Queue operations ──────────────────────────────────────────────

    def register_patient(self, name, age, complaint):
        """Add a new patient to the end of the queue."""
        patient = Patient(name, age, complaint)
        patient.ticket_number = self._ticket_counter
        self._ticket_counter += 1
        self._waiting.append(patient)
        return patient

    def call_next_patient(self):
        """Remove and return the next patient from the front of the queue (FIFO)."""
        if not self._waiting:
            return None
        patient = self._waiting.popleft()
        record = SeenRecord(patient)
        self._seen_stack.append(record)   # push onto the stack
        return record

    # ── Stack operations ──────────────────────────────────────────────

    def get_last_seen(self, n=5):
        """Return the N most recently seen patients (top of stack first)."""
        return [r.to_dict() for r in reversed(self._seen_stack[-n:])]

    # ── Utility ───────────────────────────────────────────────────────

    def get_waiting_list(self):
        return [p.to_dict() for p in self._waiting]

    def waiting_count(self):
        return len(self._waiting)

    def seen_today_count(self):
        return len(self._seen_stack)

    def total_patients_today(self):
        return self.waiting_count() + self.seen_today_count()


# Singleton instance shared across the app
clinic = ClinicQueue()
