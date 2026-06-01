from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal, engine, get_db
from authentication import authenticate_user, create_access_token, get_current_user, verify_token

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#global admin login
@app.post("/global_admins/login", response_model=schemas.GlobalAdmin)
def global_admin_login(admin: schemas.GlobalAdminCreate, db: Session = Depends(SessionLocal)):
    db_admin = crud.get_global_admin(db, admin.id)
    return db_admin

#company admin login
@app.post("/company_admins/login", response_model=schemas.CompanyAdmin)
def company_admin_login(admin: schemas.CompanyAdminCreate, db: Session = Depends(SessionLocal)):
    db_admin = crud.get_company_admin(db, admin.id)
    return db_admin

#interviewer login
@app.post("/interviewers/login", response_model=schemas.Interviewer)
def interviewer_login(interviewer: schemas.InterviewerCreate, db: Session = Depends(SessionLocal)):
    db_interviewer = crud.get_interviewer(db, interviewer.id)
    return db_interviewer

#candidate login
@app.post("/candidates/login", response_model=schemas.Candidate)
def candidate_login(candidate: schemas.CandidateCreate, db: Session = Depends(SessionLocal)):
    db_candidate = crud.get_candidate(db, candidate.id)
    return db_candidate

