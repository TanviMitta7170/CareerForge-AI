# CareerForge AI – Intelligent Career Pathing & Viral Content Generator

CareerForge AI is a full-stack AI-driven career coaching assistant built using **Streamlit**, **Python**, and **Google Gemini (Flash)** for intelligent skill gap analysis and automated portfolio building. It automates the most confusing phase of a student's journey: moving from "learning syntax" to "building market-ready projects."

CareerForge analyzes raw resumes, identifies critical skill gaps based on target roles (e.g., SDE, AI Engineer), assigns specific micro-projects, and generates high-engagement LinkedIn content to validate the learning. The system utilizes a multi-agent architecture to ensure students don't just learn, but effectively showcase their growth.

## Key Features
* **AI-Powered Resume Scanning:** Agent 1 (The Scanner) detects conceptual gaps against real-world market trends.
* **Micro-Project Assignment:** Agent 2 (The Mentor) generates weekend-sized, portfolio-ready project tasks.
* **Viral Content Generation:** Agent 3 (The Publisher) uses the STAR method to write high-engagement LinkedIn posts.
* **Multi-Agent Architecture:** Sequential logic flow (Scanner → Mentor → Publisher).
* **Streamlit "Cyberpunk" UI:** A professional, dark-themed dashboard for focused interaction.
* **Resilient API Handling:** Built on `gemini-flash-latest` to avoid quota limits and ensure speed.
* **Session State Management:** Persists user progress across the coaching lifecycle.

## System Story
Modern computer science students face a "Tutorial Hell" problem: they know the basics but lack the specific, applied skills recruiters look for (e.g., Caching, API Gateways, JWT).

CareerForge automates the mentorship process:
1. **Normalizes** the student's current skill set.
2. **Identifies** the gap between their resume and their target role (e.g., Full-Stack Developer).
3. **Assigns** a concrete coding task to bridge that gap.
4. **Articulates** the achievement professionally for social proof.

This reduces the time spent "wondering what to build" and ensures every line of code contributes to employability.

## Architecture Overview

### Frontend & Logic (Streamlit)
* **Single Page Application (SPA):** Runs via `app.py`.
* **State Management:** Uses `st.session_state` to handle the transition between Agents.
* **UI/UX:** Custom CSS injection for the Cyberpunk aesthetic.

### Python Agent System
* **Agent 1 (The Scanner):** inputs(Resume + Role) → outputs(3 Market Gaps).
* **Agent 2 (The Mentor):** inputs(Selected Gap) → outputs(Micro-Project Specification).
* **Agent 3 (The Publisher):** inputs(Project Evidence) → outputs(Viral LinkedIn Post).

### Gemini Intelligence
* **Model:** `gemini-flash-latest` (Optimized for speed and higher rate limits).
* **Prompt Engineering:** Role-based prompting (Recruiter Persona, Engineering Manager Persona, Copywriter Persona).

## Workflow Overview
1. **Student** → Pastes Resume & Selects Target Role.
2. **Agent 1** → Scans & Identifies 3 critical gaps (e.g., "Redis Caching").
3. **Student** → Selects one gap to tackle.
4. **Agent 2** → Generates a specific project idea (e.g., "Build a Rate Limiter").
5. **Student** → Builds the project & pastes the summary/code.
6. **Agent 3** → Verifies evidence & writes a LinkedIn post.
7. **System** → Ready for the next module.

## Installation & Setup

### Prerequisites
* Python 3.10+
* A Google AI Studio API Key

### 1. Repository Setup
```bash
# Clone Repository
git clone [https://github.com/your-username/CareerForge-AI.git](https://github.com/your-username/CareerForge-AI.git)
cd CareerForge-AI

# Create Virtual Environment (Optional but recommended)
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 2. Dependency Installation
```bash
pip install -r requirements.txt
```
*Note: Ensure `google-generativeai` and `streamlit` are in your requirements file.*

### 3. Running the Application
```bash
streamlit run app.py
```
The application will launch automatically at `http://localhost:8501`.

### 4. Authentication
Once the UI loads, enter your **Google API Key** in the sidebar to activate the Agents.

## Folder Structure
```text
CareerForge-AI/
│
├── app.py                # Main application entry point & Agent logic
├── requirements.txt      # Python dependencies
├── README.md             # Documentation
└── .gitignore            # Git configuration
```

## Observability & Logging
* **UI Feedback:** The application uses Streamlit spinners and success boxes to indicate Agent status.
* **Error Handling:** Try/Except blocks around API calls catch `404` (Model not found) or `429` (Quota exceeded) errors and display user-friendly messages.

## Troubleshooting
**"Model not found" or 404 Error:**
* Ensure your `app.py` is using `gemini-flash-latest` or `gemini-1.5-flash` depending on your region.
* Check if your API key is valid in Google AI Studio.

**"Quota Exceeded" or 429 Error:**
* You are hitting the free tier rate limit. Wait 60 seconds and try again.
* We switched to `gemini-flash-latest` to minimize this issue.

## Future Enhancements
We are actively working on Version 12 with the following features:

* **Immediate Module Transition:** Logic to seamlessly trigger the next recommended gap analysis immediately after a project is verified, creating an infinite learning loop.
* **Auto-Resume Updater:** The system will parse the original resume and automatically append the newly completed project/skill to the "Experience" section.
* **ATS-Optimized Resume Generator:** A new feature to export the updated resume as a PDF that passes Applicant Tracking System (ATS) filters with a high score.
* **Gamification:** Adding XP and "Badges" for every gap filled to encourage streak retention.
* **GitHub Integration:** Automatically push the user's micro-project code to a new GitHub repository from within the app.
