from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = "transform-with-ankitsingh-local"

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
LEADS_FILE = DATA_DIR / "leads.json"

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PHONE_RE = re.compile(r"^[+\d][\d\s\-()]{7,}$")

PROGRAMS = [
    {
        "slug": "12-week",
        "name": "The 12-Week Transformation",
        "eyebrow": "01",
        "best_for": "Those needing a total body and habit overhaul.",
        "includes": [
            "Personalized meal plans",
            "Custom workouts",
            "Weekly check-ins",
        ],
        "summary": "A structured reset for body composition, training, and daily habits — built so the results last after week 12.",
    },
    {
        "slug": "vip",
        "name": "1-on-1 VIP Coaching",
        "eyebrow": "02",
        "tag": "In-Person or Hybrid",
        "best_for": "Busy professionals who need maximum accountability and form correction.",
        "includes": [
            "24/7 chat support",
            "Mobility training",
            "Elite-level programming",
        ],
        "summary": "High-touch coaching for people who want faster progress, cleaner technique, and a coach in their corner every day.",
    },
    {
        "slug": "group",
        "name": "Small Group Strength",
        "eyebrow": "03",
        "best_for": "Powerlifters or those who thrive in a community environment.",
        "includes": [
            "Strength-focused cycles",
            "Gold's Gym-inspired mobility techniques",
        ],
        "summary": "Train hard with a small crew. Get strong, stay mobile, and feed off the room.",
    },
]

PROCESS = [
    {
        "step": "01",
        "title": "The Discovery Call",
        "body": "We discuss your goals, your lifestyle, and your hurdles.",
    },
    {
        "step": "02",
        "title": "The Blueprint",
        "body": "I build your custom training and nutrition plan.",
    },
    {
        "step": "03",
        "title": "The Execution",
        "body": "We train. You track. I support you 24/7.",
    },
    {
        "step": "04",
        "title": "The Result",
        "body": "Sustainable strength and a body you’re proud of.",
    },
]

NAV = [
    {"label": "Home", "endpoint": "home"},
    {"label": "About Ankit", "endpoint": "about"},
    {"label": "Programs", "endpoint": "programs"},
    {"label": "Apply Now", "endpoint": "apply"},
]


def load_leads() -> list[dict]:
    if not LEADS_FILE.exists():
        return []
    try:
        return json.loads(LEADS_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []


def save_lead(lead: dict) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    leads = load_leads()
    leads.append(lead)
    LEADS_FILE.write_text(json.dumps(leads, indent=2), encoding="utf-8")


@app.context_processor
def inject_globals():
    return {
        "brand": "transform_with_ankitsingh",
        "coach": "Ankit Singh",
        "nav_items": NAV,
        "programs": PROGRAMS,
        "process_steps": PROCESS,
    }


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/programs")
def programs():
    return render_template("programs.html")


@app.route("/apply", methods=["GET", "POST"])
def apply():
    selected = request.args.get("program", "")
    form = {
        "name": "",
        "email": "",
        "phone": "",
        "goal": "",
        "program": selected,
        "lifestyle": "",
        "message": "",
    }

    if request.method == "POST":
        form = {key: request.form.get(key, "").strip() for key in form}
        errors = validate_application(form)
        if errors:
            for error in errors:
                flash(error, "error")
            return render_template("apply.html", form=form), 400

        save_lead(
            {
                **form,
                "submitted_at": datetime.now(timezone.utc).isoformat(),
            }
        )
        return redirect(url_for("success"))

    return render_template("apply.html", form=form)


@app.route("/apply/success")
def success():
    return render_template("success.html")


def validate_application(form: dict) -> list[str]:
    errors: list[str] = []
    if len(form["name"]) < 2:
        errors.append("Please enter your full name.")
    if not EMAIL_RE.match(form["email"]):
        errors.append("Please enter a valid email address.")
    if not PHONE_RE.match(form["phone"]):
        errors.append("Please enter a valid phone number.")
    if not form["goal"]:
        errors.append("Please choose your primary goal.")
    if not form["program"]:
        errors.append("Please choose the program you are applying for.")
    if len(form["lifestyle"]) < 12:
        errors.append("Tell me a little about your current lifestyle so I can prepare for the call.")
    return errors


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
