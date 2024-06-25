import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random
from datetime import datetime, timedelta

# Set page config
st.set_page_config(page_title="Hospital Dashboard", layout="wide")

# Sample data generation (replace with your actual data)
def generate_sample_data():
    departments = ['Cardiology', 'Neurology', 'Orthopedics', 'Pediatrics']
    physicians = ['Dr. Smith', 'Dr. Johnson', 'Dr. Williams', 'Dr. Brown']
    
    wait_times = [random.randint(10, 60) for _ in range(30)]
    occupancy_rates = [random.randint(50, 100) for _ in range(30)]
    demographics = {'Age 0-18': 20, 'Age 19-40': 35, 'Age 41-60': 30, 'Age 61+': 15}
    
    appointments = pd.DataFrame({
        'Date': [datetime.now().date() + timedelta(days=i) for i in range(10)],
        'Time': [f"{random.randint(8, 17):02d}:00" for _ in range(10)],
        'Department': [random.choice(departments) for _ in range(10)],
        'Physician': [random.choice(physicians) for _ in range(10)],
        'Patient': [f"Patient {i+1}" for i in range(10)]
    })
    
    return wait_times, occupancy_rates, demographics, appointments, departments, physicians

# Generate sample data
wait_times, occupancy_rates, demographics, appointments, departments, physicians = generate_sample_data()

# Sidebar for filters
st.sidebar.header("Filters")
selected_department = st.sidebar.selectbox("Select Department", ["All"] + departments)
selected_physician = st.sidebar.selectbox("Select Physician", ["All"] + physicians)

# Main dashboard
st.title("Hospital Dashboard")

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Avg. Patient Wait Time", f"{sum(wait_times) // len(wait_times)} min")
col2.metric("Avg. Bed Occupancy Rate", f"{sum(occupancy_rates) // len(occupancy_rates)}%")
col3.metric("Readmission Rate", "12%")  # Replace with actual data

# Charts
col1, col2 = st.columns(2)

# Line chart for patient wait times
fig_wait_times = px.line(x=range(1, 31), y=wait_times, labels={'x': 'Day', 'y': 'Wait Time (minutes)'})
fig_wait_times.update_layout(title="Patient Wait Times (Last 30 Days)")
col1.plotly_chart(fig_wait_times, use_container_width=True)

# Bar chart for occupancy rates
fig_occupancy = px.bar(x=range(1, 31), y=occupancy_rates, labels={'x': 'Day', 'y': 'Occupancy Rate (%)'})
fig_occupancy.update_layout(title="Bed Occupancy Rates (Last 30 Days)")
col2.plotly_chart(fig_occupancy, use_container_width=True)

# Pie chart for patient demographics
fig_demographics = px.pie(values=demographics.values(), names=demographics.keys())
fig_demographics.update_layout(title="Patient Demographics")
st.plotly_chart(fig_demographics, use_container_width=True)

# Table for upcoming appointments
st.subheader("Upcoming Appointments and Schedules")
st.dataframe(appointments, use_container_width=True)

# Apply filters (in a real scenario, you'd filter the data before creating charts)
if selected_department != "All" or selected_physician != "All":
    st.warning(f"Filters applied: Department - {selected_department}, Physician - {selected_physician}")
    st.info("Note: In a real scenario, the data would be filtered based on these selections.")