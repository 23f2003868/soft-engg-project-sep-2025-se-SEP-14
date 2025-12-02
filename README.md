# Job Portal Application (ApplAI)  — Full Stack

This is a job portal application that supports complete user flows for Candidates, Recruiters, and Hiring Managers. The system includes a Vue-based frontend and a Flask-based backend, both working together as a complete full-stack solution.

---

## 🛠️ Tech Stack

### Frontend
| Technology     | Purpose                                  |
| -------------- | ---------------------------------------- |
| **Vue 3**      | Main frontend framework                  |
| **Vue Router** | Handles page navigation                  |
| **Vuex**       | Global state management                  |
| **Vite**       | Project scaffolding & development server |



### Backend
| Technology            | Purpose                      |
| --------------------- | ---------------------------- |
| **Flask**             | Backend framework            |
| **SQLAlchemy**        | ORM for database operations  |
| **JWT**               | Token-based auth for APIs    |
| **Flask-Login**       | Authentication handler       |
| **Werkzeug**          | Security + file uploads      |
| **Google Gemini API** | AI job description generator |
| **Redis (optional)**  | Caching layer                |


---

## 🧭 Frontend Routes Overview

The project uses **Vue Router** for client-side navigation.  
Below is a complete list of routes and their corresponding components.

| **Path**             | **Route Name**          | **Component**               | **Description**          |
| -------------------- | ----------------------- | --------------------------- | ------------------------ |
| `/`                  | `home`                  | `HomeView.vue`              | Landing page             |
| `/login`             | `login`                 | `LogIn.vue`                 | Login page               |
| `/signup`            | `signup`                | `SignUp.vue`                | Register new user        |
| `/about`             | `about`                 | `About.vue`                 | About the platform       |
| `/contact`           | `contact`               | `Contact.vue`               | Contact & support        |
| `/jobs`              | `job`                   | `JobListing.vue`            | All job listings         |
| `/recruiter`         | `recruiter-dashboard`   | `RecruiterDashboard.vue`    | Main recruiter dashboard |
| `/recruiter/profile` | `recruiter-profile`     | `RecruiterProfile.vue`      | Update recruiter details |
| `/recruiter/tracker` | `SmartCandidateTracker` | `SmartCandidateTracker.vue` | Applicant tracking       |
| `/candidate`         | `candidate-dashboard`   | `CandidateDashboard.vue`    | Candidate dashboard      |
| `/candidate/profile` | `candidate-profile`     | `CandidateProfile.vue`      | Update candidate details |

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

## 📁 Project Structure (Frontend)

```
frontend/
├── public/
│   └── images/
│       └── team/
│           ├── Anushka.jpg
│           ├── Deval.jpg
│           ├── Mangesh.jpg
│           ├── Prasoon.jpg
│           ├── Praul.jpg
│           ├── Shyaam.jpg
│           ├── Suvrat.jpg
│           └── Tripurari.jpg
│
├── src/
│   ├── assets/
│   ├── components/
│   │   ├── CandidateNavbar.vue
│   │   ├── ChatBot.vue
│   │   ├── Footer.vue
│   │   ├── JobManagement.vue
│   │   ├── Navbar.vue
│   │   └── RecruiterNavbar.vue
│   │
│   ├── router/
│   │   └── index.js
│   │
│   ├── views/
│   │   ├── About.vue
│   │   ├── CandidateDashboard.vue
│   │   ├── CandidateProfile.vue
│   │   ├── Contact.vue
│   │   ├── HomeView.vue
│   │   ├── JobListing.vue
│   │   ├── LogIn.vue
│   │   ├── RecruiterDashboard.vue
│   │   ├── RecruiterProfile.vue
│   │   ├── SignUp.vue
│   │   └── SmartCandidateTracker.vue
│   │
│   ├── App.vue
│   └── main.js
│
├── index.html
├── jsconfig.json
├── package.json
├── package-lock.json
├── vite.config.js
├── .gitignore
└── README.md
```

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

## 🚀 Getting Started

Follow these steps to set up and run the project locally.

### 1. Clone the Repository
```bash
git clone https://github.com/21f1001963/soft-engg-project-sep-2025-se-SEP-14.git
```

### 2. Navigate to the Frontend Directory

```bash
cd frontend
```

### 3. Install Dependencies

```bash
npm install
```

### 4. Run Frontend
```bash
npm run dev
```

### 5. Create and activate virtual environment
```bash
cd backend
python -m venv venv
venv\Scripts\Activate  (Windows)
source venv/bin/activate (Linux/Mac)
```

### 6. Install dependencies
```bash
pip install -r requirements.txt
```

### 7. Add Environment Variables  
Create a `.env` file:

```bash
GOOGLE_API_KEY=your_key
```

### 8. Initialize Database
```bash
flask db init
flask db migrate -m "initial db"
flask db upgrade
```

### 9. Run Backend
```bash
python run.py
```

### 10. Run Celery Server
```bash
celery -A app.celery_app.celery worker --loglevel=info --pool=solo
```

Server runs at:
```bash
http://localhost:5173/  (Frontend)
http://127.0.0.1:5000   (Backend)
```



