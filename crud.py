from sqlalchemy.orm import Session
import models, schemas
from fastapi import HTTPException
import hashlib
from datetime import datetime

def get_global_admin(db: Session, admin_id: int):
    return db.query(models.GlobalAdmin).filter(models.GlobalAdmin.id == admin_id).first()

def create_global_admin(db: Session, admin: schemas.GlobalAdminCreate):
    hashed_password = hashlib.sha256(admin.password.encode()).hexdigest()
    db_admin = models.GlobalAdmin(name=admin.name, email=admin.email, password=hashed_password)
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin

#global admin specific
def add_company(db: Session, company: schemas.CompanyCreate):
    db_company = models.Company(name=company.name)
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return {"detail": "Company added successfully", "company": db_company}

#global admin specific
def get_company(db: Session, company_id: int):
    return db.query(models.Company).filter(models.Company.id == company_id).first()

#global admin specific
def delete_company(db: Session, company_id: int):
    db_company = db.query(models.Company).filter(models.Company.id == company_id).first()
    if not db_company:
        raise HTTPException(status_code=404, detail="Company not found")
    db.delete(db_company)
    db.commit()
    return {"detail": "Company deleted successfully"}

#company admin specific
def add_company_admin(db: Session, admin: schemas.CompanyAdminCreate):
    hashed_password = hashlib.sha256(admin.password.encode()).hexdigest()
    db_admin = models.CompanyAdmin(name=admin.name, email=admin.email, password=hashed_password, company_id=admin.company_id)
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return {"detail": "Company admin added successfully", "company_admin": db_admin}

#company admin login
def get_company_admin(db: Session, admin_id: int):
    return db.query(models.CompanyAdmin).filter(models.CompanyAdmin.id == admin_id).first()

#company admin specific
def delete_company_admin(db: Session, admin_id: int):
    db_admin = db.query(models.CompanyAdmin).filter(models.CompanyAdmin.id == admin_id).first()
    if not db_admin:
        raise HTTPException(status_code=404, detail="Company admin not found")
    db.delete(db_admin)
    db.commit()
    return {"detail": "Company admin deleted successfully"}

#company admin specific
def add_interviewer(db: Session, interviewer: schemas.InterviewerCreate):
    hashed_password = hashlib.sha256(interviewer.password.encode()).hexdigest()
    db_interviewer = models.Interviewer(name=interviewer.name, email=interviewer.email, password=hashed_password, company_id=interviewer.company_id)
    db.add(db_interviewer)
    db.commit()
    db.refresh(db_interviewer)
    return {"detail": "Interviewer added successfully", "interviewer": db_interviewer}

#for interviewer login
def get_interviewer(db: Session, interviewer_id: int):
    return db.query(models.Interviewer).filter(models.Interviewer.id == interviewer_id).first()

#company admin specific
def delete_interviewer(db: Session, interviewer_id: int):
    db_interviewer = db.query(models.Interviewer).filter(models.Interviewer.id == interviewer_id).first()
    if not db_interviewer:
        raise HTTPException(status_code=404, detail="Interviewer not found")
    db.delete(db_interviewer)
    db.commit()
    return {"detail": "Interviewer deleted successfully"}

#candidate specific create new account
def create_candidate(db: Session, candidate: schemas.CandidateCreate):
    hashed_password = hashlib.sha256(candidate.password.encode()).hexdigest()
    db_candidate = models.Candidate(name=candidate.name, email=candidate.email, password=hashed_password)
    db.add(db_candidate)
    db.commit()
    db.refresh(db_candidate)
    return db_candidate

#for checking login credentials of candidate
def get_candidate(db: Session, candidate_id: int):
    return db.query(models.Candidate).filter(models.Candidate.id == candidate_id).first()

#company admin specific
def add_job(db: Session, job: schemas.JobCreate):
    db_job = models.Job(title=job.title, description=job.description, company_id=job.company_id, vacancies=job.vacancies)
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return {"detail": "Job added successfully", "job": db_job}

#company admin specific
def delete_job(db: Session, job_id: int):
    db_job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not db_job:
        raise HTTPException(status_code=404, detail="Job not found")
    db.delete(db_job)
    db.commit()
    return {"detail": "Job deleted successfully"}

#candidate specific
def create_application(db: Session, application: schemas.ApplicationCreate):
    db_application = models.Application(candidate_id=application.candidate_id, job_id=application.job_id, resume=application.resume, status=application.status)
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    return {"detail": "Application created successfully", "application": db_application}

#company admin specific
def delete_application(db: Session, application_id: int):
    db_application = db.query(models.Application).filter(models.Application.id == application_id).first()
    if not db_application:
        raise HTTPException(status_code=404, detail="Application not found")
    db.delete(db_application)
    db.commit()
    return {"detail": "Application deleted successfully"}

#company admin specific
def create_interview(db: Session, interview: schemas.InterviewCreate):
    db_interview = models.Interview(application_id=interview.application_id, interviewer_id=interview.interviewer_id, scheduled_time=interview.scheduled_time, candidate_id=interview.candidate_id, feedback=interview.feedback, status=interview.status)
    db.add(db_interview)
    db.commit()
    db.refresh(db_interview)
    return {"detail": "Interview created successfully", "interview": db_interview}


#candidate specific
def view_available_jobs(db: Session):
    return db.query(models.Job).filter(models.Job.vacancies > 0).all()

#candidate specific
def view_job_status(db: Session, candidate_id: int):
    applications = db.query(models.Application).filter(models.Application.candidate_id == candidate_id).all()
    return [{"job_title": app.job.title, "status": app.status} for app in applications]


#interviewer to check upcoming interviews
def view_upcoming_interviews(db: Session, interviewer_id: int):
    return db.query(models.Interview).filter(models.Interview.interviewer_id == interviewer_id, models.Interview.scheduled_time > datetime.now(), models.Interview.status == "scheduled").all()


#return feedback for a specific interview
def interview_feedback(db: Session, interview_id: int):
    interview = db.query(models.Interview).filter(models.Interview.id == interview_id).first()
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")
    interview.status = "completed"
    db.commit()
    
    return {"candidate_name": interview.application.candidate.name, "job_title": interview.application.job.title, "feedback": interview.feedback, "status": interview.status}

#company admin rejecting all the missed interviews of a specific company
def missed_interviews(db: Session, company_id: int):
    missed_interviews = db.query(models.Interview).join(models.Job).filter(models.Job.company_id == company_id, models.Interview.scheduled_time < datetime.now(), models.Interview.status == "scheduled").all()
    for interview in missed_interviews:
        interview.status = "rejected"
        interview.feedback = "Candidate missed the interview"
    db.commit()
    return {"detail": f"{len(missed_interviews)} missed interviews marked as rejected"}

#update status of application (company admin only)
def update_application_status(db: Session, application_id: int, status: str):
    application = db.query(models.Application).filter(models.Application.id == application_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    application.status = status
    db.commit()
    return {"detail": "Application status updated successfully", "application": application}