from sqlalchemy.orm import Session
import models, schemas
from fastapi import HTTPException
import hashlib

def get_global_admin(db: Session, admin_id: int):
    return db.query(models.GlobalAdmin).filter(models.GlobalAdmin.id == admin_id).first()

def create_global_admin(db: Session, admin: schemas.GlobalAdminCreate):
    hashed_password = hashlib.sha256(admin.password.encode()).hexdigest()
    db_admin = models.GlobalAdmin(name=admin.name, email=admin.email, password=hashed_password)
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin

def add_company(db: Session, company: schemas.CompanyCreate):
    db_company = models.Company(name=company.name)
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return {"detail": "Company added successfully", "company": db_company}

def get_company(db: Session, company_id: int):
    return db.query(models.Company).filter(models.Company.id == company_id).first()

def delete_company(db: Session, company_id: int):
    db_company = db.query(models.Company).filter(models.Company.id == company_id).first()
    if not db_company:
        raise HTTPException(status_code=404, detail="Company not found")
    db.delete(db_company)
    db.commit()
    return {"detail": "Company deleted successfully"}

def add_company_admin(db: Session, admin: schemas.CompanyAdminCreate):
    hashed_password = hashlib.sha256(admin.password.encode()).hexdigest()
    db_admin = models.CompanyAdmin(name=admin.name, email=admin.email, password=hashed_password, company_id=admin.company_id)
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return {"detail": "Company admin added successfully", "company_admin": db_admin}

def get_company_admin(db: Session, admin_id: int):
    return db.query(models.CompanyAdmin).filter(models.CompanyAdmin.id == admin_id).first()

def delete_company_admin(db: Session, admin_id: int):
    db_admin = db.query(models.CompanyAdmin).filter(models.CompanyAdmin.id == admin_id).first()
    if not db_admin:
        raise HTTPException(status_code=404, detail="Company admin not found")
    db.delete(db_admin)
    db.commit()
    return {"detail": "Company admin deleted successfully"}

def add_interviewer(db: Session, interviewer: schemas.InterviewerCreate):
    hashed_password = hashlib.sha256(interviewer.password.encode()).hexdigest()
    db_interviewer = models.Interviewer(name=interviewer.name, email=interviewer.email, password=hashed_password, company_id=interviewer.company_id)
    db.add(db_interviewer)
    db.commit()
    db.refresh(db_interviewer)
    return {"detail": "Interviewer added successfully", "interviewer": db_interviewer}

def get_interviewer(db: Session, interviewer_id: int):
    return db.query(models.Interviewer).filter(models.Interviewer.id == interviewer_id).first()

def delete_interviewer(db: Session, interviewer_id: int):
    db_interviewer = db.query(models.Interviewer).filter(models.Interviewer.id == interviewer_id).first()
    if not db_interviewer:
        raise HTTPException(status_code=404, detail="Interviewer not found")
    db.delete(db_interviewer)
    db.commit()
    return {"detail": "Interviewer deleted successfully"}

def create_candidate(db: Session, candidate: schemas.CandidateCreate):
    hashed_password = hashlib.sha256(candidate.password.encode()).hexdigest()
    db_candidate = models.Candidate(name=candidate.name, email=candidate.email, password=hashed_password)
    db.add(db_candidate)
    db.commit()
    db.refresh(db_candidate)
    return {"detail": "Candidate created successfully", "candidate": db_candidate}

def get_candidate(db: Session, candidate_id: int):
    return db.query(models.Candidate).filter(models.Candidate.id == candidate_id).first()

def add_job(db: Session, job: schemas.JobCreate):
    db_job = models.Job(title=job.title, description=job.description, company_id=job.company_id, vacancies=job.vacancies)
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return {"detail": "Job added successfully", "job": db_job}

def delete_job(db: Session, job_id: int):
    db_job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not db_job:
        raise HTTPException(status_code=404, detail="Job not found")
    db.delete(db_job)
    db.commit()
    return {"detail": "Job deleted successfully"}

def create_application(db: Session, application: schemas.ApplicationCreate):
    db_application = models.Application(candidate_id=application.candidate_id, job_id=application.job_id, status=application.status)
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    return {"detail": "Application created successfully", "application": db_application}

def delete_application(db: Session, application_id: int):
    db_application = db.query(models.Application).filter(models.Application.id == application_id).first()
    if not db_application:
        raise HTTPException(status_code=404, detail="Application not found")
    db.delete(db_application)
    db.commit()
    return {"detail": "Application deleted successfully"}

def create_interview(db: Session, interview: schemas.InterviewCreate):
    db_interview = models.Interview(application_id=interview.application_id, interviewer_id=interview.interviewer_id, scheduled_at=interview.scheduled_at)
    db.add(db_interview)
    db.commit()
    db.refresh(db_interview)
    return {"detail": "Interview created successfully", "interview": db_interview}