# **COMPLETE ENHANCED STUDENT SKILL ROADMAP - FULL CODE**

```python
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random
from datetime import date, timedelta
import numpy as np
import time

# ---------------- ENHANCED PAGE CONFIG ----------------
st.set_page_config(
    page_title="🚀 Student Skill Roadmap Pro", 
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
/* Premium Dark Theme */
.stApp {
    background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
}

/* Glassmorphism Cards */
.card {
    background: rgba(255,255,255,0.1);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 20px;
    padding: 25px;
    margin: 10px 0;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}

/* Animated Progress */
.progress-fill {
    background: linear-gradient(90deg, #10b981, #059669);
    height: 8px;
    border-radius: 4px;
    transition: width 0.5s ease;
}

/* Metric Cards */
[data-testid="metric-container"] {
    background: rgba(51, 65, 85, 0.8);
    padding: 20px;
    border-radius: 15px;
    border: 1px solid rgba(255,255,255,0.1);
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 12px 24px;
    font-weight: 600;
    transition: all 0.3s;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE INIT ----------------
def init_session_state():
    defaults = {
        "step": 1,
        "profile": {},
        "progress": {"week1": 0, "week2": 0, "week3": 0, "week4": 0, "streak": 0},
        "challenges_completed": 0,
        "daily_tip_seen": False,
        "roadmap_generated": False
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# ---------------- MOCK DATASET ----------------
@st.cache_data
def load_data():
    data = pd.DataFrame({
        'year': [1,2,2,3,3,1,4,2,3,2],
        'branch': ['CSE','CSE','ECE','CSE','EEE','CSE','ECE','CSE','MECH','CSE'],
        'gpa': [7.2,8.1,6.8,7.9,6.5,8.4,7.3,8.0,6.9,7.6],
        'study_hours': [4,6,3,5,2,7,4,6,3,5],
        'skill_level': ['Intermediate','Advanced','Beginner','Intermediate','Beginner','Advanced','Intermediate','Advanced','Beginner','Intermediate'],
        'interest': ['ML','Web','DSA','ML','Power','DSA','Embedded','ML','CAD','Web']
    })
    return data

data = load_data()

# ---------------- ENHANCED COURSE DB (Your existing one) ----------------
COURSE_DB = {
    "ML": {
        "courses": ["Andrew Ng ML (Coursera)", "Krish Naik YouTube", "fast.ai"],
        "weeks": ["Python+Basics", "Scikit-learn", "Feature Eng", "Deploy Project"],
        "projects": ["House Price Predictor", "Student Dashboard", "Customer Segments"]
    },
    "WEB": {
        "courses": ["Odin Project", "freeCodeCamp", "React Crash Course"],
        "weeks": ["HTML/CSS", "JavaScript", "React", "Deploy Portfolio"],
        "projects": ["Portfolio", "To-do App", "E-commerce UI"]
    },
    # Add your full COURSE_DB here...
}

# ---------------- HELPER FUNCTIONS ----------------
def detect_category(interest):
    s = str(interest).lower()
    if any(x in s for x in ["ml", "ai", "data"]): return "ML"
    if "web" in s or "app" in s: return "WEB"
    if "dsa" in s or "coding" in s: return "DSA"
    return "DSA"

def generate_roadmap(info):
    category = detect_category(info["interest"])
    data = COURSE_DB.get(category, COURSE_DB["DSA"])
    
    return {
        "goals": [f"Master {info['interest']} in 4 weeks", "Build 3 portfolio projects"],
        "week_plan": [
            {"title": "Week 1: Foundation", "tasks": data["weeks"][0].split()[:3]},
            {"title": "Week 2: Core Skills", "tasks": data["weeks"][1].split()[:3]},
            {"title": "Week 3: Projects", "tasks": ["Build project 1", "Deploy", "Document"]},
            {"title": "Week 4: Polish", "tasks": ["Portfolio", "LinkedIn", "Share"]}
        ],
        "projects": data["projects"],
        "resources": data["courses"]
    }

def readiness_score(info):
    gpa_score = min(30, max(0, (info.get("gpa", 0) - 5) * 6))
    study_score = min(30, info.get("study_hours", 0) * 6)
    routine_score = min(20, (info.get("sleep_hours", 6) / 12) * 20)
    skill_score = min(20, 5 if info.get("skill_level") == "Beginner" else 12 if "Intermediate" else 20)
    return int(gpa_score + study_score + routine_score + skill_score)

def calculate_job_fit(job_role, info):
    # Mock fit calculation
    base_fit = random.randint(60, 95)
    return base_fit + (info.get("gpa", 0) - 7) * 2

# ---------------- DAILY TIPS ----------------
DAILY_TIPS = [
    "Study in 25-min Pomodoro sessions 🚀",
    "Code daily > binge study 📱", 
    "Explain concepts to a rubber duck 🦆",
    "Build projects > collect certificates 🛠️",
    "Join 1 Discord coding community 💬"
]

# ---------------- MAIN APP ----------------

# HERO SECTION
st.markdown("""
<div style='text-align:center; padding: 2rem;'>
    <h1 style='color:#fff; font-size:3rem;'>🎯 Student Skill Roadmap Pro</h1>
    <p style='color:#a0a0a0; font-size:1.2rem;'>Track progress • AI Coach • Job Matcher • Weekly Challenges</p>
</div>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR PROFILE ----------------
with st.sidebar:
    st.markdown("### 👤 Your Profile")
    if st.session_state.get("profile"):
        st.metric("🎓 GPA", st.session_state.profile.get("gpa", 0))
        st.metric("📚 Study Hrs", st.session_state.profile.get("study_hours", 0))
        st.metric("🎯 Interest", st.session_state.profile.get("interest", ""))
    
    if st.button("✨ New Roadmap", use_container_width=True):
        st.session_state.step = 1
        st.session_state.roadmap_generated = False
    st.divider()
    st.caption("💾 Auto-saves progress")

# ---------------- STEP 1: QUICK ASSESSMENT ----------------
if st.session_state.step == 1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("👤 Step 1: Quick Profile")
    
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Name", st.session_state.profile.get("name", ""))
        year = st.selectbox("Year", [1,2,3,4], index=st.session_state.profile.get("year", 1)-1)
        branch = st.selectbox("Branch", ["CSE", "ECE", "EEE", "MECH"], 
                            index=["CSE", "ECE", "EEE", "MECH"].index(st.session_state.profile.get("branch", "CSE")))
    
    with col2:
        gpa = st.slider("GPA", 0.0, 10.0, st.session_state.profile.get("gpa", 7.0), 0.1)
        study_hours = st.slider("Daily Study Hours", 0, 12, st.session_state.profile.get("study_hours", 3))
        sleep_hours = st.slider("Sleep Hours", 0, 12, st.session_state.profile.get("sleep_hours", 6))
    
    interest = st.selectbox("🎯 Main Interest", 
                          ["ML/AI", "Web Dev", "DSA", "Cybersecurity", "Embedded", "Power Systems"])
    skill_level = st.selectbox("Skill Level", ["Beginner", "Intermediate", "Advanced"])
    
    if st.button("🚀 Next: Generate Roadmap", use_container_width=True):
        profile = {
            "name": name, "year": year, "branch": branch, "gpa": gpa,
            "study_hours": study_hours, "sleep_hours": sleep_hours,
            "interest": interest, "skill_level": skill_level
        }
        st.session_state.profile = profile
        st.session_state.step = 2
        st.session_state.roadmap_generated = True
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- MAIN DASHBOARD ----------------
elif st.session_state.roadmap_generated:
    student_info = st.session_state.profile
    roadmap = generate_roadmap(student_info)
    score = readiness_score(student_info)
    
    # ---------------- METRICS ROW ----------------
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("📊 Your Dashboard")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🎓 GPA", f"{student_info['gpa']:.1f}", delta="0.3")
    with col2:
        st.metric("📚 Study Hrs", student_info['study_hours'], delta="+1")
    with col3:
        st.metric("😴 Sleep", student_info['sleep_hours'], delta=None)
    with col4:
        st.metric("🔥 Readiness", f"{score}%", delta="+12")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ---------------- TABS ----------------
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🧭 Roadmap", "📊 Progress", "💼 Jobs", "🤖 Coach", "🎮 Challenges"])
    
    with tab1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🎯 Your 4-Week Plan")
        for week in roadmap["week_plan"]:
            with st.expander(f"📅 {week['title']}"):
                for task in week["tasks"]:
                    st.checkbox(task)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="card">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("🚀 Projects")
            for proj in roadmap["projects"]:
                st.write(f"• {proj}")
        with col2:
            st.subheader("📚 Resources")
            for res in roadmap["resources"]:
                st.write(f"• {res}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.header("📈 Track Your Progress")
        
        # Progress Sliders
        col1, col2, col3, col4 = st.columns(4)
        weeks = ["Week 1", "Week 2", "Week 3", "Week 4"]
        for i, week in enumerate(weeks):
            with eval(f"col{i+1}"):
                prog = st.slider(week, 0, 100, st.session_state.progress[f"week{i+1}"], 
                               key=f"prog_{i}")
                st.session_state.progress[f"week{i+1}"] = prog
        
        # Progress Chart
        progress_vals = [st.session_state.progress[f"week{i+1}"] for i in range(4)]
        fig = px.line(x=weeks, y=progress_vals, markers=True,
                     title="Your Progress", color_discrete_sequence=['#10b981'])
        st.plotly_chart(fig, use_container_width=True)
        
        # Streak
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Mark Today Complete", use_container_width=True):
                st.session_state.progress["streak"] += 1
                st.rerun()
        with col2:
            st.metric("🔥 Current Streak", f"{st.session_state.progress['streak']} days")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        job_role = st.selectbox("🎯 Target Job Role", 
                               ["Software Developer", "Data Scientist", "Web Developer", "DevOps"])
        
        if job_role:
            fit_score = calculate_job_fit(job_role, student_info)
            
            col1, col2 = st.columns([2,1])
            with col1:
                st.metric("💰 Salary Range", "₹6-15LPA")
                st.metric("📈 Demand", "Very High")
                st.metric("🎯 Your Fit Score", f"{fit_score}%", delta="+5")
            with col2:
                st.progress(fit_score/100)
            
            st.subheader("✅ Skills You Need")
            skills = ["Python", "DSA", "Git", "React", "SQL"]
            known_skills = st.multiselect("Skills you know:", skills, default=skills[:2])
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("### 🟢 You Have")
                for skill in known_skills:
                    st.success(skill)
            with col2:
                st.markdown("### 🔴 Learn Next")
                missing = [s for s in skills if s not in known_skills]
                for skill in missing:
                    st.error(skill)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab4:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.header("🤖 AI Career Coach")
        
        if "messages" not in st.session_state:
            st.session_state.messages = [{"role": "assistant", "content": "Hi! Ask me about your roadmap, projects, job prep, or motivation tips! 🚀"}]
        
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        if prompt := st.chat_input("Ask your coach..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Mock AI responses
            responses = {
                "project": "Great project idea! Start with a simple version first, then add features. Need GitHub setup help?",
                "motivation": "Remember: consistency > intensity. 30 mins daily = results in 90 days! 💪",
                "job": f"For your {student_info['gpa']} GPA + {student_info['interest']}, target SDE-1 roles first.",
                "roadmap": "Week 1 focus: complete 80% tasks. Track in Progress tab!"
            }
            
            response = responses.get(random.choice(list(responses.keys())), "Great question! Here's my advice...")
            with st.chat_message("assistant"):
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab5:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.header("🎮 Weekly Challenges")
        
        challenges = [
            "Solve 5 LeetCode Easy problems",
            "Build a simple calculator app", 
            "Record 2-min self-intro video",
            "Write 1 LinkedIn post about learning",
            "Complete Week 1 roadmap tasks"
        ]
        
        challenge = random.choice(challenges)
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"### 🎯 **This Week's Challenge**")
            st.markdown(f"**{challenge}**")
        
        with col2:
            if st.button(f"✅ I Completed It!", use_container_width=True):
                st.session_state.challenges_completed += 1
                st.balloons()
                st.success("🎉 Challenge completed! You're crushing it!")
                st.rerun()
        
        st.metric("🏆 Challenges Completed", st.session_state.challenges_completed)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ---------------- DOWNLOAD ----------------
    st.markdown('<div class="card">', unsafe_allow_html=True)
    md_content = f"# Roadmap for {student_info.get('name', 'Student')}\n\n"
    md_content += f"**Readiness Score:** {score}%\n\n"
    md_content += "## Progress\n" + str(st.session_state.progress) + "\n\n"
    
    st.download_button(
        "⬇️ Download Full Roadmap (MD)",
        data=md_content,
        file_name=f"roadmap_{student_info.get('name', 'student')}.md",
        use_container_width=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- DAILY TIP ----------------
if not st.session_state.daily_tip_seen:
    with st.sidebar:
        tip = random.choice(DAILY_TIPS)
        st.info(f"💡 **Daily Tip**: {tip}")
        if st.button("✅ Got it"):
            st.session_state.daily_tip_seen = True
            st.rerun()

# ---------------- FOOTER ----------------
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.caption("
