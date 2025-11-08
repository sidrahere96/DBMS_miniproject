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
