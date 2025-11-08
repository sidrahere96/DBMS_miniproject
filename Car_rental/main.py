"""
Main entry point for Car Rental System
Optimized with proper exception handling, error recovery, and logout management
"""
import sys
import traceback
import customtkinter as ctk
from datetime import datetime


def setup_initial_data():
    """Setup initial data (admin user and sample cars)"""
    from database import Database
    from models import Car
    from auth import AuthManager
    
    db = Database()
    auth = AuthManager()
    
    try:
        # Check if admin exists
        admin = db.get_user_by_email("admin@carrental.com")
        if not admin:
            print("Creating default admin account...")
            success, message = auth.register_user(
                email="admin@carrental.com",
                password="admin123",
                name="Administrator",
                role="admin",
                phone="9876543210",
                address="Head Office, Mumbai"
            )
            if success:
                print("✓ Admin account created")
                print("  Email: admin@carrental.com")
                print("  Password: admin123")
            else:
                print(f"✗ Failed to create admin: {message}")
                return False
    except Exception as e:
        print(f"✗ Error checking/creating admin: {e}")
        return False
    
    try:
        # Add sample cars if none exist
        cars = db.get_all_cars()
        if len(cars) == 0:
            print("Adding sample cars...")
            sample_cars = [
                Car(
                    car_id=db.generate_id("CAR_"),
                    brand="Toyota",
                    model="Fortuner",
                    year=2023,
                    daily_rate=3500.0,
                    status="Available",
                    color="Pearl White",
                    fuel_type="Diesel",
                    seats=7
                ),
                Car(
                    car_id=db.generate_id("CAR_"),
                    brand="Honda",
                    model="City",
                    year=2024,
                    daily_rate=2000.0,
                    status="Available",
                    color="Silver",
                    fuel_type="Petrol",
                    seats=5
                ),
                Car(
                    car_id=db.generate_id("CAR_"),
                    brand="Hyundai",
                    model="Creta",
                    year=2023,
                    daily_rate=2500.0,
                    status="Available",
                    color="Red",
                    fuel_type="Petrol",
                    seats=5
                ),
                Car(
                    car_id=db.generate_id("CAR_"),
                    brand="Maruti",
                    model="Swift",
                    year=2024,
                    daily_rate=1500.0,
                    status="Available",
                    color="Blue",
                    fuel_type="Petrol",
                    seats=5
                ),
                Car(
                    car_id=db.generate_id("CAR_"),
                    brand="Mahindra",
                    model="Thar",
                    year=2023,
                    daily_rate=3000.0,
                    status="Available",
                    color="Black",
                    fuel_type="Diesel",
                    seats=4
                ),
                Car(
                    car_id=db.generate_id("CAR_"),
                    brand="Kia",
                    model="Seltos",
                    year=2024,
                    daily_rate=2800.0,
                    status="Available",
                    color="White",
                    fuel_type="Diesel",
                    seats=5
                ),
            ]
            
            success_count = 0
            for car in sample_cars:
                try:
                    if db.add_car(car):
                        print(f"  ✓ Added {car.brand} {car.model}")
                        success_count += 1
                    else:
                        print(f"  ✗ Failed to add {car.brand} {car.model}")
                except Exception as e:
                    print(f"  ✗ Error adding {car.brand} {car.model}: {e}")
            
            if success_count > 0:
                print(f"Successfully added {success_count}/{len(sample_cars)} cars")
            else:
                print("Warning: No sample cars were added")
                
    except Exception as e:
        print(f"✗ Error setting up sample cars: {e}")
        return False
    
    return True


def initialize_firebase():
    """Initialize Firebase with proper error handling"""
    from config import Config
    
    try:
        Config.initialize_firebase()
        return True
    except FileNotFoundError:
        print()
        print("=" * 60)
        print("ERROR: Firebase credentials not found!")
        print("=" * 60)
        print()
        print("Please follow these steps:")
        print("1. Go to Firebase Console (https://console.firebase.google.com)")
        print("2. Select your project or create a new one")
        print("3. Go to Project Settings > Service Accounts")
        print("4. Click 'Generate New Private Key'")
        print("5. Save the file as 'serviceAccountKey.json' in project root")
        print()
        print("Expected location: ./serviceAccountKey.json")
        print("=" * 60)
        return False
    except Exception as e:
        print()
        print("=" * 60)
        print("ERROR: Firebase initialization failed!")
        print("=" * 60)
        print(f"Error: {str(e)}")
        print()
        print("Common solutions:")
        print("1. Verify serviceAccountKey.json is valid JSON")
        print("2. Check your internet connection")
        print("3. Ensure Firebase project has Firestore enabled")
        print("4. Verify service account has proper permissions")
        print()
        print("=" * 60)
        return False


def start_application():
    """Start the GUI application with error handling"""
    from ui.login_window import LoginWindow
    
    try:
        app = LoginWindow()
        # Handle window close properly
        app.protocol("WM_DELETE_WINDOW", lambda: on_closing(app))
        app.mainloop()
    except KeyboardInterrupt:
        print("\n\nApplication interrupted by user")
        cleanup_and_exit(0)
    except Exception as e:
        print()
        print("=" * 60)
        print("ERROR: Application crashed!")
        print("=" * 60)
        print(f"Error: {str(e)}")
        print()
        print("Full traceback:")
        traceback.print_exc()
        print("=" * 60)
        cleanup_and_exit(1)


def on_closing(window):
    """Handle window closing event"""
    try:
        print("\nClosing application...")
        window.quit()
        window.destroy()
        cleanup_and_exit(0)
    except Exception as e:
        print(f"Error during shutdown: {e}")
        cleanup_and_exit(1)


def cleanup_and_exit(exit_code=0):
    """Cleanup resources and exit application"""
    try:
        # Logout current user if any
        from auth import AuthManager
        auth = AuthManager()
        if auth.is_logged_in():
            auth.logout()
            print("User logged out")
    except Exception as e:
        print(f"Cleanup warning: {e}")
    
    print("Application terminated")
    sys.exit(exit_code)


def check_dependencies():
    """Check if all required dependencies are installed"""
    required_modules = {
        'customtkinter': 'customtkinter',
        'firebase_admin': 'firebase-admin',
        'PIL': 'Pillow',
        'tkcalendar': 'tkcalendar'
    }
    
    missing_modules = []
    
    for module_name, package_name in required_modules.items():
        try:
            __import__(module_name)
        except ImportError:
            missing_modules.append(package_name)
    
    if missing_modules:
        print()
        print("=" * 60)
        print("ERROR: Missing required dependencies!")
        print("=" * 60)
        print()
        print("Missing packages:")
        for package in missing_modules:
            print(f"  - {package}")
        print()
        print("Install missing packages with:")
        print(f"  pip install {' '.join(missing_modules)}")
        print()
        print("Or install all requirements:")
        print("  pip install -r requirements.txt")
        print()
        print("=" * 60)
        return False
    
    return True


def main():
    """Main application entry point with comprehensive error handling"""
    from config import Config
    
    # Print header
    print()
    print("=" * 60)
    print(f"  {Config.APP_NAME} v{Config.APP_VERSION}")
    print("=" * 60)
    print()
    
    # Check dependencies
    print("Checking dependencies...")
    if not check_dependencies():
        sys.exit(1)
    print("✓ All dependencies installed")
    print()
    
    # Initialize Firebase
    print("Initializing Firebase...")
    if not initialize_firebase():
        sys.exit(1)
    print("✓ Firebase initialized successfully")
    print()
    
    # Setup initial data
    print("Setting up initial data...")
    if not setup_initial_data():
        print()
        print("Warning: Some initialization steps failed")
        print("The application will continue, but some features may not work")
        print()
    print("✓ Initial data setup complete")
    print()
    
    # Application ready
    print("=" * 60)
    print("✓ Application ready!")
    print("=" * 60)
    print()
    print("Default Admin Credentials:")
    print("  Email: admin@carrental.com")
    print("  Password: admin123")
    print()
    print("Starting GUI...")
    print("=" * 60)
    print()
    
    # Start application
    start_application()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nApplication terminated by user")
        cleanup_and_exit(0)
    except SystemExit:
        # Allow sys.exit() calls to work normally
        raise
    except Exception as e:
        print()
        print("=" * 60)
        print("FATAL ERROR: Unexpected error occurred!")
        print("=" * 60)
        print(f"Error: {str(e)}")
        print()
        print("Full traceback:")
        traceback.print_exc()
        print()
        print("=" * 60)
        cleanup_and_exit(1)
