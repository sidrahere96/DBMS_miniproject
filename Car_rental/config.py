"""
Configuration file for Car Rental System
Handles Firebase initialization and app settings
"""
import firebase_admin
from firebase_admin import credentials, firestore, auth
import os

class Config:
    # App Configuration
    APP_NAME = "Car Rental System"
    APP_VERSION = "1.0.0"
    
    # UI Configuration
    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 700
    
    # Theme Colors
    PRIMARY_COLOR = "#1f538d"
    SECONDARY_COLOR = "#14375e"
    SUCCESS_COLOR = "#2ecc71"
    DANGER_COLOR = "#e74c3c"
    WARNING_COLOR = "#f39c12"
    BG_COLOR = "#f0f0f0"
    
    # Firebase
    _firebase_initialized = False
    _db = None
    
    @classmethod
    def initialize_firebase(cls, credential_path="serviceAccountKey.json"):
        """Initialize Firebase Admin SDK"""
        if not cls._firebase_initialized:
            try:
                if not os.path.exists(credential_path):
                    raise FileNotFoundError(
                        f"Firebase credentials file not found: {credential_path}\n"
                        "Please download serviceAccountKey.json from Firebase Console"
                    )
                
                cred = credentials.Certificate(credential_path)
                firebase_admin.initialize_app(cred)
                cls._db = firestore.client()
                cls._firebase_initialized = True
                print("✓ Firebase initialized successfully")
            except Exception as e:
                print(f"✗ Firebase initialization error: {e}")
                raise
    
    @classmethod
    def get_db(cls):
        """Get Firestore database instance"""
        if not cls._firebase_initialized:
            cls.initialize_firebase()
        return cls._db

# Initialize Firebase on module import
try:
    Config.initialize_firebase()
except Exception as e:
    print(f"Warning: {e}")
