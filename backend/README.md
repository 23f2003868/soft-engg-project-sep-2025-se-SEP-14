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
│   └── api.py
│
├── config.py
├── celery_worker.py
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

### 4. Add Environment Variables  
Create a `.env` file:

```bash
GOOGLE_API_KEY=your_key
```

### 5. Initialize Database
```bash
>>> flask db init
>>> flask db migrate -m "initial db"
>>> flask db upgrade
```

### 6. Run Backend
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
|--------|----------|-------------|
| POST | `/api/register-candidate` | Register |
| POST | `/api/update-candidate` | Update profile |
| GET | `/api/candidate-job-requests` | Get job applications |

### 🧑‍💼 Recruiter
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/register-recruiter` | Register |
| POST | `/api/update-recruiter` | Update profile |
| GET | `/api/jobs` | Get jobs created |
| POST | `/api/job` | Create job |
| PUT | `/api/job/<id>` | Update job |
| DELETE | `/api/job/<id>` | Delete job |

### 🤖 Chatbot
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/chatbot/response` | Get chatbot reply |
| GET | `/api/chatbot/history` | Fetch history |

---

## 📌 Notes

- Backend validates **required fields** to prevent technical errors.
- Resume upload supports **pdf**.
- Candidate resume path updates correctly with timestamp.
- All API responses are SweetAlert-friendly.

---

## ✔ Final Notes
This backend is production-ready with strong validation, structured routing, and perfect Vue integration.