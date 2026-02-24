# app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from streamlit_lottie import st_lottie
import requests

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="Student Skill Roadmap",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ---------------- Custom Colors & CSS ----------------
st.markdown("""
<style>
/* Hide menu/footer */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* App background */
.stApp {
    background: linear-gradient(to bottom, #0f172a, #1e293b);
    color: white;
}

/* Cards */
.card {
    background-color: #1e293b;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 5px 15px rgba(0,0,0,0.4);
    margin-bottom: 20px;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(135deg, #2563eb, #7c3aed);
    color: white;
    border-radius: 10px;
    height: 45px;
    width: 100%;
    font-weight: bold;
}

/* Metrics */
[data-testid="metric-container"] {
    background-color: #334155;
    border-radius: 12px;
    padding: 10px;
    margin-bottom: 10px;
}

/* Center Lottie */
.lottie-container {
    display: flex;
    justify-content: center;
    align-items: center;
}
</style>
""", unsafe_allow_html=True)

# ---------------- Load Dataset ----------------
@st.cache_data
def load_data():
    try:
        return pd.read_csv("student_performance_extended.csv")
    except FileNotFoundError:
        st.warning("Dataset not found.")
        return pd.DataFrame()

data = load_data()

# ---------------- Lottie Animations ----------------
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_success = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_jbrw3hcz.json")
lottie_improve = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_jtbfg2nb.json")

# ---------------- Placement Prediction ----------------
def placement_success_prediction(info):
    score = 0
    gpa = float(info.get("gpa", 0))
    score += 25 if gpa >= 8 else 20 if gpa >= 7 else 15 if gpa >= 6 else 8

    sh = int(info.get("study_hours", 0))
    score += 15 if sh >= 5 else 10 if sh >= 3 else 5

    skill = info.get("skill_level", "Beginner")
    score += 20 if skill == "Advanced" else 15 if skill == "Intermediate" else 8

    comm = info.get("communication", "Average")
    score += 15 if comm == "Good" else 10 if comm == "Average" else 5

    stress = info.get("stress_level", "Medium")
    score += 10 if stress == "Low" else 7 if stress == "Medium" else 4

    sleep = int(info.get("sleep_hours", 6))
    score += 10 if sleep >= 7 else 7 if sleep >= 6 else 4

    failures = int(info.get("failures", 0))
    score -= min(failures * 2, 5)

    score = max(0, min(score, 100))
    level = "High" if score >= 75 else "Medium" if score >= 50 else "Low"
    return score, level

# ---------------- Readiness Score ----------------
def readiness_breakdown(info):
    academics = min(int(info["gpa"] * 3), 30)
    skills = 20 if info["skill_level"] == "Advanced" else 15 if info["skill_level"] == "Intermediate" else 10
    routine = 20 if info["sleep_hours"] >= 7 else 15 if info["sleep_hours"] >= 6 else 8
    communication = 20 if info["communication"] == "Good" else 15 if info["communication"] == "Average" else 8
    total = min(academics + skills + routine + communication, 100)
    return {
        "Academics": academics,
        "Skills": skills,
        "Routine": routine,
        "Communication": communication,
        "Total": total
    }

# ---------------- Main Inputs (Vertical) ----------------
st.markdown('<div class="card"><h2>🎓 Student Skill Roadmap Dashboard</h2><p>Rule-Based Placement Predictor</p></div>', unsafe_allow_html=True)

name = st.text_input("Student Name")
year = st.selectbox("Year", [1,2,3,4])
branch = st.selectbox("Branch", ["CSE", "IT", "ECE", "EEE"])
gpa = st.slider("GPA", 0.0, 10.0, 7.0, 0.1)
study_hours = st.slider("Study Hours", 0, 12, 3)
failures = st.number_input("Failures", 0, 10, 0)
sleep_hours = st.slider("Sleep Hours", 0, 12, 6)
skill_level = st.selectbox("Skill Level", ["Beginner", "Intermediate", "Advanced"])
stress_level = st.selectbox("Stress Level", ["Low", "Medium", "High"])
communication = st.selectbox("Communication", ["Poor", "Average", "Good"])

if st.button("🔍 Generate Report"):

    student_info = {
        "gpa": gpa,
        "study_hours": study_hours,
        "failures": failures,
        "sleep_hours": sleep_hours,
        "skill_level": skill_level,
        "stress_level": stress_level,
        "communication": communication
    }

    # ---------------- Readiness Score ----------------
    score = readiness_breakdown(student_info)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📈 Readiness Score")
    st.progress(score["Total"]/100)
    st.metric("📚 Academics", f'{score["Academics"]}/30')
    st.metric("🧠 Skills", f'{score["Skills"]}/20')
    st.metric("🛌 Routine", f'{score["Routine"]}/20')
    st.metric("💬 Communication", f'{score["Communication"]}/20')
    st.markdown('</div>', unsafe_allow_html=True)

    # ---------------- Placement Prediction ----------------
    placement_score, placement_level = placement_success_prediction(student_info)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🎯 Placement Success Prediction")
    st.progress(placement_score/100)
    st.write(f"Placement Score: {placement_score}/100")

    # Lottie Animations
    if placement_level=="High":
        st.success("High chances of placement! 🎉")
        st_lottie(lottie_success, height=200)
    elif placement_level=="Medium":
        st.warning("Moderate chances — Improve consistency.")
    else:
        st.error("Low chances — Immediate improvement needed.")
        st_lottie(lottie_improve, height=200)
    st.markdown('</div>', unsafe_allow_html=True)

    # ---------------- Animated Plotly Chart ----------------
    if not data.empty and {"year","gpa","study_hours"}.issubset(data.columns):
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📊 Year-wise GPA Progression (Animated)")
        fig = px.scatter(
            data,
            x="study_hours",
            y="gpa",
            animation_frame="year",
            color="skill_level",
            template="plotly_dark",
            size_max=30
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ---------------- 4-Week Skill Roadmap ----------------
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🧭 4-Week Skill Plan")
    st.write("Week 1: Fundamentals")
    st.write("Week 2: Practice + Mini Project")
    st.write("Week 3: Major Project")
    st.write("Week 4: Resume + Mock Interview")
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- Dataset Preview ----------------
with st.expander("📊 Dataset Preview"):
    st.dataframe(data)

st.caption("Mini RTP Project | Student Skill Roadmap System")
