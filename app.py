import streamlit as st
import google.generativeai as genai
import pdfplumber
import json
import os

# --- 1. PAGE CONFIG & THEME ---
st.set_page_config(page_title="CareerForge v11: The Coach", layout="wide", page_icon="🧬")

st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #c9d1d9; }
    .stTextInput input, .stTextArea textarea { background-color: #161b22; color: #58a6ff; border: 1px solid #30363d; }
    .stButton button { background-color: #238636; color: white; border-radius: 6px; }
    h1, h2, h3 { color: #58a6ff; }
    .success-box { padding: 15px; background-color: #1f6feb20; border: 1px solid #1f6feb; border-radius: 5px; }
    .agent-box { padding: 15px; background-color: #161b22; border-left: 5px solid #8957e5; margin-bottom: 20px; }
    .stProgress > div > div { background-color: #238636; }
    </style>
""", unsafe_allow_html=True)

# --- 2. SESSION STATE MANAGEMENT ---
HISTORY_FILE = "session_history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return {}

def save_history():
    with open(HISTORY_FILE, "w") as f:
        json.dump({
            "step": st.session_state.step,
            "resume_text": st.session_state.resume_text,
            "target_role": st.session_state.target_role,
            "gaps_found": st.session_state.gaps_found,
            "selected_gap": st.session_state.selected_gap,
            "project_idea": st.session_state.project_idea,
        }, f)

if "loaded" not in st.session_state:
    history = load_history()
    st.session_state.step = history.get("step", 1)
    st.session_state.resume_text = history.get("resume_text", "")
    st.session_state.target_role = history.get("target_role", "")
    st.session_state.gaps_found = history.get("gaps_found", "")
    st.session_state.selected_gap = history.get("selected_gap", "")
    st.session_state.project_idea = history.get("project_idea", "")
    st.session_state.loaded = True

# --- 3. SIDEBAR CONFIG ---
with st.sidebar:
    st.title("🧬 CareerForge-AI")
    api_key = st.text_input("Google API Key", type="password")

    st.write("---")
    st.markdown(f"**Current Step:** {st.session_state.step} of 3")
    st.progress(st.session_state.step / 3)

    if st.button("🔄 Reset Coach"):
        if os.path.exists(HISTORY_FILE):
            os.remove(HISTORY_FILE)
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# --- 4. THE AGENT LOGIC (with streaming) ---
def get_agent_response(prompt):
    if not api_key:
        return "⚠️ Please enter API Key in Sidebar."
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt, stream=True)
        output = st.empty()
        full_text = ""
        for chunk in response:
            if chunk.text:
                full_text += chunk.text
                output.markdown(full_text)
        return full_text
    except Exception as e:
        return f"Error: {str(e)}"

# --- 5. MAIN WORKFLOW ---
st.title("🚀 CareerForge: Intelligent Career Pathing")
st.caption(f"Step {st.session_state.step} of 3")
st.progress(st.session_state.step / 3)
st.write("")

# === STEP 1 ===
if st.session_state.step == 1:
    st.markdown("### 1️⃣ Agent 1: The Scanner")
    st.info("I will scan your current profile against market trends to find your 'Growth Gaps'.")

    col1, col2 = st.columns(2)
    with col1:
        uploaded_file = st.file_uploader("📄 Upload your Resume (PDF)", type="pdf")
        resume_input = ""
        if uploaded_file:
            with pdfplumber.open(uploaded_file) as pdf:
                resume_input = "\n".join(
                    page.extract_text() for page in pdf.pages if page.extract_text()
                )
            st.success("✅ Resume extracted successfully!")
            with st.expander("Preview extracted text"):
                st.text(resume_input[:1000] + ("..." if len(resume_input) > 1000 else ""))
        else:
            resume_input = st.text_area(
                "Or paste your Resume / Skill Summary:",
                height=200,
                placeholder="E.g., B.Tech CS student. Knows Java, Basic Python. Built a To-Do list app..."
            )

    with col2:
        role = st.selectbox("Select Your Target Path:",
                            ["Full-Stack Developer", "Backend Engineer (SDE)", "Frontend Specialist", "AI/ML Engineer"])

    if st.button("🔍 Analyze Gaps"):
        if not resume_input:
            st.error("Please upload a PDF or paste your resume text.")
        else:
            with st.spinner(f"Scanning market trends for {role}..."):
                prompt = f"""
                Act as a Senior Tech Recruiter.
                User Resume: {resume_input}
                Target Role: {role}

                Identify 3 specific 'Market Gaps' in their profile. These should be concepts they are missing (e.g., 'Redis Caching' instead of just 'Databases', or 'JWT Auth' instead of 'Login').
                Output ONLY a bulleted list of the 3 gaps with a 1-sentence explanation for each.
                """
                response = get_agent_response(prompt)
                st.session_state.resume_text = resume_input
                st.session_state.target_role = role
                st.session_state.gaps_found = response
                st.session_state.step = 2
                save_history()
                st.rerun()

# === STEP 2 ===
elif st.session_state.step == 2:
    st.markdown(f"### 2️⃣ Agent 2: The Mentor (Targeting: {st.session_state.target_role})")

    st.markdown('<div class="agent-box"><b>🕵️ Analysis Complete. Here are your missing links:</b><br>' +
                st.session_state.gaps_found.replace('\n', '<br>') + '</div>', unsafe_allow_html=True)

    gap_input = st.text_input("Which gap do you want to tackle first?", placeholder="E.g., Caching with Redis")

    if st.button("💡 Generate Project Idea"):
        with st.spinner("Designing a micro-project..."):
            prompt = f"""
            Act as a Senior Engineering Mentor.
            The student wants to learn: "{gap_input}" for the role of {st.session_state.target_role}.

            1. Explain the concept simply in 2 sentences.
            2. Assign a specific 'Micro-Project' to build this weekend.
            3. List 3 key technical keywords they must use in the code.
            """
            response = get_agent_response(prompt)
            st.session_state.selected_gap = gap_input
            st.session_state.project_idea = response
            st.session_state.step = 3
            save_history()
            st.rerun()

# === STEP 3 ===
elif st.session_state.step == 3:
    st.markdown("### 3️⃣ Agent 3: The Publisher")

    st.markdown(f'<div class="success-box"><b>📘 Your Mission:</b><br>{st.session_state.project_idea}</div>',
                unsafe_allow_html=True)

    st.write("---")
    st.write("Once you have built the project, describe what you did below to generate your 'Verification Post'.")

    learning_evidence = st.text_area("What did you build? (Paste summary or code snippet)", height=150)

    if st.button("✍️ Verify & Generate LinkedIn Post"):
        with st.spinner("Agent 3 is crafting your LinkedIn post..."):
            prompt = f"""
            Act as a Viral Tech LinkedIn Copywriter.
            The User just learned: "{st.session_state.selected_gap}"
            User's Project Evidence: "{learning_evidence}"
            Target Audience: Recruiters and Engineering Managers.

            Write a high-engagement LinkedIn Post.

            Follow this exact structure:
            1. **The Hook**: A catchy opening line about the problem they solved.
            2. **The "Before"**: Briefly mention the gap they had.
            3. **The "Build" (STAR Method)**: Describe the Solution and the Action taken using technical keywords.
            4. **The "After"**: The result or key learning.
            5. **Call to Action**: A question to the audience.
            6. **Hashtags**: 5 relevant tags.

            Tone: Professional yet humble and enthusiastic.
            Format: Clean spacing, use emojis sparingly but effectively.
            """
            final_response = get_agent_response(prompt)

            st.markdown("### 🎉 Ready-to-Post LinkedIn Update")
            st.text_area("Copy this to LinkedIn:", value=final_response, height=400)

            st.download_button(
                label="📥 Download Post as .txt",
                data=final_response,
                file_name=f"linkedin_post_{st.session_state.selected_gap.replace(' ', '_')}.txt",
                mime="text/plain"
            )

            st.balloons()

    st.write("---")
    if st.button("🔁 Tackle Another Gap"):
        st.session_state.step = 2
        save_history()
        st.rerun()