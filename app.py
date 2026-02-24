# app_unique_corrected.py
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

# ---------------- Gradient Background & CSS ----------------
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.stApp { background: linear-gradient(to bottom, #e0f7fa, #f0f4c3); color: #111827; }

/* Hero Section */
.hero { background-color: rgba(255,255,255,0.8); border-radius: 25px; padding: 30px; text-align: center; box-shadow: 0px 5px 20px rgba(0,0,0,0.15); margin-bottom: 20px; }

/* Student Background Card */
.background-card { background-color: #ffffff; padding: 20px; border-radius: 20px; box-shadow: 0px 5px 15px rgba(0,0,0,0.1); margin-bottom: 20px; display:flex; align-items:center; }
.profile-pic { border-radius:50%; width:80px; height:80px; margin-right:20px; object-fit:cover; }

/* Step Cards */
.step-card { background-color: #ffffff; padding: 20px; border-left: 8px solid #2563eb; border-radius: 15px; margin-bottom: 20px; box-shadow: 0px 5px 15px rgba(0,0,0,0.1); }

/* Timeline */
.timeline { position: relative; margin: 20px 0; padding-left: 40px; }
.timeline::before { content: ''; position: absolute; left: 20px; top: 0; width: 4px; height: 100%; background: #2563eb; border-radius: 2px; }
.timeline-item { position: relative; margin-bottom: 20px; }
.timeline-item::before { content: ''; position: absolute; left: 12px; width: 16px; height: 16px; background: #ff6f61; border-radius: 50%; top: 0; }
</style>
""", unsafe_allow_html=True)

# ---------------- Load Dataset ----------------
@st.cache_data
def load_data():
    try:
        return pd.read_csv("student_performance_extended.csv")
    except:
        return pd.DataFrame()
data = load_data()

# ---------------- Lottie ----------------
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_success = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_jbrw3hcz.json")
lottie_improve = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_jtbfg2nb.json")
lottie_hero = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_hzgq1iov.json")

# ---------------- Placement Prediction ----------------
def placement_success_prediction(info):
    score = 0
    gpa = float(info.get("gpa",0))
    score += 25 if gpa>=8 else 20 if gpa>=7 else 15 if gpa>=6 else 8
    sh = int(info.get("study_hours",0))
    score += 15 if sh>=5 else 10 if sh>=3 else 5
    skill = info.get("skill_level","Beginner")
    score += 20 if skill=="Advanced" else 15 if skill=="Intermediate" else 8
    comm = info.get("communication","Average")
    score += 15 if comm=="Good" else 10 if comm=="Average" else 5
    stress = info.get("stress_level","Medium")
    score += 10 if stress=="Low" else 7 if stress=="Medium" else 4
    sleep = int(info.get("sleep_hours",6))
    score += 10 if sleep>=7 else 7 if sleep>=6 else 4
    failures = int(info.get("failures",0))
    score -= min(failures*2,5)
    score = max(0,min(score,100))
    level = "High" if score>=75 else "Medium" if score>=50 else "Low"
    return score, level

# ---------------- Readiness ----------------
def readiness_breakdown(info):
    academics = min(int(info["gpa"]*3),30)
    skills = 20 if info["skill_level"]=="Advanced" else 15 if info["skill_level"]=="Intermediate" else 10
    routine = 20 if info["sleep_hours"]>=7 else 15 if info["sleep_hours"]>=6 else 8
    communication = 20 if info["communication"]=="Good" else 15 if info["communication"]=="Average" else 8
    total = min(academics+skills+routine+communication,100)
    return {"Academics":academics,"Skills":skills,"Routine":routine,"Communication":communication,"Total":total}

# ---------------- Hero Section ----------------
st.markdown('<div class="hero"><h1>🚀 Student Skill Dashboard</h1><p>Track Readiness, Placement & Roadmap</p></div>', unsafe_allow_html=True)
st_lottie(lottie_hero,height=200)

# ---------------- Student Input ----------------
st.markdown('<div class="step-card"><h3>Enter Student Details</h3></div>', unsafe_allow_html=True)
name = st.text_input("Student Name")
profile_pic_url = st.text_input("Profile Picture URL (optional)")
year = st.selectbox("Year",[1,2,3,4])
branch = st.selectbox("Branch",["CSE","IT","ECE","EEE"])
gpa = st.slider("GPA",0.0,10.0,7.0,0.1)
study_hours = st.slider("Study Hours",0,12,3)
failures = st.number_input("Failures",0,10,0)
sleep_hours = st.slider("Sleep Hours",0,12,6)
skill_level = st.selectbox("Skill Level",["Beginner","Intermediate","Advanced"])
stress_level = st.selectbox("Stress Level",["Low","Medium","High"])
communication = st.selectbox("Communication",["Poor","Average","Good"])

if st.button("📊 Generate Dashboard"):

    info = {
        "gpa":gpa,
        "study_hours":study_hours,
        "failures":failures,
        "sleep_hours":sleep_hours,
        "skill_level":skill_level,
        "stress_level":stress_level,
        "communication":communication
    }

    # ---------------- Student Background ----------------
    pic_html = f'<img src="{profile_pic_url}" class="profile-pic">' if profile_pic_url else ''
    st.markdown(f'''
    <div class="background-card">{pic_html}
        <div>
            <h3>{name or "Student Name"}</h3>
            <p>Year: {year} | Branch: {branch}</p>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    # ---------------- Step Cards ----------------
    metrics = {
        "GPA": gpa,
        "Study Hours": study_hours,
        "Skill Level": skill_level,
        "Sleep Hours": sleep_hours,
        "Communication": communication
    }
    for key,value in metrics.items():
        st.markdown(f'<div class="step-card"><h4>{key}</h4><p style="font-size:22px">{value}</p></div>', unsafe_allow_html=True)

    # ---------------- Readiness Radial ----------------
    score = readiness_breakdown(info)
    st.markdown('<div class="step-card"><h4>Readiness Score</h4></div>', unsafe_allow_html=True)
    fig_radial = px.pie(names=["Completed","Remaining"], values=[score["Total"],100-score["Total"]],
                        hole=0.7, color_discrete_sequence=["#2563eb","#d1d5db"])
    fig_radial.update_layout(showlegend=False, margin=dict(t=0,b=0,l=0,r=0))
    st.plotly_chart(fig_radial,use_container_width=True)

    # ---------------- Placement ----------------
    placement_score, placement_level = placement_success_prediction(info)
    st.markdown('<div class="step-card"><h4>Placement Prediction</h4></div>', unsafe_allow_html=True)
    st.progress(placement_score/100)
    st.write(f"Score: {placement_score}/100")
    if placement_level=="High":
        st.success("High chances 🎉")
        st_lottie(lottie_success,height=150)
    elif placement_level=="Medium":
        st.warning("Moderate chances")
    else:
        st.error("Low chances")
        st_lottie(lottie_improve,height=150)

    # ---------------- 4-Week Roadmap ----------------
    st.markdown('<div class="step-card"><h4>🧭 4-Week Skill Roadmap</h4></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="timeline">
        <div class="timeline-item"><b>Week 1:</b> 📖 Fundamentals</div>
        <div class="timeline-item"><b>Week 2:</b> ⚙️ Practice + Mini Project</div>
        <div class="timeline-item"><b>Week 3:</b> 🛠 Major Project</div>
        <div class="timeline-item"><b>Week 4:</b> 🎯 Resume + Mock Interview</div>
    </div>
    """, unsafe_allow_html=True)

    # ---------------- Analytics ----------------
    if not data.empty:
        st.markdown('<div class="step-card"><h4>📊 Analytics Dashboard</h4></div>', unsafe_allow_html=True)
        st.metric("Total Students", len(data))
        if "gpa" in data.columns:
            st.metric("Average GPA", f"{data['gpa'].mean():.2f}")
        if "study_hours" in data.columns:
            st.metric("Average Study Hours", f"{data['study_hours'].mean():.2f}")
        if {"study_hours","gpa"}.issubset(data.columns):
            fig_scatter = px.scatter(data,x="study_hours",y="gpa",color="skill_level",
                                     template="plotly_white",title="GPA vs Study Hours")
            st.plotly_chart(fig_scatter,use_container_width=True)
        if {"branch","gpa"}.issubset(data.columns):
            branch_avg = data.groupby("branch")["gpa"].mean().reset_index()
            fig_bar = px.bar(branch_avg,x="branch",y="gpa",color="gpa",
                             template="plotly_white", title="Branch-wise GPA")
            st.plotly_chart(fig_bar,use_container_width=True)
        if "stress_level" in data.columns:
            fig_hist = px.histogram(data,x="stress_level",color="stress_level",
                                    template="plotly_white",title="Stress Levels")
            st.plotly_chart(fig_hist,use_container_width=True)
        if "skill_level" in data.columns:
            fig_pie = px.pie(data,names="skill_level",
                             template="plotly_white",title="Skill Levels")
            st.plotly_chart(fig_pie,use_container_width=True)

# ---------------- Dataset Preview ----------------
with st.expander("📊 Dataset Preview"):
    st.dataframe(data)

st.caption("🚀 Modern Student Skill Dashboard | Unique Design | Student Background + Correct Roadmap Order")
