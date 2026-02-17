import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import date
import requests

# ---------------- Page Config ----------------
st.set_page_config(page_title="Student Skill Roadmap", layout="centered")

# ---------------- Load Dataset ----------------
@st.cache_data
def load_data():
    return pd.read_csv("student_performance_extended.csv")

data = load_data()

# ---------------- Placement Prediction (Rule-Based) ----------------
def placement_success_prediction(info):
    score = 0

    gpa = float(info.get("gpa", 0))
    if gpa >= 8:
        score += 25
    elif gpa >= 7:
        score += 20
    elif gpa >= 6:
        score += 15
    else:
        score += 8

    sh = int(info.get("study_hours", 0))
    if sh >= 5:
        score += 15
    elif sh >= 3:
        score += 10
    else:
        score += 5

    skill = info.get("skill_level", "Beginner")
    if skill == "Advanced":
        score += 20
    elif skill == "Intermediate":
        score += 15
    else:
        score += 8

    comm = info.get("communication", "Average")
    if comm == "Good":
        score += 15
    elif comm == "Average":
        score += 10
    else:
        score += 5

    stress = info.get("stress_level", "Medium")
    if stress == "Low":
        score += 10
    elif stress == "Medium":
        score += 7
    else:
        score += 4

    sleep = int(info.get("sleep_hours", 6))
    if sleep >= 7:
        score += 10
    elif sleep >= 6:
        score += 7
    else:
        score += 4

    failures = int(info.get("failures", 0))
    score -= min(failures * 2, 5)

    score = max(0, min(score, 100))

    if score >= 75:
        level = "High"
    elif score >= 50:
        level = "Medium"
    else:
        level = "Low"

    return score, level

# ---------------- Readiness Score ----------------
def readiness_breakdown(info):
    academics = min(int(info["gpa"] * 3), 30)
    skills = 20 if info["skill_level"] == "Advanced" else 15 if info["skill_level"] == "Intermediate" else 10
    routine = 20 if info["sleep_hours"] >= 7 else 15 if info["sleep_hours"] >= 6 else 8
    communication = 20 if info["communication"] == "Good" else 15 if info["communication"] == "Average" else 8

    total = academics + skills + routine + communication
    total = min(total, 100)

    return {
        "Academics": academics,
        "Skills": skills,
        "Routine": routine,
        "Communication": communication,
        "Total": total
    }

# ---------------- Analytics Dashboard ----------------
def show_analytics_dashboard(df):
    st.markdown("## 📊 Advanced Analytics Dashboard")

    if df.empty:
        st.warning("Dataset is empty.")
        return

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Students", len(df))
    if "gpa" in df.columns:
        col2.metric("Average GPA", f"{df['gpa'].mean():.2f}")
    if "study_hours" in df.columns:
        col3.metric("Avg Study Hours", f"{df['study_hours'].mean():.2f}")

    st.divider()

    if "gpa" in df.columns and "study_hours" in df.columns:
        st.subheader("📈 GPA vs Study Hours")
        fig = px.scatter(df, x="study_hours", y="gpa",
                         color="gpa", template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

    if "branch" in df.columns and "gpa" in df.columns:
        st.subheader("🎓 Branch-wise Average GPA")
        branch_avg = df.groupby("branch")["gpa"].mean().reset_index()
        fig = px.bar(branch_avg, x="branch", y="gpa",
                     color="gpa", template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

    if "stress_level" in df.columns:
        st.subheader("😰 Stress Level Distribution")
        fig = px.histogram(df, x="stress_level",
                           color="stress_level", template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

    if "skill_level" in df.columns:
        st.subheader("🧠 Skill Level Distribution")
        fig = px.pie(df, names="skill_level",
                     template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

    if "year" in df.columns and "gpa" in df.columns:
        st.subheader("📚 Year-wise Performance")
        year_avg = df.groupby("year")["gpa"].mean().reset_index()
        fig = px.line(year_avg, x="year", y="gpa",
                      markers=True, template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

# ---------------- GitHub Pull Requests ----------------
@st.cache_data
def fetch_github_prs(owner, repo, token=None):
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls?state=all"
    headers = {"Authorization": f"token {token}"} if token else {}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch PRs: {response.status_code}")
        return []

# ---------------- UI ----------------
st.title("🎓 Student Skill Roadmap & Placement Predictor")
st.caption("RTP Project | Rule-Based Intelligence + Analytics Dashboard")

st.divider()

# Student Input
name = st.text_input("Student Name")
year = st.selectbox("Year", [1, 2, 3, 4])
branch = st.selectbox("Branch", ["CSE", "IT", "ECE", "EEE"])
gpa = st.slider("GPA", 0.0, 10.0, 7.0, 0.1)
study_hours = st.slider("Study Hours", 0, 12, 3)
failures = st.number_input("Failures", 0, 10, 0)
sleep_hours = st.slider("Sleep Hours", 0, 12, 6)
skill_level = st.selectbox("Skill Level", ["Beginner", "Intermediate", "Advanced"])
stress_level = st.selectbox("Stress Level", ["Low", "Medium", "High"])
communication = st.selectbox("Communication", ["Poor", "Average", "Good"])

st.divider()

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

    st.success(f"Report Generated for {name or 'Student'}")

    # Readiness Score
    score = readiness_breakdown(student_info)
    st.subheader("📈 Readiness Score")
    st.progress(score["Total"] / 100)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Academics", f'{score["Academics"]}/30')
    c2.metric("Skills", f'{score["Skills"]}/20')
    c3.metric("Routine", f'{score["Routine"]}/20')
    c4.metric("Communication", f'{score["Communication"]}/20')

    # Placement Prediction
    placement_score, placement_level = placement_success_prediction(student_info)
    st.subheader("🎯 Placement Success Prediction")
    st.progress(placement_score / 100)
    st.write(f"Placement Readiness Score: {placement_score}/100")

    if placement_level == "High":
        st.success("High chances of placement 🎉")
    elif placement_level == "Medium":
        st.warning("Moderate chances — Improve consistency.")
    else:
        st.error("Low chances — Immediate improvement needed.")

    st.caption("Rule-based placement evaluation (No ML used).")
    st.divider()

    # Tabs: Roadmap | Analytics | GitHub PRs
    tab1, tab2, tab3 = st.tabs(["🧭 Roadmap", "📊 Analytics", "🔀 GitHub PRs"])

    with tab1:
        st.write("### 4-Week Skill Plan")
        st.write("Week 1: Fundamentals")
        st.write("Week 2: Practice + Mini Project")
        st.write("Week 3: Major Project")
        st.write("Week 4: Resume + Mock Interview")

    with tab2:
        show_analytics_dashboard(data)

    with tab3:
        st.write("### Fetch GitHub Pull Requests")
        owner = st.text_input("GitHub Owner/User", "your-username", key="owner")
        repo = st.text_input("Repository Name", "your-repo", key="repo")
        token = st.text_input("GitHub Token (optional for private repos)", type="password", key="token")

        if st.button("Fetch PRs", key="fetch_prs"):
            prs = fetch_github_prs(owner, repo, token or None)
            if prs:
                for pr in prs:
                    st.markdown(f"**#{pr['number']} {pr['title']}** by {pr['user']['login']}")
                    st.write(f"State: {pr['state']} | Created at: {pr['created_at']}")
                    st.markdown("---")
            else:
                st.info("No pull requests found.")

st.divider()

with st.expander("📊 Dataset Preview"):
    st.dataframe(data)

st.caption("Mini RTP Project | Student Skill Roadmap System")














