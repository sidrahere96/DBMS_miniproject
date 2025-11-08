# Car Rental Management System

A Python-based Car Rental Management System built with **CustomTkinter** for the GUI and **Firebase** for the database.  
It includes secure admin login, car management, and real-time rental synchronization.

---

## Installation & Setup

```bash
# 1. Clone the Repository
git clone https://github.com/sidrahere96/sidra-1.git
cd sidra-1/Car_rental

# 2. Create and Activate Virtual Environment
python -m venv venv
.\venv\Scripts\activate        # Windows
# or
source venv/bin/activate       # macOS / Linux

# 3. Install Dependencies
pip install -r requirements.txt

# 4. Create .env File
# (Add your Firebase and Google credentials here)
echo FIREBASE_API_KEY=your_api_key > .env
echo FIREBASE_AUTH_DOMAIN=your_project_id.firebaseapp.com >> .env
echo FIREBASE_DATABASE_URL=https://your_project_id.firebaseio.com >> .env
echo FIREBASE_PROJECT_ID=your_project_id >> .env
echo FIREBASE_STORAGE_BUCKET=your_project_id.appspot.com >> .env
echo FIREBASE_MESSAGING_SENDER_ID=your_sender_id >> .env
echo FIREBASE_APP_ID=your_app_id >> .env
echo GOOGLE_APPLICATION_CREDENTIALS=C:\Users\Admin\firebase_keys\serviceAccountKey.json >> .env

# 5. Run the Application
python main.py
```
### FIREBASE SETUP
```bash
# 1. Go to https://console.firebase.google.com
# 2. Create a new project
# 3. Enable Realtime Database or Firestore
# 4. Go to Project Settings → Service Accounts
# 5. Generate a new private key JSON
# 6. Save it securely at:
#    C:\Users\Admin\firebase_keys\serviceAccountKey.json
```
### FOLDER STRUCTURE
```bash
Car_rental/
│
├── ui/                # GUI components
├── models/            # Data models
├── auth.py            # Authentication logic
├── database.py        # Firebase connection
├── config.py          # Config loader
├── utils.py           # Helper utilities
├── main.py            # Application entry point
├── requirements.txt   # Dependencies
└── .env               # Environment variables
```

### REQUIREMENT
```bash
# 1. Never commit .env or secret JSON files
# 2. If keys are exposed, revoke and regenerate in Firebase Console
# 3. Use GitHub Push Protection to block accidental secret uploads
```
