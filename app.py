








import streamlit as st
import pandas as pd
from datetime import date

# ---------------- Page config ----------------
st.set_page_config(page_title="Student Skill Roadmap", layout="centered")
# ---------------- UI THEME (HTML/CSS) ----------------
st.markdown("""
<style>
/* ===== Page background + font ===== */
.stApp{
  background: radial-gradient(1200px 600px at 10% 0%, rgba(99,102,241,.25), transparent 60%),
              radial-gradient(1000px 600px at 90% 10%, rgba(16,185,129,.18), transparent 55%),
              linear-gradient(180deg, #0b1220 0%, #070b14 100%);
  color: #e5e7eb;
}

/* Wider + clean spacing */
.block-container{
  padding-top: 2rem;
  padding-bottom: 2rem;
  max-width: 1050px;
}

/* Hide streamlit menu/footer */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* ===== Typography ===== */
h1, h2, h3 { letter-spacing: .2px; }
small, .stCaption { color: rgba(229,231,235,.75) !important; }

/* ===== Cards ===== */
.card{
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.10);
  border-radius: 18px;
  padding: 18px 18px;
  box-shadow: 0 12px 35px rgba(0,0,0,0.35);
  margin-bottom: 14px;
}

.card-title{
  font-size: 1.15rem;
  font-weight: 700;
  margin: 0 0 6px 0;
}
.card-sub{
  margin: 0;
  color: rgba(229,231,235,.75);
  font-size: .95rem;
}

/* ===== Inputs ===== */
.stTextInput input, .stNumberInput input, .stTextArea textarea{
  border-radius: 12px !important;
  border: 1px solid rgba(255,255,255,0.14) !important;
  background: rgba(255,255,255,0.06) !important;
}
.stSelectbox [data-baseweb="select"]{
  border-radius: 12px !important;
  background: rgba(255,255,255,0.06) !important;
  border: 1px solid rgba(255,255,255,0.14) !important;
}

/* Sliders */
.stSlider [data-baseweb="slider"]{
  padding-top: 6px;
}

/* ===== Buttons ===== */
.stButton button{
  width: 100%;
  border-radius: 14px;
  padding: 11px 14px;
  border: 1px solid rgba(255,255,255,0.18);
  background: linear-gradient(135deg, rgba(99,102,241,.95), rgba(16,185,129,.85));
  color: white;
  font-weight: 800;
}
.stButton button:hover{
  transform: translateY(-1px);
  filter: brightness(1.05);
}

/* ===== Tabs styling ===== */
.stTabs [data-baseweb="tab"]{
  border-radius: 12px;
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.10);
}
.stTabs [aria-selected="true"]{
  background: rgba(255,255,255,0.10) !important;
}

/* ===== Metrics ===== */
[data-testid="stMetric"]{
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.10);
  border-radius: 16px;
  padding: 14px 14px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.25);
}

/* Dataframe look */
[data-testid="stDataFrame"]{
  border-radius: 16px;
  overflow: hidden;
  border: 1px solid rgba(255,255,255,0.10);
}
</style>
""", unsafe_allow_html=True)


# ---------------- Load dataset ----------------
@st.cache_data
def load_data():
    df = pd.read_csv("student_performance_final.csv")
    df.columns = df.columns.str.lower()
    return df

data = load_data()

# ---------------- Helpers ----------------
def safe_unique(df, col, fallback):
    return sorted(df[col].dropna().unique()) if col in df.columns else fallback

def normalize_yes_no(x):
    if isinstance(x, str):
        x = x.strip().lower()
        if x in ("yes", "y", "true", "1"):
            return "Yes"
    return "No"

def get_similar_students(df, info):
    """Simple similarity filter (no ML): same year + branch + interest + skill_level if possible."""
    f = df.copy()

    # Normalize columns if present
    if "hostel" in f.columns:
        f["hostel"] = f["hostel"].apply(normalize_yes_no)

    # Apply filters only if columns exist
    for k, col in [
        ("year", "year"),
        ("branch", "branch"),
        ("interest", "interest"),
        ("skill_level", "skill_level"),
    ]:
        if col in f.columns and k in info and info[k] is not None:
            f = f[f[col] == info[k]]

    return f

def build_week_plan(interest, skill_level, budget_level):
    """A structured 4-week roadmap (generic but clean)."""
    free_note = "Use free resources (YouTube/NPTEL/free Coursera audits)." if budget_level == "Low" else "Consider 1 paid course + mentorship for speed."

    if skill_level == "Beginner":
        project = "Mini project: build a basic end-to-end demo"
        depth = "Focus on fundamentals + consistent practice"
    else:
        project = "Project: build a portfolio-grade real-world application"
        depth = "Focus on advanced concepts + real datasets + deployment"

    return [
        {
            "title": "Week 1 — Foundation",
            "bullets": [
                f"{depth} in **{interest}** (core concepts).",
                "Set up tools (GitHub, editor, notes).",
                "Daily practice: 45–60 mins.",
                free_note,
            ],
        },
        {
            "title": "Week 2 — Skill Building",
            "bullets": [
                "Solve 10–15 practice problems / exercises.",
                "Start a structured course + take notes.",
                "Build 1 small component (feature/module) daily.",
            ],
        },
        {
            "title": "Week 3 — Projects & Proof",
            "bullets": [
                project,
                "Add README + screenshots + clear steps.",
                "Push code daily to GitHub (commit streak).",
            ],
        },
        {
            "title": "Week 4 — Career Readiness",
            "bullets": [
                "Resume: add project + skills + links.",
                "Mock interview / presentations (2 sessions).",
                "Polish project + deploy (if possible).",
                "Plan next month based on gaps.",
            ],
        },
    ]

def generate_structured_roadmap(info, df):
    """Return a rich roadmap object (not just flat strings)."""
    steps = []
    risks = []
    habits = []
    goals = []

    # --- Data-driven insights from similar students ---
    sim = get_similar_students(df, info)
    sim_note = None
    if len(sim) >= 5:
        # Try to use columns if present
        avg_gpa = sim["gpa"].mean() if "gpa" in sim.columns else None
        avg_study = sim["study_hours"].mean() if "study_hours" in sim.columns else None
        if avg_gpa is not None and avg_study is not None:
            sim_note = f"Based on **{len(sim)} similar students** (same year/branch/interest/skill), average GPA is **{avg_gpa:.2f}** and average study hours is **{avg_study:.1f}/day**."
    else:
        sim_note = f"Not enough similar-student rows for strong stats (found {len(sim)}). Using rule-based roadmap."

    # --- Core goals ---
    goals.append(f"Build a clear learning path in **{info['interest']}**.")
    if info["gpa"] < 6.0:
        goals.append("Improve academic consistency (target +0.5 GPA in next semester).")
    if info["study_hours"] < 3:
        goals.append("Increase study hours gradually to a sustainable level.")
    if info["communication"] in ("Poor", "Low"):
        goals.append("Improve communication through weekly speaking/writing practice.")

    # --- Risks & fixes ---
    if info["stress_level"] == "High" or info["confusion_level"] == "High":
        risks.append("High stress/confusion can reduce consistency → use weekly planning + short focused sessions.")
        habits.append("10 min breathing/meditation + 25/5 Pomodoro (2 cycles).")

    if info["hostel"] == "Yes":
        habits.append("Hostel routine: fixed sleep + fixed study slot + limit late-night scrolling.")
    else:
        habits.append("Home routine: fixed study slot + communicate study time to family.")

    if info["family_support"] == "Low":
        steps.append("Get external support: mentor/teacher/peer group + online communities.")
    else:
        steps.append("Use family support: share weekly goals and ask for accountability.")

    if info["budget"] == "Low":
        steps.append("Use free resources first + build projects (proof > certificates).")
    else:
        steps.append("Pick 1 high-quality paid course OR mentorship for faster progress.")

    # --- Study upgrade ---
    if info["study_hours"] < 3:
        steps.append("Study plan: add +30 mins/week until you reach 3–4 hours/day.")
    if info["gpa"] < 6.0:
        steps.append("Academics: revise daily + weekly tests + focus on weak subjects.")

    # --- Communication ---
    if info["communication"] in ("Poor", "Low"):
        steps.append("Communication: 2 short talks/week + write 1 summary/day (5–7 lines).")

    week_plan = build_week_plan(info["interest"], info["skill_level"], info["budget"])

    # --- Resources by interest (simple mapping) ---
    interest_lower = str(info["interest"]).lower()
    if "data" in interest_lower or "ml" in interest_lower or "ai" in interest_lower:
        resources = [
            "NPTEL / YouTube: Python + ML basics",
            "Kaggle: datasets + notebooks",
            "GitHub: portfolio + README",
            "LeetCode/HackerRank: fundamentals (optional)",
        ]
        projects = [
            "Student performance prediction / analysis dashboard",
            "Mini recommender system",
            "Simple ML model + Streamlit deployment",
        ]
    elif "web" in interest_lower:
        resources = [
            "MDN Web Docs (HTML/CSS/JS)",
            "Frontend practice: small clones",
            "GitHub Pages / Vercel for deployment",
        ]
        projects = [
            "Portfolio website",
            "To-do app + local storage",
            "Mini full-stack CRUD app",
        ]
    else:
        resources = [
            "YouTube + NPTEL fundamentals",
            "One structured course (beginner → intermediate)",
            "Build 2–3 projects + document well",
        ]
        projects = [
            "1 mini project",
            "1 intermediate project",
            "1 portfolio-grade project",
        ]

    return {
        "similar_note": sim_note,
        "goals": goals,
        "risks": risks,
        "habits": habits,
        "steps": steps,
        "week_plan": week_plan,
        "resources": resources,
        "projects": projects,
    }


def roadmap_to_markdown(name, info, roadmap):
    def s(x):
        # Convert anything (including numpy types) to clean string
        try:
            if pd.isna(x):
              return ""
        except Exception:
            pass
        return str(x)

    lines = []
    lines.append(f"# Personalized Roadmap for {s(name) or 'Student'}")
    lines.append(f"**Generated on:** {date.today().isoformat()}")
    lines.append("")
    lines.append("## Profile")

    keys = [
        "year", "branch", "interest", "skill_level", "budget", "hostel",
        "study_hours", "gpa", "stress_level", "confusion_level",
        "communication", "family_support"
    ]
    for k in keys:
        lines.append(f"- **{k.replace('_',' ').title()}**: {s(info.get(k))}")

    lines.append("")
    lines.append("## Data Insight")
    lines.append(s(roadmap.get("similar_note", "")))
    lines.append("")
    lines.append("## Goals")
    for g in roadmap.get("goals", []):
        lines.append(f"- {s(g)}")

    lines.append("")
    risks = roadmap.get("risks", [])
    if risks:
        lines.append("## Risks to Watch")
        for r in risks:
            lines.append(f"- {s(r)}")
        lines.append("")

    lines.append("## Daily Habits")
    for h in roadmap.get("habits", []):
        lines.append(f"- {s(h)}")
    lines.append("")

    lines.append("## Action Steps")
    for step in roadmap.get("steps", []):
        lines.append(f"- {s(step)}")
    lines.append("")

    lines.append("## 4-Week Plan")
    for w in roadmap.get("week_plan", []):
        lines.append(f"### {s(w.get('title',''))}")
        for b in w.get("bullets", []):
            lines.append(f"- {s(b)}")
        lines.append("")

    lines.append("## Suggested Projects")
    for p in roadmap.get("projects", []):
        lines.append(f"- {s(p)}")
    lines.append("")

    lines.append("## Resources")
    for r in roadmap.get("resources", []):
        lines.append(f"- {s(r)}")
    lines.append("")

    return "\n".join(lines)
def clamp(x, lo, hi):
    return max(lo, min(hi, x))

def level_to_bucket(skill_level: str):
    s = str(skill_level).lower()
    if "begin" in s:
        return "Beginner"
    if "inter" in s:
        return "Intermediate"
    if "adv" in s:
        return "Advanced"
    return "Beginner"

def readiness_breakdown(info):
    # Academics (0–30)
    g = float(info.get("gpa", 0))
    if g >= 8: academics = 30
    elif g >= 7: academics = 26
    elif g >= 6: academics = 20
    elif g >= 5: academics = 14
    else: academics = 8

    # Skills (0–30) based on skill_level + study_hours
    lvl = level_to_bucket(info.get("skill_level", "Beginner"))
    sh = int(info.get("study_hours", 0))
    base = 12 if lvl == "Beginner" else 20 if lvl == "Intermediate" else 26
    bonus = 6 if sh >= 4 else 3 if sh >= 3 else 1
    skills = clamp(base + bonus, 0, 30)

    # Routine (0–20) sleep + stress + confusion
    sleep = int(info.get("sleep_hours", 6))
    stress = info.get("stress_level", "Medium")
    confusion = info.get("confusion_level", "Medium")

    routine = 0
    routine += 8 if sleep >= 7 else 5 if sleep >= 6 else 2
    routine += 6 if stress == "Low" else 4 if stress == "Medium" else 2
    routine += 6 if confusion == "Low" else 4 if confusion == "Medium" else 2
    routine = clamp(routine, 0, 20)

    # Communication (0–20)
    comm = str(info.get("communication", "Average"))
    communication = 20 if comm in ("Good", "High") else 14 if comm in ("Average", "Medium") else 8

    total = academics + skills + routine + communication  # /100
    return {
        "Academics": academics,
        "Skills": skills,
        "Routine": routine,
        "Communication": communication,
        "Total": clamp(total, 0, 100)
    }


# ---------------- UI ----------------
# st.title("🎓 Personalized Student Skill Roadmap")
# st.caption("A cleaner roadmap output with week-wise plan + data-driven insights.")
# st.divider()

# st.header("📋 Enter Your Details")
st.markdown("""
<div class="card">
  <div class="card-title">🎓 Personalized Student Skill Roadmap</div>
  <p class="card-sub">Cleaner UI + week-wise plan + data-driven insights (rule-based + dataset filtering).</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="card">
  <div class="card-title">📋 Enter Your Details</div>
  <p class="card-sub">Fill your profile to generate a personalized roadmap and readiness score.</p>
</div>
""", unsafe_allow_html=True)


# Pick options safely (won't crash if columns missing)
years = safe_unique(data, "year", [1, 2, 3, 4])
branches = safe_unique(data, "branch", ["CSE", "IT", "ECE", "EEE"])
interests = safe_unique(data, "interest", ["ML", "Web", "DSA"])
budgets = safe_unique(data, "budget_level", ["Low", "Medium", "High"])
skill_levels = safe_unique(data, "skill_level", ["Beginner", "Intermediate", "Advanced"])
stress_levels = safe_unique(data, "stress_level", ["Low", "Medium", "High"])
conf_levels = safe_unique(data, "confusion_level", ["Low", "Medium", "High"])
comm_levels = safe_unique(data, "communication_level", ["Poor", "Average", "Good"])
st.markdown('<div class="card">', unsafe_allow_html=True)
name = st.text_input("Student Name", "")
year = st.selectbox("Year", years)
branch = st.selectbox("Branch", branches)
gpa = st.slider("GPA", 0.0, 10.0, 7.0, 0.1)
study_hours = st.slider("Daily Study Hours", 0, 12, 3)
failures = st.number_input("Number of Failures", min_value=0, max_value=10, value=0)
hostel = st.selectbox("Hostel?", ["Yes", "No"])
sleep_hours = st.slider("Daily Sleep Hours", 0, 12, 6)
family_support = st.selectbox("Family Support Level", ["Low", "Medium", "High"])
interest = st.selectbox("Primary Interest", interests)
budget = st.selectbox("Budget Level", budgets)
skill_level = st.selectbox("Skill Level", skill_levels)
stress_level = st.selectbox("Stress Level", stress_levels)
confusion_level = st.selectbox("Confusion Level", conf_levels)
communication = st.selectbox("Communication Level", comm_levels)
st.markdown('</div>', unsafe_allow_html=True)
st.divider()
st.markdown("""
<div class="card">
  <div class="card-title">🚀 Generate</div>
  <p class="card-sub">Click below to create your roadmap + 4-week plan + projects & resources.</p>
</div>
""", unsafe_allow_html=True)


# ---------------- Generate Roadmap ----------------
if st.button("🔍 Generate My Roadmap"):
    student_info = {
        "year": year,
        "branch": branch,
        "gpa": float(gpa),
        "study_hours": int(study_hours),
        "failures": int(failures),
        "hostel": hostel,
        "sleep_hours": int(sleep_hours),
        "family_support": family_support,
        "interest": interest,
        "budget": budget,
        "skill_level": skill_level,
        "stress_level": stress_level,
        "confusion_level": confusion_level,
        "communication": communication,
    }

    roadmap = generate_structured_roadmap(student_info, data)

    st.success(f"✅ Roadmap Generated for {name or 'Student'}")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    # Quick dashboard metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("GPA", f"{gpa:.1f}")
    col2.metric("Study Hours/day", f"{study_hours}")
    col3.metric("Sleep Hours", f"{sleep_hours}")

    # A simple "readiness" score (just UI)
    # readiness = 0
    # readiness += 30 if gpa >= 7 else 20 if gpa >= 6 else 10
    # readiness += 25 if study_hours >= 4 else 15 if study_hours >= 3 else 8
    # readiness += 20 if stress_level != "High" else 8
    # readiness += 15 if confusion_level != "High" else 8
    # readiness += 10 if communication in ("Average", "Good") else 5
    # readiness = min(readiness, 100)

    # st.write("### 📈 Readiness Score")
    # st.progress(readiness / 100)
    # st.caption("This score is a UI indicator (not an official assessment).")
    score = readiness_breakdown(student_info)

    st.markdown("### 📈 Readiness Score (Breakdown)")
    st.progress(score["Total"] / 100)
    st.caption("UI indicator (not an official assessment).")
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Academics", f'{score["Academics"]}/30')
    c2.metric("Skills", f'{score["Skills"]}/30')
    c3.metric("Routine", f'{score["Routine"]}/20')
    c4.metric("Communication", f'{score["Communication"]}/20')


    tab1, tab2, tab3, tab4 = st.tabs(["🧭 Roadmap", "🗓️ 4-Week Plan", "🧪 Projects", "📚 Resources"])

    with tab1:
        st.info(roadmap["similar_note"])
        st.subheader("🎯 Goals")
        for g in roadmap["goals"]:
            st.write(f"✅ {g}")

        if roadmap["risks"]:
            st.subheader("⚠️ Risks to Watch")
            for r in roadmap["risks"]:
                st.write(f"• {r}")

        st.subheader("🧠 Daily Habits")
        for h in roadmap["habits"]:
            st.write(f"🟩 {h}")

        st.subheader("✅ Action Steps")
        for i, s in enumerate(roadmap["steps"], 1):
            st.write(f"{i}. {s}")

    with tab2:
        for w in roadmap["week_plan"]:
            with st.expander(w["title"], expanded=True):
                for b in w["bullets"]:
                    st.write(f"• {b}")

    with tab3:
        st.subheader("Suggested Projects")
        for p in roadmap["projects"]:
            st.write(f"🚀 {p}")
        st.caption("Tip: Add screenshots + README + clear results. That makes your project look strong.")

    with tab4:
        st.subheader("Recommended Resources")
        for r in roadmap["resources"]:
            st.write(f"📌 {r}")

    # Download as markdown
    md = roadmap_to_markdown(name, student_info, roadmap)
    st.download_button(
        label="⬇️ Download Roadmap (Markdown)",
        data=md.encode("utf-8"),
        file_name=f"roadmap_{(name or 'student').replace(' ','_').lower()}.md",
        mime="text/markdown",
    )
    st.markdown('</div>', unsafe_allow_html=True)
    st.divider()

# ---------------- Dataset preview ----------------
with st.expander("📊 Sample Student Dataset (Preview)", expanded=False):
    st.dataframe(data, use_container_width=True)

st.caption("Mini Project | Student Skill Roadmap | Streamlit Web App")














