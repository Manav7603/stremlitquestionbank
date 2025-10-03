import streamlit as st
from typing import Dict, List, Optional, Any
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime
import random

class UIComponents:
    def __init__(self):
        self.subject_colors = {
            "Physics": "#FF5733",
            "Chemistry": "#33A1FD",
            "Botany": "#2ECC71",
            "Zoology": "#9B59B6"
        }
        self.motivational_quotes = [
            "Every great journey begins with a single step! 🚀",
            "Your first entry marks the start of something amazing! ✨",
            "Welcome to your NEET preparation journey! 📚",
            "First entry logged - the adventure begins! 🌟",
            "You've taken the first step towards success! 🎯"
        ]
        
    def setup_page_config(self):
        """Set up the page configuration."""
        st.set_page_config(
            page_title="NEET Study Tracker",
            page_icon="📚",
            layout="wide",
            initial_sidebar_state="expanded",
        )
        
    def setup_custom_css(self):
        """Set up custom CSS styles."""
        st.markdown("""
        <style>
            .main-header {
                font-size: 2.5rem;
                font-weight: bold;
                color: #3366ff;
                text-align: center;
                margin-bottom: 1rem;
                padding-bottom: 1rem;
                border-bottom: 2px solid #f0f2f6;
            }
            .sub-header {
                font-size: 1.5rem;
                font-weight: bold;
                color: #0040C1;
                margin-top: 1rem;
                margin-bottom: 0.5rem;
            }
            .metric-card {
                background-color: #ffffff;
                border-radius: 8px;
                padding: 15px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
                text-align: center;
            }
            .metric-value {
                font-size: 1.8rem;
                font-weight: bold;
                color: #3366ff;
            }
            .metric-label {
                font-size: 0.9rem;
                color: #666;
            }
            .metric-description {
                font-size: 0.9rem;
                color: #666;
            }
        </style>
        """, unsafe_allow_html=True)
        
    def show_metric_card(self, label: str, value: str, description: str):
        """Display a metric card."""
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-value'>{value}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-label'>{label}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-description'>{description}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
            
    def show_subject_pie_chart(self, data: pd.DataFrame, title: str):
        """Display a pie chart for subject distribution."""
        # Ensure we have the correct column names
        if 'Study Hours' in data.columns:
            values_col = 'Study Hours'
        elif 'Study Duration' in data.columns:
            values_col = 'Study Duration'
        else:
            st.error("No study time data found in the dataframe")
            return
            
        fig = px.pie(
            data,
            values=values_col,
            names='Subject',
            title=title,
            color='Subject',
            color_discrete_map=self.subject_colors
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
        
    def show_performance_trend(self, data: pd.DataFrame):
        """Display performance trend over time."""
        fig = px.line(
            data,
            x='Date',
            y='Performance',
            color='Subject',
            title='Performance Trend by Subject',
            color_discrete_map=self.subject_colors
        )
        fig.update_layout(
            xaxis_title='Date',
            yaxis_title='Performance Score',
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)
        
    def show_study_time_chart(self, data: pd.DataFrame):
        """Display study time distribution."""
        fig = px.bar(
            data,
            x='Date',
            y='Study Duration',
            color='Subject',
            title='Daily Study Time by Subject',
            color_discrete_map=self.subject_colors
        )
        fig.update_layout(
            xaxis_title='Date',
            yaxis_title='Study Duration (hours)',
            barmode='stack'
        )
        st.plotly_chart(fig, use_container_width=True)
        
    def show_loading_spinner(self, message: str = "Loading..."):
        """Display a loading spinner."""
        return st.spinner(message)
        
    def show_error_message(self, message: str):
        """Display an error message."""
        st.error(message)
        
    def show_success_message(self, message: str):
        """Display a success message."""
        st.success(message)
        
    def show_warning_message(self, message: str):
        """Display a warning message."""
        st.warning(message)
        
    def show_info_message(self, message: str):
        """Display an info message."""
        st.info(message)
        
    def show_confirmation_dialog(self, message: str) -> bool:
        """Show a confirmation dialog."""
        return st.button(message)
        
    def show_date_picker(self, label: str, default_value: datetime = None) -> datetime:
        """Show a date picker."""
        return st.date_input(label, value=default_value or datetime.now())
        
    def show_subject_selector(self, label: str = "Select Subject") -> str:
        """Show a subject selector."""
        return st.selectbox(label, list(self.subject_colors.keys()))
        
    def show_number_input(self, label: str, min_value: float, max_value: float, 
                         default_value: float = 0.0, step: float = 0.5) -> float:
        """Show a number input field."""
        return st.number_input(
            label,
            min_value=min_value,
            max_value=max_value,
            value=default_value,
            step=step
        )
        
    def show_text_input(self, label: str, default_value: str = "") -> str:
        """Show a text input field."""
        return st.text_input(label, value=default_value)
        
    def show_text_area(self, label: str, default_value: str = "") -> str:
        """Show a text area field."""
        return st.text_area(label, value=default_value)
        
    def show_slider(self, label: str, min_value: int, max_value: int, 
                   default_value: int = 5) -> int:
        """Show a slider input."""
        return st.slider(
            label,
            min_value=min_value,
            max_value=max_value,
            value=default_value
        )
        
    def show_first_entry_toast(self):
        """Display a creative toast notification for first entry."""
        st.markdown("""
        <style>
            @keyframes slideIn {
                from { transform: translateY(-100%); opacity: 0; }
                to { transform: translateY(0); opacity: 1; }
            }
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
            .first-entry-toast {
                position: fixed;
                top: 20px;
                right: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 20px;
                border-radius: 15px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.2);
                z-index: 1000;
                animation: slideIn 0.5s ease-out;
                max-width: 400px;
                border-left: 5px solid #ffd700;
            }
            .first-entry-toast h3 {
                margin: 0 0 10px 0;
                font-size: 1.5em;
                color: #ffd700;
                animation: fadeIn 1s ease-out;
            }
            .first-entry-toast p {
                margin: 0;
                font-size: 1.1em;
                line-height: 1.4;
            }
            .first-entry-toast .emoji {
                font-size: 1.5em;
                margin-right: 10px;
            }
            .first-entry-toast .confetti {
                position: absolute;
                width: 10px;
                height: 10px;
                background-color: #ffd700;
                opacity: 0;
                animation: confetti 2s ease-out infinite;
            }
            @keyframes confetti {
                0% { transform: translateY(0) rotate(0deg); opacity: 1; }
                100% { transform: translateY(100px) rotate(360deg); opacity: 0; }
            }
        </style>
        """, unsafe_allow_html=True)
        
        quote = random.choice(self.motivational_quotes)
        st.markdown(f"""
        <div class="first-entry-toast">
            <h3>🎉 Welcome to NEET Study Tracker!</h3>
            <p>{quote}</p>
            <div class="confetti" style="left: 10%; animation-delay: 0s;"></div>
            <div class="confetti" style="left: 30%; animation-delay: 0.2s;"></div>
            <div class="confetti" style="left: 50%; animation-delay: 0.4s;"></div>
            <div class="confetti" style="left: 70%; animation-delay: 0.6s;"></div>
            <div class="confetti" style="left: 90%; animation-delay: 0.8s;"></div>
        </div>
        """, unsafe_allow_html=True)
        
        # Add a small delay to ensure the toast is visible
        st.markdown("""
        <script>
            setTimeout(function() {
                document.querySelector('.first-entry-toast').style.display = 'none';
            }, 5000);
        </script>
        """, unsafe_allow_html=True)
        
    def show_subject_comparison(self, actual_hours: pd.DataFrame, ideal_hours: pd.Series):
        """Display a comparison between actual and ideal study time distribution."""
        # Convert ideal hours to DataFrame
        ideal_df = pd.DataFrame({
            'Subject': ideal_hours.index,
            'Study Hours': ideal_hours.values
        })
        
        # Calculate total hours for percentage calculation
        total_actual = actual_hours['Study Hours'].sum()
        total_ideal = ideal_df['Study Hours'].sum()
        
        # Calculate percentages
        actual_hours['Percentage'] = (actual_hours['Study Hours'] / total_actual * 100).round(1)
        ideal_df['Percentage'] = (ideal_df['Study Hours'] / total_ideal * 100).round(1)
        
        # Create a combined DataFrame for visualization
        comparison_df = pd.merge(
            actual_hours[['Subject', 'Percentage']].rename(columns={'Percentage': 'Actual'}),
            ideal_df[['Subject', 'Percentage']].rename(columns={'Percentage': 'Ideal'}),
            on='Subject'
        )
        
        # Create the bar chart
        fig = go.Figure()
        
        # Add actual hours bar
        fig.add_trace(go.Bar(
            name='Actual',
            x=comparison_df['Subject'],
            y=comparison_df['Actual'],
            marker_color=[self.subject_colors[sub] for sub in comparison_df['Subject']],
            opacity=0.8
        ))
        
        # Add ideal hours bar
        fig.add_trace(go.Bar(
            name='Ideal',
            x=comparison_df['Subject'],
            y=comparison_df['Ideal'],
            marker_color=[self.subject_colors[sub] for sub in comparison_df['Subject']],
            opacity=0.4
        ))
        
        # Update layout
        fig.update_layout(
            title='Actual vs Ideal Study Time Distribution',
            xaxis_title='Subject',
            yaxis_title='Percentage of Total Study Time',
            barmode='group',
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        st.plotly_chart(fig, use_container_width=True) 