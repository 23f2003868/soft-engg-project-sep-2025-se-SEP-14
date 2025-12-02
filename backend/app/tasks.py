from app import db
from app.models import Candidate
from app.utils import parse_pdf, extract_skills_from_resume
from app.celery_app import celery
import os

from dotenv import load_dotenv
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

@celery.task(bind=True)
def parse_resume_and_update(self, candidate_id, file_path):
    try:
        candidate = Candidate.query.filter_by(candidate_id=candidate_id).first()
        if not candidate:
            return False

        candidate.resume_parse_status = "PARSING"
        candidate.resume_parse_error = None
        db.session.commit()

        resume_text = parse_pdf(file_path)
        if not resume_text or len(resume_text.strip()) < 20:
            candidate.resume_parse_status = "FAILED"
            candidate.resume_parse_error = "Resume text could not be extracted."
            db.session.commit()
            return False

        skills = extract_skills_from_resume(resume_text, GOOGLE_API_KEY)

        if not skills:
            candidate.resume_parse_status = "FAILED"
            candidate.resume_parse_error = "Skill extraction failed."
            db.session.commit()
            return False

        candidate.skills = ",".join(skills)
        candidate.resume_parse_status = "SUCCESS"
        db.session.commit()

        return True

    except Exception as e:
        candidate = Candidate.query.filter_by(candidate_id=candidate_id).first()
        if candidate:
            candidate.resume_parse_status = "FAILED"
            candidate.resume_parse_error = str(e)
            db.session.commit()
        return False
