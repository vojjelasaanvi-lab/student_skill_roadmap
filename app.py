import streamlit as st
import pandas as pd
from datetime import date

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Student Skill Roadmap", layout="wide")

# ---------------- CSS ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #020617, #0f172a, #1e293b);
    color: white;
}
.card {
    background: rgba(30, 41, 59, 0.7);
    padding: 20px;
    border-radius: 16px;
    margin-bottom: 20px;
}
h1, h2, h3 {
    color: #e2e8f0;
}
.stButton > button {
    background: linear-gradient(135deg, #6366f1, #22c55e);
    color: white;
    font-weight: bold;
}
section[data-testid="stSidebar"] {
    background: #020617;
}
</style>
""", unsafe_allow_html=True)

# ---------------- DATA ----------------
@st.cache_data
def load_data():
    df = pd.read_csv("student_performance_final.csv")
    df.columns = df.columns.str.lower()
    return df

data = load_data()

def safe_unique(df, col, fallback):
    return sorted(df[col].dropna().unique()) if col in df.columns else fallback

years = safe_unique(data, "year", [1,2,3,4])
branches = safe_unique(data, "branch", ["CSE","ECE","EEE"])
interests = safe_unique(data, "interest", ["ML","Web","DSA"])
budgets = ["Low","Medium","High"]
skill_levels = ["Beginner","Intermediate","Advanced"]
stress_levels = ["Low","Medium","High"]
conf_levels = ["Low","Medium","High"]
comm_levels = ["Poor","Average","Good"]

# ---------------- SIDEBAR ----------------
st.sidebar.title("🎓 Skill Roadmap")
page = st.sidebar.radio(
    "Navigate",
    ["🏠 Home", "🧠 Build Roadmap", "🧩 Skill Analysis", "📊 Dataset"]
)

# ---------------- HOME ----------------
if page == "🏠 Home":
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #1e293b, #0f172a);
        padding: 60px;
        border-radius: 20px;
        text-align: center;
        color: white;">
        <h1>🎯 Student Skill Roadmap</h1>
        <p>Build your personalized career roadmap 🚀</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    col1.metric("📊 Analysis", "Data Driven")
    col2.metric("🧠 Planning", "4 Weeks")
    col3.metric("🎯 Output", "Career Ready")

# ---------------- ROADMAP ----------------
if page == "🧠 Build Roadmap":

    st.header("📋 Student Profile")

    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Name")
        year = st.selectbox("Year", years)
        branch = st.selectbox("Branch", branches)
        gpa = st.slider("GPA", 0.0, 10.0, 7.0)

    with col2:
        study_hours = st.slider("Study Hours", 0, 12, 3)
        sleep_hours = st.slider("Sleep Hours", 0, 12, 6)
        hostel = st.selectbox("Hostel", ["Yes","No"])
        family_support = st.selectbox("Family Support", ["Low","Medium","High"])

    st.divider()

    st.header("🎯 Career Preferences")
    col3, col4 = st.columns(2)

    with col3:
        interest = st.selectbox("Interest", interests)
        skill_level = st.selectbox("Skill Level", skill_levels)

    with col4:
        budget = st.selectbox("Budget", budgets)
        communication = st.selectbox("Communication", comm_levels)

    st.divider()

    st.header("⚠️ Mental State")
    col5, col6 = st.columns(2)

    with col5:
        stress_level = st.selectbox("Stress", stress_levels)
    with col6:
        confusion_level = st.selectbox("Confusion", conf_levels)

    # ---------------- BUTTON ----------------
    if st.button("🚀 Generate Roadmap"):

        # Simple readiness score
        score = int((gpa*5) + (study_hours*3) + (sleep_hours*2))

        st.success(f"Roadmap Generated for {name or 'Student'} 🎉")

        # Dashboard
        st.markdown("## 📊 Dashboard")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("GPA", gpa)
        c2.metric("Study", study_hours)
        c3.metric("Sleep", sleep_hours)
        c4.metric("Score", f"{score}/100")

        st.progress(score/100)

        # Tabs
        tab1, tab2, tab3, tab4 = st.tabs(["🧭 Roadmap","🗓️ Plan","🚀 Projects","📚 Resources"])

        with tab1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.write("🎯 Focus on your selected interest:", interest)
            st.write("📈 Improve consistency and build projects")
            st.markdown('</div>', unsafe_allow_html=True)

        with tab2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.write("Week 1: Basics")
            st.write("Week 2: Core")
            st.write("Week 3: Practice")
            st.write("Week 4: Project")
            st.markdown('</div>', unsafe_allow_html=True)

        with tab3:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.write("• Portfolio Project")
            st.write("• Mini App")
            st.write("• Real-world Project")
            st.markdown('</div>', unsafe_allow_html=True)

        with tab4:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.write("• YouTube")
            st.write("• Coursera")
            st.write("• NPTEL")
            st.markdown('</div>', unsafe_allow_html=True)

# ---------------- SKILL ANALYSIS ----------------
if page == "🧩 Skill Analysis":

    JOBS = {
        "Software Developer": ["Python","DSA","SQL","Git"],
        "Data Scientist": ["Python","Pandas","ML","Stats"],
        "Web Developer": ["HTML","CSS","JS","React"]
    }

    st.header("🧩 Skill Gap Analysis")

    role = st.selectbox("Choose Role", list(JOBS.keys()))
    skills = JOBS[role]

    st.write("Required Skills:", ", ".join(skills))

    known = st.multiselect("Your Skills", skills)

    if known:
        match = int(len(known)/len(skills)*100)
        st.progress(match/100)
        st.write(f"Match: {match}%")

        st.subheader("Missing Skills")
        for s in skills:
            if s not in known:
                st.write("❌", s)

# ---------------- DATASET ----------------
if page == "📊 Dataset":
    st.header("Dataset Preview")
    st.dataframe(data)
