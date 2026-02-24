# app_unique_modern.py
import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_lottie import st_lottie
import requests

# ---------------- Page Config ----------------
st.set_page_config(page_title="Student Skill Dashboard", layout="centered")

# ---------------- CSS ----------------
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stApp {background: linear-gradient(to bottom, #fdfbfb, #ebedee); color:#111827;}

/* Hero Card */
.hero-card { background: linear-gradient(135deg,#a1c4fd,#c2e9fb); padding:25px; border-radius:25px; margin-bottom:20px; text-align:center; box-shadow: 0 5px 20px rgba(0,0,0,0.1);}
.profile-pic {border-radius:50%; width:100px; height:100px; object-fit:cover; margin-bottom:15px;}

/* Mini Radials inside Hero */
.mini-radial { display:inline-block; margin:0 10px; }

/* Step Cards */
.step-card { background:#ffffff; padding:20px; border-radius:20px; box-shadow:0 5px 15px rgba(0,0,0,0.1); margin-bottom:20px; }

/* Roadmap */
.roadmap-card { background:#ffffff; padding:20px; border-left:10px solid; border-radius:15px; margin-bottom:15px; }
</style>
""", unsafe_allow_html=True)

# ---------------- Lottie ----------------
def load_lottie(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_success = load_lottie("https://assets10.lottiefiles.com/packages/lf20_jbrw3hcz.json")
lottie_improve = load_lottie("https://assets2.lottiefiles.com/packages/lf20_jtbfg2nb.json")
lottie_hero = load_lottie("https://assets2.lottiefiles.com/packages/lf20_hzgq1iov.json")

# ---------------- Dataset ----------------
@st.cache_data
def load_data():
    try:
        return pd.read_csv("student_performance_extended.csv")
    except:
        return pd.DataFrame()
data = load_data()

# ---------------- Prediction ----------------
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

def readiness_breakdown(info):
    academics = min(int(info["gpa"]*3),30)
    skills = 20 if info["skill_level"]=="Advanced" else 15 if info["skill_level"]=="Intermediate" else 10
    routine = 20 if info["sleep_hours"]>=7 else 15 if info["sleep_hours"]>=6 else 8
    communication = 20 if info["communication"]=="Good" else 15 if info["communication"]=="Average" else 8
    total = min(academics+skills+routine+communication,100)
    return {"Academics":academics,"Skills":skills,"Routine":routine,"Communication":communication,"Total":total}

# ---------------- Hero ----------------
st.markdown('<div class="hero-card">', unsafe_allow_html=True)
st_lottie(lottie_hero,height=150)
name = st.text_input("Student Name")
profile_pic = st.text_input("Profile Picture URL (optional)")
year = st.selectbox("Year",[1,2,3,4])
branch = st.selectbox("Branch",["CSE","IT","ECE","EEE"])
gpa = st.slider("GPA",0.0,10.0,7.0,0.1)
study_hours = st.slider("Study Hours",0,12,3)
failures = st.number_input("Failures",0,10,0)
sleep_hours = st.slider("Sleep Hours",0,12,6)
skill_level = st.selectbox("Skill Level",["Beginner","Intermediate","Advanced"])
stress_level = st.selectbox("Stress Level",["Low","Medium","High"])
communication = st.selectbox("Communication",["Poor","Average","Good"])

if profile_pic:
    st.markdown(f'<img src="{profile_pic}" class="profile-pic">',unsafe_allow_html=True)
st.markdown(f"<h2>{name or 'Student Name'}</h2>",unsafe_allow_html=True)
st.markdown(f"<p>Year {year} | Branch: {branch}</p>",unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ---------------- Generate Dashboard ----------------
if st.button("Generate Dashboard"):

    info = {"gpa":gpa,"study_hours":study_hours,"failures":failures,"sleep_hours":sleep_hours,
            "skill_level":skill_level,"stress_level":stress_level,"communication":communication}

    # Readiness & Placement Mini Radials
    score = readiness_breakdown(info)
    placement_score, placement_level = placement_success_prediction(info)
    st.markdown(f'''
    <div style="text-align:center">
        <div class="mini-radial"><b>Readiness</b><br>{score['Total']}%</div>
        <div class="mini-radial"><b>Placement</b><br>{placement_score}%</div>
    </div>
    ''',unsafe_allow_html=True)

    # Metrics Step Cards
    metrics = {"GPA":gpa,"Study Hours":study_hours,"Skill Level":skill_level,
               "Sleep Hours":sleep_hours,"Communication":communication}
    for k,v in metrics.items():
        st.markdown(f'<div class="step-card"><h4>{k}</h4><p style="font-size:22px">{v}</p></div>',unsafe_allow_html=True)

    # Placement Status with Animation
    if placement_level=="High":
        st.success("High chances 🎉")
        st_lottie(lottie_success,height=150)
    elif placement_level=="Medium":
        st.warning("Moderate chances")
    else:
        st.error("Low chances")
        st_lottie(lottie_improve,height=150)

    # 4-Week Roadmap Modern Style
    roadmap = [
        ("Week 1","📖 Fundamentals","#ff6f61"),
        ("Week 2","⚙️ Practice + Mini Project","#f9d423"),
        ("Week 3","🛠 Major Project","#6a2c70"),
        ("Week 4","🎯 Resume + Mock Interview","#4a90e2")
    ]
    st.markdown("<h3>🧭 4-Week Skill Roadmap</h3>",unsafe_allow_html=True)
    for week,title,color in roadmap:
        st.markdown(f'<div class="roadmap-card" style="border-color:{color}"><b>{week}:</b> {title}</div>',unsafe_allow_html=True)

    # Analytics Dashboard
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

# Dataset Preview
with st.expander("📊 Dataset Preview"):
    st.dataframe(data)

st.caption("🚀 Unique Modern Student Skill Dashboard | Gradient Hero | Colorful Roadmap | Analytics")
