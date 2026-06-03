from pydantic import BaseModel
from datetime import datetime

#login for all users
class Login(BaseModel):
    email: str
    password: str
    role: str

#global admin
class GlobalAdminBase(BaseModel):
    name: str
    email: str
    password: str

class GlobalAdminCreate(GlobalAdminBase):
    pass

class GlobalAdmin(GlobalAdminBase):
    id: int

    class Config:
        from_attributes = True


#company
class CompanyBase(BaseModel):
    name: str

class CompanyCreate(CompanyBase):
    pass

class Company(CompanyBase):
    id: int

    class Config:
        from_attributes = True


#company admin
class CompanyAdminBase(BaseModel):
    name: str
    email: str
    password: str

class CompanyAdminCreate(CompanyAdminBase):
    pass

class CompanyAdmin(CompanyAdminBase):
    id: int

    class Config:
        from_attributes = True


#interviewer
class InterviewerBase(BaseModel):
    name: str
    email: str
    password: str

class InterviewerCreate(InterviewerBase):
    pass

class Interviewer(InterviewerBase):
    id: int

    class Config:
        from_attributes = True


#candidate
class CandidateBase(BaseModel):
    name: str
    email: str
    password: str

class CandidateCreate(CandidateBase):
    pass

class Candidate(CandidateBase):
    id: int

    class Config:
        from_attributes = True


#job
class JobBase(BaseModel):
    title: str
    description: str
    company_id: int
    vacancies: int

class JobCreate(JobBase):
    pass

class Job(JobBase):
    id: int

    class Config:
        from_attributes = True


#application
class ApplicationBase(BaseModel):
    candidate_id: int
    job_id: int
    company_id: int
    resume: str
    status: str = "applied"
    
class ApplicationCreate(ApplicationBase):
    pass

class Application(ApplicationBase):
    id: int

    class Config:
        from_attributes = True


#interview
class InterviewBase(BaseModel):
    application_id: int
    interviewer_id: int
    scheduled_time: datetime
    candidate_id: int
    company_id: int
    feedback: str = None
    status: str = "scheduled"

class InterviewCreate(InterviewBase):
    pass

class Interview(InterviewBase):
    id: int

    class Config:
        from_attributes = True