# Project Description

This is a job portal application that supports full user flows for Candidates, Recruiters, and Hiring Managers.

---

## 🛠️ Tech Stack

| Technology | Purpose |
| :--- | :--- |
| **Vue 3** | Core JavaScript Framework (Composition API) |
| **Vue Router** | Client-Side Routing for page navigation |
| **Vuex** | State Management (for global data) |
| **Vite** | Project Scaffolding and Build Tool |

---

## 🧭 Frontend Routes Overview

The project uses **Vue Router** for client-side navigation.  
Below is a complete list of routes and their corresponding components.

| **Path** | **Route Name** | **Component** | **Description** |
|-----------|----------------|----------------|------------------|
| `/` | `home` | `HomeView.vue` | Landing page of the application |
| `/login` | `login` | `LogIn.vue` | Login page for existing users |
| `/signup` | `signup` | `SignUp.vue` | Registration page for new users |
| `/about` | `about` | `About.vue` | Information about the platform |
| `/contact` | `contact` | `Contact.vue` | Contact page for help and support |
| `/jobs` | `job` | `JobListing.vue` | Displays all job listings |
| `/recruiter` | `recruiter-dashboard` | `RecruiterDashboard.vue` | Main dashboard for recruiters |
| `/recruiter/profile` | `recruiter-profile` | `RecruiterProfile.vue` | Manage recruiter profile information |
| `/recruiter/tracker` | `SmartCandidateTracker` | `SmartCandidateTracker.vue` | Smart tracking system |
| `/candidate` | `candidate-dashboard` | `CandidateDashboard.vue` | Dashboard for candidates |
| `/candidate/profile` | `candidate-profile` | `CandidateProfile.vue` | Candidate profile management page |

---

## 📁 Project Structure

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
│   │   ├── RecruiterNavbar.vue
│   │   └── RecruiterStatsCard.vue
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

## 📁 Key Folders

The application is structured for scalability:

* **`src/views/`**: Contains full-page components (e.g., LogIn, Dashboard).
* **`src/components/`**: Contains small, reusable UI elements (e.g., Button, Navbar).
* **`src/router/`**: Defines all application routes (URLs).
* **`src/assets/`**: Holds global styles, images, and fonts.

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

### 4. Run the Development Server
```bash
npm run dev
```

The application will now be running on `http://localhost:5173/`