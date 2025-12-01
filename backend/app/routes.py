# ---------------------------------Imports-------------------------------------------
from functools import wraps
from operator import and_
import os
import datetime
import jwt

from flask import (
    Blueprint, json, jsonify, flash, request, redirect,
    url_for, render_template, send_from_directory
)
from flask_login import (
    login_user, current_user, logout_user,
    login_required, LoginManager
)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from app import db, redis_client
from app.forms import (
    RegisterAdminForm, RegisterCandidateForm,
    RegisterRecruiterForm, CreateJobForm
)
from app.models import CandidateJobRequest, Job, Recruiter, Candidate, User,Conversation

from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool 
from langchain_core.messages import HumanMessage,AIMessage


import pickle

CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
SCOPES = ["https://www.googleapis.com/auth/calendar.events"]





main = Blueprint("main", __name__)

UPLOAD_FOLDER = "C:/resumes/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ---------------------------------Login Manager-------------------------------------
login_manager = LoginManager()
login_manager.login_view = "main.api_login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# ---------------------------------JWT Token-----------------------------------------
SECRET_KEY = "SECRET_KEY1111111111111111111111"



def generate_jwt_token(user):
    expiration = datetime.datetime.utcnow() + datetime.timedelta(
        minutes=30
    )

    payload = {
        "user_id": str(user.user_id),
        "email": user.email,
        "role": user.role,
        "exp": expiration
    }

    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Authorization: Bearer <token>
        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]
            parts = auth_header.split()
            if len(parts) == 2 and parts[0] == "Bearer":
                token = parts[1]

        if not token:
            return jsonify({"success": False, "message": "Token is missing"}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            from app.models import User
            current_user = User.query.get(data["user_id"])
            if not current_user:
                return jsonify({"success": False, "message": "User not found"}), 404
        except Exception as e:
            return jsonify({"success": False, "message": "Invalid token"}), 401

        return f(current_user, *args, **kwargs)

    return decorated


@main.route('/api/login', methods=['POST'])
def api_login():
    try:
        data = request.get_json() or {}

        email = data.get("email", "").strip()
        password = data.get("password", "").strip()

        # ---------------------- VALIDATION ----------------------
        errors = {}

        if not email:
            errors["email"] = "Email is required."
        if not password:
            errors["password"] = "Password is required."

        if errors:
            return jsonify({
                "success": False,
                "message": "Validation errors",
                "errors": errors
            }), 422  # Unprocessable Entity

        # ---------------------- USER CHECK ----------------------
        user = User.query.filter_by(email=email, status="ACTV").first()

        if not user or not check_password_hash(user.password, password):
            return jsonify({
                "success": False,
                "message": "Invalid email or password."
            }), 401

        # ---------------------- SUCCESS ----------------------
        token = generate_jwt_token(user)

        print("LOGIN USER FIRSTNAME =", user.firstname) 

        return jsonify({
            "success": True,
            "message": "Login successful!",
            "token": token,
            "expires_in_minutes": 30,
            "user": {
                "id": user.user_id,
                "email": user.email,
                "role": user.role,
                "firstname": user.firstname
            }
        }), 200
        
    

    except Exception as e:
        return jsonify({
            "success": False,
            "message": "Server error",
            "error": str(e)
        }), 500



@main.route('/api/logout', methods=['POST'])
@token_required
def logout_api(current_user):
    try:
        return jsonify({
            "success": True,
            "message": "Logged out successfully. Please delete token on client side."
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"An error occurred: {str(e)}"
        }), 500


#vueonly--------------------------------------------------------------------------------------------------

@main.route('/api/index', methods=['POST'])
@token_required
def api_index(current_user):
    try:
        # Base user data
        user_data = {
            "id": str(current_user.user_id),
            "email": current_user.email,
            "role": current_user.role,
            "firstname": current_user.firstname,
            "lastname": current_user.lastname,
            "status": current_user.status
        }

        # ------------------------------------
        #    ADD CANDIDATE DETAILS
        # ------------------------------------
        if current_user.role == "CANDIDATE":
            candidate = Candidate.query.filter_by(user_id=current_user.user_id).first()
            if not candidate:
                return jsonify({"success": False, "message": "Candidate profile missing"}), 404

            user_data["candidate"] = {
                "candidate_id": str(candidate.candidate_id),
                "age": candidate.age,
                "education": candidate.education,
                "resume_file_path": candidate.resume_file_path
            }

        # ------------------------------------
        #    ADD RECRUITER DETAILS
        # ------------------------------------
        elif current_user.role == "RECRUITER":
            recruiter = Recruiter.query.filter_by(user_id=current_user.user_id).first()
            if not recruiter:
                return jsonify({"success": False, "message": "Recruiter profile missing"}), 404

            user_data["recruiter"] = {
                "recruiter_id": str(recruiter.recruiter_id),
                "company": recruiter.company,
                "position": recruiter.position,
                "linkdin_profile_path": recruiter.linkdin_profile_path
            }

        # ------------------------------------
        # SUCCESS RESPONSE
        # ------------------------------------
        return jsonify({
            "success": True,
            "message": "User data loaded",
            "user": user_data
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"An error occurred: {str(e)}"
        }), 500



def get_token_from_header():
    auth_header = request.headers.get('Authorization', None)
    if not auth_header or not auth_header.startswith("Bearer "):
        return None
    return auth_header.split(" ")[1]



from flask import request, jsonify
from werkzeug.security import generate_password_hash

def normalize_description(desc):
    """Ensure job.description is always returned as clean text."""
    if desc is None:
        return ""

    # Already clean string
    if isinstance(desc, str):
        return desc

    # If list → join recursively
    if isinstance(desc, list):
        parts = [normalize_description(x) for x in desc]
        return "\n".join([p for p in parts if p])

    # If dict → extract known fields
    if isinstance(desc, dict):
        pieces = []

        if "text" in desc:
            pieces.append(desc["text"])

        if "value" in desc:
            pieces.append(desc["value"])

        if "children" in desc:
            pieces.append(normalize_description(desc["children"]))

        # Recursively extract
        for key, value in desc.items():
            if key not in ["text", "value", "children"]:
                pieces.append(normalize_description(value))

        return "\n".join(pieces)

    # Fallback → convert to string
    return str(desc)


@main.route('/api/register-recruiter', methods=['POST'])
def register_recruiter():
    try:
        data = request.get_json() or {}

        # ---------------------- VALIDATION ----------------------
        required = [
            "firstname", "lastname", "email", "password",
            "company", "position", "linkdin_profile_path"
        ]

        errors = {}

        for field in required:
            if not data.get(field):
                errors[field] = f"{field.replace('_', ' ').title()} is required."

        # Email validation
        if data.get("email") and "@" not in data["email"]:
            errors["email"] = "Please enter a valid email address."

        # If any validation errors
        if errors:
            return jsonify({
                "success": False,
                "message": "Validation errors",
                "errors": errors
            }), 422

        # ---------------------- DUPLICATE EMAIL CHECK ----------------------
        existing_user = User.query.filter_by(email=data["email"]).first()
        if existing_user:
            return jsonify({
                "success": False,
                "message": "Email already registered.",
                "errors": {"email": "This email is already in use."}
            }), 409  # Conflict

        # ---------------------- CREATE USER ----------------------
        hashed_password = generate_password_hash(data["password"])

        new_user = User(
            firstname=data["firstname"],
            lastname=data["lastname"],
            email=data["email"],
            password=hashed_password,
            role="RECRUITER",
            status="ACTV"
        )
        db.session.add(new_user)
        db.session.commit()

        # ---------------------- CREATE RECRUITER ----------------------
        new_recruiter = Recruiter(
            user_id=new_user.user_id,
            company=data["company"],
            position=data["position"],
            linkdin_profile_path=data["linkdin_profile_path"],
            status="ACTV"
        )
        db.session.add(new_recruiter)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Recruiter registered successfully.",
            "data": {
                "user_id": new_user.user_id,
                "email": new_user.email,
                "role": new_user.role
            }
        }), 201  # Created

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": "Server error occurred.",
            "error": str(e)
        }), 500


@main.route('/api/update-recruiter', methods=['POST'])
@token_required
def update_recruiter(current_user):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No input data provided"}), 400

        # ---- VALIDATE REQUIRED FIELDS ----
        required_fields = ['firstname', 'lastname', 'email', 'company', 'position']
        for field in required_fields:
            if not data.get(field):
                return jsonify({"success": False, "error": f"{field} is required"}), 400

        # ---- FETCH USER ----
        user = User.query.filter_by(user_id=current_user.user_id, status="ACTV").first()
        if not user:
            return jsonify({"success": False, "error": "User not found"}), 404

        # ---- CHECK EMAIL DUPLICATION ----
        if data["email"] != user.email:
            existing_user = User.query.filter_by(email=data["email"]).first()
            if existing_user:
                return jsonify({"success": False, "error": "Email already in use"}), 400

        # ---- FETCH RECRUITER RECORD ----
        recruiter = Recruiter.query.filter_by(user_id=user.user_id, status="ACTV").first()
        if not recruiter:
            return jsonify({"success": False, "error": "Recruiter profile not found"}), 404

        # ---- VALIDATE LINKEDIN URL ----
        linkedin = data.get("linkdin_profile_path", "")
        if linkedin and not linkedin.startswith("http"):
            return jsonify({"success": False, "error": "Invalid LinkedIn URL"}), 400        

        # ---- UPDATE USER ----
        user.firstname = data.get("firstname", user.firstname)
        user.lastname = data.get("lastname", user.lastname)
        user.email = data.get("email", user.email)

        # ---- UPDATE RECRUITER ----
        recruiter.company = data.get("company", recruiter.company)
        recruiter.position = data.get("position", recruiter.position)
        recruiter.linkdin_profile_path = linkedin

        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Recruiter details updated successfully"
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500



@main.route('/api/jobs', methods=['GET'])
@token_required
def get_jobs(current_user):
    try:
        if current_user.role=="RECRUITER":
            jobs_data = Job.query.filter_by(created_by=current_user.user_id, status="ACTV").all()

            jobs = []
            for job in jobs_data:
                jobs.append({
                    "job_id": job.job_id,
                    "job_title": job.job_title,
                    "location": job.location,
                    "job_type": job.job_type,
                    "experience": job.experience,
                    "description": normalize_description(job.description),
                    "start_date": str(job.start_date),
                    "end_date": str(job.end_date),
                    "status": job.status
                })

            return jsonify({
                "jobs": jobs
            }), 200
        else:
            return jsonify({
                'message': 'Invalid Recruiter!',
            }), 400

    except Exception as e:
        return jsonify({"error": f"Failed to fetch jobs: {str(e)}"}), 500



from flask import send_file

# Define the folder where the file should be saved
UPLOAD_FOLDER = "C:/resumes/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure the folder exists

@main.route('/api/register-candidate', methods=['POST'])
def register_candidate():
    try:
        # ---------------------- Check File + Form ----------------------
        if "file" not in request.files:
            return jsonify({
                "success": False,
                "message": "Resume file is required.",
                "errors": {"file": "Please upload a resume file."}
            }), 400

        if "user_data" not in request.form:
            return jsonify({
                "success": False,
                "message": "User data is missing.",
                "errors": {"user_data": "User data is required in form-data."}
            }), 400

        # Parse user_data from JSON string
        try:
            user_data = json.loads(request.form["user_data"])
        except:
            return jsonify({
                "success": False,
                "message": "Invalid user_data format. Must be JSON."
            }), 400

        file = request.files["file"]

        # ---------------------- VALIDATION ----------------------
        required = ["firstname", "lastname", "email", "password", "education", "age"]
        errors = {}

        for field in required:
            if not user_data.get(field):
                errors[field] = f"{field.replace('_', ' ').title()} is required."

        # Email format
        if user_data.get("email") and "@" not in user_data["email"]:
            errors["email"] = "Please enter a valid email address."

        # Password
        if user_data.get("password") and len(user_data["password"]) < 6:
            errors["password"] = "Password must be at least 6 characters."

        # Age
        if user_data.get("age"):
            try:
                if int(user_data["age"]) < 18:
                    errors["age"] = "Minimum age must be 18."
            except:
                errors["age"] = "Age must be a number."

        # If validation errors exist
        if errors:
            return jsonify({
                "success": False,
                "message": "Validation errors",
                "errors": errors
            }), 422

        # ---------------------- Duplicate Email Check ----------------------
        existing_user = User.query.filter_by(email=user_data["email"]).first()
        if existing_user:
            return jsonify({
                "success": False,
                "message": "Email already registered.",
                "errors": {"email": "This email is already in use."}
            }), 409

        # ---------------------- Validate Resume File ----------------------
        if not allowed_file(file.filename):
            return jsonify({
                "success": False,
                "message": "Invalid resume file type.",
                "errors": {"file": "Allowed formats: PNG, JPG, JPEG, GIF, PDF"}
            }), 400

        # Create unique filename
        original = secure_filename(file.filename)
        ext = os.path.splitext(original)[1]
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_filename = f"resume_{timestamp}{ext}"
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)

        # Save file
        file.save(file_path)

        # ---------------------- CREATE USER ----------------------
        hashed_password = generate_password_hash(user_data["password"])
        new_user = User(
            firstname=user_data["firstname"],
            lastname=user_data["lastname"],
            email=user_data["email"],
            password=hashed_password,
            role="CANDIDATE",
            status="ACTV"
        )
        db.session.add(new_user)
        db.session.commit()

        # ---------------------- CREATE CANDIDATE ----------------------
        new_candidate = Candidate(
            user_id=new_user.user_id,
            education=user_data["education"],
            age=user_data["age"],
            resume_file_path=file_path,
            status="ACTV"
        )
        db.session.add(new_candidate)
        db.session.commit()

        try:
            from app.utils import parse_pdf, extract_skills_from_resume
            GOOGLE_API_KEY = GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
            resume_text = parse_pdf(file_path)
            print(resume_text)
            skills = extract_skills_from_resume(resume_text, GOOGLE_API_KEY)
            print(skills)
            new_candidate.skills = ','.join(skills)
            db.session.commit()
        except Exception as e:
            print(e)

        return jsonify({
            "success": True,
            "message": "Candidate registered successfully.",
            "data": {
                "user_id": new_user.user_id,
                "email": new_user.email,
                "role": new_user.role
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": "Server error occurred.",
            "error": str(e)
        }), 500


@main.route('/api/update-candidate', methods=['POST'])
@token_required
def update_candidate(current_user):
    try:
        # Ensure required payload exists
        if 'user_data' not in request.form:
            return jsonify({"error": "User data is required"}), 400

        user_data = json.loads(request.form['user_data'])
        resume_file = request.files.get('file')

        # Fetch user + candidate
        user = User.query.filter_by(user_id=current_user.user_id, status="ACTV").first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        candidate = Candidate.query.filter_by(user_id=user.user_id).first()
        if not candidate:
            return jsonify({"error": "Candidate not found"}), 404

        # -----------------------------
        # VALIDATION (Fixes your issue)
        # -----------------------------
        required_fields = ["firstname", "lastname", "email", "age", "education"]

        missing = [f for f in required_fields if not user_data.get(f)]

        if missing:
            return jsonify({
                "error": f"Missing required fields: {', '.join(missing)}"
            }), 400

        # -----------------------------
        # UPDATE FIELDS (safe update)
        # -----------------------------
        user.firstname = user_data["firstname"]
        user.lastname = user_data["lastname"]
        user.email = user_data["email"]

        candidate.age = user_data["age"]
        candidate.education = user_data["education"]

        # -----------------------------
        # OPTIONAL RESUME UPDATE
        # -----------------------------
        if resume_file:
            original_filename = secure_filename(resume_file.filename)
            extension = os.path.splitext(original_filename)[1]
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            unique_filename = f"{user.user_id}_{timestamp}{extension}"

            file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
            resume_file.save(file_path)

            candidate.resume_file_path = file_path

        db.session.commit()

        return jsonify({"message": "Candidate updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500




def allowed_file(filename):
    """
    Function to check if the uploaded file type is allowed (example: images, PDFs)
    """
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@main.route('/api/job', methods=['POST'])
@token_required
def create_job_api(current_user):
    try:
        GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
        if not GOOGLE_API_KEY:
            return jsonify({"success": False, "error": "GOOGLE_API_KEY not found"}), 500

        # Only recruiters
        if current_user.role != "RECRUITER":
            return jsonify({"success": False, "message": "Only recruiters can create jobs."}), 403

        data = request.get_json() or {}

        # ------------------ VALIDATION ------------------
        required = ["job_title", "location", "job_type", "description_keywords", "experience", "start_date", "end_date"]
        errors = {f: f"{f.replace('_', ' ').title()} is required." for f in required if not data.get(f)}

        if errors:
            return jsonify({"success": False, "errors": errors}), 422

        experience = data.get("experience", None)

        # Validate experience if provided
        if experience is not None:
            try:
                experience = int(experience)
                if experience < 0:
                    return jsonify({"success": False, "errors": {"experience": "Experience cannot be negative"}}), 400
            except:
                return jsonify({"success": False, "errors": {"experience": "Experience must be a number"}}), 400


        # ------------------ DATE PARSING ------------------
        try:
            start_date = datetime.datetime.strptime(data["start_date"], "%Y-%m-%d").date()
            end_date = datetime.datetime.strptime(data["end_date"], "%Y-%m-%d").date()
        except Exception as e:
            return jsonify({"success": False, "errors": {"date": "Invalid date format"}}), 400

        if end_date < start_date:
            return jsonify({"success": False, "errors": {"date": "End date cannot be earlier than start date"}}), 400

        # ------------------ GEMINI MODEL ------------------
        gemini_llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.7,
            google_api_key=GOOGLE_API_KEY
        )

        prompt = f"""
Return ONLY clean Markdown text. No JSON. No code blocks.

### {data['job_title']} ({data['job_type']})

Write a 2–3 line introduction.

#### 🔹 Key Responsibilities
- 5–7 bullet points

#### 🔹 Required Skills & Qualifications
- 5–7 bullet points
Include these keywords: {data['description_keywords']}

#### 🔹 Preferred / Nice-to-Have Skills
- 2–4 bullet points

#### 🔹 What You Will Gain
- 3–4 bullet points

Formatting rules:
- Markdown only
- Use headings ### and ####
- Bullet points "-", "•"
- No AI mention
"""

        print("\n Sending prompt to Gemini...\n")

        ai_response = gemini_llm.invoke(prompt)

        # ------------------ CLEAN ANY TYPE OF GEMINI OUTPUT ------------------
        def extract_text(content):
            """ Recursively extract pure text from any Gemini output """
            if content is None:
                return ""

            if isinstance(content, str):
                return content

            if isinstance(content, list):
                return "\n".join(extract_text(item) for item in content)

            if isinstance(content, dict):
                parts = []

                if "text" in content:
                    parts.append(content["text"])

                if "value" in content:
                    parts.append(content["value"])

                if "children" in content:
                    parts.append(extract_text(content["children"]))

                for k, v in content.items():
                    if k not in ["text", "value", "children"]:
                        parts.append(extract_text(v))

                return "\n".join([p for p in parts if p])

            return str(content)

        raw_content = ai_response.content

        generated_description = extract_text(raw_content).strip()

        generated_description = str(generated_description) 

        # ------------------ SAVE JOB ------------------
        new_job = Job(
            created_by=current_user.user_id,
            job_title=data["job_title"],
            location=data["location"],
            job_type=data["job_type"],
            description=generated_description,
            start_date=start_date,
            end_date=end_date,
            experience=experience,
            status="ACTV"
        )

        db.session.add(new_job)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Job created successfully!",
            "description": generated_description
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500



@main.route('/api/job/<int:job_id>', methods=['PUT'])
@token_required
def update_job_api(current_user, job_id):
    try:
        if current_user.role != "RECRUITER":
            return jsonify({"success": False, "message": "Invalid recruiter"}), 403

        data = request.get_json() or {}

        # Required fields
        required = ["job_title", "location", "job_type", "description", "experience", "start_date", "end_date"]
        errors = {}

        for field in required:
            if not data.get(field):
                errors[field] = f"{field.replace('_', ' ').title()} is required."

        if errors:
            return jsonify({"success": False, "errors": errors}), 422

        # Fetch job
        job = Job.query.filter_by(job_id=job_id, created_by=current_user.user_id).first()
        if not job:
            return jsonify({"success": False, "message": "Job not found"}), 404

        experience = data.get("experience")
        try:
            experience = int(experience)
            if experience < 0:
                return jsonify({"success": False, "errors": {"experience": "Experience cannot be negative"}}), 400
        except:
            return jsonify({"success": False, "errors": {"experience": "Experience must be a number"}}), 400


        # Convert dates
        try:
            start_date = datetime.datetime.strptime(data["start_date"], "%Y-%m-%d").date()
            end_date = datetime.datetime.strptime(data["end_date"], "%Y-%m-%d").date()

            if end_date < start_date:
                return jsonify({
                    "success": False,
                    "errors": {"date": "End date cannot be earlier than start date"}
                }), 400

        except:
            return jsonify({"success": False, "message": "Invalid date format"}), 400

        # Update job
        job.job_title = data["job_title"]
        job.location = data["location"]
        job.job_type = data["job_type"]
        job.description = normalize_description(data["description"])
        job.experience = experience
        job.start_date = start_date
        job.end_date = end_date

        db.session.commit()

        return jsonify({"success": True, "message": "Job updated successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500


@main.route('/api/job/<int:job_id>', methods=['DELETE'])
@token_required
def delete_job_api(current_user, job_id):
    """
    Delete a job created by the logged-in recruiter.
    Only the owner can delete the job.
    """

    try:
        # Only recruiters allowed
        if current_user.role != "RECRUITER":
            return jsonify({"success": False, "message": "Only recruiters can delete jobs."}), 403

        # Find job created by this recruiter
        job = Job.query.filter_by(job_id=job_id, created_by=current_user.user_id).first()
        if not job:
            return jsonify({"success": False, "message": "Job not found or not owned by you."}), 404

        # Delete job
        db.session.delete(job)
        db.session.commit()

        return jsonify({"success": True, "message": "Job deleted successfully."}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": "Server error", "error": str(e)}), 500



@main.route('/api/candidate-job-request', methods=['POST'])
@token_required
def create_candidate_job_request(current_user):
    data = request.get_json()

    # Validate required fields
    required_fields = [ 'job_id', 'status']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400

    # Validate status
    valid_statuses = ['APPLIED', 'SHORTLISTED', 'INTERVIEWED', 'OFFERED', 'HIRED', 'UNDER_TEST']
    if data['status'] not in valid_statuses:
        return jsonify({"error": "Invalid status"}), 400
    
    # Create new record
    new_request = CandidateJobRequest(
        candidate_id=current_user.user_id,
        job_id=data['job_id'],
        status=data['status'],
    )

    db.session.add(new_request)
    db.session.commit()

    return jsonify({"message": "Candidate job request created successfully", "id": new_request.candidate_job_request_id}), 201



@main.route('/api/candidate-job-requests', methods=['GET'])
@token_required
def get_candidate_job_requests(current_user):
    recruiter_id = current_user.user_id

    # Query with joins
    results = db.session.query(
        CandidateJobRequest.candidate_job_request_id,
        CandidateJobRequest.candidate_id,
        User.firstname,
        User.lastname,
        CandidateJobRequest.job_id,
        Job.job_title,
        CandidateJobRequest.test_score,
        CandidateJobRequest.interview_scheduled_datetime,
        CandidateJobRequest.status,
        CandidateJobRequest.status_change_date
    ).join(Job, CandidateJobRequest.job_id == Job.job_id) \
     .join(Candidate, CandidateJobRequest.candidate_id == Candidate.user_id) \
     .join(User, Candidate.user_id == User.user_id) \
     .filter(Job.created_by == recruiter_id).all()

    # Format response
    data = []
    for r in results:
        data.append({
            "candidate_job_request_id": r.candidate_job_request_id,
            "candidate_id": r.candidate_id,
            "candidate_name": f"{r.firstname} {r.lastname}",
            "job_id": r.job_id,
            "job_title": r.job_title,
            "test_score": r.test_score,
            "interview_scheduled_datetime": r.interview_scheduled_datetime.strftime('%Y-%m-%d %H:%M:%S') if r.interview_scheduled_datetime else None,
            "status": r.status,
            "status_change_date": r.status_change_date.strftime('%Y-%m-%d %H:%M:%S') if r.status_change_date else None
        })

    return jsonify(data), 200


@main.route('/api/candidate-job-request/<int:request_id>', methods=['PUT'])
@token_required
def update_candidate_job_request(current_user, request_id):
    data = request.get_json()

    # Fetch existing record
    candidate_request = CandidateJobRequest.query.get(request_id)
    if not candidate_request:
        return jsonify({"error": "Candidate job request not found"}), 404

    # Validate status if provided
    valid_statuses = ['APPLIED', 'SHORTLISTED', 'INTERVIEWED', 'OFFERED', 'HIRED', 'UNDER_TEST']
    if 'status' in data and data['status'] not in valid_statuses:
        return jsonify({"error": "Invalid status"}), 400

    # Update fields if present
    if 'job_id' in data:
        candidate_request.job_id = data['job_id']
    if 'test_score' in data:
        candidate_request.test_score = data['test_score']
    if 'interview_scheduled_datetime' in data and data['interview_scheduled_datetime']:
        try:
            candidate_request.interview_scheduled_datetime = datetime.datetime.strptime(
                data['interview_scheduled_datetime'], "%Y-%m-%d %H:%M:%S"
            )
        except ValueError:
            return jsonify({"error": "Invalid datetime format. Use YYYY-MM-DD HH:MM:SS"}), 400
    if 'status' in data:
        candidate_request.status = data['status']

    # Always update status_change_date
    candidate_request.status_change_date = datetime.datetime.utcnow()

    db.session.commit()

    return jsonify({
        "message": "Candidate job request updated successfully",
        "id": candidate_request.candidate_job_request_id
    }), 200


def get_conversations(user_id: int, job_id: int):
    """Retrieve the conversation list for a given user and job."""
    convo = Conversation.query.filter_by(user_id=user_id, job_id=job_id).first()
    if convo is None or convo.data is None:
        return []
    
    # Deserialize the conversation
    return pickle.loads(convo.data)


def insert_conversation(job_id: int, user_id: int, messages_list):
    """Insert or update the conversation list for a given user and job."""
    # Serialize the conversation
    serialized = pickle.dumps(messages_list)
    
    # Try to fetch existing conversation
    convo = Conversation.query.filter_by(user_id=user_id, job_id=job_id).first()
    
    if convo:
        # Update existing
        convo.data = serialized
    else:
        # Insert new
        convo = Conversation(job_id=job_id, user_id=user_id, data=serialized)
        db.session.add(convo)
    
    db.session.commit()


#get response from chatbot
#use /api/chatbot/response
def chatbot_response(job_id,user_id,query):
    llm = ChatGoogleGenerativeAI(
        model='gemini-2.5-flash'
    )
    # llm_with_tools = llm.bind_tools()
    messages = get_conversations(user_id,job_id)
    query = "Help the user in queries related to the job post id" + str(job_id) + " do not reveal this job id to the user" + query
    messages.append(HumanMessage(query))
    response = llm.invoke(messages)
    messages.append(response)

    #tools not defined 
    final_response = response
    
    #append final response to messages object
    messages.append(final_response)
    #insert new messages into database
    insert_conversation(11,1,messages)
    return final_response.content[0]['text']


# use /api/chatbot/history/
def get_conversation_history(user_id: int, job_id: int):
    """
    Retrieve conversation history for a given user and job,
    excluding SystemMessage and ToolMessage, and format as JSON.
    """
    messages = get_conversations(user_id, job_id)
    conversation_history = []

    for msg in messages:
        if isinstance(msg, HumanMessage):
            conversation_history.append({
                "role": "human",
                "content": msg.content
            })
        elif isinstance(msg, AIMessage):
            conversation_history.append({
                "role": "ai",
                "content": msg.content
            })
        # SystemMessage and ToolMessage are ignored

    return jsonify(conversation_history)






@main.route('/api/credibility-test/<int:job_id>', methods=['GET'])
@token_required
def send_questions(current_user,job_id):
    candidate = Candidate.query.filter_by(user_id=current_user.user_id).first()
    skills_string = str(candidate.skills)
    if not skills_string:
        return "resume not parsed"
    job_post = Job.query.filter_by(job_id=job_id).first()
    job_description = job_post.description

    llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash')

    query = f"""
    You are generating interview screening questions.

    Use these two inputs:
    - Skills: {skills_string}
    - Job Description: {job_description}

    Generate EXACTLY 10 multiple-choice interview questions:
    - The FIRST 5 MCQs MUST come ONLY from the candidate skills.
    - The NEXT 5 MCQs MUST come ONLY from the job description.
    - EACH question must have:
        - EXACTLY 4 options labeled "A", "B", "C", "D".
        - EXACTLY ONE correct option.
        - A field "correct_option" containing ONLY the letter of the correct answer (A/B/C/D).

    Return the output STRICTLY in this JSON format:

    {{
        "questions": [
            {{
                "question": "<question text>",
                "options": {{
                    "A": "<option text>",
                    "B": "<option text>",
                    "C": "<option text>",
                    "D": "<option text>"
                }},
                "correct_option": "<A/B/C/D>"
            }},
            ...
            (10 items total)
        ]
    }}

    NO additional text.
    NO markdown.
    ONLY valid JSON.
"""


    response = llm.invoke(query)

    # Gemini content is inside:
    model_json = response.content

    import json
    questions_json = json.loads(model_json)

    questions_json["job_id"] = job_id

    return jsonify(questions_json)



@main.route('/api/credibility-test/<int:job_id>', methods=['POST'])
@token_required
def submit_test(current_user, job_id):
    data = request.get_json()

    if not data or "score" not in data:
        return jsonify({"error": "score is required"}), 400

    score = data.get("score")

    # Find candidate-job relation
    cjr = CandidateJobRequest.query.filter_by(
        candidate_id=current_user.user_id,
        job_id=job_id
    ).first()

    if not cjr:
        return jsonify({"error": "candidate-job relation not found"}), 404

    # Update the test score
    cjr.test_score = score
    cjr.status_change_date = datetime.utcnow()

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "database error", "details": str(e)}), 500

    return jsonify({
        "message": "test score submitted successfully",
        "job_id": job_id,
        "candidate_id": current_user.user_id,
        "score": score
    }), 200
