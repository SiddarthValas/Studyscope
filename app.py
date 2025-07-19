import json
import streamlit as st
import os
import pickle
import time
from backend.search_engine import get_answer_from_notes
from backend.pdf_utils import upload_and_process_pdf
from backend.quiz_generator import generate_quiz_from_notes
from backend.gpt_helper import get_gpt_response

def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.set_page_config(page_title="StudyScope", page_icon="🔮", layout="wide", initial_sidebar_state="expanded")
load_css("style.css")
# --- Utility Functions ---
def save_notes_and_tasks(subject):
    data = {
        "tasks": st.session_state.get("tasks", []),
        "note": st.session_state.get("note", ""),
        "burnout_logs": st.session_state.get("burnout_logs", [])
    }
    with open(f"subjects/{subject}/notes.json", "w") as f:
        json.dump(data, f)

def load_notes_and_tasks(subject):
    try:
        with open(f"subjects/{subject}/notes.json", "r") as f:
            data = json.load(f)
            st.session_state.tasks = data.get("tasks", [])
            st.session_state.note = data.get("note", "")
            st.session_state.burnout_logs = data.get("burnout_logs", [])
    except FileNotFoundError:
        st.session_state.tasks = []
        st.session_state.note = ""
        st.session_state.burnout_logs = []
        st.warning(f"No saved notes found for subject '{subject}'. Starting fresh.")

# --- UI Setup ---
st.set_page_config(page_title="📚 StudyScope", layout="wide")
st.markdown("""
    <style>
    body, .stApp {
        background-color: #1E1E2F;
        color: #F0F0F0;
        font-family: 'Segoe UI', sans-serif;
    }
    .stTextInput > div > div > input,
    .stTextArea > div > textarea,
    .stSelectbox > div > div > div > div,
    .stButton button {
        background-color: #2D2D44;
        color: #F0F0F0;
        border-radius: 10px;
        border: 1px solid #444;
    }
    .stButton button:hover {
        background-color: #4466AA;
        color: white;
    }
    .st-bp {
        background-color: #1E1E2F;
    }
    .stCheckbox > label {
        color: #F0F0F0;
    }
    .stRadio > div > label {
        color: #F0F0F0;
    }
    .stMarkdown, .stCaption, .stInfo, .stSuccess, .stWarning, .stError {
        color: #F0F0F0 !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📚 StudyScope: Ask Anything From Your Notes")

# --- Subject Dropdown ---
if not os.path.exists("subjects"):
    st.error("No 'subjects' folder found. Please create 'subjects/<subject_name>' and add PDFs.")
    st.stop()

subjects = [
    d for d in os.listdir("subjects")
    if os.path.isdir(os.path.join("subjects", d)) and not d.startswith('.')
]

if not subjects:
    st.warning("No valid subject folders found in 'subjects/'. Please create one.")
    st.stop()

subject = st.selectbox("📁 Select Subject", subjects)
load_notes_and_tasks(subject)

# --- Ask Question ---
st.subheader("❓ Ask a Study Question")
question = st.text_input("Ask a question from your notes:")
use_gpt = st.checkbox("Use AI fallback (Flan-T5) if nothing found")

if st.button("🔍 Search"):
    if not question.strip():
        st.warning("Please type your question.")
    else:
        result = get_answer_from_notes(question, subject)
        if result:
            matched_chunk, score = result
            st.caption(f"🔎 Similarity Score: {score:.2f}")
            if matched_chunk:
                st.info("🧠 Found a relevant note chunk:")
                st.code(matched_chunk, language="markdown")

                st.info("Generating AI answer...")
                prompt = f"""You are a helpful tutor. Use the following context from class notes to answer the question.

Context: {matched_chunk}

Question: {question}

Answer:"""
                with st.spinner("🤖 Thinking..."):
                    gpt_answer = get_gpt_response(prompt)
                st.success("✅ AI-generated answer based on your notes:")
                st.write(gpt_answer)
        else:
            if use_gpt:
                st.info("No match found in notes. Using AI fallback...")
                with st.spinner("🤖 Thinking..."):
                    gpt_answer = get_gpt_response(question)
                st.markdown("### 🤖 AI Says:")
                st.write(gpt_answer)
            else:
                st.error("❌ No relevant answer found in notes.")

# --- 🧪 Auto-Generate Quiz ---
st.subheader("🧪 Auto-Generate Quiz from Your Notes")
if st.button("🎯 Generate Quiz"):
    try:
        with open(f"subjects/{subject}/texts.pkl", "rb") as f:
            notes_data = pickle.load(f)
        quiz = generate_quiz_from_notes(notes_data)
        for i, q in enumerate(quiz):
            st.markdown(f"**Q{i+1}. {q['question']}**")
            st.radio("Choose:", q['options'], key=f"q{i}")
    except Exception as e:
        st.error(f"❌ Failed to generate quiz: {e}")

# --- ✅ To-Do Tracker ---
st.subheader("🗓 To-Do Tracker")
new_task = st.text_input("Add a new task")
col1, col2 = st.columns([1, 5])
with col1:
    if st.button("➕ Add Task"):
        if new_task:
            st.session_state.tasks.append(new_task)
            save_notes_and_tasks(subject)
        else:
            st.warning("Task can't be empty!")
with col2:
    if st.button("🧹 Clear All"):
        st.session_state.tasks = []
        save_notes_and_tasks(subject)

for i, task in enumerate(st.session_state.tasks):
    st.checkbox(task, key=f"task_{i}")

# --- 📝 Quick Notes ---
st.subheader("📝 Quick Notes")
note = st.text_area("Jot something down...", value=st.session_state.note, height=150)
if st.button("📂 Save Note"):
    st.session_state.note = note
    save_notes_and_tasks(subject)
    st.success("Note saved!")

# --- 📄 Upload New PDF Notes ---
st.subheader("📄 Upload New PDF Notes")
pdf_file = st.file_uploader("Upload PDF", type=["pdf"])
if pdf_file:
    added_chunks = upload_and_process_pdf(pdf_file, subject)
    st.success(f"✅ Uploaded and indexed {added_chunks} new chunks into '{subject}'!")
    with open(f"subjects/{subject}/texts.pkl", "wb") as f:
        pickle.dump(added_chunks, f)

# --- 🧠 Daily Burnout Check-In ---
st.subheader("🧠 Daily Burnout Check-In")
mood = st.selectbox("How are you feeling today?", [
    "😄 I'm energetic and focused",
    "🙂 I'm okay but not great",
    "😐 A bit tired or distracted",
    "😞 Feeling burned out / overwhelmed"
])
if st.button("📝 Log Mood"):
    st.session_state.burnout_logs.append((mood, question))
    save_notes_and_tasks(subject)
    st.success("Mood logged for today!")
if st.session_state.burnout_logs:
    last_mood = st.session_state.burnout_logs[-1][0]
    st.caption("🧘 Personalized Suggestion:")
    if "burned out" in last_mood.lower():
        st.info("🌿 Take a short break. Maybe step outside or stretch a little?")
    elif "tired" in last_mood.lower():
        st.info("💧 Stay hydrated and consider switching to a lighter task.")
    elif "okay" in last_mood.lower():
        st.info("📌 You're doing fine! Try the Pomodoro method for focus.")
    elif "energetic" in last_mood.lower():
        st.info("🚀 Great energy! Push through your current goals.")

# --- ⏳ Study Time Tracker ---
st.subheader("⏳ Study Time Tracker")
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()
elapsed_time = time.time() - st.session_state.start_time
minutes = int(elapsed_time // 60)
seconds = int(elapsed_time % 60)
st.info(f"🕒 You've been studying for: **{minutes} min {seconds} sec**")
if st.button("🔁 Reset Timer"):
    st.session_state.start_time = time.time()
    st.success("⏱️ Timer reset!")
