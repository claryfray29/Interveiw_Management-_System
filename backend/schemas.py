from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

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

class CompanyUserCreate(BaseModel):
    name: str
    email: str
    password: str
    account_type: str
    role_id: Optional[int] = None

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
    skills: Optional[str] = None
    resume: Optional[str] = None

class CandidateCreate(CandidateBase):
    interested_roles: list[int] = []
    skills: Optional[str] = None

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
    skills_required: str

class Job(JobBase):
    id: int
    company_id: int
    skills_required: Optional[str] = None  # was missing from JobBase, needed by Jobs.jsx

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
    status: str = "applied"  # was missing — caused badge to not render and status column to be blank

    class Config:
        from_attributes = True


#interview
class InterviewBase(BaseModel):
    application_id: int
    interviewer_id: int
    scheduled_start: datetime
    scheduled_end: datetime
    status: str = "scheduled"

class InterviewCreate(InterviewBase):
    pass

class Interview(InterviewBase):
    id: int

    class Config:
        from_attributes = True

class CompanyWithAdminCreate(BaseModel):
    company_name: str
    super_admin_name: str
    super_admin_email: EmailStr
    super_admin_password: str