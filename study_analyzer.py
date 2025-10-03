import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta

class StudyAnalyzer:
    def __init__(self, data: List[Dict[str, Any]]):
        self.data = pd.DataFrame(data)
        if not self.data.empty:
            self.data['Date'] = pd.to_datetime(self.data['Date'])
            self._preprocess_data()
            
    def _preprocess_data(self):
        """Preprocess the data for analysis."""
        # Convert study duration to numeric
        self.data['Study Duration'] = self.data['Study Duration'].apply(
            lambda x: float(x.split()[0]) if isinstance(x, str) else 0
        )
        
        # Convert performance to numeric
        self.data['Performance'] = self.data['Performance'].apply(
            lambda x: float(x) if pd.notna(x) and x != '' else 0
        )
        
        # Convert questions attempted to numeric
        self.data['Questions Attempted'] = self.data['Questions Attempted'].apply(
            lambda x: int(x) if pd.notna(x) and x != '' else 0
        )
        
        # Convert motivation to numeric
        self.data['Motivation'] = self.data['Motivation'].apply(
            lambda x: int(x) if pd.notna(x) and x != '' else 0
        )
        
    def calculate_overall_stats(self) -> Dict[str, Any]:
        """Calculate overall statistics."""
        if self.data.empty:
            return {}
            
        stats = {
            'total_study_hours': self.data['Study Duration'].sum(),
            'total_days': self.data['Date'].nunique(),
            'total_questions': self.data['Questions Attempted'].sum(),
            'avg_motivation': self.data['Motivation'].mean(),
            'avg_performance': self.data['Performance'].mean(),
            'current_streak': self._calculate_streak()
        }
        
        return stats
        
    def _calculate_streak(self) -> int:
        """Calculate the current study streak."""
        if self.data.empty:
            return 0
            
        dates = sorted(self.data['Date'].dt.date.unique())
        current_streak = 1
        
        for i in range(len(dates)-1):
            if (dates[i+1] - dates[i]).days == 1:
                current_streak += 1
            else:
                break
                
        return current_streak
        
    def get_subject_stats(self) -> Dict[str, Dict[str, float]]:
        """Calculate statistics by subject."""
        if self.data.empty:
            return {}
            
        subject_stats = {}
        for subject in self.data['Subject'].unique():
            subject_data = self.data[self.data['Subject'] == subject]
            
            stats = {
                'total_hours': subject_data['Study Duration'].sum(),
                'total_questions': subject_data['Questions Attempted'].sum(),
                'avg_performance': subject_data['Performance'].mean(),
                'avg_motivation': subject_data['Motivation'].mean(),
                'study_days': subject_data['Date'].nunique()
            }
            
            subject_stats[subject] = stats
            
        return subject_stats
        
    def get_performance_trend(self) -> pd.DataFrame:
        """Get performance trend over time."""
        if self.data.empty:
            return pd.DataFrame()
            
        return self.data.sort_values('Date').groupby(['Date', 'Subject'])['Performance'].mean().reset_index()
        
    def get_study_time_distribution(self) -> pd.DataFrame:
        """Get study time distribution by subject."""
        if self.data.empty:
            return pd.DataFrame()
            
        return self.data.groupby(['Date', 'Subject'])['Study Duration'].sum().reset_index()
        
    def get_weekly_summary(self) -> Dict[str, Any]:
        """Get summary for the current week."""
        if self.data.empty:
            return {}
            
        today = datetime.now()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        
        week_data = self.data[
            (self.data['Date'].dt.date >= start_of_week.date()) &
            (self.data['Date'].dt.date <= end_of_week.date())
        ]
        
        if week_data.empty:
            return {}
            
        summary = {
            'total_hours': week_data['Study Duration'].sum(),
            'total_questions': week_data['Questions Attempted'].sum(),
            'days_studied': week_data['Date'].nunique(),
            'subjects_studied': week_data['Subject'].nunique(),
            'avg_performance': week_data['Performance'].mean(),
            'avg_motivation': week_data['Motivation'].mean()
        }
        
        return summary
        
    def get_study_patterns(self) -> Dict[str, Any]:
        """Analyze study patterns."""
        if self.data.empty:
            return {}
            
        patterns = {
            'preferred_days': self._analyze_preferred_days(),
            'preferred_hours': self._analyze_preferred_hours(),
            'subject_balance': self._analyze_subject_balance()
        }
        
        return patterns
        
    def _analyze_preferred_days(self) -> Dict[str, float]:
        """Analyze which days of the week are preferred for studying."""
        if self.data.empty:
            return {}
            
        self.data['Day of Week'] = self.data['Date'].dt.day_name()
        day_distribution = self.data.groupby('Day of Week')['Study Duration'].sum()
        return day_distribution.to_dict()
        
    def _analyze_preferred_hours(self) -> Dict[str, float]:
        """Analyze preferred study hours."""
        if self.data.empty:
            return {}
            
        # Assuming study duration is in hours
        hour_distribution = self.data.groupby('Study Duration').size()
        return hour_distribution.to_dict()
        
    def _analyze_subject_balance(self) -> Dict[str, float]:
        """Analyze balance between subjects."""
        if self.data.empty:
            return {}
            
        subject_hours = self.data.groupby('Subject')['Study Duration'].sum()
        total_hours = subject_hours.sum()
        
        if total_hours == 0:
            return {}
            
        balance = (subject_hours / total_hours * 100).round(2)
        return balance.to_dict()
        
    def get_study_efficiency(self) -> Dict[str, float]:
        """Calculate study efficiency metrics."""
        if self.data.empty:
            return {}
            
        efficiency = {
            'questions_per_hour': self.data['Questions Attempted'].sum() / self.data['Study Duration'].sum() if self.data['Study Duration'].sum() > 0 else 0,
            'performance_per_hour': self.data['Performance'].mean() / self.data['Study Duration'].mean() if self.data['Study Duration'].mean() > 0 else 0,
            'consistency_score': self._calculate_consistency_score()
        }
        
        return efficiency
        
    def _calculate_consistency_score(self) -> float:
        """Calculate a consistency score based on study patterns."""
        if self.data.empty:
            return 0.0
            
        # Calculate the number of days studied
        days_studied = self.data['Date'].nunique()
        
        # Calculate the total date range
        date_range = (self.data['Date'].max() - self.data['Date'].min()).days + 1
        
        # Calculate the consistency score (0-100)
        consistency = (days_studied / date_range) * 100 if date_range > 0 else 0
        
        return round(consistency, 2) 