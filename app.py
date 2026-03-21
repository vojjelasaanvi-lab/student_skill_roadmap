








import streamlit as st
import pandas as pd
from datetime import date

# ---------------- Page config ----------------
st.set_page_config(page_title="Student Skill Roadmap", layout="centered")
# ---------------- UI THEME (HTML/CSS) ----------------
st.markdown("""
<style>

/* ===== MAIN BACKGROUND ===== */
[data-testid="stAppViewContainer"]{
    background: linear-gradient(135deg,#1e3a8a,#0f172a,#020617);
}

/* ===== TEXT COLOR ===== */
/* ===== TEXT (ONLY MAIN BODY) ===== */
[data-testid="stAppViewContainer"]{
    color:#f8fafc;
}

/* ===== FIX TABS (Week1 Week2 Week3) ===== */
.stTabs [data-baseweb="tab"]{
    background: rgba(255,255,255,0.08);
    color:#e2e8f0 !important;
    border-radius:10px;
    padding:8px 16px;
}

.stTabs [aria-selected="true"]{
    background: linear-gradient(135deg,#6366f1,#22c55e) !important;
    color:white !important;
}

/* ===== FIX EXPANDER (week content) ===== */
.streamlit-expanderHeader{
    color:#f8fafc !important;
    font-weight:600;
}

/* ===== FIX MARKDOWN TEXT ===== */
.stMarkdown{
    color:#e2e8f0 !important;
}

/* ===== LABELS ===== */
label{
    color:#cbd5f5 !important;
    font-weight:600;
}

/* ===== INPUT BOX ===== */
input{
    background: rgba(255,255,255,0.08) !important;
    color:white !important;
    border-radius:10px !important;
}

/* ===== SELECTBOX ===== */
[data-baseweb="select"]{
    background: rgba(255,255,255,0.08) !important;
    border-radius:10px !important;
}

/* ===== BUTTON ===== */
.stButton > button{
    background:linear-gradient(135deg,#6366f1,#22c55e);
    color:white;
    border-radius:12px;
    padding:10px;
    font-weight:700;
}

/* ===== METRIC ===== */
[data-testid="stMetric"]{
    background:rgba(255,255,255,0.05);
    padding:14px;
    border-radius:14px;
}

/* ===== DATAFRAME ===== */
[data-testid="stDataFrame"]{
    border-radius:12px;
}
/* ===== FIX EXPANDER HEADER (WHITE BAR ISSUE) ===== */
.streamlit-expanderHeader{
    background: rgba(255,255,255,0.08) !important;
    color: #f8fafc !important;
    border-radius: 10px;
}

/* Remove white background inside expander */
.streamlit-expanderContent{
    background: transparent !important;
}

/* Fix arrow icon color */
.streamlit-expanderHeader svg{
    color: #f8fafc !important;
}

</style>
""", unsafe_allow_html=True)
st.markdown("""
<h1 style='text-align:center; font-size:40px'>
🎓 Student Skill Roadmap Generator
</h1>
""", unsafe_allow_html=True)
st.markdown("""
<style>

[data-testid="stAppViewContainer"]{
    background-image: 
    linear-gradient(rgba(15,23,42,0.9),rgba(2,6,23,0.95)),
    url("https://images.unsplash.com/photo-1555066931-4365d14bab8c");

    background-size: cover;
    background-position: center;
    background-attachment: fixed;
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
# =========================
# FULL COURSE DATABASE
# =========================
COURSE_DB = {
    # ---------- CSE / Data / AI ----------
    "ML": {
        "courses": [
            "Andrew Ng — Machine Learning Specialization (Coursera)",
            "Krish Naik — Machine Learning Playlist (YouTube)",
            "fast.ai — Practical Deep Learning for Coders",
        ],
        "weeks": [
            "Python + Numpy/Pandas + basics of ML (Regression, metrics).",
            "Scikit-learn: Decision Trees, Random Forest, model validation.",
            "Feature engineering + classification + overfitting control.",
            "Project: Build an end-to-end ML app and deploy via Streamlit.",
        ],
        "projects": [
            "House Price Predictor",
            "Student Performance Dashboard + Prediction",
            "Customer Segmentation (K-Means)",
        ],
    },

    "WEB": {
        "courses": [
            "The Odin Project (Full Stack foundations)",
            "FreeCodeCamp — Responsive Web Design",
            "JavaScript/React Crash Course (YouTube) + practice projects",
        ],
        "weeks": [
            "HTML + CSS (Flex/Grid) + build 1 landing page.",
            "JavaScript (DOM, ES6, Fetch API) + small interactive UI.",
            "React basics (components, state, props) + mini app.",
            "Project: Deploy a portfolio-grade site/app (GitHub Pages/Vercel).",
        ],
        "projects": [
            "Portfolio Website (Dark mode + sections)",
            "To-do App (LocalStorage)",
            "Mini E-commerce Product Gallery UI",
        ],
    },

    "DSA": {
        "courses": [
            "Striver A2Z DSA Sheet (TakeUForward)",
            "NeetCode 150 (structured problems)",
            "Abdul Bari — Algorithms (YouTube)",
        ],
        "weeks": [
            "Arrays/Strings + time complexity + 20 problems.",
            "Linked List + Stack/Queue + 15 problems.",
            "Trees + Recursion/Backtracking + 12 problems.",
            "Sorting/Searching + DP basics + mock interview set.",
        ],
        "projects": [
            "Sorting Visualizer",
            "Sudoku Solver",
            "Pathfinding Visualizer (BFS/Dijkstra)",
        ],
    },

    "CYBER": {
        "courses": [
            "TryHackMe — Pre Security / Beginner Path",
            "OverTheWire (Bandit) — Linux basics practice",
            "YouTube: Networking + Web security basics (OWASP Top 10)",
        ],
        "weeks": [
            "Linux + networking basics + command line practice.",
            "Web fundamentals + OWASP Top 10 (SQLi, XSS, auth issues).",
            "Hands-on labs (TryHackMe rooms) + write notes.",
            "Project: Security checklist + demo report (mini pentest style).",
        ],
        "projects": [
            "Basic Web Security Audit Report (OWASP checklist)",
            "Password strength checker + hashing demo",
            "Phishing awareness mini-site (educational)",
        ],
    },

    # ---------- ECE ----------
    "ECE": {
        "courses": [
            "NPTEL — Digital Circuits / Microprocessors (choose 1)",
            "Embedded Systems (Arduino/ESP32) playlist (YouTube)",
            "VLSI Basics / Communication Systems intro (NPTEL/YouTube)",
        ],
        "weeks": [
            "Core: C basics + digital logic fundamentals (gates, flip-flops).",
            "Embedded basics: Arduino/ESP32 + sensors (read data, print/plot).",
            "Choose one: VLSI basics OR Communication Systems basics.",
            "Project: Mini IoT/Embedded demo + documentation + results.",
        ],
        "projects": [
            "IoT Temperature/Humidity Monitor (sensor + dashboard)",
            "Arduino Sensor Data Logger",
            "Mini Communication System simulation report (basic)",
        ],
    },

    "COMM_SYSTEMS": {
        "courses": [
            "NPTEL — Communication Systems",
            "Signals & Systems basics (YouTube/NPTEL)",
            "MATLAB/Python signal processing basics (tutorial series)",
        ],
        "weeks": [
            "Signals basics: sampling, frequency, noise concept.",
            "AM/FM basics + modulation/demodulation understanding.",
            "Digital comm intro: ASK/FSK/PSK concept + simple plots.",
            "Project: small simulation notebook + report (plots + explanation).",
        ],
        "projects": [
            "AM/FM simulation notebook",
            "Noise impact on signal plots",
            "Digital modulation demo (basic)",
        ],
    },

    "VLSI": {
        "courses": [
            "NPTEL — VLSI Design",
            "Digital Electronics (NPTEL/YouTube)",
            "Verilog basics playlist (YouTube)",
        ],
        "weeks": [
            "Digital design recap + number systems + logic optimization.",
            "Verilog basics: modules, testbench, simulation flow.",
            "Combinational + sequential circuits in Verilog.",
            "Project: design a small digital system + simulate + report.",
        ],
        "projects": [
            "4-bit ALU in Verilog",
            "Traffic Light Controller (FSM) in Verilog",
            "Simple Counter/Shift Register designs",
        ],
    },

    "SIGNAL": {
        "courses": [
            "NPTEL — Signals and Systems / DSP intro",
            "Python for Signal Processing (NumPy/Scipy) tutorials",
            "YouTube: DSP basics (filters, FFT)",
        ],
        "weeks": [
            "Signals basics + plotting + basic transforms concept.",
            "FFT basics + noise removal concept.",
            "Filters (low/high pass) concept + simple implementations.",
            "Project: signal cleaning / analysis notebook + report.",
        ],
        "projects": [
            "Noise filtering demo (FFT + filter)",
            "Audio signal analysis notebook",
            "Sensor signal smoothing + plots",
        ],
    },

    "IOT": {
        "courses": [
            "Arduino/ESP32 IoT playlist (YouTube)",
            "NPTEL — Introduction to IoT",
            "Basics of MQTT/HTTP + simple dashboards",
        ],
        "weeks": [
            "Microcontroller + sensor basics + read values.",
            "Send data: serial/log file + basic visualization.",
            "Add connectivity (Wi-Fi/MQTT/HTTP) basic.",
            "Project: IoT dashboard demo + short video + README.",
        ],
        "projects": [
            "Smart home sensor dashboard",
            "Weather station mini project",
            "Room monitoring (temp/light) demo",
        ],
    },

    "EMBEDDED": {
        "courses": [
            "Embedded C basics (YouTube)",
            "Arduino/ESP32 practical series",
            "Basics of interrupts/timers (tutorial series)",
        ],
        "weeks": [
            "Embedded C: loops, pointers basics, debugging mindset.",
            "GPIO + sensor interfacing + basic timing.",
            "Interrupts/timers basics + simple control logic.",
            "Project: embedded mini demo + documentation.",
        ],
        "projects": [
            "Digital stopwatch timer",
            "Sensor-based alert system",
            "LED patterns with interrupts/timers",
        ],
    },

    # ---------- EEE ----------
    "EEE": {
        "courses": [
            "NPTEL — Power Systems",
            "NPTEL — Electrical Machines",
            "Industrial Automation basics (YouTube/NPTEL)",
        ],
        "weeks": [
            "Basics: power system components + machines recap.",
            "Protection & control basics + simple problem practice.",
            "Renewable/Smart grid basics (choose 1 focus).",
            "Project: mini case-study/report with calculations + charts.",
        ],
        "projects": [
            "Load analysis mini report (Excel/Python)",
            "Renewable energy comparison case study",
            "Basic fault analysis notes + examples",
        ],
    },

    "POWER": {
        "courses": [
            "NPTEL — Power Systems (core)",
            "Protection & Switchgear basics (YouTube/NPTEL)",
            "Power flow intro (basic concepts)",
        ],
        "weeks": [
            "Power system overview + per-unit basics (light).",
            "Protection basics (relays, faults) + examples.",
            "Transmission/distribution concepts + reliability.",
            "Project: load/fault calculation sheet + report.",
        ],
        "projects": [
            "Fault calculation worksheet + explanation",
            "Load estimation report for hostel/house",
            "Transmission line parameter mini notebook",
        ],
    },

    "RENEW": {
        "courses": [
            "NPTEL — Renewable Energy",
            "Solar PV basics (YouTube/NPTEL)",
            "Wind energy basics (tutorial series)",
        ],
        "weeks": [
            "Solar PV basics + components + sizing idea.",
            "Wind/other renewables basics + pros/cons.",
            "Hybrid systems + storage basics (battery).",
            "Project: solar sizing calculator + mini report.",
        ],
        "projects": [
            "Solar sizing calculator (Excel/Python)",
            "Renewable comparison infographic/report",
            "Microgrid case study summary",
        ],
    },

    "SMARTGRID": {
        "courses": [
            "Smart Grid basics (NPTEL/YouTube)",
            "Power electronics intro (for grid integration)",
            "SCADA basics overview (intro)",
        ],
        "weeks": [
            "Smart grid concept + components + communication basics.",
            "Demand response + metering + grid monitoring concepts.",
            "Grid integration of renewables + challenges.",
            "Project: smart grid concept report + diagram + demo slides.",
        ],
        "projects": [
            "Smart grid architecture diagram + report",
            "Demand response mini case study",
            "Energy monitoring dashboard concept",
        ],
    },

    "AUTOMATION": {
        "courses": [
            "Industrial Automation basics (YouTube/NPTEL)",
            "PLC fundamentals (intro course)",
            "Sensors + actuators basics",
        ],
        "weeks": [
            "Automation basics + sensors/actuators overview.",
            "PLC fundamentals (ladder logic concept).",
            "Control basics: feedback, stability concept.",
            "Project: automation workflow diagram + mini case study.",
        ],
        "projects": [
            "PLC ladder logic mini examples (documented)",
            "Sensor-actuator workflow demo (simulation/report)",
            "Industry process automation case study",
        ],
    },

    "ELECTRICAL_DESIGN": {
        "courses": [
            "Electrical Design basics (YouTube/notes)",
            "AutoCAD Electrical basics (optional)",
            "Basics of wiring, safety, standards (overview)",
        ],
        "weeks": [
            "Wiring basics + safety + common components.",
            "Reading single-line diagrams (SLD) basics.",
            "Load calculation + protection selection basics.",
            "Project: Create an SLD + load sheet + report.",
        ],
        "projects": [
            "Single-line diagram + explanation",
            "Load calculation sheet for a building",
            "Protection device selection notes",
        ],
    },

    # ---------- Mechanical ----------
    "MECH": {
        "courses": [
            "CAD basics (Fusion 360/SolidWorks tutorials)",
            "NPTEL — Manufacturing / Thermal Engineering (choose 1)",
            "Robotics basics (intro course/playlist)",
        ],
        "weeks": [
            "CAD basics: sketches + 3 simple parts.",
            "Manufacturing basics OR Thermal basics (choose one).",
            "Robotics basics + mechanisms overview.",
            "Project: design + report (CAD model + documentation).",
        ],
        "projects": [
            "CAD assembly mini project",
            "Manufacturing process comparison report",
            "Thermal analysis mini notes + examples",
        ],
    },

    "CAD": {
        "courses": [
            "Fusion 360 / SolidWorks beginner tutorials",
            "Engineering drawing basics (YouTube)",
            "Basic GD&T overview (optional)",
        ],
        "weeks": [
            "Sketching + constraints + 3 practice parts.",
            "3D modeling + assembly basics.",
            "Drawings + dimensions + tolerances basics.",
            "Project: model + drawing pack + short explanation.",
        ],
        "projects": [
            "CAD model of simple machine part",
            "Assembly of basic mechanism",
            "Drawing sheet pack (PDF) + notes",
        ],
    },

    "ROBOTICS": {
        "courses": [
            "Robotics basics playlist (YouTube)",
            "Arduino basics (for small robotics demos)",
            "Mechanisms + control intro (overview)",
        ],
        "weeks": [
            "Basics: sensors + motors overview + simple control idea.",
            "Arduino motor control basics + small demo.",
            "Robot mechanisms + path planning intro (basic).",
            "Project: mini robot demo plan + documentation/video.",
        ],
        "projects": [
            "Line follower robot plan/demo",
            "Obstacle avoidance mini demo",
            "Robot arm concept + CAD (optional)",
        ],
    },

    "AUTO": {
        "courses": [
            "Automobile basics (YouTube/NPTEL)",
            "Engine + transmission basics overview",
            "Vehicle dynamics intro (basic)",
        ],
        "weeks": [
            "Vehicle components + engine basics.",
            "Transmission + braking + steering basics.",
            "Vehicle dynamics intro + safety concepts.",
            "Project: vehicle subsystem report + diagrams.",
        ],
        "projects": [
            "Vehicle subsystem case study (brakes/engine)",
            "Maintenance checklist + explanation",
            "Auto trends summary report",
        ],
    },

    "THERMAL": {
        "courses": [
            "NPTEL — Thermal Engineering basics",
            "Heat transfer intro playlist (YouTube)",
            "Basic thermodynamics notes + problems",
        ],
        "weeks": [
            "Thermo basics: laws + properties + simple problems.",
            "Heat transfer basics (conduction/convection/radiation).",
            "Cycles overview (Rankine/Brayton) basic.",
            "Project: mini thermal calculation sheet + report.",
        ],
        "projects": [
            "Heat loss calculation mini sheet",
            "Thermal cycle summary report",
            "Cooling system concept notes",
        ],
    },

    "MANUFACTURING": {
        "courses": [
            "NPTEL — Manufacturing Processes",
            "Metrology basics (YouTube/NPTEL)",
            "Lean manufacturing overview (intro)",
        ],
        "weeks": [
            "Manufacturing basics: casting/forming/machining overview.",
            "Metrology basics + quality concepts.",
            "Lean basics (5S, waste reduction).",
            "Project: process comparison + case study report.",
        ],
        "projects": [
            "Manufacturing process comparison report",
            "Lean 5S checklist for workshop",
            "Quality control mini notes + examples",
        ],
    },

    # ---------- Soft Skills ----------
    "SOFT": {
        "courses": [
            "Basic Communication Skills playlist (YouTube)",
            "TED Talks (practice + notes)",
            "Resume & Interview basics resources",
        ],
        "weeks": [
            "Daily speaking practice + 5–7 lines writing summary.",
            "Improve vocabulary + clarity + small presentations.",
            "Mock interview practice + feedback from peers.",
            "Project: 2-min self intro video + updated resume.",
        ],
        "projects": [
            "2-min self-introduction video",
            "Resume + LinkedIn update checklist",
            "Weekly speaking practice log",
        ],
    },
}

# =========================
# PERFECT DETECTION FOR YOUR CSV INTERESTS
# =========================
def detect_category(interest: str) -> str:
    s = str(interest).lower()

    # ML / Data
    if any(k in s for k in ["ai/ml", "ml", "ai", "data science", "data analysis"]):
        return "ML"

    # Web + App
    if "web" in s:
        return "WEB"
    if "app" in s:
        return "WEB"

    # DSA / Competitive
    if "competitive coding" in s:
        return "DSA"

    # Cybersecurity
    if "cyber" in s:
        return "CYBER"

    # ECE
    if any(k in s for k in ["embedded", "vlsi", "iot"]):
        # choose a more specific track if desired
        if "vlsi" in s: return "VLSI"
        if "iot" in s: return "IOT"
        if "embedded" in s: return "EMBEDDED"
        return "ECE"
    if any(k in s for k in ["signal processing"]):
        return "SIGNAL"
    if any(k in s for k in ["communication systems"]):
        return "COMM_SYSTEMS"

    # EEE
    if any(k in s for k in ["power systems"]):
        return "POWER"
    if any(k in s for k in ["renewable energy"]):
        return "RENEW"
    if any(k in s for k in ["smart grid systems"]):
        return "SMARTGRID"
    if any(k in s for k in ["industrial automation"]):
        return "AUTOMATION"
    if any(k in s for k in ["electrical design"]):
        return "ELECTRICAL_DESIGN"

    # Mechanical
    if any(k in s for k in ["robotics"]):
        return "ROBOTICS"
    if any(k in s for k in ["cad design"]):
        return "CAD"
    if any(k in s for k in ["automobile engineering"]):
        return "AUTO"
    if any(k in s for k in ["thermal engineering"]):
        return "THERMAL"
    if any(k in s for k in ["manufacturing"]):
        return "MANUFACTURING"

    # Soft skills
    if "communication skills" in s:
        return "SOFT"

    return "DSA"

# =========================
# WEEK PLAN BUILDER (returns week_plan, courses, projects)
# =========================
def build_week_plan(interest, skill_level, budget_level):
    category = detect_category(interest)
    data = COURSE_DB.get(category, COURSE_DB["DSA"])  # safe fallback

    free_note = "Use free resources (YouTube/NPTEL/free audits)." if str(budget_level) == "Low" else "Consider 1 paid course for faster progress."
    lvl = str(skill_level).lower()
    practice = "45–60 mins daily practice." if "begin" in lvl else "60–90 mins daily practice."

    week_plan = []
    for i in range(4):
        week_plan.append({
            "title": f"Week {i+1} — " + ["Foundation", "Core Skills", "Build Projects", "Portfolio & Review"][i],
            "bullets": [
                f"Course focus: {data['courses'][min(i, len(data['courses'])-1)]}",
                data["weeks"][i],
                practice,
                free_note,
            ]
        })

    return week_plan, data["courses"], data["projects"]         
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

    week_plan, course_resources, course_projects = build_week_plan(
        info["interest"], info["skill_level"], info["budget"]
)
# Use course database resources
    resources = course_resources
    projects = course_projects
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














