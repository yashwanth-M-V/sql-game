# 🛒 Supermarket SQL Game

A fun, interactive way to learn SQL using a realistic supermarket database.

check the game in 
https://begineer-sql-game.streamlit.app/

📌 Overview

Supermarket SQL Game is an interactive learning app built with Python, SQLite, and Streamlit.
Users practice SQL queries on a fully populated supermarket database with 40 curated questions ranging from beginner to advanced.

The game includes:

🎯 SQL challenges (40 questions: beginner → advanced)

🧠 Automatic answer checking

⭐ Score tracking

⏭ Next question auto-progression

🔍 Database explorer (tables, schema, sample data)

💾 Realistic supermarket dataset with 13 tables

It’s a complete SQL learning playground suitable for students, developers, and interview prep.

📂 Project Structure
sql-game/
│
├── app.py                         # Main Streamlit application
├── requirements.txt
│
├── database/
│   ├── create_supermarket_db.py   # Builds supermarket.db
│   └── supermarket.db             # SQLite database
│
├── utils/
│   ├── db.py                      # DB access functions
│   └── evaluator.py               # Answer comparison logic
│
└── questions/
    └── supermarket.json           # 40 SQL questions

⚙️ Installation & Setup
1️⃣ Create a virtual environment
python3 -m venv venv
source venv/Scripts/activate     # Windows (Git Bash/PowerShell)

2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Generate the supermarket database
cd database
python create_supermarket_db.py
cd ..

This creates:

database/supermarket.db

4️⃣ Run the app
streamlit run app.py

The app will open in your browser:
localhost:8501

🧠 Features
✔ 40 SQL Questions

5 Beginner

10 Intermediate

25 Advanced

Each question includes the correct SQL solution internally for evaluation.

✔ Automatic Scoring

Earn 10 points for every correct answer.

✔ Auto-Progression

When a user answers correctly, the app automatically moves to the next question.

✔ Skip / Next Button

Users can skip questions anytime.

✔ Database Explorer

Explore the dataset before querying:

View all tables

View schema (column names + types)

Preview first 5 rows

✔ Error Handling

Friendly SQL error messages and comparison logging.

🗄 Supermarket Database Structure

The SQLite database includes 13 realistic supermarket tables:

categories

products

inventory

suppliers

purchase_orders

purchase_order_items

customers

carts

cart_items

bills

bill_items

payments

employees

Over 600 rows of real sample data simulate real-world SQL challenges.

🙌 Tech Stack

Streamlit – UI/Frontend

SQLite – Database

Python – Backend logic

Pandas – Data handling

🚀 Future Improvements

Potential extensions:

Difficulty filters

User login + saved progress

Timer and streak bonuses

Mobile-friendly UI

Additional datasets (Hospital, F1 Racing)

Want these? Just ask!

📄 License

MIT License.
Feel free to use, modify, and share.

✨ Author

Yashwanth Madyala Venkata
If you'd like, I can generate a polished author section for GitHub.
