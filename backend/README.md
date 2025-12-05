# Backend Overview
This backend is built using **Flask**, featuring authentication, role-based access, job creation, candidate & recruiter profiles, resume uploads, smart job descriptions (via Gemini API), and chatbot conversation storage.

---

## 🛠️ Tech Stack

| Technology | Purpose |
|----------|---------|
| **Python** | Core programming language |
| **Flask** | Backend web framework |
| **Flask-Login** | Authentication and session management |
| **JWT (PyJWT)** | Token-based authentication |
| **SQLite / MySQL** | Database support |
| **SQLAlchemy ORM** | Database modeling |
| **Werkzeug** | Security, password hashing |
| **Google Gemini API** | AI-based job description generator |
| **SweetAlert2 Compatible Responses** | For clean frontend alerts |
| **Redis (Optional)** | Caching system |

---

## 📁 Project Structure (Backend)

```
backend/
│
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── forms.py
│   ├── tasks.py
│   ├── utils.py
│   └── celery_app.py
│
├── config.py
├── requirements.txt
├── Team 14_APIs_YAMLfile.yaml
├── README.md
└── run.py
```

---

## 🔑 Features

### ✔ User Authentication  
- JWT login  
- Password hashing  
- Role-based access (Candidate, Recruiter)

### ✔ Candidate Module  
- Registration with resume upload  
- Profile update  
- Validation for age, resume, email  
- Resume file-path stored dynamically  
- Candidate job requests (apply, track status)

### ✔ Recruiter Module  
- Create & manage jobs  
- Gemini-powered job descriptions  
- Update recruiter profile  
- LinkedIn URL validation (backend enforced)

### ✔ Job Management  
- Add, update, list jobs  
- Clean Markdown descriptions  
- Normalization for AI-generated content

### ✔ Chatbot for Job Queries  
- History stored in DB using BLOB  
- Per-user + per-job conversation context  
- Gemini API responses

---

## ⚙️ Installation & Setup

### 1. Clone the repo
```bash
git clone https://github.com/21f1001963/soft-engg-project-sep-2025-se-SEP-14.git
```

### 2. Create and activate virtual environment
```bash
cd backend
python -m venv venv
venv/Scripts/activate   (Windows)
source venv/bin/activate (Linux/Mac)
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```
### 4. Google OAuth & Calendar Setup for Beginners 📅

The application supports interview scheduling and Google Meet link creation, requiring a Recruiter to authorize access to their Google Calendar via **OAuth 2.0**.

1.  Go to the **Google Cloud Console**.
2.  **Create a new project**.
3.  Navigate to **APIs & Services** > **Enabled APIs & Services**.
4.  Click **+ ENABLE APIS AND SERVICES** and enable the **Google Calendar API**.
5.  Go to **APIs & Services** > **OAuth consent screen**.
    * Set the **User Type** to **External** and proceed.
    * Add the required **scope**: `.../auth/calendar.events`.
    * For testing, add your own email as a **Test User**.
6.  Go to **APIs & Services** > **Credentials**.
    * Click **+ CREATE CREDENTIALS** and select **OAuth client ID**.
    * **Application type**: Select **Web application**.
    * **Name**: Choose a name (e.g., `Flask-Recruiter-App`).
    * **Authorized JavaScript origins**: Add `http://localhost:5173` (your Frontend URL).
    * **Authorized redirect URIs**: Add your full backend redirect endpoint: `http://127.0.0.1:5000/api/google-oauth-callback`.
7.  Click **CREATE** and note down the **Client ID** and **Client Secret**.

### 5. Add Environment Variables  
Create a `.env` file:

```bash
GOOGLE_API_KEY=your_key
GOOGLE_CLIENT_ID=your_client_id
GOOGLE_CLIENT_SECRET=your_client_secret
GOOGLE_REDIRECT_URI=http://localhost:5000/api/google-oauth-callback
```

### 6. Initialize Database
```bash
flask db init
flask db migrate -m "initial db"
flask db upgrade
```

### 7. Run Backend
```bash
python run.py
```

Server runs at:
```bash
http://127.0.0.1:5000
```

---

## 🧪 API Endpoints Overview

### 🔐 Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/login` | Login (JWT) |
| POST | `/api/logout` | Logout |

### 👤 Candidate
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| **POST** | `/api/register-candidate` | Register (Requires form data + resume upload) |
| **POST** | `/api/update-candidate` | Update profile (optional new resume upload) |
| **GET** | `/api/applied-jobs` | Get all applied jobs and status for the candidate |
| **POST** | `/api/save-job` | Save a job to the candidate's list |
| **DELETE** | `/api/save-job/<int:job_id>` | Remove a job from saved list |
| **GET** | `/api/saved-jobs-details` | Get the details of all saved jobs |
| **GET** | `/api/resume-status` | Get asynchronous resume parsing status (PENDING/SUCCESS/FAILED) |
| **POST** | `/api/resume-retry` | Restart resume parsing task |
| **POST** | `/api/job-apply` | Apply for a job (requires test score in DB) |

### 🧑‍💼 Recruiter
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| **POST** | `/api/register-recruiter` | Register a new recruiter |
| **POST** | `/api/update-recruiter` | Update recruiter profile |
| **GET** | `/api/jobs-all` | Get all active jobs (for public/candidate listings) |
| **GET** | `/api/jobs` | Get jobs created **by the current recruiter** |
| **POST** | `/api/job` | Create new job (can auto-generate description via Gemini) |
| **PUT** | `/api/job/<int:job_id>` | Update job details |
| **DELETE** | `/api/job/<int:job_id>` | Delete job |
| **GET** | `/api/recruiter/jobs` | Get recruiter's jobs with applicant statistics |
| **GET** | `/api/recruiter/stats` | Get recruiter's overall dashboard statistics |
| **GET** | `/api/recruiter/applications-paged` | Get paginated application list for a specific `job_id` |
| **GET** | `/api/candidate-job-requests` | Get all applications for all jobs created by the recruiter (legacy/flat) |
| **PUT** | `/api/candidate-job-request/<int:request_id>` | Update application status (e.g., to SHORTLISTED) or set interview time |
| **POST** | `/api/schedule-interview/<int:cjr_id>` | Schedules interview, creates Google Meet link, and updates status to `INTERVIEW_SCHEDULED` |

### 🤖 AI (Chatbot & Test)
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| **POST** | `/api/chatbot/response` | Get a chatbot reply based on job context (powered by Gemini) |
| **GET** | `/api/chatbot/history/<int:job_id>` | Fetch conversation history for a job |
| **POST** | `/api/chatbot/clear` | Clear conversation history |
| **GET** | `/api/credibility-test/<int:job_id>` | Generate and retrieve the 10-question credibility test (MCQ) |
| **POST** | `/api/credibility-test/<int:job_id>` | Submit test score. Automatically updates application status to **APPLIED**. |

### 📅 Google Calendar (Interview Scheduling Helpers)
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| **GET** | `/api/google-oauth-url` | Get URL to start the Google Calendar authorization process |
| **GET** | `/api/google-oauth-callback` | Google redirect endpoint (handles code exchange with frontend script) |
| **POST** | `/api/google-exchange-code` | Exchange OAuth code for tokens and save them to the Recruiter's profile |
| **GET** | `/api/google-status` | Check if the Recruiter's Google account is connected |
| **POST** | `/api/google-create-event` | Low-level endpoint to manually create an event using a token |

---

## 📌 Notes

- Backend validates **required fields** to prevent technical errors.
- Resume upload supports **pdf**.
- Candidate resume path updates correctly with timestamp.
- All API responses are SweetAlert-friendly.

---

## ✔ Final Notes
This backend is production-ready with strong validation, structured routing, and perfect Vue integration.