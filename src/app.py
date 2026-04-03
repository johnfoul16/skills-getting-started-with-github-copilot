"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Team basketball practice and inter-school games",
        "schedule": "Mondays, Wednesdays, 5:00 PM - 7:00 PM",
        "max_participants": 15,
        "participants": ["alex@mergington.edu", "maria@mergington.edu"]
    },
    "Swimming Club": {
        "description": "Swim training and technique improvement",
        "schedule": "Tuesdays, Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["leah@mergington.edu", "noah@mergington.edu"]
    },
    "Track and Field": {
        "description": "Track events and field training for sprint and long jump",
        "schedule": "Fridays, 3:00 PM - 5:00 PM",
        "max_participants": 25,
        "participants": ["ethan@mergington.edu", "mia@mergington.edu"]
    },
    "Art Club": {
        "description": "Drawing, painting, and mixed media projects",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["sarah@mergington.edu", "david@mergington.edu"]
    },
    "Drama Society": {
        "description": "Acting workshops and stage production rehearsals",
        "schedule": "Tuesdays, 4:00 PM - 6:00 PM",
        "max_participants": 20,
        "participants": ["oliver@mergington.edu", "ava@mergington.edu"]
    },
    "Photography Club": {
        "description": "Learn photography skills and organize photo exhibitions",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["lucas@mergington.edu", "emma@mergington.edu"]
    },
    "Debate Team": {
        "description": "Prepare for debate competitions and develop public speaking",
        "schedule": "Mondays, 4:00 PM - 5:30 PM",
        "max_participants": 16,
        "participants": ["grace@mergington.edu", "owen@mergington.edu"]
    },
    "Math Olympiad": {
        "description": "Advanced problem-solving sessions for math competitions",
        "schedule": "Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 18,
        "participants": ["sophie@mergington.edu", "henry@mergington.edu"]
    },
    "Science Club": {
        "description": "Hands-on experiments and science fair project development",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": ["isabella@mergington.edu", "liam@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    # Validate student is not already signed up
    activity = activities[activity_name]
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student is already signed up for this activity")


    # Get the specific activity
    activity = activities[activity_name]

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}
