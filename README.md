# 🚗 Car Rental Management System

A Python-based **Car Rental Management System** using **CustomTkinter** for its GUI and **Firebase** for database management.  
It provides secure admin login, car management, and real-time booking synchronization with Firebase.

---

## ⚙️ Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/sidrahere96/sidra-1.git
cd sidra-1/Car_rental
```
### 2️⃣ Create and Activate Virtual Environment
```bash
python -m venv venv
.\venv\Scripts\activate      # Windows
# or
source venv/bin/activate     # macOS / Linux
```
### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt

🔐 Environment Configuration

Create a .env file in the project root and add:

FIREBASE_API_KEY=your_api_key
FIREBASE_AUTH_DOMAIN=your_project_id.firebaseapp.com
FIREBASE_DATABASE_URL=https://your_project_id.firebaseio.com
FIREBASE_PROJECT_ID=your_project_id
FIREBASE_STORAGE_BUCKET=your_project_id.appspot.com
FIREBASE_MESSAGING_SENDER_ID=your_sender_id
FIREBASE_APP_ID=your_app_id
GOOGLE_APPLICATION_CREDENTIALS=C:\Users\Admin\firebase_keys\serviceAccountKey.json


⚠️ Keep .env and serviceAccountKey.json private — both are ignored by Git.

☁️ Firebase Setup

Go to Firebase Console

Create a new project

Enable Realtime Database or Firestore

In Project Settings → Service Accounts, generate a private key JSON

Save it at
C:\Users\Admin\firebase_keys\serviceAccountKey.json
```
▶️ Run the Application
python main.py

🧩 Features

GUI built with CustomTkinter

Firebase Realtime Database integration

Secure admin login & authentication

CRUD operations for cars, users, and rentals

.env-based credential handling

Modular and scalable structure

📁 Folder Structure
Car_rental/
│
├── ui/                # GUI components
├── models/            # Data models
├── auth.py            # Authentication logic
├── database.py        # Firebase connection
├── config.py          # Config loader
├── utils.py           # Helper utilities
├── main.py            # Application entry
├── requirements.txt   # Dependencies
└── .env               # Environment variables

🧾 Example .gitignore
__pycache__/
*.pyc
venv/
.env
firebase_keys/
serviceAccountKey.json
.vscode/
.DS_Store
Thumbs.db

🛠️ Requirements
pip install customtkinter firebase-admin python-dotenv google-cloud-storage

🛡️ Security

Don’t commit secrets or .env files

Regenerate Firebase keys if exposed

Use GitHub Push Protection

📜 License

MIT License — free to use and modify with attribution.

👩‍💻 Author

Sidra
🔗 GitHub Profile

🧠 Python | Firebase | Cloud Development
