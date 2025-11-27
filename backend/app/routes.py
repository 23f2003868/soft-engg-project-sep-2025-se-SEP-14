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
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    try:
        user = User.query.filter_by(email=email, status="ACTV").first()

        if user and check_password_hash(user.password, password):

            token = generate_jwt_token(user)

            return jsonify({
                "success": True,
                "message": "Login successful!",
                "token": token,
                "expires_in_minutes": 30
            }), 200

        return jsonify({
            "success": False,
            "message": "Invalid email or password."
        }), 401

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"An error occurred: {str(e)}"
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
    user_data = {
            "id": str(current_user.user_id),
            "email": current_user.email,
            "role": current_user.role,
            "firstname": current_user.firstname,
            "lastname": current_user.lastname,
            "status": current_user.status
        }
    email = current_user.email

    try:
        user = User.query.filter_by(email=email, status="ACTV").first()
        if user:
            # Serialize the user object manually
            candidate_data={}
            recruiter_data={}
            if user.role=="CANDIDATE":
                candidate_data = {
                    'candidate_id': str(user.candidate.candidate_id),
                    'age':str(user.candidate.age),
                    'education':str(user.candidate.education),
                    'resume_file_path':str(user.candidate.resume_file_path),
                    }
            if user.role=="RECRUITER":
                recruiter_data = {
                    'recruiter_id': str(user.recruiter.recruiter_id),
                    'company':user.recruiter.company,
                    'position':user.recruiter.position,
                    'linkdin_profile_path':user.recruiter.linkdin_profile_path,
                    }
            user_data = {
                "id":  str(user.user_id),
                "email": user.email,
                "role": user.role,
                'firstname':user.firstname,
                'lastname':user.lastname,
                "status": user.status,
                "candidate":candidate_data,
                "recruiter":recruiter_data

            }
            return jsonify({
                "success": True,
                "message": "Login successful!",
                "user": user_data
            }), 200
        else:
            return jsonify({
                "success": False,
                "message": "Invalid email or password."
            }), 401
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

@main.route('/api/register-recruiter', methods=['POST'])
def register_recruiter():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No input data provided"}), 400

        # Validate required fields
        required_fields = [
            'firstname', 'lastname', 'email', 'password', 'company',
            'position', 'linkdin_profile_path'
        ]
        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"Missing field: {field}"}), 400

        # Prepare user and recruiter data
        hashed_password = generate_password_hash(data['password'])
        new_user=User(
                firstname=data['firstname'],
                lastname=data['lastname'],
                email=data['email'],
                password=hashed_password,
                role='RECRUITER',
                status='ACTV'
        )
        db.session.add(new_user)
        db.session.commit()

        new_recruiter = Recruiter(
            company = data['company'],
            user_id=new_user.user_id,
            position =data['position'],
            linkdin_profile_path=data['linkdin_profile_path'],
            status = 'ACTV'
        )
        

        db.session.add(new_recruiter)
        db.session.commit()
        return jsonify({"message": "Recruiter register Successfully."}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main.route('/api/update-recruiter', methods=['POST'])
@token_required
def update_recruiter(current_user):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No input data provided"}), 400

        # Retrieve the user using the email (as email is unique)
        email = current_user.email
        user = User.query.filter_by(email=email, status="ACTV").first()
        
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Update customer details (excluding password)
        user.firstname = data.get('firstname', user.firstname)
        user.lastname = data.get('lastname', user.lastname)
        user.email = data.get('email', user.email)
        recruiter = Recruiter.query.filter_by(user_id=user.user_id).first()
        if not recruiter:
            return jsonify({"error": "Recruiter not found"}), 404
        recruiter.company = data['company']
        recruiter.position = data['position']
        recruiter.linkdin_profile_path=data['position']

        db.session.commit()

        return jsonify({"message": "Recruiter details updated successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main.route('/api/jobs', methods=['GET'])
@token_required
def get_jobs(current_user):
    try:
        if current_user.role=="RECRUITER":
            jobs_data = Job.query.filter(
                Job.status == 'ACTV',
                Job.created_by == current_user.user_id
            ).all()

            jobs = []
            for job in jobs_data:
                jobs.append({
                    "job_id": job.job_id,
                    "job_title": job.job_title,
                    "location": job.location,
                    "job_type": job.job_type,
                    "description": job.description,
                    "status": job.status
                })

            return jsonify({
                "count": len(jobs),
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
        # redis_client.delete('all_professionals')
        if 'file' not in request.files or 'user_data' not in request.form:
            return jsonify({"error": "Missing file or user data"}), 400

        user_data = json.loads(request.form['user_data'])
        file = request.files['file']

        if not allowed_file(file.filename):
            return jsonify({"error": "Invalid file type"}), 400

        # Generate a unique filename
        original_filename = secure_filename(file.filename)
        extension = os.path.splitext(original_filename)[1]
        current_date = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_filename = f"{os.path.splitext(original_filename)[0]}_{current_date}{extension}"
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)

        # Save the file to the specified folder
        file.save(file_path)
        hashed_password = generate_password_hash(user_data['password'])
        # Create User record
        user = User(
            firstname=user_data['firstname'],
            lastname=user_data['lastname'],
            email=user_data['email'],
            password=hashed_password,
            role="CANDIDATE",
            status="ACTV"
        )
        db.session.add(user)
        db.session.commit()
        # Create Service Professional record
        candidate = Candidate(
            user_id=user.user_id,
            education=user_data['education'],
            age=user_data['age'],
            resume_file_path=file_path,  # Save the full path
            status="ACTV",
        )
        db.session.add(candidate)
        db.session.commit()

        return jsonify({"message": "Candidate Register Successfully!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main.route('/api/update-candidate', methods=['POST'])
@token_required
def update_candidate(current_user):
    try:
        data = request.get_json()

        email = current_user.email
        if not email:
            return jsonify({"error": "Email is required"}), 400

        user = User.query.filter_by(email=email, status="ACTV").first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Update user fields
        user.firstname = data.get('firstname', user.firstname)
        user.lastname = data.get('lastname', user.lastname)
        user.email = data.get('email', user.email)

        candidate = Candidate.query.filter_by(user_id=user.user_id).first()
        if not candidate:
            return jsonify({"error": "Candidate not found"}), 404

        candidate.education = data.get('education', candidate.education)
        candidate.age = data.get('age', candidate.age)

        db.session.commit()

        return jsonify({"message": "Candidate information updated successfully!"}), 200

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
        google_api_key = os.getenv("GOOGLE_API_KEY")

        gemini_llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.7,
            google_api_key=google_api_key  # Add this
        )

        data = request.get_json()
        if current_user.role=="RECRUITER":
            # Input validation
            errors = {}
            if not data.get('job_title'):
                errors['job_title'] = 'Job title is required.'
            if not data.get('location'):
                errors['location'] = 'Job Location is required.'
            if not data.get('job_type'):
                errors['job_type'] = 'Job Type is required.'
            if not data.get('description_keywords'):
                errors['description_keywords'] = 'Description keywords are required.'

            if errors:
                return jsonify({'errors': errors}), 400

            # Check if job already exists
            if Job.query.filter(and_(Job.job_title == data['job_title'], Job.created_by == current_user.user_id)).first():
                return jsonify({'errors': {'job_title': 'A job with this title already exists.'}}), 400

            job_title = data['job_title']
            job_type = data['job_type']
            keywords = data['description_keywords']

            # -------------------------------
            # GEMINI + LANGCHAIN
            # -------------------------------
            prompt = f"""
            Write a professional job description of around 100 words.
            Details:
            - Job Title: {job_title}
            - Job Type: {job_type}
            - Important Keywords: {keywords}

            Create a clear, attractive, and structured job description suitable for a hiring portal. just give job description which i directly use to store as my description.
            """

            ai_response = gemini_llm.invoke(prompt)
            generated_description = ai_response.content.strip()

            # -------------------------------
            # Save Job
            # -------------------------------
            job = Job(
                created_by=current_user.user_id,
                job_title=job_title,
                location=data['location'],
                job_type=job_type,
                description=generated_description
            )

            db.session.add(job)
            db.session.commit()

            return jsonify({
                'message': 'Job created successfully!',
                'generated_description': generated_description
            }), 201
        else:
            return jsonify({
                'message': 'Invalid Requiter!',
            }), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/job/<int:job_id>', methods=['PUT'])
@token_required
def update_job_api(current_user, job_id):
    try:
        google_api_key = os.getenv("GOOGLE_API_KEY")

        gemini_llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.7,
            google_api_key=google_api_key  # Add this
        )
        data = request.get_json()
        if current_user.role=="RECRUITER":
            # Fetch job by ID
            job = Job.query.get(job_id)
            if not job:
                return jsonify({'error': 'Job not found'}), 404

            # Input validation
            errors = {}
            if not data.get('job_title'):
                errors['job_title'] = 'Job title is required.'
            if not data.get('location'):
                errors['location'] = 'Job location is required.'
            if not data.get('job_type'):
                errors['job_type'] = 'Job type is required.'
            if not data.get('description_keywords'):
                errors['description_keywords'] = 'Description is required.'

            if errors:
                return jsonify({'errors': errors}), 400

            # Check for duplicate job title (excluding this job)
            existing_job = Job.query.filter(
                Job.job_title == data['job_title'],
                Job.job_id != job_id,
                Job.created_by==current_user.user_id
            ).first()

            if existing_job:
                return jsonify({'errors': {'job_title': 'A job with this title already exists.'}}), 400


            job_title = data['job_title']
            job_type = data['job_type']
            keywords = data['description_keywords']

            # -------------------------------
            # GEMINI + LANGCHAIN
            # -------------------------------
            prompt = f"""
            Write a professional job description of around 100 words.
            Details:
            - Job Title: {job_title}
            - Job Type: {job_type}
            - Important Keywords: {keywords}

            Create a clear, attractive, and structured job description suitable for a hiring portal. just give job description which i directly use to store as my description.
            """

            ai_response = gemini_llm.invoke(prompt)
            generated_description = ai_response.content.strip()
            # Update job details
            job.created_by = current_user.user_id
            job.job_title = data['job_title']
            job.location = data['location']
            job.job_type = data['job_type']
            job.description = generated_description

            db.session.commit()

            return jsonify({'message': 'Job updated successfully!'}), 200
        else:
            return jsonify({
                'message': 'Invalid Requiter!',
            }), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


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
