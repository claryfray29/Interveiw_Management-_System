from pydantic import BaseModel
from datetime import datetime

class RoleBase(BaseModel):
    name: str

class RoleCreate(RoleBase):
    pass

class Role(RoleBase):
    id: int

    class Config:
        from_attributes = True

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
    role_id: int
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
    interested_roles: list[int] = []

class CandidateCreate(CandidateBase):
    #pass
    interested_roles: list[int] = []

class Candidate(CandidateBase):
    id: int
    interested_roles: list[Role] = []

    class Config:
        from_attributes = True


#job
class JobBase(BaseModel):
    title: str
    description: str
    vacancies: int
    role_id: int

class JobCreate(JobBase):
    pass

class Job(JobBase):
    id: int
    company_id: int

    class Config:
        from_attributes = True


#application
class ApplicationBase(BaseModel):
    job_id: int
    resume: str
    
class ApplicationCreate(ApplicationBase):
    pass

class Application(ApplicationBase):
    id: int
    candidate_id: int
    company_id: int

    class Config:
        from_attributes = True


#interview
class InterviewBase(BaseModel):
    application_id: int
    interviewer_id: int
    scheduled_start: datetime
    scheduled_end: datetime
    # candidate_id: int
    # company_id: int
    # feedback: str = None
    status: str = "scheduled"

class InterviewCreate(InterviewBase):
    pass

class Interview(InterviewBase):
    id: int

    class Config:
        from_attributes = True