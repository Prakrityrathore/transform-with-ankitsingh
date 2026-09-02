from __future__ import annotations

from flask import Flask, redirect, render_template

app = Flask(__name__)

INSTAGRAM_HANDLE = "transform_with_ankitsingh"
INSTAGRAM_URL = f"https://www.instagram.com/{INSTAGRAM_HANDLE}/"

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
        "title": "The Instagram DM",
        "body": "Message me @transform_with_ankitsingh. We discuss your goals, your lifestyle, and your hurdles.",
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
]


@app.context_processor
def inject_globals():
    return {
        "brand": INSTAGRAM_HANDLE,
        "coach": "Ankit Singh",
        "nav_items": NAV,
        "programs": PROGRAMS,
        "process_steps": PROCESS,
        "instagram_handle": INSTAGRAM_HANDLE,
        "instagram_url": INSTAGRAM_URL,
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


@app.route("/apply")
@app.route("/apply/success")
def apply_redirect():
    return redirect(INSTAGRAM_URL, code=302)


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
