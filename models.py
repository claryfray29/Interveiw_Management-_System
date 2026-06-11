from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table, Boolean
from sqlalchemy.orm import relationship

from database import Base

candidate_roles = Table(
    "candidate_roles",
    Base.metadata,
    Column("candidate_id", Integer, ForeignKey("candidates.id")),
    Column("role_id", Integer, ForeignKey("roles.id"))
)

class GlobalAdmin(Base):
    __tablename__ = "global_admins"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

class Company(Base):
    __tablename__ = "companies" 

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)

    admins = relationship("CompanyAdmin", back_populates="company", cascade="all, delete-orphan")
    interviewers = relationship("Interviewer", back_populates="company", cascade="all, delete-orphan")
    jobs = relationship("Job", back_populates="company", cascade="all, delete-orphan")
    applications = relationship("Application", back_populates="company", cascade="all, delete-orphan")
    interviews = relationship("Interview", back_populates="company", cascade="all, delete-orphan")



class CompanyAdmin(Base):
    __tablename__ = "company_admins"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    is_super_admin = Column(Boolean, nullable=False, default=False)

    company = relationship("Company", back_populates="admins")

class Interviewer(Base):
    __tablename__ = "interviewers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)

    company = relationship("Company", back_populates="interviewers")
    interviews = relationship("Interview", back_populates="interviewer")

class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    interested_roles = relationship("Role", secondary=candidate_roles, back_populates="candidates")

    applications = relationship("Application", back_populates="candidate")
    interviews = relationship("Interview", back_populates="candidate")

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    vacancies = Column(Integer, nullable=False, default=0)

    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)

    company = relationship("Company", back_populates="jobs")
    applications = relationship("Application", back_populates="job", cascade="all, delete-orphan")

    role = relationship("Role", back_populates="jobs")

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    resume = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False, default="applied")
    #applied_at = Column(DateTime, nullable=False)

    candidate = relationship("Candidate", back_populates="applications")
    job = relationship("Job", back_populates="applications")
    company = relationship("Company", back_populates="applications")
    interviews = relationship("Interview", back_populates="application")

class Interview(Base):
    __tablename__ = "interviews"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False)
    interviewer_id = Column(Integer, ForeignKey("interviewers.id"), nullable=False)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=False)
    role = Column(Integer, ForeignKey("roles.id"), nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    scheduled_time = Column(DateTime, nullable=False)
    status = Column(String(50), nullable=False, default="scheduled")
    feedback = Column(String(255))

    application = relationship("Application", back_populates="interviews")
    interviewer = relationship("Interviewer", back_populates="interviews")
    candidate = relationship("Candidate", back_populates="interviews")
    company = relationship("Company", back_populates="interviews")

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)

    candidates = relationship("Candidate", secondary=candidate_roles, back_populates="interested_roles")
    jobs = relationship("Job", back_populates="role")