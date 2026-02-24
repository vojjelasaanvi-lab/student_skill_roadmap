# app_unique_animated.py
import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_lottie import st_lottie
import requests

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="Student Skill Dashboard",
    layout="centered"
)

# ---------------- Animated Background & CSS ----------------
st.markdown("""
<style>

/* Hide default UI */
#MainMenu, footer, header { visibility: hidden; }

/* Full animated gradient */
.stApp {
  animation: gradientBG 12s ease infinite;
  background-size: 400% 400%;
  color: #111827;
}

@keyframes gradientBG {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

/* Hero card */
.hero-card {
  background: rgba(255,255,255,0.9);
  border-radius: 25px;
  padding: 25px;
  text-align: center;
  box-shadow: 0 8px 30px rgba(0,0,0,0.15);
  margin-bottom: 25px;
}

/* Student profile */
.profile-pic { border-radius:50%; width:100px; height:100px; object-fit:cover; margin-top:10px; }

/* Section card */
.section-card {
  background: #ffffff;
  padding: 18px;
  border-radius: 20px;
  box-shadow: 0 5px 18px rgba(0,0,0,0.1);
  margin-bottom: 20px;
}

/* Roadmap bars */
.roadmap-bar {
  background: #2563eb;
  border-radius: 15px;
  height: 12px;
  animation: slideIn 1.5s ease-out;
}
@keyframes slideIn {
  from { width: 0%; }
  to { width: 100%; }
}

</style>
""", unsafe_allow_html=True)

# ---------------- Lottie Loader ----------------
def load_lottie(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# New lively Lottie animation
lottie_banner = load_lottie("https://assets10.lottiefiles.com/packages/lf20_jtbfg2nb.json")
lottie_high = load_lottie("https://assets1.lottiefiles.com/packages/lf20_jbrw3hcz.json")
lottie_low = load_lottie("https://assets2.lottiefiles.com/packages/lf20_9ryr1i.json")

# ---------------- Load Dataset ----------------
@st.cache_data
def load_data():
    try:
        return pd.read_csv("student_performance_extended.csv")
    except:
        return pd.DataFrame()

data = load_data()

# ---------------- Placement Prediction Logic ----------------
def placement_success_prediction(info):
    score = 0
    gpa = float(info["gpa"]); score += 25 if gpa>=8 else 20 if gpa>=7 else 15 if gpa>=6 else 8
    sh = int(info["study_hours"]); score += 15 if sh>=5 else 10 if sh>=3 else 5
    skill = info["skill_level"]; score += 20 if skill=="Advanced" else 15 if skill=="Intermediate" else 8
    comm = info["communication"]; score += 15 if comm=="Good" else 10 if comm=="Average" else 5
    stress = info["stress_level"]; score += 10 if stress=="Low" else 7 if stress=="Medium" else 4
    sleep = int(info["sleep_hours"]); score += 10 if sleep>=7 else 7 if sleep>=6 else 4
    fail = int(info["failures"]); score -= min(fail*2,5)
    score = max(0, min(score,100))
    level = "High" if score>=75 else "Medium" if score>=50 else "Low"
    return score, level

# ---------------- Readiness Breakdown ----------------
def readiness_breakdown(info):
    acad = min(int(info["gpa"]*3),30)
    skills = 20 if info["skill_level"]=="Advanced" else 15 if info["skill_level"]=="Intermediate" else 10
    routine = 20 if info["sleep_hours"]>=7 else 15 if info["sleep_hours"]>=6 else 8
    comm = 20 if info["communication"]=="Good" else 15 if info["communication"]=="Average" else 8
    total = min(acad+skills+routine+comm,100)
    return {"Academics":acad,"Skills":skills,"Routine":routine,"Communication":comm,"Total":total}

# ---------------- Hero Banner ----------------
st.markdown('<div class="hero-card">', unsafe_allow_html=True)
st_lottie(lottie_banner, height=180)
st.markdown("<h1>🎓 Student Skill Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p>A dynamic place to track readiness, placements & skill progress</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ---------------- Student Input ----------------
name = st.text_input("Student Name")
profile_url = st.text_input("Profile Picture URL (optional)")
year = st.selectbox("Year",[1,2,3,4])
branch = st.selectbox("Branch", ["CSE","IT","ECE","EEE"])
gpa = st.slider("GPA",0.0,10.0,7.0,0.1)
study_hours = st.slider("Study Hours",0,12,3)
failures = st.number_input("Failures",0,10,0)
sleep_hours = st.slider("Sleep Hours",0,12,6)
skill_level = st.selectbox("Skill Level", ["Beginner","Intermediate","Advanced"])
stress_level = st.selectbox("Stress Level", ["Low","Medium","High"])
communication = st.selectbox("Communication", ["Poor","Average","Good"])

if st.button("Generate Dashboard"):

    info = {
        "gpa":gpa,
        "study_hours":study_hours,
        "failures":failures,
        "sleep_hours":sleep_hours,
        "skill_level":skill_level,
        "stress_level":stress_level,
        "communication":communication
    }

    # ---------------- Student Profile ----------------
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    if profile_url:
        st.image(profile_url, width=100)
    st.markdown(f"<h2>{name or 'Student Name'}</h2>", unsafe_allow_html=True)
    st.markdown(f"<p>Year: {year} | Branch: {branch}</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ---------------- Readiness & Placement ----------------
    score = readiness_breakdown(info)
    placement_score, placement_level = placement_success_prediction(info)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("<h3>📌 Summary</h3>", unsafe_allow_html=True)
    st.markdown(f"<p>Readiness Score: <b>{score['Total']}%</b></p>", unsafe_allow_html=True)
    st.markdown(f"<p>Placement Score: <b>{placement_score}%</b></p>", unsafe_allow_html=True)

    if placement_level=="High":
        st_lottie(lottie_high, height=150)
    elif placement_level=="Low":
        st_lottie(lottie_low, height=150)

    st.markdown('</div>', unsafe_allow_html=True)

    # ---------------- Vertical Metric Cards ----------------
    metrics = {"GPA":gpa, "Study Hours":study_hours,
               "Skill Level":skill_level, "Sleep Hours":sleep_hours,
               "Communication":communication}
    for label,val in metrics.items():
        st.markdown(f'<div class="section-card"><b>{label}:</b> {val}</div>', unsafe_allow_html=True)

    # ---------------- 4-Week Skill Roadmap ----------------
    st.markdown('<h3>🧭 4-Week Skill Roadmap</h3>', unsafe_allow_html=True)
    roadmap = [
        ("Week 1", "📖 Fundamentals", "40%"),
        ("Week 2", "⚙️ Practice + Mini Project", "60%"),
        ("Week 3", "🛠 Major Project", "80%"),
        ("Week 4", "🎯 Resume + Mock Interview", "100%")
    ]
    for week, desc, pct in roadmap:
        st.markdown(f'''
        <div class="section-card">
            <b>{week}:</b> {desc}
            <div class="roadmap-bar" style="width:{pct};"></div>
        </div>
        ''', unsafe_allow_html=True)

    # ---------------- Analytics ----------------
    if not data.empty:
        st.markdown('<div class="section-card"><h3>📊 Analytics Dashboard</h3>', unsafe_allow_html=True)
        st.metric("Total Students", len(data))
        if "gpa" in data.columns:
            st.metric("Average GPA", f"{data['gpa'].mean():.2f}")
        fig1 = None
        if {"study_hours","gpa"}.issubset(data.columns):
            fig1 = px.scatter(data,x="study_hours",y="gpa",color="skill_level",
                              template="plotly_white", title="GPA vs Study Hours")
            st.plotly_chart(fig1, use_container_width=True)
        if {"branch","gpa"}.issubset(data.columns):
            branch_avg = data.groupby("branch")["gpa"].mean().reset_index()
            fig2 = px.bar(branch_avg,x="branch",y="gpa",color="gpa",
                          template="plotly_white", title="Branch-wise GPA")
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

# ---------------- Dataset Preview ----------------
with st.expander("📊 Dataset Preview"):
    st.dataframe(data)

st.caption("🚀 Animated Modern Skill Dashboard")
