import streamlit as st

# Page Configuration
st.set_page_config(page_title="Xylem L&D Strategy Dashboard", layout="wide")

st.title("📊 Student Success Framework: Performance & ROI Dashboard")
st.markdown("---")

# --- DATA STRUCTURE FOR DISTRICTS AND CENTERS ---
center_data = {
    "Trivandrum": {
        "Sreekaryam Hybrid": {"happy": 80, "anxious": 20, "angry": 5},
        "Statue Hybrid": {"happy": 60, "anxious": 15, "angry": 8},
        "Gokulam ISP": {"happy": 90, "anxious": 10, "angry": 2},
        "MGM ISP": {"happy": 75, "anxious": 25, "angry": 4},
        "Saraswathi ISP": {"happy": 85, "anxious": 12, "angry": 3},
        "Neyyatinkara Tuition": {"happy": 50, "anxious": 30, "angry": 12}
    },
    "Calicut": {
        "Future Campus": {"happy": 110, "anxious": 18, "angry": 4},
        "Gokulam School": {"happy": 95, "anxious": 12, "angry": 2},
        "Sadhbhava School": {"happy": 88, "anxious": 15, "angry": 5}
    }
}

# --- SIDEBAR: OPERATIONAL INPUTS ---
st.sidebar.header("Operational Inputs")
avg_salary = st.sidebar.number_input("Average Mentor Salary (Annual)", value=400000)
num_mentors = st.sidebar.number_input("Total Mentors", value=50)
attrition_rate = st.sidebar.slider("Current Annual Attrition Rate (%)", 0, 100, 30)
admin_hours_leak = st.sidebar.slider("Admin Hours Lost/Day per Mentor", 0, 8, 4)

# --- SECTION 1: ECONOMICS OF ATTRITION ---
st.header("1. Economics of Attrition")
# Formula: Using a standard 0.5x salary multiplier for fully burdened attrition cost
k_multiplier = 0.5
total_attrition_cost = (num_mentors * (attrition_rate / 100)) * (avg_salary * k_multiplier)

col1, col2 = st.columns(2)
with col1:
    st.metric("Total Annual Attrition Cost", f"₹{total_attrition_cost:,.0f}")
    st.caption("Based on Recruitment + Training + Vacancy Loss + Churn Risk")

with col2:
    target_reduction = 0.10 # Proposed 10% reduction
    potential_savings = total_attrition_cost * target_reduction
    st.metric("Projected L&D Savings (Phase 1)", f"₹{potential_savings:,.0f}", delta="10% Reduction Goal")

st.markdown("---")

# --- SECTION 2: STUDENT SENTIMENT INDEX (SSI) ---
st.header("2. Student Sentiment Index (SSI)")
st.info("Weighted score based on center-specific parent CRM logs. High negative weighting helps identify churn risks early.")

# Dropdown 1: District
district = st.selectbox("Select District", options=["Trivandrum", "Calicut"])

# Dropdown 2: Center (Conditional based on District)
center_options = list(center_data[district].keys())
center = st.selectbox("Select Center", options=center_options)

# Fetch pre-set data for the selected center
default_vals = center_data[district][center]

st.write(f"### Live Log Data: {center}")
col3, col4, col5 = st.columns(3)

with col3:
    happy = st.number_input("Happy Logs", value=default_vals["happy"])
with col4:
    anxious = st.number_input("Anxious Logs", value=default_vals["anxious"])
with col5:
    angry = st.number_input("Angry Logs", value=default_vals["angry"])

# --- SSI CALCULATION ---
total_logs = happy + anxious + angry

if total_logs > 0:
    # UPDATED FORMULA: ((happy * 1) + (anxious * 0.5) + (angry * -2)) / total_logs
    ssi_raw = ((happy * 1) + (anxious * 0.5) + (angry * -2)) / total_logs
    
    # Normalize for the progress bar (Visuals only)
    display_val = max(0.0, min((ssi_raw + 2) / 3, 1.0)) 
    
    st.subheader(f"Current SSI Score: {ssi_raw:.2f}")
    st.progress(display_val)
    
    if ssi_raw < 0:
        st.error("🚨 CRITICAL: Immediate intervention required. High negative sentiment.")
    elif ssi_raw < 0.5:
        st.warning("⚠️ ATTENTION: Sentiment is dipping. Review parent liaison logs.")
    else:
        st.success("✅ STABLE: Center maintaining healthy parent relationships.")
else:
    st.write("Enter log data to calculate the Sentiment Index.")

st.markdown("---")

# --- SECTION 3: RECOVERED CAPACITY ---
st.header("3. Recovered Operational Capacity")
total_weekly_hours = num_mentors * 6 * 8 # 6 days, 8 hours
total_leaked_hours = num_mentors * 6 * admin_hours_leak
efficiency = ((total_weekly_hours - total_leaked_hours) / total_weekly_hours) * 100

st.write(f"Based on current data, the mentor workforce is operating at **{efficiency:.1f}% efficiency** due to administrative drag.")
st.write(f"By deploying the **Digital Manual**, we recover **{total_leaked_hours} hours per week** across the organization.")

st.markdown("---")
st.caption("Confidential L&D Proposal | Xylem Learning")