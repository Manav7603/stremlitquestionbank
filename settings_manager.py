import json
import os
from typing import Dict, Any, Optional
from datetime import datetime
import logging

class SettingsManager:
    def __init__(self, settings_file: str = "settings.json"):
        self.settings_file = settings_file
        self.settings = self._load_settings()
        
    def _load_settings(self) -> Dict[str, Any]:
        """Load settings from file."""
        default_settings = {
            "notifications": {
                "enabled": True,
                "daily_reminder": True,
                "weekly_summary": True,
                "reminder_time": "20:00"
            },
            "study_goals": {
                "daily_hours": 6,
                "weekly_hours": 42,
                "daily_questions": 50,
                "weekly_questions": 350
            },
            "preferences": {
                "theme": "light",
                "language": "en",
                "timezone": "UTC",
                "date_format": "%Y-%m-%d"
            },
            "data_management": {
                "auto_backup": True,
                "backup_frequency": "daily",
                "last_backup": None
            }
        }
        
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    loaded_settings = json.load(f)
                    # Merge with default settings to ensure all keys exist
                    return {**default_settings, **loaded_settings}
            return default_settings
        except Exception as e:
            logging.error(f"Error loading settings: {e}")
            return default_settings
            
    def save_settings(self) -> bool:
        """Save settings to file."""
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=4)
            return True
        except Exception as e:
            logging.error(f"Error saving settings: {e}")
            return False
            
    def get_setting(self, key_path: str) -> Any:
        """Get a specific setting value."""
        keys = key_path.split('.')
        value = self.settings
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return None
            
    def set_setting(self, key_path: str, value: Any) -> bool:
        """Set a specific setting value."""
        keys = key_path.split('.')
        current = self.settings
        
        try:
            for key in keys[:-1]:
                if key not in current:
                    current[key] = {}
                current = current[key]
            current[keys[-1]] = value
            return self.save_settings()
        except Exception as e:
            logging.error(f"Error setting {key_path}: {e}")
            return False
            
    def update_notification_settings(self, enabled: bool, daily_reminder: bool, 
                                   weekly_summary: bool, reminder_time: str) -> bool:
        """Update notification settings."""
        self.settings["notifications"] = {
            "enabled": enabled,
            "daily_reminder": daily_reminder,
            "weekly_summary": weekly_summary,
            "reminder_time": reminder_time
        }
        return self.save_settings()
        
    def update_study_goals(self, daily_hours: float, weekly_hours: float,
                          daily_questions: int, weekly_questions: int) -> bool:
        """Update study goals."""
        self.settings["study_goals"] = {
            "daily_hours": daily_hours,
            "weekly_hours": weekly_hours,
            "daily_questions": daily_questions,
            "weekly_questions": weekly_questions
        }
        return self.save_settings()
        
    def update_preferences(self, theme: str, language: str, 
                          timezone: str, date_format: str) -> bool:
        """Update user preferences."""
        self.settings["preferences"] = {
            "theme": theme,
            "language": language,
            "timezone": timezone,
            "date_format": date_format
        }
        return self.save_settings()
        
    def update_data_management(self, auto_backup: bool, 
                             backup_frequency: str) -> bool:
        """Update data management settings."""
        self.settings["data_management"] = {
            "auto_backup": auto_backup,
            "backup_frequency": backup_frequency,
            "last_backup": datetime.now().isoformat()
        }
        return self.save_settings()
        
    def reset_to_defaults(self) -> bool:
        """Reset all settings to default values."""
        default_settings = {
            "notifications": {
                "enabled": True,
                "daily_reminder": True,
                "weekly_summary": True,
                "reminder_time": "20:00"
            },
            "study_goals": {
                "daily_hours": 6,
                "weekly_hours": 42,
                "daily_questions": 50,
                "weekly_questions": 350
            },
            "preferences": {
                "theme": "light",
                "language": "en",
                "timezone": "UTC",
                "date_format": "%Y-%m-%d"
            },
            "data_management": {
                "auto_backup": True,
                "backup_frequency": "daily",
                "last_backup": None
            }
        }
        
        self.settings = default_settings
        return self.save_settings()
        
    def export_settings(self) -> str:
        """Export settings as a JSON string."""
        return json.dumps(self.settings, indent=4)
        
    def import_settings(self, settings_json: str) -> bool:
        """Import settings from a JSON string."""
        try:
            imported_settings = json.loads(settings_json)
            self.settings = imported_settings
            return self.save_settings()
        except Exception as e:
            logging.error(f"Error importing settings: {e}")
            return False 