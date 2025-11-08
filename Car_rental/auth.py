"""
Authentication module for Car Rental System
Handles user login, registration, and session management
"""
from typing import Optional, Tuple
from models import User
from database import Database
import hashlib

class AuthManager:
    def __init__(self):
        self.db = Database()
        self.current_user: Optional[User] = None
    
    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(self, email: str, password: str, name: str, 
                     role: str = "customer", phone: str = "", 
                     address: str = "") -> Tuple[bool, str]:
        """Register a new user"""
        try:
            # Check if user already exists
            existing_user = self.db.get_user_by_email(email)
            if existing_user:
                return False, "Email already registered"
            
            # Generate user ID
            uid = self.db.generate_id("USER_")
            
            # Create user object
            user = User(
                uid=uid,
                email=email,
                name=name,
                role=role,
                phone=phone,
                address=address
            )
            
            # Store user in database
            if self.db.create_user(user):
                # Store password hash separately (in production, use Firebase Auth)
                self.db.db.collection('auth').document(uid).set({
                    'email': email,
                    'password_hash': self.hash_password(password)
                })
                return True, "Registration successful"
            else:
                return False, "Failed to create user"
            
        except Exception as e:
            return False, f"Registration error: {str(e)}"
    
    def login(self, email: str, password: str) -> Tuple[bool, str, Optional[User]]:
        """Login user with email and password"""
        try:
            # Get user by email
            user = self.db.get_user_by_email(email)
            if not user:
                return False, "Invalid email or password", None
            
            # Verify password
            auth_doc = self.db.db.collection('auth').document(user.uid).get()
            if not auth_doc.exists:
                return False, "Authentication data not found", None
            
            auth_data = auth_doc.to_dict()
            password_hash = self.hash_password(password)
            
            if auth_data.get('password_hash') != password_hash:
                return False, "Invalid email or password", None
            
            # Set current user
            self.current_user = user
            return True, "Login successful", user
            
        except Exception as e:
            return False, f"Login error: {str(e)}", None
    
    def logout(self):
        """Logout current user"""
        self.current_user = None
    
    def is_logged_in(self) -> bool:
        """Check if user is logged in"""
        return self.current_user is not None
    
    def is_admin(self) -> bool:
        """Check if current user is admin"""
        return self.current_user and self.current_user.role == "admin"
    
    def get_current_user(self) -> Optional[User]:
        """Get currently logged in user"""
        return self.current_user
