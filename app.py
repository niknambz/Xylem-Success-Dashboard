import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(page_title="Xylem L&D Strategy Dashboard", layout="wide")

st.title("📊 Student Success Framework: Performance & ROI Dashboard")
st.markdown("---")

# --- SIDEBAR: INPUT PARAMETERS ---
st.sidebar.header("Operational Inputs")
avg_salary = st.sidebar.number_input("Average Mentor Salary (Annual)", value=400000)
num_mentors = st.sidebar.number_input("Total Mentors", value=50)
attrition_rate = st.sidebar.slider("Current Annual Attrition Rate (%)", 0, 100, 30)
admin_hours_leak = st.sidebar.slider("Admin Hours Lost/Day per Mentor", 0, 8, 4)

# --- SECTION 1: ECONOMICS OF ATTRITION ---
st.header("1. Economics of Attrition")
# Formula: (Recruitment + Training) + (Vacancy Loss) + (Churn Risk) 
# Using a standard 0.5x salary multiplier for fully burdened attrition cost
k_multiplier = 0.5
total_attrition_cost = (num_mentors * (attrition_rate / 100)) * (avg_salary * k_multiplier)

col1, col2 = st.columns(2)
with col1:
    st.metric("Total Annual Attrition Cost", f"₹{total_attrition_cost:,.0f}")
    st.caption("Based on the 'Success Gap' formula ")

with col2:
    target_reduction = 0.10 # Proposed 10% reduction [cite: 113]
    potential_savings = total_attrition_cost * target_reduction
    st.metric("Projected L&D Savings (Phase 1)", f"₹{potential_savings:,.0f}", delta="10% Reduction")

# --- SECTION 2: STUDENT SENTIMENT INDEX (SSI) ---
st.header("2. Student Sentiment Index (SSI)")
st.info("Weighted score based on parent CRM logs and sentiment tags ")

col3, col4, col5 = st.columns(3)
with col3:
    happy = st.number_input("Happy Logs", value=150)
with col4:
    anxious = st.number_input("Anxious Logs", value=40)
with col5:
    angry = st.number_input("Angry Logs", value=10)

# Weighted Formula: SSI = (Happy*1 + Anxious*0.5 + Angry*-1) / Total
total_logs = happy + anxious + angry
if total_logs > 0:
    ssi_score = ((happy * 1) + (anxious * 0.5) + (angry * -1)) / total_logs
    st.subheader(f"Current SSI Score: {ssi_score:.2f} / 1.00")
    st.progress(max(0.0, min(ssi_score, 1.0)))

# --- SECTION 3: RECOVERED CAPACITY ---
st.header("3. Recovered Operational Capacity")
# [cite: 105, 107]
total_weekly_hours = num_mentors * 6 * 8 # 6 days, 8 hours
total_leaked_hours = num_mentors * 6 * admin_hours_leak
efficiency = ((total_weekly_hours - total_leaked_hours) / total_weekly_hours) * 100

st.write(f"Currently, the mentor team is operating at **{efficiency:.1f}% efficiency** due to admin drag.")
st.write(f"By deploying the **Digital Manual**, we recover **{total_leaked_hours} hours per week** of Success Manager time[cite: 107].")