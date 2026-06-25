from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal, engine, get_db
from fastapi.security import OAuth2PasswordRequestForm
from authentication import authenticate_user, create_access_token, get_current_user, verify_token, Token, login_for_access_token
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True, 
    allow_methods=["*"], 
    allow_headers=["*"]
)

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

@app.put("/candidates/profile")
def update_profile(skills: str, resume: str, current_user: schemas.Candidate = Depends(get_current_user), db: Session = Depends(get_db)):
    if getattr(current_user, "system_role", None) != "candidate":
        raise HTTPException(status_code=403, detail="Not authorized to perform this action")
        
    return crud.update_candidate_profile(db, candidate_id=current_user.id, skills=skills, resume_url=resume)

#add company (global admin only)
# @app.post("/companies/")
# def add_company(company: schemas.CompanyCreate, current_user: schemas.GlobalAdmin = Depends(get_current_user), db: Session = Depends(get_db)):
#     if getattr(current_user, "system_role", None) != "global_admin":
#         raise HTTPException(status_code=403, detail="Not authorized to perform this action")
#     return crud.add_company(db, company)

@app.post("/companies/", status_code=201)
def add_company(payload: schemas.CompanyWithAdminCreate, current_user: schemas.GlobalAdmin = Depends(get_current_user), db: Session = Depends(get_db)):
    if getattr(current_user, "system_role", None) != "global_admin":
        raise HTTPException(status_code=403, detail="Not authorized to perform this action")
    
    return crud.add_company(db, payload)

#delete company (global admin only)
@app.delete("/companies/{company_id}")
def delete_company(company_id: int, current_user: schemas.GlobalAdmin = Depends(get_current_user), db: Session = Depends(get_db)):
    if getattr(current_user, "system_role", None) != "global_admin":
        raise HTTPException(status_code=403, detail="Not authorized to perform this action")
    return crud.delete_company(db, company_id)

#delete company admin (company admin only)
@app.delete("/company_admins/{admin_id}")
def delete_company_admin(admin_id: int, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    if getattr(current_user, "system_role", None) != "company_admin":
        raise HTTPException(status_code=403, detail="Not authorized to perform this action")
    
    is_super = getattr(current_user, "is_super_admin", False)
    if not is_super:
        raise HTTPException(
            status_code=403, 
            detail="Only a Company Super Admin can delete company admins."
        )
        
    return crud.delete_company_admin_secure(db, admin_id=admin_id, company_id=current_user.company_id)

# #add interviewer (company admin only)
# @app.post("/interviewers/")
# def add_interviewer(interviewer: schemas.InterviewerCreate, current_user: schemas.CompanyAdmin = Depends(get_current_user), db: Session = Depends(get_db)):
#     if getattr(current_user, "system_role", None) != "company_admin":
#         raise HTTPException(status_code=403, detail="Not authorized to perform this action")
#     return crud.add_interviewer(db, interviewer, company_id=current_user.company_id)

@app.post("/companies/users")
def create_company_user(payload: schemas.CompanyUserCreate, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    role = getattr(current_user, "system_role", None)
    
    if role != "company_admin":
        raise HTTPException(status_code=403, detail="Not authorized to perform company user updates")
    
    is_super = getattr(current_user, "is_super_admin", False)
    
    if payload.account_type == "company_admin" and not is_super:
        raise HTTPException(status_code=403, detail="Unauthorise")
        
    if payload.account_type not in ["company_admin", "interviewer"]:
        raise HTTPException(status_code=400, detail="Invalid account type target.")

    return crud.create_company_user(db, user_data=payload, company_id=current_user.company_id)

#delete interviewer (company admin only)
@app.delete("/interviewers/{interviewer_id}")
def delete_interviewer(interviewer_id: int, current_user: schemas.CompanyAdmin = Depends(get_current_user), db: Session = Depends(get_db)):
    if getattr(current_user, "system_role", None) != "company_admin":
        raise HTTPException(status_code=403, detail="Not authorized to perform this action")
    return crud.delete_interviewer(db, interviewer_id, company_id=current_user.company_id)

#add job (company admin only)
@app.post("/jobs/")
def add_job(job: schemas.JobCreate, current_user: schemas.CompanyAdmin = Depends(get_current_user), db: Session = Depends(get_db)):
    if getattr(current_user, "system_role", None) != "company_admin":
        raise HTTPException(status_code=403, detail="Not authorized to perform this action")
    return crud.add_job(db, job, company_id=current_user.company_id)

#delete job (company admin only)
@app.delete("/jobs/{job_id}")
def delete_job(job_id: int, current_user: schemas.CompanyAdmin = Depends(get_current_user), db: Session = Depends(get_db)):
    if getattr(current_user, "system_role", None) != "company_admin":
        raise HTTPException(status_code=403, detail="Not authorized to perform this action")
    return crud.delete_job(db, job_id)

#delete application (company admin only)
@app.delete("/applications/{application_id}")
def delete_application(application_id: int, current_user: schemas.CompanyAdmin = Depends(get_current_user), db: Session = Depends(get_db)):
    if getattr(current_user, "system_role", None) != "company_admin" and getattr(current_user, "system_role", None) != "candidate":
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
def view_available_jobs(current_user: schemas.Candidate = Depends(get_current_user), db: Session = Depends(get_db)):
    if getattr(current_user, "system_role", None) != "candidate":
        raise HTTPException(status_code=403, detail="Not authorized to perform this action")
    return crud.view_available_jobs(db, candidate_id=current_user.id)

#post application for some job (candidate only)
@app.post("/applications/")
def create_application(application: schemas.ApplicationCreate, current_user: schemas.Candidate = Depends(get_current_user), db: Session = Depends(get_db)):
    if getattr(current_user, "system_role", None) != "candidate":
        raise HTTPException(status_code=403, detail="Not authorized to perform this action")
    return crud.create_application(db, application, candidate_id=current_user.id)

#get job application status (candidate only)
@app.get("/applications/status")
def view_job_status(current_user: schemas.Candidate = Depends(get_current_user), db: Session = Depends(get_db)):
    if getattr(current_user, "system_role", None) != "candidate":
        raise HTTPException(status_code=403, detail="Not authorized to perform this action")
    return crud.view_job_status(db, candidate_id=current_user.id)

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
        
    return crud.interview_feedback(db, interview_id=interview_id, feedback=feedback,current_interviewer=current_user)

#company can view applications
@app.get("/companies/applications")
def view_company_applications(job_id: Optional[int] = None, current_user: schemas.CompanyAdmin = Depends(get_current_user), db: Session = Depends(get_db)):
    if getattr(current_user, "system_role", None) != "company_admin":
        raise HTTPException(status_code=403, detail="Not authorized to perform this action")
    
    return crud.company_view_applications(db, company_id=current_user.company_id, job_id=job_id)

#update application status (company admin only)
@app.put("/applications/{application_id}/status")
def update_application_status(application_id: int, status: str, current_user: schemas.CompanyAdmin = Depends(get_current_user), db: Session = Depends(get_db)):
    if getattr(current_user, "system_role", None) != "company_admin":
        raise HTTPException(status_code=403, detail="Not authorized to perform this action")
    return crud.update_application_status(db, application_id, status)


