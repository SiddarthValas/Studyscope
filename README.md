
# StudyScope

## AI-Powered Study Companion for Modern Learners

⸻

Overview

StudyScope is an intelligent, student-first productivity platform that empowers learners to take charge of their studies with precision, focus, and balance. Built with a blend of AI, natural language processing, and intuitive design, it supports document-based question answering, stress monitoring, and streamlined task management—all in one app.

⸻

Features

1. Document-Based Q&A

Upload PDFs (textbooks, notes, articles) and ask natural language questions. The system searches for answers directly from the document content, falling back to GPT when necessary.

2. Burnout Analyzer

Includes a simple yet insightful burnout check-in that gauges user well-being and provides instant feedback to avoid academic fatigue.

3. Smart To-Do List

A persistent, session-based task list tailored for daily academic tracking. Stay organized and never miss a deadline.

4. Subject-wise Question History

Categorizes and stores all questions by subject so students can track what they’ve asked, learned, and explored—organized, searchable, and reviewable.

5. Secure Authentication

Includes user-based login using streamlit-authenticator, with pre-defined accounts and a guest mode:
	•	Users: sidd, rashi, guest
	•	Session-managed with persistent state per user

⸻

Tech Stack

Layer	Technology
Interface	Streamlit
Styling	Custom CSS (style.css)
Authentication	streamlit-authenticator
PDF Parsing	PyMuPDF
Vector Search	FAISS
NLP Fallback	OpenAI GPT
Document Handling	fitz, langchain, tiktoken


⸻

How It Works
	1.	Upload a PDF document.
	2.	Ask a question in natural language.
	3.	The app first checks your document using semantic similarity.
	4.	If no relevant match is found, it falls back to GPT.
	5.	Tracks all questions by subject.
	6.	Analyze burnout with a form-based survey.
	7.	Use the built-in to-do list to manage tasks.

⸻

Installation Guide
	1.	Clone the Repository

git clone https://github.com/your-username/studyscope.git
cd studyscope


	2.	Set Up Virtual Environment

python -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate


	3.	Install Dependencies

pip install -r requirements.txt


	4.	Run the App

streamlit run app.py



⸻

Folder Structure

studyscope/
├── app.py                         # Main app logic
├── style.css                      # Custom dark-mode theme
├── backend/
│   ├── pdf_utils.py               # PDF upload & chunking
│   ├── qa_utils.py                # Question answering logic
│   └── auth_config.py             # Authenticator config
├── data/
│   └── sample_pdfs/               # Demo PDFs
├── requirements.txt
└── README.md


⸻

Deployment Notes
	•	App runs locally via streamlit run app.py
	•	Easily deployable to Streamlit Cloud
	•	Add OPENAI_API_KEY to .streamlit/secrets.toml or environment variables
	•	Recommended: GitHub repo should include sample PDFs and config files

⸻

Project Vision

“StudyScope is designed for the modern student — curious, busy, and ambitious. By blending AI with real academic needs, it aims to reduce friction in studying and bring clarity, calm, and focus to the learning journey.”

⸻

Authors

Siddarth Valasubramanian
Built in collaboration with Rashi


⸻
