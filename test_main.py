import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import hashlib
from datetime import datetime

from database import Base, get_db
from main import app
import models

# 1. Setup an isolated, in-memory SQLite database configuration for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_db.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 2. Dependency override wrapper to intercept endpoints using get_db
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    """Drops and recreates testing tables before running each test module."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    # Seed fundamental testing authorization profiles
    db = TestingSessionLocal()
    hashed_password = hashlib.sha256("securepassword".encode()).hexdigest()
    
    # Create Global Admin
    global_admin = models.GlobalAdmin(name="Global Admin", email="global@test.com", password=hashed_password)
    db.add(global_admin)
    
    # Create testing Corporate Entity
    company = models.Company(id=1, name="Test Corp")
    db.add(company)
    db.commit()
    
    # Create Company Admin, Interviewer, and Candidate profiles
    company_admin = models.CompanyAdmin(name="Company Admin", email="admin@test.com", password=hashed_password, company_id=1)
    interviewer = models.Interviewer(id=1, name="John Doe", email="interviewer@test.com", password=hashed_password, company_id=1)
    candidate = models.Candidate(id=1, name="Jane Smith", email="candidate@test.com", password=hashed_password)
    
    db.add_all([company_admin, interviewer, candidate])
    db.commit()
    db.close()

# =========================================================================
# UNIFIED AUTHENTICATION GATES TESTING
# =========================================================================

def test_login_success_candidate():
    """Verifies that a registered candidate gets a bearer token with their exact role context."""
    response = client.post(
        "/login",
        json={"email": "candidate@test.com", "password": "securepassword", "role": "candidate"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_failure_wrong_password():
    """Ensures bad user credentials block system initialization access requests with a 400 error."""
    response = client.post(
        "/login",
        json={"email": "candidate@test.com", "password": "wrongpassword", "role": "candidate"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid email or password"

# =========================================================================
# CANDIDATE SYSTEM ACTIONS TESTING
# =========================================================================

def test_create_candidate_account():
    """Asserts registration mechanics generate clean entities."""
    response = client.post(
        "/candidates/",
        json={"name": "New Candidate", "email": "new@gmail.com", "password": "mypassword"}
    )
    assert response.status_code == 200
    #assert response.json()["detail"] == "Candidate created successfully"
    assert response.json()["email"] == "new@gmail.com"

def test_view_available_jobs_authorization_barrier():
    """Verifies unauthenticated visitors are blocked from scanning internal open positions."""
    response = client.get("/jobs/available")
    assert response.status_code == 401

def test_view_available_jobs_success():
    """Confirms candidates can fetch job vacancies once signed in with a valid token."""
    # Obtain Candidate Access Token
    login_resp = client.post("/login", json={"email": "candidate@test.com", "password": "securepassword", "role": "candidate"})
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Inject a testing job position via database hook
    db = TestingSessionLocal()
    job = models.Job(title="Software Engineer", description="Python dev", company_id=1, vacancies=3)
    db.add(job)
    db.commit()
    db.close()
    
    response = client.get("/jobs/available", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Software Engineer"

# =========================================================================
# ADMINISTRATIVE CONTROLS TESTING
# =========================================================================

def test_add_job_as_company_admin():
    """Confirms Company Admins can declare structural open corporate hiring requests."""
    login_resp = client.post("/login", json={"email": "admin@test.com", "password": "securepassword", "role": "company_admin"})
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.post(
        "/jobs/",
        json={"title": "Data Analyst", "description": "SQL specialist", "company_id": 1, "vacancies": 2},
        headers=headers
    )
    assert response.status_code == 200
    assert response.json()["detail"] == "Job added successfully"

def test_insufficient_permissions_guard():
    """Ensures a Candidate cannot perform administrative actions like deleting a corporate structure."""
    login_resp = client.post("/login", json={"email": "candidate@test.com", "password": "securepassword", "role": "candidate"})
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.delete("/companies/1", headers=headers)
    assert response.status_code == 403
    assert response.json()["detail"] == "Not authorized to perform this action"

# =========================================================================
# INTERVIEWER EVALUATION MECHANICS TESTING
# =========================================================================

def test_post_interview_feedback_flow():
    """Tracks interview completion routing loops by submitting feedback scores."""
    login_resp = client.post("/login", json={"email": "interviewer@test.com", "password": "securepassword", "role": "interviewer"})
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Inject active base context elements to bypass integrity validation locks
    db = TestingSessionLocal()
    job = models.Job(id=1, title="QA Architect", description="Testing engineer", company_id=1, vacancies=1)
    app = models.Application(id=1, candidate_id=1, job_id=1, company_id=1, resume="url", status="applied")
    interview = models.Interview(id=5, application_id=1, interviewer_id=1, candidate_id=1, company_id=1, scheduled_time=datetime.now(), status="scheduled")
    db.add_all([job, app, interview])
    db.commit()
    db.close()
    
    response = client.post(
        "/interviews/5/feedback?feedback=Excellent skills exhibited across coding modules",
        headers=headers
    )
    assert response.status_code == 200
    assert response.json()["status"] == "completed"