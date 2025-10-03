import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import logging
from typing import List, Dict, Optional
import json
import os
from threading import Thread
import time

class NotificationManager:
    def __init__(self, settings_file: str = "settings.json"):
        self.settings_file = settings_file
        self.settings = self._load_settings()
        self.notification_queue = []
        self.is_running = False
        
    def _load_settings(self) -> Dict:
        """Load notification settings."""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    return json.load(f).get('notifications', {})
            return {}
        except Exception as e:
            logging.error(f"Error loading settings: {e}")
            return {}
            
    def start_notification_service(self):
        """Start the notification service in a separate thread."""
        if not self.is_running:
            self.is_running = True
            thread = Thread(target=self._notification_loop)
            thread.daemon = True
            thread.start()
            
    def stop_notification_service(self):
        """Stop the notification service."""
        self.is_running = False
        
    def _notification_loop(self):
        """Main notification loop."""
        while self.is_running:
            self._process_notification_queue()
            time.sleep(60)  # Check every minute
            
    def _process_notification_queue(self):
        """Process pending notifications."""
        current_time = datetime.now()
        
        for notification in self.notification_queue[:]:
            if notification['scheduled_time'] <= current_time:
                self._send_notification(notification)
                self.notification_queue.remove(notification)
                
    def schedule_notification(self, user_email: str, subject: str, message: str,
                            scheduled_time: datetime) -> bool:
        """Schedule a notification."""
        try:
            notification = {
                'user_email': user_email,
                'subject': subject,
                'message': message,
                'scheduled_time': scheduled_time
            }
            self.notification_queue.append(notification)
            return True
        except Exception as e:
            logging.error(f"Error scheduling notification: {e}")
            return False
            
    def _send_notification(self, notification: Dict) -> bool:
        """Send a notification via email."""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.settings.get('smtp_username', '')
            msg['To'] = notification['user_email']
            msg['Subject'] = notification['subject']
            
            msg.attach(MIMEText(notification['message'], 'plain'))
            
            with smtplib.SMTP(self.settings.get('smtp_server', ''), 
                            self.settings.get('smtp_port', 587)) as server:
                server.starttls()
                server.login(self.settings.get('smtp_username', ''),
                           self.settings.get('smtp_password', ''))
                server.send_message(msg)
                
            return True
        except Exception as e:
            logging.error(f"Error sending notification: {e}")
            return False
            
    def schedule_daily_reminder(self, user_email: str, reminder_time: str) -> bool:
        """Schedule a daily reminder."""
        try:
            hour, minute = map(int, reminder_time.split(':'))
            now = datetime.now()
            scheduled_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            
            if scheduled_time <= now:
                scheduled_time += timedelta(days=1)
                
            message = "Don't forget to log your study session today!"
            return self.schedule_notification(user_email, "Daily Study Reminder", 
                                           message, scheduled_time)
        except Exception as e:
            logging.error(f"Error scheduling daily reminder: {e}")
            return False
            
    def schedule_weekly_summary(self, user_email: str, summary_data: Dict) -> bool:
        """Schedule a weekly summary notification."""
        try:
            # Schedule for next Sunday at 8 PM
            now = datetime.now()
            days_until_sunday = (6 - now.weekday()) % 7
            scheduled_time = (now + timedelta(days=days_until_sunday)).replace(
                hour=20, minute=0, second=0, microsecond=0
            )
            
            message = self._format_weekly_summary(summary_data)
            return self.schedule_notification(user_email, "Weekly Study Summary", 
                                           message, scheduled_time)
        except Exception as e:
            logging.error(f"Error scheduling weekly summary: {e}")
            return False
            
    def _format_weekly_summary(self, summary_data: Dict) -> str:
        """Format weekly summary data into a message."""
        message = "Weekly Study Summary\n\n"
        message += f"Total Study Hours: {summary_data.get('total_hours', 0):.1f}\n"
        message += f"Total Questions Attempted: {summary_data.get('total_questions', 0)}\n"
        message += f"Days Studied: {summary_data.get('days_studied', 0)}\n"
        message += f"Average Performance: {summary_data.get('avg_performance', 0):.1f}/10\n"
        message += f"Average Motivation: {summary_data.get('avg_motivation', 0):.1f}/10\n\n"
        
        if 'subject_stats' in summary_data:
            message += "Subject-wise Summary:\n"
            for subject, stats in summary_data['subject_stats'].items():
                message += f"\n{subject}:\n"
                message += f"  Hours: {stats.get('total_hours', 0):.1f}\n"
                message += f"  Questions: {stats.get('total_questions', 0)}\n"
                message += f"  Performance: {stats.get('avg_performance', 0):.1f}/10\n"
                
        return message
        
    def schedule_goal_reminder(self, user_email: str, goal_type: str, 
                             current_value: float, target_value: float) -> bool:
        """Schedule a goal reminder notification."""
        try:
            progress = (current_value / target_value) * 100
            if progress < 50:
                message = f"Your {goal_type} progress is at {progress:.1f}%. Keep going!"
                scheduled_time = datetime.now() + timedelta(hours=1)
                return self.schedule_notification(user_email, "Goal Progress Reminder", 
                                               message, scheduled_time)
            return False
        except Exception as e:
            logging.error(f"Error scheduling goal reminder: {e}")
            return False
            
    def schedule_motivation_quote(self, user_email: str) -> bool:
        """Schedule a daily motivation quote."""
        try:
            quotes = [
                "Success is not final, failure is not fatal: It is the courage to continue that counts.",
                "The future belongs to those who believe in the beauty of their dreams.",
                "Don't watch the clock; do what it does. Keep going.",
                "The secret of your success is determined by your daily agenda.",
                "The only way to do great work is to love what you do."
            ]
            
            message = f"Today's Motivation:\n\n{quotes[datetime.now().weekday() % len(quotes)]}"
            scheduled_time = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
            
            if scheduled_time <= datetime.now():
                scheduled_time += timedelta(days=1)
                
            return self.schedule_notification(user_email, "Daily Motivation", 
                                           message, scheduled_time)
        except Exception as e:
            logging.error(f"Error scheduling motivation quote: {e}")
            return False 