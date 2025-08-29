# app.py
# One-Stop Personalized Career & Education Advisor (Full version)
# Run: streamlit run app.py

import streamlit as st
import pandas as pd
from datetime import datetime, date
from io import StringIO

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Career & Education Advisor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------ STYLES / HELPERS ------------------
def card(html):
    st.markdown(html, unsafe_allow_html=True)

def small_pill(text):
    return f"<span style='background:#eef2ff;border-radius:999px;padding:4px 10px;margin-right:6px;font-size:0.9rem;color:#1e3a8a;border:1px solid #dbeafe'>{text}</span>"

def download_df_as_csv_bytes(df, name="data.csv"):
    csv_buf = StringIO()
    df.to_csv(csv_buf, index=False)
    return csv_buf.getvalue().encode("utf-8"), name

# ---------- HERO ----------
st.markdown(
    """
    <div style="text-align:center; padding:22px; background: linear-gradient(90deg,#eef2ff,#f7f9ff); border-radius:12px;">
        <h1 style="color:#0f172a; margin-bottom:6px;">🎓 One-Stop Career & Education Advisor</h1>
        <p style="color:#334155; margin-top:0;">
            Personalized guidance to help students choose a stream, explore career paths, find government colleges nearby,
            and track important admission timelines.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")  # small spacer

# ------------------ CONTENT DATA  ------------------

# Detailed roadmap content for each stream (expanded)
roadmaps = {
    "Science": {
        "summary": "Science suits students who enjoy math, experiments, and problem-solving. Common paths: Engineering, Medicine, Pure Sciences, Computer Science.",
        "paths": [
            {
                "degree": "B.Tech / BE (Computer Science)",
                "entrance": "JEE Main & Advanced / State CET / University Entrance",
                "first_roles": "Software Engineer, QA, Developer, Data Analyst",
                "higher": "M.Tech / MS / MBA / Specialized Master's",
                "future": "Product Manager, Tech Lead, Research Scientist"
            },
            {
                "degree": "MBBS / BDS / BAMS / BHMS",
                "entrance": "NEET (UG)",
                "first_roles": "Junior Doctor, Resident, Medical Officer",
                "higher": "MD / MS / Postgraduate Specialization",
                "future": "Specialist Surgeon, Consultant, Research in Medicine"
            },
            {
                "degree": "B.Sc (Data Science / Physics / Chemistry / Biology)",
                "entrance": "CUET / University Entrance",
                "first_roles": "Lab Technician, Data Analyst, Research Assistant",
                "higher": "M.Sc / PhD / M.Tech (specialized areas)",
                "future": "Research Scientist, Specialist in domain"
            }
        ],
        "skills": ["Mathematics", "Coding basics", "Analytical reasoning", "Laboratory skills"]
    },
    "Commerce": {
        "summary": "Commerce is for students interested in accounting, finance, business, and entrepreneurship.",
        "paths": [
            {
                "degree": "B.Com / BBA",
                "entrance": "CUET / University Entrance (BBA sometimes has college tests)",
                "first_roles": "Accountant, Finance Executive, Sales/Marketing Trainee",
                "higher": "CA/CS/CMA (professional), MBA, M.Com",
                "future": "Finance Manager, Consultant, Entrepreneur"
            },
            {
                "degree": "B.Com + CA route",
                "entrance": "CA Foundation / Direct pathway after graduation",
                "first_roles": "Article Assistant, Junior Auditor",
                "higher": "CA Final + Experience",
                "future": "Partner in Firm / Financial Controller"
            },
            {
                "degree": "BBA → MBA",
                "entrance": "College/University + Management entrance for MBA (CAT, MAT)",
                "first_roles": "Business Analyst, Marketing Executive",
                "higher": "MBA / PGDM",
                "future": "Product Manager, Business Leader"
            }
        ],
        "skills": ["Numeracy", "Excel", "Basic accounting", "Communication", "Business awareness"]
    },
    "Arts/Humanities": {
        "summary": "Arts/humanities fits creative and critical thinkers: journalism, design, social sciences, languages, civil services.",
        "paths": [
            {
                "degree": "BA (Journalism, English, Psychology, Political Science)",
                "entrance": "CUET / University Entrance",
                "first_roles": "Content Writer, Reporter, Counselor, Social Researcher",
                "higher": "MA, MPhil, MBA (specializations), MEd",
                "future": "Editor, Psychologist, Policy Analyst, Civil Servant"
            },
            {
                "degree": "BFA / Design (NID/NIFT)",
                "entrance": "Design Entrance (NID / NIFT / College tests)",
                "first_roles": "Graphic Designer, Visual Artist, Animator",
                "higher": "MFA, Advanced Diplomas",
                "future": "Creative Director, Studio Owner"
            }
        ],
        "skills": ["Writing", "Design thinking", "Critical analysis", "Communication"]
    },
    "Vocational/Skill-based": {
        "summary": "Vocational education focuses on hands-on skills and quicker job-readiness: ITI, Polytechnic, B.Voc.",
        "paths": [
            {
                "degree": "Polytechnic Diploma / ITI",
                "entrance": "Institute-specific / State polytechnic exams",
                "first_roles": "Technician, Operator, Junior Engineer",
                "higher": "Lateral entry to B.Tech, Advanced Diplomas",
                "future": "Supervisor, Technician Lead, Entrepreneur"
            },
            {
                "degree": "B.Voc / Hotel Management / Culinary",
                "entrance": "University/Institute entrance",
                "first_roles": "Chef, Hotel Operations, Tourism Executive",
                "higher": "Advanced hospitality diplomas, business courses",
                "future": "Restaurant Owner, Hospitality Manager"
            }
        ],
        "skills": ["Tool handling", "Customer service", "Practical craft", "Workplace readiness"]
    },
}

# Sample government colleges directory (demo data)
college_data = pd.DataFrame([
    {
        "college_name": "Govt. Science College, Chennai",
        "district": "Chennai",
        "state": "Tamil Nadu",
        "streams": "Science,Computer Science,Mathematics",
        "courses": "B.Sc Physics; B.Sc Computer Science; B.Sc Mathematics",
        "facilities": "Hostel, Labs, Library, Internet",
        "contact": "044-xxxx-xxxx"
    },
    {
        "college_name": "Govt. Commerce College, Delhi",
        "district": "New Delhi",
        "state": "Delhi",
        "streams": "Commerce,Management",
        "courses": "B.Com; BBA",
        "facilities": "Library, WiFi, Career Cell",
        "contact": "011-xxxx-xxxx"
    },
    {
        "college_name": "Govt. Arts College, Mumbai",
        "district": "Mumbai",
        "state": "Maharashtra",
        "streams": "Arts,Humanities,Journalism",
        "courses": "BA English; BA Psychology; BJMC",
        "facilities": "Hostel, Library, Theatre",
        "contact": "022-xxxx-xxxx"
    },
    {
        "college_name": "District Polytechnic, Pune",
        "district": "Pune",
        "state": "Maharashtra",
        "streams": "Vocational,Engineering Diploma",
        "courses": "Diploma Civil; Diploma Mechanical",
        "facilities": "Workshops, Labs, Placement Cell",
        "contact": "020-xxxx-xxxx"
    },
    {
        "college_name": "Govt. Institute of Technology, Bhopal",
        "district": "Bhopal",
        "state": "Madhya Pradesh",
        "streams": "Science,Engineering,Computer Science",
        "courses": "B.Tech CSE; B.Tech ECE",
        "facilities": "Hostel, Labs, Library, WiFi",
        "contact": "0755-xxxx-xxxx"
    },
])

# Timeline tracker sample (admissions/exams/scholarships)
timeline_data = pd.DataFrame([
    {"event": "CUET UG Application Opens", "start_date": "2025-03-01", "end_date": "2025-03-31", "type": "Exam/Admission"},
    {"event": "NEET UG Exam", "start_date": "2025-05-05", "end_date": "2025-05-05", "type": "Exam"},
    {"event": "State Engineering CET", "start_date": "2025-04-10", "end_date": "2025-04-10", "type": "Exam"},
    {"event": "National Scholarship Portal - Application Window", "start_date": "2025-06-01", "end_date": "2025-08-31", "type": "Scholarship"},
    {"event": "College Counseling (State Level)", "start_date": "2025-06-15", "end_date": "2025-07-05", "type": "Counseling"},
])

# Study resources (simple curated list)
study_resources = [
    {"title": "NCERT Textbooks (Free)", "type": "Books", "note": "Basic foundation for all streams.", "link": "https://ncert.nic.in/"},
    {"title": "Swayam Courses (Government MOOC)", "type": "MOOC", "note": "Short online courses in many streams.", "link": "https://swayam.gov.in/"},
    {"title": "Khan Academy (STEM)", "type": "MOOC", "note": "Free lessons in maths, science and computing.", "link": "https://www.khanacademy.org/"},
    {"title": "NPTEL (Engineering)", "type": "MOOC", "note": "University-level engineering courses.", "link": "https://nptel.ac.in/"},
    {"title": "National Scholarship Portal", "type": "Scholarship", "note": "Apply for government scholarships.", "link": "https://scholarships.gov.in/"},
]

# Motivational tips (short)
career_tips = [
    "Pick a path you can stay motivated in for 2–4 years.",
    "Balance passion with reasonable job-market awareness.",
    "Use small projects/internships to validate interests.",
    "Skills and communication often matter more than a single exam score.",
    "You can change direction later with focused courses — early skills matter."
]

# ------------------ SIDEBAR (Quick Nav + Filters) ------------------
st.sidebar.header("Quick Actions")
side_nav = st.sidebar.radio("Go to", ["Home", "Quiz", "Course → Career", "Colleges Directory", "Timeline", "Resources & FAQs", "About"])

st.sidebar.markdown("---")
st.sidebar.markdown("**Filter colleges** (quick demo)")
filter_stream = st.sidebar.selectbox("Stream to filter (substring match)", ["All", "Science", "Commerce", "Arts", "Vocational", "Engineering", "Management"])
filter_state = st.sidebar.selectbox("State (optional)", ["All"] + sorted(college_data["state"].unique().tolist()))
if st.sidebar.button("Apply filter & open Colleges"):
    side_nav = "Colleges Directory"

st.sidebar.markdown("---")
st.sidebar.caption("This is a demo dataset. Replace with real government college CSV for real deployment.")

# ------------------ PAGES ------------------

def page_home():
    st.header("Welcome Student 👋")
    st.write(
        "Use this portal to: take an aptitude quiz, view expanded course-to-career roadmaps, "
        "search a sample directory of government colleges, track important admissions/exam timelines, and access study resources."
    )
    # Three feature cards
    c1, c2, c3 = st.columns(3)
    with c1:
        card(f"<div style='padding:12px; border-radius:8px; background:#f8fafc;'><h3>🧠 Quiz</h3><p>Quick aptitude quiz that suggests a stream.</p></div>")
    with c2:
        card(f"<div style='padding:12px; border-radius:8px; background:#f8fafc;'><h3>📈 Career Roadmaps</h3><p>Detailed degree → entrance → jobs → higher studies pathways.</p></div>")
    with c3:
        card(f"<div style='padding:12px; border-radius:8px; background:#f8fafc;'><h3>🏛️ Colleges & Timeline</h3><p>Sample government colleges directory + admission timelines.</p></div>")

def page_quiz():
    st.header("🧠 Aptitude & Interest Quiz")
    st.write("Answer honestly. The recommendation is rules-based and meant to guide your next steps — not decide your future.")
    # Collect some basic info
    name = st.text_input("Name (optional)")
    student_class = st.selectbox("Current class/grade", ["Class 10", "Class 11", "Class 12", "Other"], index=2)

    st.markdown("---")
    st.subheader("Quiz Questions")
    # questions (expanded)
    q1 = st.radio("1) Which subject do you enjoy the most?",
                  ["Math & Science", "Business & Numbers", "Arts & Languages", "Practical/Hands-on"], index=0)
    q2 = st.radio("2) What type of career excites you?",
                  ["Engineer/Doctor/Researcher", "Business/Accountant/Manager", "Writer/Designer/Teacher", "Technical/Vocational Jobs"], index=0)
    q3 = st.radio("3) Which school activity would you choose?",
                  ["Science fair / coding / lab", "Commerce club / mock trading", "Debate / arts / theatre", "Workshops / practical sessions"], index=0)
    q4 = st.radio("4) How comfortable are you with mathematics?",
                  ["Love it / strong", "Okay (for business)", "Not my favorite", "Prefer practical skills"], index=0)
    q5 = st.radio("5) Long term goal you prefer?",
                  ["Tech / Research / Medicine", "Business / Finance", "Creative / Teaching / Social work", "Hands-on skilled work"], index=0)

    # scoring rules map
    mapping = {
        "Math & Science": "Science", "Engineer/Doctor/Researcher": "Science", "Science fair / coding / lab": "Science",
        "Love it / strong": "Science", "Tech / Research / Medicine": "Science",
        "Business & Numbers": "Commerce", "Business/Accountant/Manager": "Commerce", "Commerce club / mock trading": "Commerce",
        "Okay (for business)": "Commerce", "Business / Finance": "Commerce",
        "Arts & Languages": "Arts/Humanities", "Writer/Designer/Teacher": "Arts/Humanities", "Debate / arts / theatre": "Arts/Humanities",
        "Not my favorite": "Arts/Humanities", "Creative / Teaching / Social work": "Arts/Humanities",
        "Practical/Hands-on": "Vocational/Skill-based", "Technical/Vocational Jobs": "Vocational/Skill-based", "Workshops / practical sessions": "Vocational/Skill-based",
        "Prefer practical skills": "Vocational/Skill-based", "Hands-on skilled work": "Vocational/Skill-based"
    }

    if st.button("🔎 Suggest my Stream"):
        # compute score
        answers = [q1, q2, q3, q4, q5]
        scores = {"Science": 0, "Commerce": 0, "Arts/Humanities": 0, "Vocational/Skill-based": 0}
        for a in answers:
            mapped = mapping.get(a)
            if mapped:
                scores[mapped] += 1
        # decide
        best = max(scores, key=lambda k: scores[k])
        # tie-handling (if equal scores)
        vals = sorted(scores.values(), reverse=True)
        if len(set(scores.values())) == 1:  # all equal
            st.info("Your interests span multiple streams. Consider exploring small projects in each to decide.")
        st.success(f"✅ Suggested Stream: **{best}**")
        # show expanded roadmap for chosen stream
        st.markdown("---")
        st.subheader(f"📚 Expanded Roadmap: {best}")
        data = roadmaps[best]
        st.write(data["summary"])
        for p in data["paths"]:
            st.markdown(f"**{p['degree']}**  \nEntrance: {p['entrance']}  \nFirst roles: {p['first_roles']}  \nHigher studies: {p['higher']}  \nFuture: {p['future']}")
            st.markdown("---")
        st.markdown("**Key skills to build:** " + ", ".join(data["skills"]))
        # download result (CSV)
        res_df = pd.DataFrame([{
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "name": name or "Anonymous",
            "class": student_class,
            "suggested_stream": best,
            **{f"score_{k}": v for k, v in scores.items()}
        }])
        csv_bytes, fname = download_df_as_csv_bytes(res_df, name="career_quiz_result.csv")
        st.download_button("⬇️ Download my result (CSV)", data=csv_bytes, file_name=fname, mime="text/csv")
        st.info("Tip: Try small online courses or internships to validate the suggested stream.")

def page_roadmap():
    st.header("📈 Course → Career Roadmaps (Explore by Stream)")
    stream_pick = st.selectbox("Choose a stream", list(roadmaps.keys()))
    r = roadmaps[stream_pick]
    st.write(r["summary"])
    st.markdown("**Paths & Examples**")
    for item in r["paths"]:
        st.markdown(f"### {item['degree']}")
        col_a, col_b = st.columns([2,1])
        with col_a:
            st.markdown(f"- **Entrance:** {item['entrance']}")
            st.markdown(f"- **First Job Roles:** {item['first_roles']}")
            st.markdown(f"- **Higher Studies:** {item['higher']}")
            st.markdown(f"- **Future Scope:** {item['future']}")
        with col_b:
            st.markdown(small_pill("Skills"))
            st.write(", ".join(r["skills"]))
        st.markdown("---")
    st.markdown("**Practical advice:**")
    st.write(
        "- Start small: online course or project in the area you like.  "
        "- Document your work: a portfolio helps more than a single test score.  "
        "- Talk to seniors and teachers in that subject."
    )

def page_colleges():
    st.header("🏛️ Government Colleges Directory (Sample Data)")
    st.write("This is a demo list. Replace with your state's college dataset (CSV) for production use.")
    # filters from sidebar applied
    df = college_data.copy()
    if filter_stream != "All":
        df = df[df["streams"].str.contains(filter_stream, case=False, na=False)]
    if filter_state != "All":
        df = df[df["state"] == filter_state]

    st.markdown(f"**Showing {len(df)} colleges** (filters applied).")
    # Search box
    search = st.text_input("Search college name / district / course (substring):")
    if search:
        search = search.strip().lower()
        df = df[df.apply(lambda row: search in (str(row["college_name"]).lower() + "|" + str(row["district"]).lower() + "|" + str(row["courses"]).lower()), axis=1)]

    # display table & cards
    if df.empty:
        st.warning("No colleges found for given filters.")
    else:
        for _, row in df.iterrows():
            with st.container():
                c1, c2 = st.columns([4,1])
                with c1:
                    st.markdown(f"**{row['college_name']}** — {row['district']}, {row['state']}")
                    st.markdown(f"- Streams: {row['streams']}")
                    st.markdown(f"- Courses: {row['courses']}")
                    st.markdown(f"- Facilities: {row['facilities']}")
                with c2:
                    st.markdown(f"**Contact**\n{row['contact']}")
                st.markdown("---")
        # allow download of visible df
        csv_bytes, fname = download_df_as_csv_bytes(df, name="colleges_filtered.csv")
        st.download_button("⬇️ Download visible colleges (CSV)", data=csv_bytes, file_name=fname, mime="text/csv")

    # allow user to upload their own college CSV
    st.markdown("### Upload your own colleges CSV (optional)")
    uploaded = st.file_uploader("Upload CSV (columns: college_name, state, district, streams, courses, facilities, contact)", type=["csv"])
    if uploaded:
        try:
            u_df = pd.read_csv(uploaded)
            st.success(f"Uploaded {len(u_df)} rows. Preview:")
            st.dataframe(u_df.head())
            csv_bytes2, fn2 = download_df_as_csv_bytes(u_df, name="uploaded_colleges.csv")
            st.download_button("⬇️ Download uploaded CSV", data=csv_bytes2, file_name=fn2, mime="text/csv")
        except Exception as e:
            st.error(f"Failed to read CSV: {e}")

def page_timeline():
    st.header("📅 Timeline Tracker — Admissions, Exams & Scholarships")
    # show upcoming events sorted by start_date
    df = timeline_data.copy()
    df["start_date"] = pd.to_datetime(df["start_date"])
    df["end_date"] = pd.to_datetime(df["end_date"])
    df = df.sort_values("start_date")
    st.table(df[["event", "start_date", "end_date", "type"]].assign(
        start_date=lambda d: d["start_date"].dt.date, end_date=lambda d: d["end_date"].dt.date
    ))
    # highlight next upcoming event
    today = pd.Timestamp(date.today())
    upcoming = df[df["start_date"] >= today]
    if not upcoming.empty:
        next_event = upcoming.iloc[0]
        st.success(f"Next Important: **{next_event['event']}** on {next_event['start_date'].date()}")
    else:
        st.info("No upcoming events in the demo timeline. Add more events via code or CSV upload.")

    # allow upload of timeline CSV
    st.markdown("### Upload timeline CSV (optional)")
    t_uploaded = st.file_uploader("CSV columns: event,start_date(YYYY-MM-DD),end_date,type", type=["csv"], key="timeline_upl")
    if t_uploaded:
        try:
            tdf = pd.read_csv(t_uploaded)
            tdf["start_date"] = pd.to_datetime(tdf["start_date"]).dt.date
            tdf["end_date"] = pd.to_datetime(tdf["end_date"]).dt.date
            st.dataframe(tdf)
            csv_bytes, fname = download_df_as_csv_bytes(tdf, name="uploaded_timeline.csv")
            st.download_button("⬇️ Download uploaded timeline", data=csv_bytes, file_name=fname, mime="text/csv")
        except Exception as e:
            st.error(f"Upload failed: {e}")

def page_resources_faqs():
    st.header("📚 Study Resources & Scholarships")
    st.write("Curated list of free and official resources to help you get started.")
    for r in study_resources:
        st.markdown(f"**{r['title']}** — *{r['type']}*  \n{r['note']}  \nLink: {r['link']}")
    st.markdown("---")
    st.header("❓ Frequently Asked Questions")
    with st.expander("Is graduation worth it vs short-term courses?"):
        st.write("Graduation gives broader options (higher studies, government jobs, eligibility for many roles). "
                 "Short-term courses are good for quick entry but may limit long-term progression. Consider hybrid: degree + short-term skill courses.")
    with st.expander("What if I like two streams equally?"):
        st.write("Try small projects, internships or online courses in both areas. Choose the one you can work on consistently for years.")
    with st.expander("How to improve chances for competitive exams (JEE/NEET/CA)?"):
        st.write("Start early, follow a structured study plan, practice mock tests regularly, and join coaching if required.")
    with st.expander("Can vocational students pursue higher education?"):
        st.write("Yes. Many vocational diplomas allow lateral entry to degree courses or higher diplomas; skill experience is valued by industry.")
    st.markdown("### Quick Career Tips")
    for t in career_tips:
        st.markdown(f"- {t}")

def page_about():
    st.header("ℹ️ About this Project")
    st.markdown(
        """
        **One-Stop Career & Education Advisor** is a beginner-friendly Streamlit prototype for helping students
        choose academic streams and plan careers. It is a rules-based guidance tool and a starting point for a larger system.
        """
    )
    st.markdown("**What you can add next (future work):**")
    st.markdown("- Integrate a full government colleges dataset (with programs & cut-offs).")
    st.markdown("- Add regional language support and offline features.")
    st.markdown("- Build an ML-based recommender using student historical outcomes and stronger psychometrics.")
    st.markdown("- Integrate an admin panel for counselors to add timelines, college data, and local events.")

# ------------------ NAVIGATION ------------------
if side_nav == "Home":
    page_home()
elif side_nav == "Quiz":
    page_quiz()
elif side_nav == "Course → Career":
    page_roadmap()
elif side_nav == "Colleges Directory":
    page_colleges()
elif side_nav == "Timeline":
    page_timeline()
elif side_nav == "Resources & FAQs":
    page_resources_faqs()
elif side_nav == "About":
    page_about()
else:
    page_home()

# ------------------ FOOTER ------------------
st.markdown("---")
st.caption("Built with ❤️ using Streamlit — demo data only. Replace sample CSVs with real data to deploy in the field.")
