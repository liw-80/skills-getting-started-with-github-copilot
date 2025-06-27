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
    # Sports activities
    "Soccer Team": {
        "description": "Join the school soccer team and compete in local leagues",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 18,
        "participants": []
    },
    "Basketball Club": {
        "description": "Practice basketball skills and play friendly matches",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": []
    },
    # Artistic activities
    "Drama Club": {
        "description": "Act, direct, and participate in school theater productions",
        "schedule": "Mondays, 3:30 PM - 5:00 PM",
        "max_participants": 25,
        "participants": []
    },
    "Art Workshop": {
        "description": "Explore painting, drawing, and sculpture techniques",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": []
    },
    # Intellectual activities
    "Math Olympiad": {
        "description": "Prepare for math competitions and solve challenging problems",
        "schedule": "Fridays, 2:00 PM - 3:30 PM",
        "max_participants": 15,
        "participants": []
    },
    "Science Club": {
        "description": "Conduct experiments and explore scientific concepts",
        "schedule": "Wednesdays, 4:00 PM - 5:00 PM",
        "max_participants": 20,
        "participants": []
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

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student already signed up")
    # Validate max participants not exceeded
    if len(activity["participants"]) >= activity["max_participants"]:
        raise HTTPException(status_code=400, detail="Maximum participants reached") 
    # Validate email format
    if "@" not in email or "." not in email.split("@")[-1]:
        raise HTTPException(status_code=400, detail="Invalid email format")
    # Validate email domain
    if not email.endswith("@mergington.edu"):
        raise HTTPException(status_code=400, detail="Email must be a Mergington High School email")
    # Validate email is not empty
    if not email:   
        raise HTTPException(status_code=400, detail="Email cannot be empty")
    # Validate email is not too long
    if len(email) > 255:
        raise HTTPException(status_code=400, detail="Email is too long")
    # Validate email is not too short
    if len(email) < 5:
        raise HTTPException(status_code=400, detail="Email is too short")
    # Validate email does not contain spaces
    if " " in email:
        raise HTTPException(status_code=400, detail="Email cannot contain spaces")
    # Validate email does not contain special characters
    if not email.replace(".", "").replace("@", "").isalnum():   
        raise HTTPException(status_code=400, detail="Email cannot contain special characters")
    # Validate email is not a duplicate
    for activity in activities.values():
        if email in activity["participants"]:
            raise HTTPException(status_code=400, detail="Email already signed up for another activity")
        
    # Validate email is not a school staff email
    if email.startswith("myshcool") or email.startswith("admin") or email.startswith("teacher"):
        raise HTTPException(status_code=400, detail="Email cannot be a school staff email") 
    # Validate email is not a student email from another school
    if email.endswith("@otherhighschool.edu"):
        raise HTTPException(status_code=400, detail="Email must be a Mergington High School student email")     
       

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}
