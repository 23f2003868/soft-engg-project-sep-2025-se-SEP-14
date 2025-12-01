from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from sqlalchemy import BLOB

from app import db

# User model for all users (Admin, Customer, Service Professional)
class User(db.Model,UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # admin, customer, service_professional
    status = db.Column(db.String(10), nullable=False, default='ACTV')
    status_change_date = db.Column(db.DateTime, default=datetime.utcnow)
    # Relationships
    recruiter = db.relationship('Recruiter', backref='user', uselist=False, cascade="all, delete-orphan", passive_deletes=True)
    candidate = db.relationship('Candidate', backref='user', uselist=False, cascade="all, delete-orphan", passive_deletes=True)
    job = db.relationship('Job', backref='job', uselist=False, cascade="all, delete-orphan", passive_deletes=True)

    def get_id(self):
        # Flask-Login expects the return value to be a string
        return str(self.user_id)
    
    def to_dict(self):
        """Convert User object to a dictionary."""
        return {
            'user_id': self.user_id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'email': self.email,
            'role': self.role,
            'status': self.status,
            'status_change_date': self.status_change_date.strftime('%Y-%m-%d %H:%M:%S') if self.status_change_date else None
        }

# Recruiter model
class Recruiter(db.Model):
    recruiter_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'))
    company = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    linkdin_profile_path=db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(10), nullable=False, default='ACTV')
    status_change_date = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'recruiter_id': self.service_professional_id,
            'user_id': self.user_id,
            'company': self.company,
            'position': self.position,
            'linkdin_profile_path': self.linkdin_profile_path,
            'status': self.status,
            'status_change_date': self.status_change_date.strftime('%Y-%m-%d %H:%M:%S') if self.status_change_date else None
        }

# Candidate model
class Candidate(db.Model):
    candidate_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'))
    age = db.Column(db.Integer, nullable=False)
    education = db.Column(db.String(100), nullable=False)
    resume_file_path = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(10), nullable=False, default='ACTV')
    status_change_date = db.Column(db.DateTime, default=datetime.utcnow)
    skills = db.Column(db.Text)

    def to_dict(self):
        return {
            'candidate_id': self.candidate_id,
            'user_id': self.user_id,
            'age': self.age,
            'education': self.education,
            'resume_file_path': self.resume_file_path,
            'status': self.status,
            'status_change_date': self.status_change_date.strftime('%Y-%m-%d %H:%M:%S') if self.status_change_date else None
        }

class Job(db.Model):
    job_id = db.Column(db.Integer, primary_key=True)
    created_by = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'))
    job_title = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    job_type = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(10), nullable=False, default='ACTV')

    
    def to_dict(self):
        return {
            "job_id": self.job_id,
            "created_by": self.created_by,
            "job_title": self.job_title,
            "location": self.location,
            "job_type": self.job_type,
            "description": self.description,
            "start_date": str(self.start_date),
            "end_date": str(self.end_date),
            "experience": self.experience,
            "status": self.status
        }


class CandidateJobRequest(db.Model):
    candidate_job_request_id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'))
    job_id = db.Column(db.Integer, db.ForeignKey('job.job_id', ondelete='CASCADE'))
    test_score = db.Column(db.Integer, nullable=True)
    interview_scheduled_datetime = db.Column(db.DateTime,nullable=True)
    status = db.Column(db.String(100), nullable=False, default='ACTV')
    status_change_date = db.Column(db.DateTime, default=datetime.utcnow)

class SavedJob(db.Model):
    __tablename__ = "saved_jobs"

    saved_job_id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey("job.job_id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)



class Conversation(db.Model):
    __tablename__ = 'conversations'
    job_id = db.Column(db.Integer, db.ForeignKey('job.job_id'), primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True, nullable=False)
    data = db.Column(BLOB, nullable=True)  # Stores binary data, can be pickled objects, JSON bytes, etc.

    # Optional: Relationships
    job = db.relationship('Job', backref=db.backref('conversations', cascade='all, delete-orphan'))
    user = db.relationship('User', backref=db.backref('conversations', cascade='all, delete-orphan'))
