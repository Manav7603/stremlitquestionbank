import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataManager:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self._ensure_data_dir()
        
    def _ensure_data_dir(self) -> None:
        """Ensure the data directory exists."""
        try:
            if not os.path.exists(self.data_dir):
                os.makedirs(self.data_dir)
        except Exception as e:
            logger.error(f"Failed to create data directory: {e}")
            raise

    def _get_file_path(self, filename: str) -> str:
        """Get the full path for a data file."""
        return os.path.join(self.data_dir, filename)

    def load_data(self, filename: str) -> List[Dict[str, Any]]:
        """Load data from a JSON file with error handling."""
        file_path = self._get_file_path(filename)
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            logger.error(f"Error loading data from {filename}: {e}")
            return []

    def save_data(self, filename: str, data: List[Dict[str, Any]]) -> bool:
        """Save data to a JSON file with error handling and backup."""
        file_path = self._get_file_path(filename)
        backup_path = f"{file_path}.backup"
        
        try:
            # Create backup if file exists
            if os.path.exists(file_path):
                os.replace(file_path, backup_path)
            
            # Save new data
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=4)
            
            # Remove backup if save was successful
            if os.path.exists(backup_path):
                os.remove(backup_path)
            
            return True
        except Exception as e:
            logger.error(f"Error saving data to {filename}: {e}")
            # Restore backup if save failed
            if os.path.exists(backup_path):
                os.replace(backup_path, file_path)
            return False

    def validate_study_entry(self, entry: Dict[str, Any]) -> bool:
        """Validate a study entry before saving."""
        required_fields = ['Date', 'Subject', 'Study Duration']
        
        # Check required fields
        if not all(field in entry for field in required_fields):
            return False
        
        # Validate date format
        try:
            datetime.strptime(entry['Date'], '%Y-%m-%d')
        except ValueError:
            return False
        
        # Validate subject
        valid_subjects = ['Physics', 'Chemistry', 'Botany', 'Zoology']
        if entry['Subject'] not in valid_subjects:
            return False
        
        # Validate study duration
        try:
            duration = float(entry['Study Duration'].split()[0])
            if duration < 0 or duration > 24:
                return False
        except (ValueError, AttributeError):
            return False
        
        return True

    def backup_data(self) -> bool:
        """Create a backup of all data files."""
        try:
            backup_dir = os.path.join(self.data_dir, 'backups')
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            for filename in os.listdir(self.data_dir):
                if filename.endswith('.json'):
                    source = self._get_file_path(filename)
                    backup = os.path.join(backup_dir, f"{filename}.{timestamp}")
                    os.copy2(source, backup)
            return True
        except Exception as e:
            logger.error(f"Error creating backup: {e}")
            return False 