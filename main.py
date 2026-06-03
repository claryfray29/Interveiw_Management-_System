from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal, engine, get_db
from fastapi.security import OAuth2PasswordRequestForm
from authentication import authenticate_user, create_access_token, get_current_user, verify_token, Token, login_for_access_token

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#login for all users
@app.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # user = authenticate_user(db, data.role, data.email, data.password)
    # if not user:
    #     raise HTTPException(status_code=400, detail="Invalid email or password")
    # access_token = create_access_token(data={"sub": user.email, "role": data.role})
    #return {"access_token": access_token, "token_type": "bearer"}
    return await login_for_access_token(form_data=form_data, db=db)

#create candidate account
@app.post("/candidates/", response_model=schemas.Candidate)
def create_candidate(candidate: schemas.CandidateCreate, db: Session = Depends(get_db)):
    db_candidate = crud.create_candidate(db, candidate)
    return db_candidate

#add company (global admin only)
@app.post("/companies/")
def add_company(company: schemas.CompanyCreate, current_user: schemas.GlobalAdmin = Depends(get_current_user), db: Session = Depends(get_db)):
    if getattr(current_user, "system_role", None) != "global_admin":
        raise HTTPException(status_code=403, detail="Not authorized to perform this action")
    return crud.add_company(db, company)

#delete company (global admin only)
@app.delete("/companies/{company_id}")
def delete_company(company_id: int, current_user: schemas.GlobalAdmin = Depends(get_current_user), db: Session = Depends(get_db)):
    if getattr(current_user, "system_role", None) != "global_admin":
        raise HTTPException(status_code=403, detail="Not authorized to perform this action")
    return crud.delete_company(db, company_id)

#delete company admin (company admin only)
@app.delete("/company_admins/{admin_id}")
def delete_company_admin(admin_id: int, current_user: schemas.CompanyAdmin = Depends(get_current_user), db: Session = Depends(get_db)):
    if getattr(current_user, "system_role", None) != "company_admin":
        raise HTTPException(status_code=403, detail="Not authorized to perform this action")
    return crud.delete_company_admin(db, admin_id)

#delete interviewer (company admin only)
@app.delete("/interviewers/{interviewer_id}")
def delete_interviewer(interviewer_id: int, current_user: schemas.CompanyAdmin = Depends(get_current_user), db: Session = Depends(get_db)):
    if getattr(current_user, "system_role", None) != "company_admin":
        raise HTTPException(status_code=403, detail="Not authorized to perform this action")
    return crud.delete_interviewer(db, interviewer_id)

#add job (company admin only)
@app.post("/jobs/")
def add_job(job: schemas.JobCreate, current_user: schemas.CompanyAdmin = Depends(get_current_user), db: Session = Depends(get_db)):
    if getattr(current_user, "system_role", None) != "company_admin":
        raise HTTPException(status_code=403, detail="Not authorized to perform this action")
    return crud.add_job(db, job)

#delete job (company admin only)
@app.delete("/jobs/{job_id}")
def delete_job(job_id: int, current_user: schemas.CompanyAdmin = Depends(get_current_user), db: Session = Depends(get_db)):
    if getattr(current_user, "system_role", None) != "company_admin":
        raise HTTPException(status_code=403, detail="Not authorized to perform this action")
    return crud.delete_job(db, job_id)

#delete application (company admin only)
@app.delete("/applications/{application_id}")
def delete_application(application_id: int, current_user: schemas.CompanyAdmin = Depends(get_current_user), db: Session = Depends(get_db)):
    if getattr(current_user, "system_role", None) != "company_admin":
        raise HTTPException(status_code=403, detail="Not authorized to perform this action")
    return crud.delete_application(db, application_id)

#create interview (company admin only)
@app.post("/interviews/")
def create_interview(interview: schemas.InterviewCreate, current_user: schemas.CompanyAdmin = Depends(get_current_user), db: Session = Depends(get_db)):
    if getattr(current_user, "system_role", None) != "company_admin":
        raise HTTPException(status_code=403, detail="Not authorized to perform this action")
    return crud.create_interview(db, interview)

#get available jobs (candidate only)
@app.get("/jobs/available")
def view_available_jobs(candidate_id: int, current_user: schemas.Candidate = Depends(get_current_user), db: Session = Depends(get_db)):
    if getattr(current_user, "system_role", None) != "candidate":
        raise HTTPException(status_code=403, detail="Not authorized to perform this action")
    return crud.view_available_jobs(db)

#post application for some job (candidate only)
@app.post("/applications/")
def create_application(application: schemas.ApplicationCreate, current_user: schemas.Candidate = Depends(get_current_user), db: Session = Depends(get_db)):
    if getattr(current_user, "system_role", None) != "candidate":
        raise HTTPException(status_code=403, detail="Not authorized to perform this action")
    return crud.create_application(db, application)

#get job application status (candidate only)
@app.get("/applications/status")
def view_job_status(candidate_id: int, current_user: schemas.Candidate = Depends(get_current_user), db: Session = Depends(get_db)):
    if getattr(current_user, "system_role", None) != "candidate":
        raise HTTPException(status_code=403, detail="Not authorized to perform this action")
    return crud.view_job_status(db, candidate_id)

#get upcoming interviews (interviewer only)
@app.get("/interviews/upcoming")
def view_upcoming_interviews(current_user: schemas.Interviewer = Depends(get_current_user), db= Depends(get_db)):
    if getattr(current_user, "system_role", None) != "interviewer":
        raise HTTPException(status_code=403, detail="Not authorized to perform this action")
    return crud.view_upcoming_interviews(db, current_user.id)

#post feedback for interview (interviewer only)
@app.post("/interviews/{interview_id}/feedback")
def post_interview_feedback(interview_id: int, feedback: str, current_user: schemas.Interviewer = Depends(get_current_user), db: Session = Depends(get_db)):
    if getattr(current_user, "system_role", None) != "interviewer":
        raise HTTPException(status_code=403, detail="Not authorized to perform this action")
    return crud.interview_feedback(db, interview_id, feedback)


#update application status (company admin only)
@app.put("/applications/{application_id}/status")
def update_application_status(application_id: int, status: str, current_user: schemas.CompanyAdmin = Depends(get_current_user), db: Session = Depends(get_db)):
    if getattr(current_user, "system_role", None) != "company_admin":
        raise HTTPException(status_code=403, detail="Not authorized to perform this action")
    return crud.update_application_status(db, application_id, status)

