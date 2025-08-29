# app.py
# Run with: streamlit run app.py

import streamlit as st
import pandas as pd
from datetime import datetime
from io import StringIO

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Career & Education Advisor",
    page_icon="🎓",
    layout="wide"
)

# ------------------ HERO SECTION ------------------
st.markdown(
    """
    <div style="text-align:center; padding:20px; background:#eef2ff; border-radius:15px; margin-bottom:20px;">
        <h1 style="color:#1E3A8A;">🎓 One-Stop Career & Education Advisor</h1>
        <p style="font-size:18px; color:#334155;">
            Helping students discover the right academic stream and career roadmap through personalized guidance.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# ------------------ STREAM KNOWLEDGE ------------------
streams = {
    "Science": {
        "overview": "For those interested in Mathematics, Science, Technology, and Research.",
        "degrees": ["B.Tech/BE", "MBBS/BDS/Nursing", "B.Sc (CS, Physics, Chemistry, Biology)", "BCA"],
        "careers": ["Engineer", "Doctor", "Data Scientist", "Researcher"],
    },
    "Commerce": {
        "overview": "For students who love Business, Finance, and Management.",
        "degrees": ["B.Com", "BBA/BBM", "BA (Economics)", "BMS"],
        "careers": ["Chartered Accountant", "Banker", "Manager", "Entrepreneur"],
    },
    "Arts/Humanities": {
        "overview": "For creative and socially aware students passionate about Arts, Media, and Social Sciences.",
        "degrees": ["BA (English, Psychology, Political Science)", "BJMC", "BFA/Design", "B.Ed"],
        "careers": ["Journalist", "Designer", "Teacher", "Civil Services"],
    },
    "Vocational/Skill-based": {
        "overview": "For students who prefer hands-on, practical training and quick employability.",
        "degrees": ["Polytechnic Diploma", "ITI Trades", "Hotel Management", "B.Voc"],
        "careers": ["Technician", "Chef", "Hotel Operations", "Fashion Designer"],
    },
}

# ------------------ QUIZ QUESTIONS ------------------
quiz_questions = [
    ("Which subject do you enjoy the most?", 
     {"Math & Science": "Science", "Business & Numbers": "Commerce", "Arts & Creativity": "Arts/Humanities", "Practical Skills": "Vocational/Skill-based"}),
    ("What type of career excites you?", 
     {"Engineer/Doctor/Researcher": "Science", "Business/Accountant/Manager": "Commerce", "Writer/Designer/Teacher": "Arts/Humanities", "Technical/Vocational Jobs": "Vocational/Skill-based"}),
    ("Which activity do you prefer?", 
     {"Solving puzzles & experiments": "Science", "Managing money/business": "Commerce", "Drawing/Storytelling": "Arts/Humanities", "Hands-on practical work": "Vocational/Skill-based"}),
]

# ------------------ QUIZ FUNCTION ------------------
def run_quiz():
    responses = []
    for q, options in quiz_questions:
        choice = st.radio(q, list(options.keys()), index=None)
        responses.append(options.get(choice) if choice else None)

    if st.button("🔎 Get My Suggested Stream"):
        scores = {s: 0 for s in streams}
        for r in responses:
            if r: scores[r] += 1
        best = max(scores, key=scores.get)
        show_result(best)
        return best, scores
    return None, None

# ------------------ RESULT FUNCTION ------------------
def show_result(stream):
    data = streams[stream]
    st.success(f"✅ You are best suited for the **{stream}** stream.")
    st.write(f"**Overview:** {data['overview']}")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🎓 Popular Degrees")
        for d in data["degrees"]:
            st.markdown(f"- {d}")
    with col2:
        st.markdown("### 💼 Career Options")
        for c in data["careers"]:
            st.markdown(f"- {c}")

# ------------------ DOWNLOAD FUNCTION ------------------
def download_result(name, stream, scores):
    row = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "student_name": name,
        "suggested_stream": stream,
    }
    for s, sc in scores.items():
        row[f"score_{s}"] = sc
    df = pd.DataFrame([row])
    csv_buf = StringIO()
    df.to_csv(csv_buf, index=False)
    return csv_buf.getvalue().encode("utf-8")

# ------------------ TABS NAVIGATION ------------------
tab1, tab2, tab3, tab4 = st.tabs(["🧠 Quiz", "📈 Course → Career", "❓ FAQs", "ℹ️ About"])

# ----------- TAB 1: QUIZ -----------
with tab1:
    st.header("🧠 Aptitude & Interest Quiz")
    name = st.text_input("👤 Enter your name (optional)")

    best, scores = run_quiz()
    if best:
        csv_bytes = download_result(name or "Anonymous", best, scores)
        st.download_button("⬇️ Download My Result", data=csv_bytes, file_name="career_result.csv", mime="text/csv")

# ----------- TAB 2: COURSE TO CAREER -----------
with tab2:
    st.header("📈 Course → Career Roadmap")
    pick = st.selectbox("Select a stream to explore", list(streams.keys()))
    data = streams[pick]
    st.info(f"**{pick} Overview:** {data['overview']}")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🎓 Degrees")
        for d in data["degrees"]:
            st.markdown(f"- {d}")
    with col2:
        st.markdown("### 💼 Careers")
        for c in data["careers"]:
            st.markdown(f"- {c}")

# ----------- TAB 3: FAQ -----------
with tab3:
    st.header("❓ Frequently Asked Questions")
    with st.expander("Is Arts a good career option?"):
        st.write("Yes! Arts leads to media, design, psychology, education, and civil services.")
    with st.expander("What if I like both Science and Commerce?"):
        st.write("Pick the stream where you’ll stay motivated. You can switch later with MBA, data analytics, etc.")
    with st.expander("Can I change my stream later?"):
        st.write("Direct switching is hard, but possible via bridge courses, lateral entry, and skill-based programs.")
    with st.expander("Are vocational courses only for weak students?"):
        st.write("Not at all. Vocational streams are for hands-on learners who want faster employability.")

# ----------- TAB 4: ABOUT -----------
with tab4:
    st.header("ℹ️ About this Project")
    st.write(
        "This Career & Education Advisor is a **Streamlit-based guidance platform**. "
        "It helps students discover their best academic stream through a quiz, explore degrees and careers, "
        "and access FAQs. Future versions can integrate AI/ML for smarter recommendations."
    )
    st.markdown("**Future Enhancements:**")
    st.markdown("- Government colleges directory with courses & facilities")
    st.markdown("- Admission & scholarship timeline tracker")
    st.markdown("- Regional language support")
    st.markdown("- AI-driven recommendation engine")
