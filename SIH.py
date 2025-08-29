# app.py
# One-Stop Personalized Career & Education Advisor (Streamlit single-file app)
# Run: streamlit run app.py

import streamlit as st
from datetime import datetime
import pandas as pd
from io import StringIO

# ---------- PAGE SETUP ----------
st.set_page_config(
    page_title="Career & Education Advisor",
    page_icon="🎓",
    layout="centered",
    menu_items={
        "Get Help": "mailto:someone@example.com",
        "About": "A simple guidance portal to help students pick streams, courses, and careers."
    },
)

# Small theming helpers
def pill(text):
    st.markdown(
        f"""
        <span style="
            display:inline-block;
            padding:4px 10px;
            border-radius:999px;
            background:#f1f5f9;
            border:1px solid #e2e8f0;
            font-size:0.85rem;
        ">{text}</span>
        """,
        unsafe_allow_html=True,
    )

# ---------- DATA (RULES + CONTENT) ----------
STREAMS = ["Science", "Commerce", "Arts/Humanities", "Vocational/Skill-based"]

stream_knowledge = {
    "Science": {
        "overview": "Best if you enjoy math, science, technology, experiments, and analytical work.",
        "good_for": ["Problem solving", "Research mindset", "Math & logic"],
        "core_subjects": ["Physics", "Chemistry", "Biology", "Mathematics", "Computer Science"],
        "popular_degrees": [
            "B.Tech / BE (Engineering)",
            "MBBS / BDS / BAMS / BHMS / Nursing",
            "BSc (CS, IT, Physics, Chem, Bio, Math, Data Science)",
            "BCA (Computer Applications)"
        ],
        "typical_roles": [
            "Software Engineer, Data Analyst/Scientist",
            "Doctor, Nurse, Pharmacist",
            "Research Scientist",
            "Engineer (Mechanical, Civil, EEE, ECE, etc.)"
        ],
        "exams": ["JEE (Engineering)", "NEET (Medical)", "CUET (UG)", "State CETs"],
        "higher": ["M.Tech/MS", "MD/MS", "MSc/PhD", "MBA"],
        "skills": ["Analytical thinking", "Maths", "Coding basics", "Scientific reasoning"]
    },
    "Commerce": {
        "overview": "Great for business, finance, accounting, management, and entrepreneurship.",
        "good_for": ["Numbers & money", "Business sense", "Communication"],
        "core_subjects": ["Accounting", "Economics", "Business Studies", "Mathematics (optional)"],
        "popular_degrees": ["B.Com", "BBA/BBM", "BA (Economics)", "BMS"],
        "typical_roles": [
            "Chartered Accountant (CA), Company Secretary (CS), CMA",
            "Banking/Finance Analyst",
            "Marketing/HR/Sales Executive",
            "Entrepreneur"
        ],
        "exams": ["CA/CS/CMA Foundation", "CUET (UG)", "Bank exams (later)", "CAT (for MBA later)"],
        "higher": ["MBA", "M.Com", "PGDM", "Data Analytics (business)"],
        "skills": ["Numeracy", "Accounting basics", "Excel", "Communication", "Marketing sense"]
    },
    "Arts/Humanities": {
        "overview": "Ideal for creativity, languages, social sciences, media, design, civil services.",
        "good_for": ["Creativity", "Writing", "Public speaking", "Social awareness"],
        "core_subjects": ["History", "Political Science", "Psychology", "Sociology", "English", "Geography"],
        "popular_degrees": [
            "BA (English, Psychology, Economics, Pol. Sci., etc.)",
            "BJMC (Journalism & Mass Comm.)",
            "BFA/Design",
            "B.Ed (after graduation)"
        ],
        "typical_roles": [
            "Journalist/Content Creator",
            "Designer/Artist",
            "Teacher/Counselor",
            "Civil Services Aspirant"
        ],
        "exams": ["CUET (UG)", "Design entrance (NID/NIFT)", "State PSC/UPSC (later)"],
        "higher": ["MA/MSW", "MBA (Media/HR)", "MFA", "PhD"],
        "skills": ["Writing", "Design thinking", "Public speaking", "Critical thinking"]
    },
    "Vocational/Skill-based": {
        "overview": "Perfect if you prefer hands-on learning, quick job skills, and practical training.",
        "good_for": ["Practical mindset", "Making/building", "Early job readiness"],
        "core_subjects": ["Domain-specific skills via ITI/Polytechnic/Skilled diplomas"],
        "popular_degrees": [
            "Polytechnic Diploma",
            "ITI Trades",
            "B.Voc",
            "Hotel Management / Tourism"
        ],
        "typical_roles": [
            "Technician/Electrician/Mechanic",
            "Chef/Baker/Hotel Ops",
            "Field Technician",
            "Creative trades (Fashion/Animation)"
        ],
        "exams": ["Institute/State-level skill entrances (varies)"],
        "higher": ["Lateral entry to B.Tech", "Advanced Diplomas", "Entrepreneurship"],
        "skills": ["Tool handling", "Customer service", "Quality control", "Workplace safety"]
    },
}

# Quiz questions map each option to a stream for scoring
QUIZ = [
    {
        "q": "Which subjects do you enjoy the most?",
        "options": {
            "Math & Science": "Science",
            "Business & Numbers": "Commerce",
            "Arts & Languages": "Arts/Humanities",
            "Practical/Hands-on": "Vocational/Skill-based",
        }
    },
    {
        "q": "What type of work excites you most?",
        "options": {
            "Solving technical problems / coding / experiments": "Science",
            "Managing money / business / marketing": "Commerce",
            "Writing / design / media / teaching": "Arts/Humanities",
            "Repairing / cooking / crafting / operating machines": "Vocational/Skill-based",
        }
    },
    {
        "q": "Pick a school activity you’d choose first:",
        "options": {
            "Science fair / robotics club": "Science",
            "Commerce club / stock market game": "Commerce",
            "Debate / theatre / creative writing": "Arts/Humanities",
            "Workshop / lab practical / demo day": "Vocational/Skill-based",
        }
    },
    {
        "q": "How do you want to learn after Class 12?",
        "options": {
            "Deep theory + labs + projects": "Science",
            "Business cases + internships": "Commerce",
            "Creative portfolios + field work": "Arts/Humanities",
            "Hands-on training + quick job skills": "Vocational/Skill-based",
        }
    },
    {
        "q": "What’s your long-term goal?",
        "options": {
            "Engineer/Doctor/Scientist/Data pro": "Science",
            "CA/Manager/Banking/Entrepreneur": "Commerce",
            "Journalist/Designer/Teacher/Civil services": "Arts/Humanities",
            "Skilled professional (chef/technician/etc.)": "Vocational/Skill-based",
        }
    },
    {
        "q": "How comfortable are you with mathematics?",
        "options": {
            "Love it / strong": "Science",
            "Okay when linked to money/business": "Commerce",
            "Not my favorite": "Arts/Humanities",
            "Prefer practical work over math": "Vocational/Skill-based",
        }
    },
    {
        "q": "Pick a skill you want to master first:",
        "options": {
            "Coding / lab science / analytics": "Science",
            "Finance / Excel / sales": "Commerce",
            "Writing / design / public speaking": "Arts/Humanities",
            "Equipment handling / craft / culinary": "Vocational/Skill-based",
        }
    },
]

# ---------- HELPERS ----------
def run_quiz():
    st.header("🧠 Aptitude & Interest Quiz")
    st.write("Answer a few quick questions. Your answers help us suggest a suitable stream.")
    responses = []
    for i, item in enumerate(QUIZ, start=1):
        choice = st.radio(f"{i}. {item['q']}", list(item["options"].keys()), index=None)
        responses.append(item["options"].get(choice) if choice else None)

    proceed = st.button("🔎 Get My Suggested Stream")
    return responses, proceed

def score_stream(responses):
    # Count points per stream
    scores = {s: 0 for s in STREAMS}
    for s in responses:
        if s in scores:
            scores[s] += 1

    # Sort by score desc
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    top_stream, top_score = ranked[0]
    second_stream, second_score = ranked[1]

    # Handle empty / ties gracefully
    if top_score == 0:
        return None, ranked
    return top_stream, ranked

def show_stream_result(stream, ranked):
    if not stream:
        st.warning("Please answer the questions above to get a suggestion.")
        return

    st.success(f"✅ You seem best suited for the **{stream}** stream.")
    # Also show a compact scoreboard
    with st.expander("See how your answers scored across all streams"):
        for s, sc in ranked:
            pill(f"{s}: {sc}")

    # Knowledge card
    data = stream_knowledge[stream]
    st.markdown("---")
    st.subheader(f"📚 About {stream}")
    st.write(data["overview"])
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Core Subjects**")
        for x in data["core_subjects"]:
            st.write("•", x)
        st.markdown("**Good If You Enjoy**")
        for x in data["good_for"]:
            st.write("•", x)
        st.markdown("**Key Skills to Build**")
        for x in data["skills"]:
            st.write("•", x)
    with c2:
        st.markdown("**Popular Degrees**")
        for x in data["popular_degrees"]:
            st.write("•", x)
        st.markdown("**Typical Roles**")
        for x in data["typical_roles"]:
            st.write("•", x)
        st.markdown("**Entrance/Relevant Exams**")
        for x in data["exams"]:
            st.write("•", x)

    st.markdown("**Higher Studies Options**")
    st.write(", ".join(data["higher"]))

def show_course_to_career(stream=None):
    st.header("🗺️ Course → Career Roadmaps")
    st.write("Explore how streams map to degree programs, exams, higher studies, and job roles.")
    pick = st.selectbox("Choose a stream to explore", STREAMS, index=(STREAMS.index(stream) if stream in STREAMS else 0))
    info = stream_knowledge[pick]

    st.subheader(f"🎯 {pick}: Snapshot")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Popular Degrees**")
        for d in info["popular_degrees"]:
            st.write("•", d)
        st.markdown("**Entrance/Relevant Exams**")
        for e in info["exams"]:
            st.write("•", e)
    with c2:
        st.markdown("**Typical Job Roles**")
        for r in info["typical_roles"]:
            st.write("•", r)
        st.markdown("**Higher Studies**")
        for h in info["higher"]:
            st.write("•", h)

    st.markdown("---")
    st.subheader("📈 Simple Visual Roadmap")
    st.markdown(
        """
        ```
        Stream ──> Degree(s) ──> Entrance (if any) ──> First Job Roles ──> Higher Studies ──> Advanced Roles
        ```
        """
    )
    st.markdown("**Example Path:**")
    if pick == "Science":
        st.code("Science → B.Tech (CS) → JEE/CUET → Software Engineer → M.Tech/MBA → Senior Engineer / Product Manager")
    elif pick == "Commerce":
        st.code("Commerce → B.Com → CA/CS/CMA Foundation → Accountant/Analyst → MBA/PGDM → Finance Manager / Consultant")
    elif pick == "Arts/Humanities":
        st.code("Arts → BA (Journalism) → CUET → Reporter/Content Creator → MA/MBA → Editor / Media Manager")
    else:
        st.code("Vocational → Polytechnic Diploma → Institute/State Entrances → Technician → Lateral B.Tech/Advanced Diploma → Supervisor")

def save_result_to_csv(name, cls, best_stream, ranked):
    # Create a single-row dataframe
    row = {
        "timestamp": datetime.now().isoformat(sep=" ", timespec="seconds"),
        "name": name,
        "class": cls,
        "suggested_stream": best_stream,
    }
    # Add scores
    for s, sc in ranked:
        row[f"score_{s}"] = sc
    df = pd.DataFrame([row])

    # Return CSV bytes and a filename
    csv_buf = StringIO()
    df.to_csv(csv_buf, index=False)
    csv_bytes = csv_buf.getvalue().encode("utf-8")
    return csv_bytes, "career_advisor_result.csv"

def faq():
    st.header("❓ FAQs")
    with st.expander("Is Arts a good career option?"):
        st.write("Yes! Arts/Humanities leads to media, design, psychology, education, civil services, and more. Success depends on skills and consistency, not just stream.")
    with st.expander("What if I like both Science and Commerce?"):
        st.write("Pick the stream where you’ll stay motivated for 3–4 years. You can later switch via MBA, design/data courses, or certifications that cut across streams.")
    with st.expander("Can I change my stream later?"):
        st.write("Direct switching is limited, but bridges exist (e.g., Commerce → Data Analytics, Arts → MBA/Design, Vocational → Lateral B.Tech). Skill-building makes switches possible.")
    with st.expander("Are vocational courses only for low scorers?"):
        st.write("No. They’re for hands-on learners who want faster employability. Many skilled trades and hospitality careers have strong demand and growth.")
    with st.expander("How do I choose between multiple interests?"):
        st.write("Try small projects/internships/online courses to test your interest. Talk to mentors, and pick the path you’ll enjoy working on daily.")

def about():
    st.header("ℹ️ About this project")
    st.write(
        "This beginner-friendly guidance app helps students explore streams, courses, and careers. "
        "It uses a simple rules-based quiz (no personal data is sent anywhere). "
        "You can expand it later with real college data, notifications, and AI recommendations."
    )
    st.markdown("**Future Enhancements:**")
    st.write("• Add a government colleges directory with location & course filters.")
    st.write("• Add a timeline tracker for admissions and scholarships.")
    st.write("• Support regional languages.")
    st.write("• Train a basic ML model for smarter recommendations.")

# ---------- APP BODY ----------
st.title("🎓 One-Stop Career & Education Advisor")
st.caption("Pick your stream with confidence. Explore degrees, exams, jobs, and higher studies.")

# Sidebar nav (simple)
page = st.sidebar.radio(
    "Navigate",
    ["Home", "Quiz", "My Result", "Course → Career", "FAQs", "About"],
    index=0,
)

# Minimal “Home”
if page == "Home":
    st.header("Welcome 👋")
    st.write(
        "Use the **Quiz** to get a suggested stream. Then explore detailed **Course → Career** maps, "
        "save your result, and read **FAQs**."
    )
    st.markdown("**What this app covers:**")
    st.write("• Aptitude & interest quiz")
    st.write("• Stream suggestion (Science / Commerce / Arts / Vocational)")
    st.write("• Degrees, roles, exams, higher studies")
    st.write("• Downloadable result (CSV)")

# Quiz page
elif page == "Quiz":
    # Basic learner details (optional but useful)
    with st.expander("👤 Optional: Tell us about you", expanded=False):
        name = st.text_input("Your name (optional)")
        student_class = st.selectbox("Current class/grade", ["Class 10", "Class 11", "Class 12", "Other"], index=2)

    answers, pressed = run_quiz()
    if pressed:
        best, ranked = score_stream(answers)
        st.session_state["quiz_ranked"] = ranked
        st.session_state["quiz_best"] = best
        st.session_state["student_name"] = name
        st.session_state["student_class"] = student_class
        show_stream_result(best, ranked)

        # Save/download
        st.markdown("---")
        st.subheader("💾 Save your result")
        if best:
            csv_bytes, fname = save_result_to_csv(
                name or "Anonymous",
                student_class if "student_class" in st.session_state else "NA",
                best,
                ranked,
            )
            st.download_button("⬇️ Download result (CSV)", data=csv_bytes, file_name=fname, mime="text/csv")
            st.info("Your download is local to your device. No data is uploaded.")

# Result page (if they already took quiz)
elif page == "My Result":
    best = st.session_state.get("quiz_best")
    ranked = st.session_state.get("quiz_ranked")
    if not best:
        st.warning("No result yet. Please take the quiz first.")
    else:
        st.header("🎯 Your Suggested Stream")
        show_stream_result(best, ranked)

        st.markdown("---")
        st.subheader("🔁 Explore next")
        if st.button("Open my stream in Course → Career"):
            st.session_state["jump_to_stream"] = best
            st.switch_page("app.py")  # works within single-file rerun; harmless if ignored

# Course to Career page
elif page == "Course → Career":
    default_stream = st.session_state.get("jump_to_stream")
    show_course_to_career(default_stream)
    # Clear the jump so it doesn't persist
    if "jump_to_stream" in st.session_state:
        del st.session_state["jump_to_stream"]

# FAQs page
elif page == "FAQs":
    faq()

# About page
elif page == "About":
    about()

# Footer
st.markdown("---")
st.caption("Built with ❤️ using Streamlit. This is a learning project—customize it for your state/college data!")
