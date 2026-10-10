
import streamlit as st
import pandas as pd
import numpy as np
import os
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

# Set page configurations
st.set_page_config(
    page_title="Student Productivity & Performance AI Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for high-end professional appearance
st.markdown("""
<style>
    /* Global styling */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Title styling */
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #1e3a8a, #3b82f6, #8b5cf6);
        color: white;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px -5px rgba(59, 130, 246, 0.3);
    }
    .main-title {
        font-family: 'Outfit', sans-serif;
        font-weight: 800;
        font-size: 3rem;
        margin: 0;
        letter-spacing: -0.02em;
    }
    .main-subtitle {
        font-size: 1.1rem;
        font-weight: 300;
        opacity: 0.9;
        margin-top: 0.5rem;
    }
    
    /* Metrics Grid */
    .metric-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        height: 100%;
    }
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        border-color: #cbd5e1;
    }
    .metric-title {
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #64748b;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .metric-value {
        font-family: 'Outfit', sans-serif;
        font-size: 2.5rem;
        font-weight: 800;
        line-height: 1;
        margin: 0.5rem 0;
    }
    .metric-desc {
        font-size: 0.8rem;
        color: #94a3b8;
    }
    
    /* Status Card styling */
    .status-card {
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
        border: 1px solid;
    }
    .status-title {
        font-size: 1rem;
        text-transform: uppercase;
        font-weight: 700;
        letter-spacing: 0.08em;
    }
    .status-value {
        font-family: 'Outfit', sans-serif;
        font-size: 3rem;
        font-weight: 900;
        margin: 0.5rem 0;
        letter-spacing: -0.01em;
    }
    .status-desc {
        font-size: 1.1rem;
        font-weight: 500;
        max-width: 700px;
        margin: 0 auto;
    }
    
    /* Insight Panel styling */
    .insight-section {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 2rem;
        margin-top: 1.5rem;
        box-shadow: inset 0 2px 4px 0 rgba(0, 0, 0, 0.02);
    }
    .insight-header {
        font-family: 'Outfit', sans-serif;
        font-size: 1.4rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .insight-bullet {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02);
        display: flex;
        align-items: flex-start;
        gap: 1rem;
    }
    .bullet-icon {
        font-size: 1.5rem;
        padding: 0.25rem;
    }
    .bullet-content {
        flex: 1;
    }
    .bullet-title {
        font-weight: 700;
        font-size: 1.05rem;
        color: #1e293b;
        margin-bottom: 0.25rem;
    }
    .bullet-text {
        font-size: 0.95rem;
        color: #475569;
        line-height: 1.5;
    }
    .bullet-tip {
        font-size: 0.85rem;
        font-weight: 600;
        color: #2563eb;
        margin-top: 0.5rem;
    }
    
    /* Tabs & general elements */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1.5rem;
        border-bottom: 2px solid #e2e8f0;
        margin-bottom: 1.5rem;
    }
    .stTabs [data-baseweb="tab"] {
        font-family: 'Outfit', sans-serif;
        font-size: 1.1rem;
        font-weight: 600;
        color: #64748b;
        padding: 1rem 0.5rem;
        background: transparent;
    }
    .stTabs [aria-selected="true"] {
        color: #2563eb !important;
        border-bottom: 2px solid #2563eb;
    }
    
    /* Progress bar overlays */
    .progress-bar-container {
        margin: 1.5rem 0;
    }
    .progress-bar-label {
        display: flex;
        justify-content: space-between;
        font-size: 0.9rem;
        font-weight: 600;
        color: #334155;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- Resource Loading -----------------

@st.cache_resource
def load_ml_models():
    """Load Random Forest Model and Scaler"""
    model_path = 'student_performance_rf_model.pkl'
    scaler_path = 'scaler.pkl'
    
    if os.path.exists(model_path) and os.path.exists(scaler_path):
        model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)
        return model, scaler
    else:
        return None, None

@st.cache_data
def load_dataset():
    """Load dataset"""
    dataset_path = 'ultimate_student_productivity_dataset_5000.csv'
    if os.path.exists(dataset_path):
        return pd.read_csv(dataset_path)
    return None

model, scaler = load_ml_models()
df = load_dataset()

# Title Header
st.markdown("""
<div class="main-header">
    <h1 class="main-title">🎓 Student Academic Diagnostics & Planner</h1>
    <div class="main-subtitle">AI-Driven Performance Forecasting, Lifestyle Diagnostics, and Retentive Insights</div>
</div>
""", unsafe_allow_html=True)

# Safety stop if model files are missing
if model is None or scaler is None or df is None:
    st.error("⚠️ Error: Scaler, Dataset, or Model weights files are missing in this folder!")
    st.info("Please execute the training script `student performance.py` first to generate models and test outputs.")
    st.stop()

# ----------------- Sidebar Setup -----------------
st.sidebar.markdown("## ⚙️ Student Diagnostics Panel")
st.sidebar.markdown("Configure the parameters below to compute real-time scores and determine overall eligibility.")

# Sidebar sections
st.sidebar.markdown("### 👤 Profile & Environment")
age = st.sidebar.number_input("Age", min_value=16, max_value=25, value=20, help="Age in years")
gender = st.sidebar.selectbox("Gender", options=['Female', 'Male', 'Other'], index=0)
academic_level = st.sidebar.selectbox("Academic Level", options=['High School', 'Undergraduate', 'Postgraduate'], index=1)
internet_quality = st.sidebar.selectbox("Internet Quality", options=['Average', 'Good', 'Poor'], index=1)

st.sidebar.markdown("### 📚 Study & Attendance")
attendance = st.sidebar.slider("Attendance (%)", min_value=0, max_value=100, value=85, step=1, help="Total class attendance percentage. 75% is required to qualify.")
study_hours = st.sidebar.slider("Study Hours (Daily)", min_value=1.0, max_value=12.0, value=6.0, step=0.5, help="Average daily study time.")
self_study_hours = st.sidebar.slider("Self Study Hours (Daily)", min_value=0.5, max_value=7.5, value=3.5, step=0.5)
online_classes_hours = st.sidebar.slider("Online Classes Hours (Daily)", min_value=0.0, max_value=6.0, value=2.0, step=0.5)

st.sidebar.markdown("### 🎮 Lifestyle & Screen Time")
social_media_hours = st.sidebar.slider("Social Media (Daily Hours)", min_value=0.0, max_value=8.0, value=2.5, step=0.5)
gaming_hours = st.sidebar.slider("Gaming (Daily Hours)", min_value=0.0, max_value=5.5, value=1.0, step=0.5)
sleep_hours = st.sidebar.slider("Sleep Duration (Daily Hours)", min_value=4.0, max_value=10.0, value=7.5, step=0.5)

st.sidebar.markdown("### 🧘 Health & Context")
exercise_minutes = st.sidebar.slider("Exercise (Minutes Daily)", min_value=0, max_value=150, value=45, step=5)
caffeine_intake_mg = st.sidebar.slider("Caffeine Intake (mg Daily)", min_value=0, max_value=500, value=150, step=10, help="1 cup of coffee ~ 90-100mg caffeine")
part_time_job = st.sidebar.selectbox("Part-Time Job?", options=['No', 'Yes'], index=0)
upcoming_deadline = st.sidebar.selectbox("Upcoming Deadlines?", options=['No', 'Yes'], index=0)
mental_health_score = st.sidebar.slider("Mental Health Score (1-10)", min_value=1, max_value=10, value=7, step=1, help="Higher represents better mental well-being")

# ----------------- Feature Calculations -----------------

# Map categories
gender_map = {'Female': 0, 'Male': 1, 'Other': 2}
academic_map = {'High School': 0, 'Postgraduate': 1, 'Undergraduate': 2}
internet_map = {'Average': 0, 'Good': 1, 'Poor': 2}

gender_val = gender_map[gender]
academic_level_val = academic_map[academic_level]
internet_quality_val = internet_map[internet_quality]
part_time_job_val = 1 if part_time_job == 'Yes' else 0
upcoming_deadline_val = 1 if upcoming_deadline == 'Yes' else 0

# Intermediate features
screen_time_hours = social_media_hours + gaming_hours + 2.0  # Adding default study/utility screen time
total_leisure_screen_time = social_media_hours + gaming_hours
self_study_ratio = self_study_hours / (study_hours + 1)
sleep_deficit = abs(sleep_hours - 8.0)
study_screen_ratio = study_hours / (screen_time_hours + 1)

# Scaled variables bounds from original dataset training
# Focus Index
focus_index_raw = (study_hours * 3.5 + sleep_hours * 2.0 + mental_health_score * 1.5 - screen_time_hours * 1.2)
focus_index = 1 + 62 * (focus_index_raw - (-0.11215367045205582)) / (68.3961045306275 - (-0.11215367045205582))
focus_index = float(np.clip(focus_index, 1, 100))

# Burnout Level
burnout_level_raw = (screen_time_hours * 3.0 + upcoming_deadline_val * 25 + part_time_job_val * 20 - sleep_hours * 4.0)
burnout_level = 1 + 96 * (burnout_level_raw - (-29.88057074785734)) / (74.14039527004154 - (-29.88057074785734))
burnout_level = float(np.clip(burnout_level, 1, 100))

# Productivity Score
productivity_score_raw = (focus_index * 2.0 + sleep_hours * 1.5 - burnout_level * 0.4)
productivity_score = 1 + 97 * (productivity_score_raw - (-24.367417550540104)) / (136.54374650794557 - (-24.367417550540104))
productivity_score = float(np.clip(productivity_score, 1, 100))

# Focus per Study Hour
focus_per_study_hour = focus_index / (study_hours + 1)

# Compile array in original features order
features = np.array([[
    age, gender_val, academic_level_val, study_hours, self_study_hours, online_classes_hours,
    social_media_hours, gaming_hours, sleep_hours, screen_time_hours, exercise_minutes,
    caffeine_intake_mg, part_time_job_val, upcoming_deadline_val, internet_quality_val, mental_health_score,
    focus_index, burnout_level, productivity_score, total_leisure_screen_time, self_study_ratio,
    sleep_deficit, study_screen_ratio, focus_per_study_hour
]])

# Preprocess & Predict using ML model
features_df = pd.DataFrame(features, columns=scaler.feature_names_in_)
features_scaled = scaler.transform(features_df)
predicted_score = model.predict(features_scaled)[0]
predicted_score = float(np.clip(predicted_score, 1, 100))

# ----------------- Threshold Metrics -----------------
passing_score_threshold = 33
passing_attendance_threshold = 75

is_score_passing = predicted_score >= passing_score_threshold
is_attendance_passing = attendance >= passing_attendance_threshold

# ----------------- Main Layout -----------------
tab1, tab2, tab3 = st.tabs([
    "🎯 Predictions & AI Insights",
    "📊 Student Cohort Explorer",
    "📈 Model Calibration & Metrics"
])

# ================= TAB 1: Predictions & AI Insights =================
with tab1:
    
    # 1. Overall Pass/Fail Status Banner
    if is_score_passing and is_attendance_passing:
        status_title = "ELIGIBLE & PASSED"
        status_color = "#15803d"  # green
        status_bg = "#f0fdf4"
        status_border = "#bbf7d0"
        status_icon = "🎉"
        status_desc = f"Congratulations! You meet both academic score requirements (Predicted Score: {predicted_score:.1f}% >= 33%) and attendance standards (Current Attendance: {attendance}% >= 75%)."
    elif is_score_passing and not is_attendance_passing:
        status_title = "DETAINED (Low Attendance)"
        status_color = "#c2410c"  # orange
        status_bg = "#fff7ed"
        status_border = "#ffedd5"
        status_icon = "⚠️"
        status_desc = f"Warning! Although your academic projection is passing ({predicted_score:.1f}% >= 33%), your attendance is below the mandatory 75% threshold (Current Attendance: {attendance}%). You risk detention from exams."
    elif not is_score_passing and is_attendance_passing:
        status_title = "FAILED (Academic Shortage)"
        status_color = "#b91c1c"  # red
        status_bg = "#fef2f2"
        status_border = "#fee2e2"
        status_icon = "❌"
        status_desc = f"Action Required! Your predicted exam score ({predicted_score:.1f}%) falls below the 33% passing line. Immediate learning support and schedule updates are recommended."
    else:
        status_title = "FAILED & DETAINED"
        status_color = "#7f1d1d"  # dark red
        status_bg = "#fef2f2"
        status_border = "#fca5a5"
        status_icon = "🚨"
        status_desc = f"Critical Alert! You do not meet the minimum academic performance (Predicted Score: {predicted_score:.1f}% < 33%) and have failed to meet the attendance requirements (Current Attendance: {attendance}% < 75%)."

    st.markdown(f"""
    <div class="status-card" style="background-color: {status_bg}; border-color: {status_border}; color: {status_color};">
        <div class="status-title">{status_icon} Overall Status Classification</div>
        <div class="status-value">{status_title}</div>
        <div class="status-desc">{status_desc}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 2. Key Metrics Grid
    st.subheader("📊 Core Diagnostic Indicators")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Predicted Score</div>
            <div class="metric-value" style="color: {'#10b981' if is_score_passing else '#ef4444'};">{predicted_score:.1f}%</div>
            <div class="metric-desc">Academic threshold: 33%</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Attendance</div>
            <div class="metric-value" style="color: {'#10b981' if is_attendance_passing else '#f97316'};">{attendance}%</div>
            <div class="metric-desc">Eligibility threshold: 75%</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Focus Index</div>
            <div class="metric-value" style="color: #3b82f6;">{focus_index:.1f}</div>
            <div class="metric-desc">Concentration index (1-100)</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col4:
        burnout_color = "#ef4444" if burnout_level > 65 else ("#f97316" if burnout_level > 40 else "#10b981")
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Burnout Risk</div>
            <div class="metric-value" style="color: {burnout_color};">{burnout_level:.1f}%</div>
            <div class="metric-desc">Fatigue and pressure loading</div>
        </div>
        """, unsafe_allow_html=True)

    # 3. Threshold Visualizations
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("📉 Threshold Proximity Visuals")
    
    # Progress bar for Exam Score
    st.markdown(f"""
    <div class="progress-bar-container">
        <div class="progress-bar-label">
            <span>Exam Score Threshold Target</span>
            <span>{predicted_score:.1f}% / 100% (Passing Threshold: 33%)</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.progress(predicted_score / 100.0)
    
    # Progress bar for Attendance
    st.markdown(f"""
    <div class="progress-bar-container">
        <div class="progress-bar-label">
            <span>Attendance Eligibility Target</span>
            <span>{attendance}% / 100% (Mandatory Threshold: 75%)</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.progress(attendance / 100.0)

    # 4. Advanced AI Insights Section
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="insight-section">
        <div class="insight-header">🧠 AI Consultation & Strategic Roadmap</div>
        <p style="color: #475569; margin-bottom: 1.5rem; font-size: 1rem;">
            Below is an automated diagnostic breakdown based on the input student behavioral dataset. 
            These rules audit screen time, mental wellness, circadian hygiene, and class schedules.
        </p>
    """, unsafe_allow_html=True)
    
    # Generate dynamic, highly professional insights
    
    # Attendance insight
    if not is_attendance_passing:
        gap = 75 - attendance
        st.markdown(f"""
        <div class="insight-bullet">
            <div class="bullet-icon">🚨</div>
            <div class="bullet-content">
                <div class="bullet-title">Attendance Deficit (Shortfall: {gap}%)</div>
                <div class="bullet-text">Your current attendance stands at {attendance}%. You are detained from writing the examinations. Absenteeism severely degrades the structure of collaborative learning.</div>
                <div class="bullet-tip">Action: Immediately consult with course coordinators. Plan to attend all remaining sessions to restore eligibility above 75%.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="insight-bullet" style="border-left: 5px solid #22c55e;">
            <div class="bullet-icon">✅</div>
            <div class="bullet-content">
                <div class="bullet-title">Attendance Clearance Verified</div>
                <div class="bullet-text">You have met academic registration policies. Keeping attendance at {attendance}% protects continuous internal review marks.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Academic score insight
    if not is_score_passing:
        st.markdown(f"""
        <div class="insight-bullet">
            <div class="bullet-icon">📖</div>
            <div class="bullet-content">
                <div class="bullet-title">Critical Academic Enrichment Plan</div>
                <div class="bullet-text">Predicted exam performance is {predicted_score:.1f}%, which is below the 33% passing grade. A lack of self-study hours or high screen time limits memory encoding.</div>
                <div class="bullet-tip">Action: Double your daily study hours and schedule weekly self-mock tests. Focus on high-weightage topics.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Sleep insight
    if sleep_hours < 7.0:
        st.markdown(f"""
        <div class="insight-bullet">
            <div class="bullet-icon">🌙</div>
            <div class="bullet-content">
                <div class="bullet-title">Sleep Deficiency & Cognitive Recovery</div>
                <div class="bullet-text">You sleep for {sleep_hours:.1f} hours daily. Insufficient sleep restricts long-term memory integration and triggers early exhaustion.</div>
                <div class="bullet-tip">Action: Maintain a target of 7.5 hours of sleep, avoiding mobile screens 30 minutes before bedtime.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    # Digital screen time insight
    if total_leisure_screen_time > 4.0:
        st.markdown(f"""
        <div class="insight-bullet">
            <div class="bullet-icon">📱</div>
            <div class="bullet-content">
                <div class="bullet-title">Digital Distraction Audit</div>
                <div class="bullet-text">Your leisure screen time (gaming + social media) is {total_leisure_screen_time:.1f} hours. This triggers dopamine burnout, reducing attention spans during standard lecture sessions.</div>
                <div class="bullet-tip">Action: Set a lock-out timer on social and gaming apps for no more than 2 hours daily.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Caffeine & Stress check
    if caffeine_intake_mg > 300 and sleep_hours < 6.5:
        st.markdown(f"""
        <div class="insight-bullet">
            <div class="bullet-icon">☕</div>
            <div class="bullet-content">
                <div class="bullet-title">Caffeine-Sleep Disconnect</div>
                <div class="bullet-text">High caffeine intake ({caffeine_intake_mg}mg) combined with short sleep duration ({sleep_hours:.1f}h) indicates high dependence. This increases cortisol and elevates the Burnout Risk.</div>
                <div class="bullet-tip">Action: Switch to herbal tea after 2:00 PM and taper coffee intake down below 200mg.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Exercise & Well-being
    if exercise_minutes < 30:
        st.markdown(f"""
        <div class="insight-bullet">
            <div class="bullet-icon">🏃</div>
            <div class="bullet-content">
                <div class="bullet-title">Physical Stagnation</div>
                <div class="bullet-text">Exercise is {exercise_minutes} minutes. Mild cardiovascular training increases cerebral blood flow, improving retention rates by up to 15%.</div>
                <div class="bullet-tip">Action: Incorporate a 20-minute daily brisk walk or jog before study sessions.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # General Success note
    if is_score_passing and is_attendance_passing and total_leisure_screen_time <= 4.0 and sleep_hours >= 7.0:
        st.markdown(f"""
        <div class="insight-bullet" style="background-color: #f0fdf4; border-left: 5px solid #22c55e;">
            <div class="bullet-icon">🏆</div>
            <div class="bullet-content">
                <div class="bullet-title">High-Efficiency Student Profile</div>
                <div class="bullet-text">You display excellent parameters across focus, sleep, screen limitation, and classroom presence. Maintain this high-performance routine.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ================= TAB 2: Student Cohort Explorer =================
with tab2:
    st.subheader("📂 Cohort Analytical Database")
    st.markdown(f"Auditing a representative simulated student cohort size of **{len(df):,} records**.")
    
    # Dataset Summary Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Cohort Size", value=f"{len(df):,}")
    with col2:
        st.metric(label="Average Sleep", value=f"{df['sleep_hours'].mean():.1f} hours")
    with col3:
        st.metric(label="Average Exam Score", value=f"{df['exam_score'].mean():.1f}%")
    with col4:
        st.metric(label="Average Productivity", value=f"{df['productivity_score'].mean():.1f}")
        
    st.markdown("---")
    st.markdown("### 📊 Distribution and Inter-Variable Visuals")
    
    plot_col1, plot_col2 = st.columns(2)
    
    with plot_col1:
        st.markdown("#### Study Hours vs. Projected Exam Score")
        sample_df = df.sample(n=1000, random_state=42)
        st.scatter_chart(
            data=sample_df,
            x='study_hours',
            y='exam_score',
            color='#3b82f6',
            use_container_width=True
        )
        
    with plot_col2:
        st.markdown("#### Exam Score Distribution Histogram")
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.hist(df['exam_score'], bins=30, color='#8b5cf6', edgecolor='white', alpha=0.8)
        ax.axvline(33, color='red', linestyle='--', label='Passing Threshold (33%)')
        ax.set_title('Cohort Exam Scores', fontsize=10)
        ax.set_xlabel('Exam Score (%)', fontsize=8)
        ax.set_ylabel('Frequency', fontsize=8)
        ax.legend(fontsize=8)
        ax.grid(True, linestyle='--', alpha=0.5)
        st.pyplot(fig)
        
    st.markdown("### 🔍 Cohort Raw Records View")
    st.dataframe(df.head(100), use_container_width=True)

# ================= TAB 3: Model Calibration & Metrics =================
with tab3:
    st.subheader("📊 Model Performance Validation Reports")
    st.markdown("""
    During testing and validation, regression models were verified against the student diagnostics split (80/20 train-test ratio).
    The metrics represent validation accuracy:
    """)
    
    comparison_data = {
        "ML Algorithm": ["Linear Regression", "Random Forest Regressor", "XGBoost Regressor"],
        "R² Score (Accuracy)": ["1.00", "1.00", "1.00"],
        "Mean Absolute Error (MAE)": ["0.00", "0.16", "0.18"],
        "Root Mean Squared Error (RMSE)": ["0.00", "0.22", "0.24"]
    }
    comp_df = pd.DataFrame(comparison_data)
    st.table(comp_df)
    
    st.markdown("### 🧠 Diagnostic Feature Impact Analysis")
    st.markdown("""
    1. **Productivity Score (99% Correlation)**: The most influential feature for forecasting scores. Reflects the product of focus efficiency and sleep minus burnout.
    2. **Focus Index (98% Correlation)**: Concentration levels. Driven upward by active self-study and restorative sleep; degraded by digital screen overload.
    3. **Study Hours (80% Correlation)**: Direct study duration acts as the foundation of student academic capability.
    4. **Circadian Sleep Deficit**: Deficit parameters directly suppress the Focus Index and feed burnout levels, creating a double-penalty effect on final grades.
    """)
    st.markdown("---")
    st.caption("Developed with ❤️ as a Streamlit Student Performance Optimizer application.")
