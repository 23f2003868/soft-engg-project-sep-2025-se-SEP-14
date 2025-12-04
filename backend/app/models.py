from datetime import datetime
from flask_login import UserMixin
from sqlalchemy import BLOB
from app import db


# User model – base account for Recruiter or Candidate

class User(db.Model, UserMixin):
    __tablename__ = "user"

    user_id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(10), default="ACTV")
    status_change_date = db.Column(db.DateTime, default=datetime.utcnow)

    google_access_token = db.Column(db.Text, nullable=True)
    google_refresh_token = db.Column(db.Text, nullable=True)
    google_token_expiry = db.Column(db.DateTime, nullable=True)

    # One-to-one links
    recruiter = db.relationship(
        "Recruiter",
        backref="user",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    candidate = db.relationship(
        "Candidate",
        backref="user",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    # Utility methods
    def get_id(self):
        return str(self.user_id)

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            "role": self.role,
            "status": self.status,
            "status_change_date": self.status_change_date.strftime("%Y-%m-%d %H:%M:%S")
            if self.status_change_date else None
        }



# Recruiter profile – belongs to a User

class Recruiter(db.Model):
    __tablename__ = "recruiter"

    recruiter_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id", ondelete="CASCADE"),nullable=False, unique=True, index=True)
    company = db.Column(db.String(120), nullable=False)
    position = db.Column(db.String(120), nullable=False)
    linkdin_profile_path = db.Column(db.String(255), nullable=False)
    company_about = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(10), default="ACTV")
    status_change_date = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "recruiter_id": self.recruiter_id,
            "user_id": self.user_id,
            "company": self.company,
            "position": self.position,
            "linkdin_profile_path": self.linkdin_profile_path,
            "company_about": self.company_about,
            "status": self.status,
            "status_change_date": self.status_change_date.strftime("%Y-%m-%d %H:%M:%S")
            if self.status_change_date else None
        }



# Candidate profile – belongs to a User

class Candidate(db.Model):
    __tablename__ = "candidate"

    candidate_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id", ondelete="CASCADE"),nullable=False, unique=True, index=True)
    age = db.Column(db.Integer, nullable=False)
    education = db.Column(db.String(120), nullable=False)
    resume_file_path = db.Column(db.String(255), nullable=False)
    resume_parse_status = db.Column(db.String(20), default="PENDING")
    resume_parse_error = db.Column(db.Text, nullable=True)
    skills = db.Column(db.Text, nullable=True)  
    status = db.Column(db.String(10), default="ACTV")
    status_change_date = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "candidate_id": self.candidate_id,
            "user_id": self.user_id,
            "age": self.age,
            "education": self.education,
            "resume_file_path": self.resume_file_path,
            "skills": self.skills.split(",") if self.skills else [],
            "resume_parse_status": self.resume_parse_status,
            "resume_parse_error": self.resume_parse_error,
            "status": self.status,
            "status_change_date": self.status_change_date.strftime("%Y-%m-%d %H:%M:%S")
            if self.status_change_date else None
        }


# Job posting created by a Recruiter

class Job(db.Model):
    __tablename__ = "job"

    job_id = db.Column(db.Integer, primary_key=True)
    created_by = db.Column(db.Integer, db.ForeignKey("user.user_id", ondelete="CASCADE"), nullable=False, index=True)
    job_title = db.Column(db.String(150), nullable=False)
    location = db.Column(db.String(150), nullable=False)
    job_type = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(10), default="ACTV")

    def to_dict(self):
        return {
            "job_id": self.job_id,
            "created_by": self.created_by,
            "job_title": self.job_title,
            "location": self.location,
            "job_type": self.job_type,
            "description": self.description,
            "experience": self.experience,
            "start_date": str(self.start_date),
            "end_date": str(self.end_date),
            "status": self.status
        }


# Candidate's application to a Job

class CandidateJobRequest(db.Model):
    __tablename__ = "candidate_job_request"

    candidate_job_request_id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey("candidate.candidate_id", ondelete="CASCADE"), nullable=False, index=True)
    job_id = db.Column(db.Integer, db.ForeignKey("job.job_id", ondelete="CASCADE"), nullable=False)
    test_score = db.Column(db.Integer, nullable=True)
    interview_scheduled_datetime = db.Column(db.DateTime)
    interview_duration = db.Column(db.Integer)  
    interview_mode = db.Column(db.String(50))
    interview_meet_link = db.Column(db.String(255))
    interview_notes = db.Column(db.Text)
    google_event_id = db.Column(db.String(255))
    status = db.Column(db.String(50), default="ACTV")
    status_change_date = db.Column(db.DateTime, default=datetime.utcnow)



# Saved jobs by a candidate

class SavedJob(db.Model):
    __tablename__ = "saved_jobs"

    saved_job_id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey("candidate.candidate_id", ondelete="CASCADE"), nullable=False, index=True)
    job_id = db.Column(db.Integer, db.ForeignKey("job.job_id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)



# Conversation history between candidate and chatbot (per job)

class Conversation(db.Model):
    __tablename__ = "conversations"

    job_id = db.Column(db.Integer,db.ForeignKey("job.job_id", ondelete="CASCADE"),primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey("user.user_id", ondelete="CASCADE"),primary_key=True)
    data = db.Column(BLOB, nullable=True)
