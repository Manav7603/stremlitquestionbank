import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import calendar
import json
import os
from PIL import Image
import altair as alt
import time
from ui_components import UIComponents

# Initialize UI components
ui = UIComponents()

# Set page configuration
ui.setup_page_config()
ui.setup_custom_css()

# Initialize session state if not already done
if "data" not in st.session_state:
    # Check if file exists
    if os.path.exists("neet_study_data.json"):
        with open("neet_study_data.json", "r") as f:
            st.session_state.data = json.load(f)
    else:
        st.session_state.data = []
        # Show first entry toast if this is the first time
        ui.show_first_entry_toast()

if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Dashboard"

if "show_success" not in st.session_state:
    st.session_state.show_success = False

# Define subject colors for consistent visualization
subject_colors = {
    "Physics": "#FF5733",
    "Chemistry": "#33A1FD",
    "Botany": "#2ECC71",
    "Zoology": "#9B59B6"
}

# Define the sidebar navigation
with st.sidebar:
    st.image("https://placehold.co/600x400?text=Hello+World", width=200)
    st.markdown("### Navigation")

    # Navigation buttons
    if st.button("📊 Dashboard", use_container_width=True):
        st.session_state.active_tab = "Dashboard"
    
    if st.button("📝 Daily Entry", use_container_width=True):
        st.session_state.active_tab = "Daily Entry"
    
    if st.button("📈 Progress Analysis", use_container_width=True):
        st.session_state.active_tab = "Progress Analysis"
    
    if st.button("📋 Study Log", use_container_width=True):
        st.session_state.active_tab = "Study Log"
    
    if st.button("🎯 Target Setting", use_container_width=True):
        st.session_state.active_tab = "Target Setting"
    
    if st.button("⚙️ Settings", use_container_width=True):
        st.session_state.active_tab = "Settings"
    
    # NEET Countdown
    st.markdown("---")
    # Assuming NEET 2026 is on May 3, 2026
    neet_date = datetime(2026, 4, 3)
    today = datetime.now()
    days_left = (neet_date - today).days
    
    st.markdown("### NEET Countdown")
    # st.markdown(f"<div style='text-align: center; padding: 10px; background-color: #f0f7ff; border-radius: 5px;'><h1 style='color: #0040C1; font-size: 2.5rem;'>{days_left}</h1><p>days left</p></div>", unsafe_allow_html=True)
    st.markdown(
    f"<div style='text-align: center; padding: 10px; "
    f"background-color: #f0f7ff; border-radius: 5px;'>"
    f"<h1 style='color: #0040C1; font-size: 2.5rem;'>{days_left}</h1>"
    f"<p>days left</p></div>",
    unsafe_allow_html=True
)

    # Motivational Quote
    st.markdown("---")
    quotes = [
        "Success is not final, failure is not fatal: It is the courage to continue that counts.",
        "The future belongs to those who believe in the beauty of their dreams.",
        "Don't watch the clock; do what it does. Keep going.",
        "The secret of your success is determined by your daily agenda.",
        "The only way to do great work is to love what you do.",
        "Hard work beats talent when talent doesn't work hard.",
        "Success is the sum of small efforts, repeated day in and day out.",
        "The expert in anything was once a beginner.",
        "Believe you can and you're halfway there.",
        "Your time is limited, don't waste it living someone else's life."
    ]
    
    # Get today's date and use it to select a quote
    today = datetime.now()
    quote_index = (today.year + today.month + today.day) % len(quotes)
    selected_quote = quotes[quote_index]
    
    st.markdown("### Today's Motivation")
    st.markdown(
        f"<div style='font-style: italic; padding: 10px; background-color: #f9f9f9; "
        f"border-left: 3px solid #3366ff; border-radius: 3px;'>"
        f"{selected_quote}"
        f"</div>",
        unsafe_allow_html=True
    )

# Function to save data
def save_data():
    with open("neet_study_data.json", "w") as f:
        json.dump(st.session_state.data, f)

# Function to calculate statistics
def calculate_stats():
    if not st.session_state.data:
        return {
            'total_hours': 0,
            'total_questions': 0,
            'avg_performance': 0,
            'streak': 0
        }
    
    try:
        df = pd.DataFrame(st.session_state.data)
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Convert study duration to hours
        df['Study Hours'] = df['Study Duration'].apply(lambda x: float(x.split()[0]) if isinstance(x, str) and x else 0)
        
        # Convert questions to numeric
        df['Questions'] = df['Questions Attempted'].apply(lambda x: int(x) if pd.notna(x) and x != '' else 0)
        
        # Convert performance to numeric
        df['Performance Score'] = df['Performance'].apply(lambda x: float(x) if pd.notna(x) and x != '' else 0)
        
        # Calculate total study hours
        total_hours = df['Study Hours'].sum()
        
        # Calculate total questions attempted
        total_questions = df['Questions'].sum()
        
        # Calculate average performance score
        avg_performance = df['Performance Score'].mean()
        
        # Calculate current streak
        dates = sorted(df['Date'].dt.date.unique())
        streak = 1
        for i in range(len(dates)-1, 0, -1):
            if (dates[i] - dates[i-1]).days == 1:
                streak += 1
            else:
                break
        
        return {
            'total_hours': round(total_hours, 1),
            'total_questions': int(total_questions),
            'avg_performance': round(avg_performance, 1),
            'streak': streak
        }
    except Exception as e:
        st.error(f"Error calculating statistics: {str(e)}")
        return {
            'total_hours': 0,
            'total_questions': 0,
            'avg_performance': 0,
            'streak': 0
        }

# Dashboard Page
def show_dashboard():
    try:
        if not st.session_state.data:
            st.info("No study data available yet. Start by adding your first study session!")
            return
            
        df = pd.DataFrame(st.session_state.data)
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Convert study duration to hours
        df['Study Hours'] = df['Study Duration'].apply(lambda x: float(x.split()[0]) if isinstance(x, str) and x else 0)
        
        # Convert questions to numeric
        df['Questions'] = df['Questions Attempted'].apply(lambda x: int(x) if pd.notna(x) and x != '' else 0)
        
        # Convert performance to numeric
        df['Performance Score'] = df['Performance'].apply(lambda x: float(x) if pd.notna(x) and x != '' else 0)
        
        # Calculate statistics
        stats = calculate_stats()
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            ui.show_metric_card(
                "Total Study Hours",
                f"{stats['total_hours']}",
                "hours of dedicated study"
            )
        
        with col2:
            ui.show_metric_card(
                "Questions Attempted",
                f"{stats['total_questions']}",
                "practice questions"
            )
        
        with col3:
            ui.show_metric_card(
                "Average Performance",
                f"{stats['avg_performance']}/10",
                "performance score"
            )
        
        with col4:
            ui.show_metric_card(
                "Current Streak",
                f"{stats['streak']}",
                "days"
            )
        
        # Subject-wise distribution
        st.markdown("<div class='sub-header'>Subject Distribution</div>", unsafe_allow_html=True)
        
        # Convert study duration to hours if needed
        if 'Study Duration' in df.columns and 'Study Hours' not in df.columns:
            df['Study Hours'] = df['Study Duration'].apply(lambda x: float(x.split()[0]) if isinstance(x, str) and x else 0)
        
        subject_hours = df.groupby('Subject')['Study Hours'].sum().reset_index()
        total_hours = subject_hours['Study Hours'].sum()
        
        if total_hours > 0:
            subject_hours['Percentage'] = (subject_hours['Study Hours'] / total_hours * 100).round(1)
            
            # Calculate ideal distribution
            ideal_total = total_hours
            ideal_hours = pd.Series({
                'Physics': ideal_total * 0.3,
                'Chemistry': ideal_total * 0.3,
                'Botany': ideal_total * 0.2,
                'Zoology': ideal_total * 0.2
            })
            
            # Create pie chart
            ui.show_subject_pie_chart(subject_hours, "Study Time Distribution by Subject")
            
            # Create comparison analysis
            ui.show_subject_comparison(subject_hours, ideal_hours)
        else:
            st.info("Add study sessions to see subject distribution analysis.")
    except Exception as e:
        st.error(f"Error showing dashboard: {str(e)}")

# Daily Entry Page
def show_daily_entry():
    st.markdown("<h1 class='main-header'>Daily Study Entry</h1>", unsafe_allow_html=True)
    
    # Success message if entry was added
    if st.session_state.show_success:
        st.success("Your study entry was successfully saved!")
        st.session_state.show_success = False
        time.sleep(1)
    
    # Create columns for date and day
    col1, col2 = st.columns(2)
    
    with col1:
        entry_date = st.date_input("Date", datetime.now())
    
    with col2:
        day_of_week = calendar.day_name[entry_date.weekday()]
        st.markdown(f"<div style='padding-top: 32px;'><strong>Day:</strong> {day_of_week}</div>", unsafe_allow_html=True)
    
    # Create tabs for each subject
    subject_tabs = st.tabs(["Physics", "Chemistry", "Botany", "Zoology"])
    
    entries = []
    
    for i, subject in enumerate(["Physics", "Chemistry", "Botany", "Zoology"]):
        with subject_tabs[i]:
            st.markdown(f"<h3 style='color: {subject_colors[subject]};'>{subject} Study Entry</h3>", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                topics = st.text_area(f"Topics/Units Covered ({subject})", key=f"topics_{subject}")
                
                hours = st.number_input(
                    f"Study Duration (hours) ({subject})",
                    min_value=0.0,
                    max_value=12.0,
                    value=0.0,
                    step=0.5,
                    key=f"hours_{subject}"
                )
                
                questions = st.number_input(
                    f"Questions Attempted ({subject})",
                    min_value=0,
                    max_value=1000,
                    value=0,
                    step=5,
                    key=f"questions_{subject}"
                )
                
            with col2:
                goal = st.text_area(f"Goal/Target ({subject})", key=f"goal_{subject}")
                
                motivation = st.slider(
                    f"Energy/Motivation Level ({subject})",
                    min_value=1,
                    max_value=10,
                    value=7,
                    key=f"motivation_{subject}"
                )
                
                performance = st.slider(
                    f"Self-Assessment Performance ({subject})",
                    min_value=1,
                    max_value=10,
                    value=7,
                    key=f"performance_{subject}"
                )
            
            doubts = st.text_area(f"Anything Not Understood/Doubts ({subject})", key=f"doubts_{subject}")
            reflection = st.text_area(f"Self-Reflection ({subject})", key=f"reflection_{subject}")
            next_focus = st.text_area(f"Next Day Focus ({subject})", key=f"next_focus_{subject}")
            
            # Test results/remarks section
            col1, col2 = st.columns(2)
            with col1:
                test_name = st.text_input(f"Test Name (if any) ({subject})", key=f"test_name_{subject}")
            with col2:
                test_result = st.text_input(f"Test Result (if any) ({subject})", key=f"test_result_{subject}")
            
            other_remarks = st.text_area(f"Other Remarks ({subject})", key=f"remarks_{subject}")
            
            # Only add entries with some content
            if hours > 0 or topics or questions > 0:
                result = "GOOD" if performance >= 7 else "BAD"
                entry = {
                    "Date": entry_date.strftime("%Y-%m-%d"),
                    "Day": day_of_week,
                    "Subject": subject,
                    "Topics Covered": topics,
                    "Goal/Target": goal,
                    "Study Duration": f"{hours} hr" if hours else "",
                    "Questions Attempted": str(questions) if questions else "",
                    "Doubts": doubts,
                    "Motivation": str(motivation) if motivation else "",
                    "Self Reflection": reflection,
                    "Next Day Focus": next_focus,
                    "Performance": str(performance) if performance else "",
                    "Result": result,
                    "Test Name": test_name,
                    "Test Result": test_result,
                    "Remarks": other_remarks
                }
                entries.append(entry)
    
    # Submit button
    if st.button("Save Study Entry", use_container_width=True):
        if entries:
            st.session_state.data.extend(entries)
            save_data()
            st.session_state.show_success = True
            st.experimental_rerun()
        else:
            st.warning("Please fill in details for at least one subject before saving.")

# Progress Analysis Page
def show_progress_analysis():
    try:
        if not st.session_state.data:
            st.info("No study data available yet. Start by adding your first study session!")
            return
            
        df = pd.DataFrame(st.session_state.data)
        df['Date'] = pd.to_datetime(df['Date'])
        df['Study Hours'] = pd.to_numeric(df['Study Hours'], errors='coerce').fillna(0)
        df['Questions'] = pd.to_numeric(df['Questions'], errors='coerce').fillna(0)
        df['Performance Score'] = pd.to_numeric(df['Performance Score'], errors='coerce').fillna(0)
        
        # Create tabs for different analyses
        tab1, tab2, tab3 = st.tabs(["Subject Balance", "Performance", "Study Patterns"])
        
        with tab1:
            st.markdown("<div class='sub-header'>Subject Balance Analysis</div>", unsafe_allow_html=True)
            
            # Calculate subject-wise study hours
            subject_hours = df.groupby('Subject')['Study Hours'].sum().reset_index()
            total_hours = subject_hours['Study Hours'].sum()
            
            if total_hours > 0:
                # Calculate percentages
                subject_hours['Percentage'] = (subject_hours['Study Hours'] / total_hours * 100).round(1)
                
                # Calculate ideal distribution
                ideal_total = total_hours
                ideal_hours = pd.Series({
                    'Physics': ideal_total * 0.3,
                    'Chemistry': ideal_total * 0.3,
                    'Botany': ideal_total * 0.2,
                    'Zoology': ideal_total * 0.2
                })
                
                # Show pie chart
                ui.show_subject_pie_chart(subject_hours)
                
                # Show comparison analysis
                ui.show_subject_comparison(subject_hours, ideal_hours)
            else:
                st.info("Add study sessions to see subject balance analysis.")
        
        with tab2:
            st.markdown("<div class='sub-header'>Performance Analysis</div>", unsafe_allow_html=True)
            
            if len(df) > 0:
                # Performance trend over time
                perf_data = df.groupby(['Date', 'Subject'])['Performance Score'].mean().reset_index()
                
                if not perf_data.empty:
                    ui.show_performance_trend(perf_data)
                    
                    # Performance heatmap
                    df['Day of Week'] = df['Date'].dt.day_name()
                    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                    df['Day of Week'] = pd.Categorical(df['Day of Week'], categories=day_order, ordered=True)
                    
                    heatmap_data = df.pivot_table(
                        index='Day of Week',
                        columns='Subject',
                        values='Performance Score',
                        aggfunc='mean'
                    ).reindex(day_order)
                    
                    if not heatmap_data.empty:
                        ui.show_performance_heatmap(heatmap_data)
                    
                    # Performance correlations
                    ui.show_performance_correlations(df)
                else:
                    st.info("Add performance scores to see analysis.")
            else:
                st.info("Add study sessions to see performance analysis.")
        
        with tab3:
            st.markdown("<div class='sub-header'>Study Pattern Analysis</div>", unsafe_allow_html=True)
            
            if len(df) > 0:
                # Daily study time trend
                daily_study = df.groupby('Date')['Study Hours'].sum().reset_index()
                
                if not daily_study.empty:
                    ui.show_study_time_chart(daily_study, "Daily Study Hours")
                    
                    # Study time by day of week
                    df['Day of Week'] = df['Date'].dt.day_name()
                    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                    df['Day of Week'] = pd.Categorical(df['Day of Week'], categories=day_order, ordered=True)
                    
                    dow_study = df.groupby('Day of Week')['Study Hours'].sum().reindex(day_order).reset_index()
                    ui.show_study_time_chart(dow_study, "Study Hours by Day of Week", x='Day of Week')
                    
                    # Study consistency analysis
                    dates_studied = set(df['Date'].dt.date)
                    date_range = pd.date_range(min(dates_studied), max(dates_studied))
                    total_days = len(date_range)
                    days_studied = len(dates_studied)
                    consistency = (days_studied / total_days) * 100 if total_days > 0 else 0
                    
                    ui.show_consistency_gauge(consistency)
                    
                    # Calendar heatmap
                    all_dates = pd.DataFrame({
                        'Date': pd.date_range(start=min(df['Date'].dt.date), end=max(df['Date'].dt.date))
                    })
                    
                    study_counts = df.groupby(df['Date'].dt.date).size().reset_index()
                    study_counts.columns = ['Date', 'Count']
                    
                    calendar_data = all_dates.merge(study_counts, on='Date', how='left').fillna(0)
                    ui.show_study_calendar(calendar_data)
                else:
                    st.info("Add study hours to see pattern analysis.")
            else:
                st.info("Add study sessions to see pattern analysis.")
    except Exception as e:
        st.error(f"Error showing progress analysis: {str(e)}")

# Study Log Page
def show_study_log():
    st.markdown("<h1 class='main-header'>Study Log</h1>", unsafe_allow_html=True)
    
    if not st.session_state.data:
        st.info("No data available yet. Start by adding your daily study entries!")
        return
    
    # Convert data to DataFrame
    df = pd.DataFrame(st.session_state.data)
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Add filters at the top
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Date range filter
        min_date = df['Date'].min().date()
        max_date = df['Date'].max().date()
        
        date_range = st.date_input(
            "Date Range",
            value=(max_date - timedelta(days=7), max_date),
            min_value=min_date,
            max_value=max_date
        )
        
        if len(date_range) == 2:
            start_date, end_date = date_range
            df = df[(df['Date'].dt.date >= start_date) & (df['Date'].dt.date <= end_date)]
    
    with col2:
        # Subject filter
        subjects = ["All"] + sorted(df['Subject'].unique().tolist())
        selected_subject = st.selectbox("Subject", subjects)
        
        if selected_subject != "All":
            df = df[df['Subject'] == selected_subject]
    
    with col3:
        # Performance filter
        performance_options = ["All", "Good (7-10)", "Average (4-6)", "Poor (1-3)"]
        selected_performance = st.selectbox("Performance", performance_options)
        
        if selected_performance != "All":
            if selected_performance == "Good (7-10)":
                df = df[df['Performance'].apply(lambda x: float(x) >= 7 if pd.notna(x) and x != '' else False)]
            elif selected_performance == "Average (4-6)":
                df = df[df['Performance'].apply(lambda x: 4 <= float(x) <= 6 if pd.notna(x) and x != '' else False)]
            elif selected_performance == "Poor (1-3)":
                df = df[df['Performance'].apply(lambda x: float(x) <= 3 if pd.notna(x) and x != '' else False)]
    
    # Sort by date, most recent first
    df = df.sort_values('Date', ascending=False)
    
    # Display entries as cards
    if not df.empty:
        for _, row in df.iterrows():
            subject = row['Subject']
            date_str = row['Date'].strftime('%d %b %Y')
            day = row['Day']
            
            with st.expander(f"{date_str} ({day}) - {subject}"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"<h3 style='color: {subject_colors[subject]};'>{subject} Study Session</h3>", unsafe_allow_html=True)
                    
                    if pd.notna(row['Topics Covered']) and row['Topics Covered']:
                        st.markdown(f"**Topics Covered:** {row['Topics Covered']}")
                    
                    if pd.notna(row['Goal/Target']) and row['Goal/Target']:
                        st.markdown(f"**Goal/Target:** {row['Goal/Target']}")
                    
                    if pd.notna(row['Study Duration']) and row['Study Duration']:
                        st.markdown(f"**Study Duration:** {row['Study Duration']}")
                    
                    if pd.notna(row['Questions Attempted']) and row['Questions Attempted'] and row['Questions Attempted'] != '0':
                        st.markdown(f"**Questions Attempted:** {row['Questions Attempted']}")
                    
                    if pd.notna(row['Doubts']) and row['Doubts']:
                        st.markdown(f"**Doubts/Not Understood:** {row['Doubts']}")
                    
                    if pd.notna(row['Self Reflection']) and row['Self Reflection']:
                        st.markdown(f"**Self Reflection:** {row['Self Reflection']}")
                    
                    if pd.notna(row['Next Day Focus']) and row['Next Day Focus']:
                        st.markdown(f"**Next Day Focus:** {row['Next Day Focus']}")
                    
                    if pd.notna(row['Test Name']) and row['Test Name']:
                        st.markdown(f"**Test Name:** {row['Test Name']}")
                        
                        if pd.notna(row['Test Result']) and row['Test Result']:
                            st.markdown(f"**Test Result:** {row['Test Result']}")
                    
                    if pd.notna(row['Remarks']) and row['Remarks']:
                        st.markdown(f"**Remarks:** {row['Remarks']}")
                
                with col2:
                    # Show performance metrics
                    perf_score = float(row['Performance']) if pd.notna(row['Performance']) and row['Performance'] != '' else 0
                    motivation = float(row['Motivation']) if pd.notna(row['Motivation']) and row['Motivation'] != '' else 0
                    
                    # Performance gauge
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=perf_score,
                        title={'text': "Performance"},
                        gauge={
                            'axis': {'range': [0, 10]},
                            'bar': {'color': subject_colors[subject]},
                            'steps': [
                                {'range': [0, 4], 'color': "#FF5733"},
                                {'range': [4, 7], 'color': "#FFC300"},
                                {'range': [7, 10], 'color': "#2ECC71"}
                            ],
                            'threshold': {
                                'line': {'color': "red", 'width': 4},
                                'thickness': 0.75,
                                'value': 7
                            }
                        }
                    ))
                    fig.update_layout(height=200, margin=dict(l=20, r=20, t=30, b=20))
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Motivation gauge
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=motivation,
                        title={'text': "Motivation"},
                        gauge={
                            'axis': {'range': [0, 10]},
                            'bar': {'color': "#3366ff"},
                            'steps': [
                                {'range': [0, 4], 'color': "#FF5733"},
                                {'range': [4, 7], 'color': "#FFC300"},
                                {'range': [7, 10], 'color': "#2ECC71"}
                            ]
                        }
                    ))
                    fig.update_layout(height=200, margin=dict(l=20, r=20, t=30, b=20))
                    st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No entries match your selected filters.")

# Target Setting Page
def show_target_setting():
    st.markdown("<h1 class='main-header'>Target Setting</h1>", unsafe_allow_html=True)
    
    # Initialize weekly targets in session state if not already done
    if "weekly_targets" not in st.session_state:
        if os.path.exists("weekly_targets.json"):
            with open("weekly_targets.json", "r") as f:
                st.session_state.weekly_targets = json.load(f)
        else:
            st.session_state.weekly_targets = {
                "Physics": {"hours": 10, "questions": 100},
                "Chemistry": {"hours": 10, "questions": 100},
                "Botany": {"hours": 10, "questions": 100},
                "Zoology": {"hours": 10, "questions": 100}
            }
    
    # Initialize daily schedule in session state if not already done
    if "daily_schedule" not in st.session_state:
        if os.path.exists("daily_schedule.json"):
            with open("daily_schedule.json", "r") as f:
                st.session_state.daily_schedule = json.load(f)
        else:
            st.session_state.daily_schedule = {}
            for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
                st.session_state.daily_schedule[day] = []
                for subject in ["Physics", "Chemistry", "Botany", "Zoology"]:
                    st.session_state.daily_schedule[day].append({
                        "subject": subject,
                        "start_time": "14:00" if subject in ["Physics", "Chemistry"] else "16:00",
                        "end_time": "16:00" if subject in ["Physics", "Chemistry"] else "18:00",
                        "enabled": True if day not in ["Saturday", "Sunday"] else False
                    })
    
    # Create tabs for different target setting views
    tab1, tab2, tab3 = st.tabs(["Weekly Targets", "Daily Schedule", "Progress Tracking"])
    
    with tab1:
        st.markdown("<div class='sub-header'>Set Weekly Study Targets</div>", unsafe_allow_html=True)
        
        # Create a form for weekly targets
        with st.form("weekly_targets_form"):
            for subject in ["Physics", "Chemistry", "Botany", "Zoology"]:
                st.markdown(f"<h3 style='color: {subject_colors[subject]};'>{subject}</h3>", unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    hours = st.number_input(
                        f"Weekly study hours target ({subject})",
                        min_value=0,
                        max_value=50,
                        value=st.session_state.weekly_targets[subject]["hours"],
                        step=1,
                        key=f"target_hours_{subject}"
                    )
                
                with col2:
                    questions = st.number_input(
                        f"Weekly questions target ({subject})",
                        min_value=0,
                        max_value=1000,
                        value=st.session_state.weekly_targets[subject]["questions"],
                        step=10,
                        key=f"target_questions_{subject}"
                    )
                
                st.session_state.weekly_targets[subject] = {
                    "hours": hours,
                    "questions": questions
                }
            
            submit = st.form_submit_button("Save Weekly Targets", use_container_width=True)
            
            if submit:
                # Save to file
                with open("weekly_targets.json", "w") as f:
                    json.dump(st.session_state.weekly_targets, f)
                
                st.success("Weekly targets saved successfully!")
    
    with tab2:
        st.markdown("<div class='sub-header'>Set Daily Study Schedule</div>", unsafe_allow_html=True)
        
        # Day selector
        selected_day = st.selectbox(
            "Select day to schedule",
            options=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        )
        
        # Get the schedule for the selected day
        day_schedule = st.session_state.daily_schedule[selected_day]
        
        # Create a form for the daily schedule
        with st.form(f"daily_schedule_form_{selected_day}"):
            for i, session in enumerate(day_schedule):
                subject = session["subject"]
                
                st.markdown(f"<h3 style='color: {subject_colors[subject]};'>{subject}</h3>", unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns([1, 1, 1])
                
                with col1:
                    enabled = st.checkbox(
                        f"Schedule {subject}",
                        value=session["enabled"],
                        key=f"schedule_{selected_day}_{subject}_enabled"
                    )
                
                with col2:
                    start_time = st.time_input(
                        f"Start Time ({subject})",
                        value=datetime.strptime(session["start_time"], "%H:%M").time(),
                        key=f"schedule_{selected_day}_{subject}_start"
                    )
                
                with col3:
                    end_time = st.time_input(
                        f"End Time ({subject})",
                        value=datetime.strptime(session["end_time"], "%H:%M").time(),
                        key=f"schedule_{selected_day}_{subject}_end"
                    )
                
                # Update the session in session state
                st.session_state.daily_schedule[selected_day][i] = {
                    "subject": subject,
                    "start_time": start_time.strftime("%H:%M"),
                    "end_time": end_time.strftime("%H:%M"),
                    "enabled": enabled
                }
            
            submit = st.form_submit_button(f"Save {selected_day} Schedule", use_container_width=True)
            
            if submit:
                # Save to file
                with open("daily_schedule.json", "w") as f:
                    json.dump(st.session_state.daily_schedule, f)
                
                st.success(f"{selected_day} schedule saved successfully!")
        
        # Display the weekly schedule as a visual timetable
        st.markdown("<div class='sub-header'>Weekly Schedule Overview</div>", unsafe_allow_html=True)
        
        # Create a visual timetable
        # Hours from 8 AM to 10 PM
        hours = list(range(8, 23))
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        # Create a matrix to represent the timetable (days x hours)
        timetable = np.zeros((len(days), len(hours)), dtype=object)
        
        # Fill in the timetable with subject names
        for day_idx, day in enumerate(days):
            day_schedule = st.session_state.daily_schedule[day]
            
            for session in day_schedule:
                if session["enabled"]:
                    subject = session["subject"]
                    start_hour = int(session["start_time"].split(":")[0])
                    end_hour = int(session["end_time"].split(":")[0])
                    
                    # Adjust for our hour range starting at 8
                    start_idx = start_hour - 8
                    end_idx = end_hour - 8
                    
                    # Fill the cells with the subject name
                    for hour_idx in range(start_idx, end_idx + 1):
                        if 0 <= hour_idx < len(hours):
                            timetable[day_idx, hour_idx] = subject
        
        # Create the visual timetable
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Create a colormap
        cmap = plt.cm.colors.ListedColormap(['#f8f9fa'] + list(subject_colors.values()))
        bounds = [0, 1, 2, 3, 4, 5]
        norm = plt.cm.colors.BoundaryNorm(bounds, cmap.N)
        
        # Create an array for coloring
        color_array = np.zeros(timetable.shape)
        
        for i in range(timetable.shape[0]):
            for j in range(timetable.shape[1]):
                if timetable[i, j] == 0:
                    color_array[i, j] = 0  # Empty
                else:
                    color_array[i, j] = list(subject_colors.keys()).index(timetable[i, j]) + 1
        
        # Plot the heatmap
        heatmap = ax.pcolor(color_array, cmap=cmap, norm=norm, edgecolors='gray', linewidths=1)
        
        # Add text labels
        for i in range(timetable.shape[0]):
            for j in range(timetable.shape[1]):
                if timetable[i, j] != 0:
                    ax.text(j + 0.5, i + 0.5, timetable[i, j], 
                            ha="center", va="center", 
                            color="white", fontweight="bold")
        
        # Set ticks and labels
        ax.set_xticks(np.arange(len(hours)) + 0.5)
        ax.set_yticks(np.arange(len(days)) + 0.5)
        ax.set_xticklabels([f"{hour}:00" for hour in hours])
        ax.set_yticklabels(days)
        ax.set_title("Weekly Study Schedule")
        
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
        
        # Add a legend
        handles = [plt.Rectangle((0,0),1,1, color=color) for color in list(subject_colors.values())]
        labels = list(subject_colors.keys())
        ax.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=len(subject_colors))
        
        fig.tight_layout()
        st.pyplot(fig)
    
    with tab3:
        st.markdown("<div class='sub-header'>This Week's Progress</div>", unsafe_allow_html=True)
        
        # Calculate the current week's progress
        if st.session_state.data:
            df = pd.DataFrame(st.session_state.data)
            df['Date'] = pd.to_datetime(df['Date'])
            
            # Get the current week's data
            today = datetime.now()
            start_of_week = today - timedelta(days=today.weekday())
            end_of_week = start_of_week + timedelta(days=6)
            
            # Filter for current week
            week_df = df[(df['Date'] >= start_of_week) & (df['Date'] <= end_of_week)]
            
            if not week_df.empty:
                # Convert study duration to hours
                week_df['Study Hours'] = week_df['Study Duration'].apply(lambda x: float(x.split()[0]) if isinstance(x, str) and x else 0)
                
                # Convert questions to numeric
                week_df['Questions'] = week_df['Questions Attempted'].apply(lambda x: int(x) if pd.notna(x) and x != '' else 0)
                
                # Group by subject
                subject_progress = week_df.groupby('Subject').agg({
                    'Study Hours': 'sum',
                    'Questions': 'sum'
                }).reset_index()
                
                # Convert to dict for easier lookup
                progress_dict = {row['Subject']: {'hours': row['Study Hours'], 'questions': row['Questions']} 
                                for _, row in subject_progress.iterrows()}
                
                # Create progress cards for each subject
                for subject in ["Physics", "Chemistry", "Botany", "Zoology"]:
                    target_hours = st.session_state.weekly_targets[subject]["hours"]
                    target_questions = st.session_state.weekly_targets[subject]["questions"]
                    
                    current_hours = progress_dict.get(subject, {}).get('hours', 0)
                    current_questions = progress_dict.get(subject, {}).get('questions', 0)
                    
                    hours_percent = min(100, int((current_hours / target_hours * 100) if target_hours > 0 else 0))
                    questions_percent = min(100, int((current_questions / target_questions * 100) if target_questions > 0 else 0))
                    
                    st.markdown(f"<h3 style='color: {subject_colors[subject]};'>{subject}</h3>", unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("<div style='text-align: center;'>Study Hours</div>", unsafe_allow_html=True)
                        st.progress(hours_percent / 100)
                        st.markdown(f"<div class='progress-text'>{current_hours}/{target_hours} hours ({hours_percent}%)</div>", unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown("<div style='text-align: center;'>Questions</div>", unsafe_allow_html=True)
                        st.progress(questions_percent / 100)
                        st.markdown(f"<div class='progress-text'>{current_questions}/{target_questions} questions ({questions_percent}%)</div>", unsafe_allow_html=True)
            else:
                st.info("No study data recorded for the current week yet.")
        else:
            st.info("No study data available yet. Start by adding your daily study entries!")

# Settings Page
def show_settings():
    st.markdown("<h1 class='main-header'>Settings</h1>", unsafe_allow_html=True)
    
    # Create tabs for different settings
    tab1, tab2, tab3 = st.tabs(["Profile", "Data Management", "App Settings"])
    
    with tab1:
        st.markdown("<div class='sub-header'>Profile Information</div>", unsafe_allow_html=True)
        
        # Initialize profile data if not already done
        if "profile" not in st.session_state:
            if os.path.exists("profile_data.json"):
                with open("profile_data.json", "r") as f:
                    st.session_state.profile = json.load(f)
            else:
                st.session_state.profile = {
                    "name": "",
                    "target_college": "AIIMS",
                    "exam_year": 2026,
                    "weak_subjects": [],
                    "strong_subjects": []
                }
        
        # Create a form for profile information
        with st.form("profile_form"):
            st.session_state.profile["name"] = st.text_input(
                "Your Name",
                value=st.session_state.profile["name"]
            )
            
            st.session_state.profile["target_college"] = st.text_input(
                "Target College/Institute",
                value=st.session_state.profile["target_college"]
            )
            
            st.session_state.profile["exam_year"] = st.number_input(
                "Target NEET Year",
                min_value=2025,
                max_value=2030,
                value=st.session_state.profile["exam_year"]
            )
            
            st.session_state.profile["weak_subjects"] = st.multiselect(
                "Subjects You Find Challenging",
                options=["Physics", "Chemistry", "Botany", "Zoology"],
                default=st.session_state.profile["weak_subjects"]
            )
            
            st.session_state.profile["strong_subjects"] = st.multiselect(
                "Subjects You're Confident In",
                options=["Physics", "Chemistry", "Botany", "Zoology"],
                default=st.session_state.profile["strong_subjects"]
            )
            
            submit = st.form_submit_button("Save Profile", use_container_width=True)
            
            if submit:
                # Save to file
                with open("profile_data.json", "w") as f:
                    json.dump(st.session_state.profile, f)
                
                st.success("Profile information saved successfully!")
    
    with tab2:
        st.markdown("<div class='sub-header'>Data Management</div>", unsafe_allow_html=True)
        
        # Backup data option
        if st.button("Export All Data (Backup)", use_container_width=True):
            # Prepare all data for export
            all_data = {
                "study_data": st.session_state.data,
                "weekly_targets": st.session_state.weekly_targets if "weekly_targets" in st.session_state else {},
                "daily_schedule": st.session_state.daily_schedule if "daily_schedule" in st.session_state else {},
                "profile": st.session_state.profile if "profile" in st.session_state else {}
            }
            
            # Convert to JSON
            json_data = json.dumps(all_data, indent=4)
            
            # Create a download link
            b64 = base64.b64encode(json_data.encode()).decode()
            today = datetime.now().strftime("%Y-%m-%d")
            href = f'<a href="data:application/json;base64,{b64}" download="neet_tracker_backup_{today}.json">Download Backup File</a>'
            st.markdown(href, unsafe_allow_html=True)
            st.success("Backup file ready for download!")
        
        # Import data option
        st.markdown("<div class='sub-header'>Import Data</div>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Upload backup file (JSON)", type="json")
        
        if uploaded_file is not None:
            try:
                imported_data = json.load(uploaded_file)
                
                # Verify the data structure
                required_keys = ["study_data", "weekly_targets", "daily_schedule", "profile"]
                if all(key in imported_data for key in required_keys):
                    if st.button("Confirm Import", use_container_width=True):
                        # Update session state
                        st.session_state.data = imported_data["study_data"]
                        st.session_state.weekly_targets = imported_data["weekly_targets"]
                        st.session_state.daily_schedule = imported_data["daily_schedule"]
                        st.session_state.profile = imported_data["profile"]
                        
                        # Save to files
                        with open("neet_study_data.json", "w") as f:
                            json.dump(st.session_state.data, f)
                        
                        with open("weekly_targets.json", "w") as f:
                            json.dump(st.session_state.weekly_targets, f)
                        
                        with open("daily_schedule.json", "w") as f:
                            json.dump(st.session_state.daily_schedule, f)
                        
                        with open("profile_data.json", "w") as f:
                            json.dump(st.session_state.profile, f)
                        
                        st.success("Data imported successfully!")
                else:
                    st.error("The uploaded file doesn't have the correct data structure.")
            except Exception as e:
                st.error(f"Error importing data: {e}")
        
        # Clear data option with confirmation
        st.markdown("<div class='sub-header'>Clear Data</div>", unsafe_allow_html=True)
        st.warning("⚠️ This will delete all your study data and cannot be undone!")
        
        col1, col2 = st.columns(2)
        
        with col1:
            clear_confirmation = st.text_input("Type 'DELETE' to confirm")
        
        with col2:
            if st.button("Clear All Data", use_container_width=True):
                if clear_confirmation == "DELETE":
                    # Clear session state
                    st.session_state.data = []
                    
                    # Remove data files
                    if os.path.exists("neet_study_data.json"):
                        os.remove("neet_study_data.json")
                    
                    st.success("All study data has been cleared!")
                    time.sleep(1)
                    st.experimental_rerun()
                else:
                    st.error("Please type 'DELETE' to confirm data clearing.")
    
    with tab3:
        st.markdown("<div class='sub-header'>App Settings</div>", unsafe_allow_html=True)
        
        # Initialize app settings if not already done
        if "app_settings" not in st.session_state:
            if os.path.exists("app_settings.json"):
                with open("app_settings.json", "r") as f:
                    st.session_state.app_settings = json.load(f)
            else:
                st.session_state.app_settings = {
                    "notifications_enabled": True,
                    "neet_date": "2026-05-03",
                    "daily_goal_hours": 6,
                }
        
        # Create a form for app settings
        with st.form("app_settings_form"):
            st.session_state.app_settings["notifications_enabled"] = st.checkbox(
                "Enable Notifications",
                value=st.session_state.app_settings["notifications_enabled"]
            )
            
            st.session_state.app_settings["neet_date"] = st.date_input(
                "NEET Exam Date",
                value=datetime.strptime(st.session_state.app_settings["neet_date"], "%Y-%m-%d").date()
            ).strftime("%Y-%m-%d")
            
            st.session_state.app_settings["daily_goal_hours"] = st.number_input(
                "Daily Study Goal (hours)",
                min_value=1,
                max_value=12,
                value=st.session_state.app_settings["daily_goal_hours"]
            )
            
            submit = st.form_submit_button("Save Settings", use_container_width=True)
            
            if submit:
                # Save to file
                with open("app_settings.json", "w") as f:
                    json.dump(st.session_state.app_settings, f)
                
                st.success("App settings saved successfully!")

# Main App Logic
if st.session_state.active_tab == "Dashboard":
    show_dashboard()
elif st.session_state.active_tab == "Daily Entry":
    show_daily_entry()
elif st.session_state.active_tab == "Progress Analysis":
    show_progress_analysis()
elif st.session_state.active_tab == "Study Log":
    show_study_log()
elif st.session_state.active_tab == "Target Setting":
    show_target_setting()
elif st.session_state.active_tab == "Settings":
    show_settings()

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: #888;'>NEET Study Tracker v1.0 | Created with ❤️ for Pallav</div>", unsafe_allow_html=True)