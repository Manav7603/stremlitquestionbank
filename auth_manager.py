import hashlib
import os
import json
from typing import Dict, Optional, Tuple
import logging
from datetime import datetime, timedelta
import jwt
import secrets

class AuthManager:
    def __init__(self, auth_file: str = "auth.json"):
        self.auth_file = auth_file
        self.secret_key = self._get_or_create_secret_key()
        self.users = self._load_users()
        
    def _get_or_create_secret_key(self) -> str:
        """Get or create a secret key for JWT tokens."""
        key_file = "secret.key"
        if os.path.exists(key_file):
            with open(key_file, 'r') as f:
                return f.read().strip()
        else:
            key = secrets.token_hex(32)
            with open(key_file, 'w') as f:
                f.write(key)
            return key
            
    def _load_users(self) -> Dict[str, Dict]:
        """Load user data from file."""
        try:
            if os.path.exists(self.auth_file):
                with open(self.auth_file, 'r') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            logging.error(f"Error loading users: {e}")
            return {}
            
    def _save_users(self) -> bool:
        """Save user data to file."""
        try:
            with open(self.auth_file, 'w') as f:
                json.dump(self.users, f, indent=4)
            return True
        except Exception as e:
            logging.error(f"Error saving users: {e}")
            return False
            
    def _hash_password(self, password: str) -> str:
        """Hash a password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()
        
    def create_user(self, username: str, password: str, email: str) -> Tuple[bool, str]:
        """Create a new user."""
        if username in self.users:
            return False, "Username already exists"
            
        hashed_password = self._hash_password(password)
        self.users[username] = {
            "password": hashed_password,
            "email": email,
            "created_at": datetime.now().isoformat(),
            "last_login": None,
            "failed_attempts": 0,
            "locked_until": None
        }
        
        if self._save_users():
            return True, "User created successfully"
        return False, "Error saving user data"
        
    def authenticate_user(self, username: str, password: str) -> Tuple[bool, str, Optional[str]]:
        """Authenticate a user and return a JWT token if successful."""
        if username not in self.users:
            return False, "Invalid username or password", None
            
        user = self.users[username]
        
        # Check if account is locked
        if user["locked_until"] and datetime.fromisoformat(user["locked_until"]) > datetime.now():
            return False, "Account is locked. Please try again later.", None
            
        # Check password
        if user["password"] != self._hash_password(password):
            user["failed_attempts"] += 1
            
            # Lock account after 5 failed attempts
            if user["failed_attempts"] >= 5:
                user["locked_until"] = (datetime.now() + timedelta(minutes=30)).isoformat()
                self._save_users()
                return False, "Account locked due to too many failed attempts. Please try again in 30 minutes.", None
                
            self._save_users()
            return False, "Invalid username or password", None
            
        # Reset failed attempts and update last login
        user["failed_attempts"] = 0
        user["last_login"] = datetime.now().isoformat()
        self._save_users()
        
        # Generate JWT token
        token = jwt.encode({
            "username": username,
            "exp": datetime.now() + timedelta(days=1)
        }, self.secret_key, algorithm="HS256")
        
        return True, "Authentication successful", token
        
    def validate_token(self, token: str) -> Tuple[bool, Optional[str]]:
        """Validate a JWT token."""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            username = payload["username"]
            
            if username not in self.users:
                return False, None
                
            return True, username
        except jwt.ExpiredSignatureError:
            return False, None
        except jwt.InvalidTokenError:
            return False, None
            
    def change_password(self, username: str, old_password: str, new_password: str) -> Tuple[bool, str]:
        """Change a user's password."""
        if username not in self.users:
            return False, "User not found"
            
        user = self.users[username]
        
        if user["password"] != self._hash_password(old_password):
            return False, "Invalid current password"
            
        user["password"] = self._hash_password(new_password)
        
        if self._save_users():
            return True, "Password changed successfully"
        return False, "Error saving password"
        
    def reset_password(self, username: str, email: str) -> Tuple[bool, str]:
        """Reset a user's password."""
        if username not in self.users:
            return False, "User not found"
            
        user = self.users[username]
        
        if user["email"] != email:
            return False, "Invalid email address"
            
        # Generate a temporary password
        temp_password = secrets.token_urlsafe(8)
        user["password"] = self._hash_password(temp_password)
        
        if self._save_users():
            return True, temp_password
        return False, "Error resetting password"
        
    def update_user_profile(self, username: str, email: str) -> Tuple[bool, str]:
        """Update a user's profile information."""
        if username not in self.users:
            return False, "User not found"
            
        user = self.users[username]
        user["email"] = email
        
        if self._save_users():
            return True, "Profile updated successfully"
        return False, "Error updating profile"
        
    def delete_user(self, username: str) -> Tuple[bool, str]:
        """Delete a user account."""
        if username not in self.users:
            return False, "User not found"
            
        del self.users[username]
        
        if self._save_users():
            return True, "User deleted successfully"
        return False, "Error deleting user"
        
    def get_user_info(self, username: str) -> Optional[Dict]:
        """Get user information."""
        if username not in self.users:
            return None
            
        user = self.users[username].copy()
        # Remove sensitive information
        del user["password"]
        return user 