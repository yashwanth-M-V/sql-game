import streamlit as st
import json
import pandas as pd

from utils.db import (
    run_user_query,
    run_correct_query,
    get_all_tables,
    get_table_preview,
    get_table_schema,
)

# ----------------------------------------
# PAGE CONFIGURATION
# ----------------------------------------
st.set_page_config(page_title="Supermarket SQL Game", layout="wide")

st.title("🛒 Supermarket SQL Learning Game")
st.write("Practice SQL queries on a realistic supermarket database!")

# ----------------------------------------
# LOAD QUESTIONS
# ----------------------------------------
with open("questions/supermarket.json", "r") as f:
    QUESTIONS = json.load(f)

question_list = [q["question"] for q in QUESTIONS]

# ----------------------------------------
# SESSION POINTS
# ----------------------------------------
if "points" not in st.session_state:
    st.session_state.points = 0

# ----------------------------------------
# SIDEBAR CONTROLS
# ----------------------------------------
st.sidebar.header("🎯 Game Controls")

selected_question_text = st.sidebar.selectbox(
    "Choose a Question", question_list
)

selected_question = next(
    q for q in QUESTIONS if q["question"] == selected_question_text
)

st.sidebar.write("**Difficulty:**", selected_question.get("difficulty", "Unknown"))
st.sidebar.metric("⭐ Points", st.session_state.points)

# ----------------------------------------
# DATABASE EXPLORER
# ----------------------------------------
st.subheader("🔍 Explore the Database")

tabs = st.tabs(["📁 Tables", "📄 Schema", "📊 Preview"])

with tabs[0]:
    st.write("All tables in the supermarket database:")
    all_tables = get_all_tables()
    st.dataframe(pd.DataFrame({"Tables": all_tables}))

with tabs[1]:
    selected_table_schema = st.selectbox("Choose a table to view schema:", all_tables)
    st.write(f"Schema for **{selected_table_schema}**:")
    st.dataframe(get_table_schema(selected_table_schema))

with tabs[2]:
    selected_table_preview = st.selectbox("Choose a table to preview:", all_tables)
    st.write(f"Preview of **{selected_table_preview}**:")
    st.dataframe(get_table_preview(selected_table_preview))

# ----------------------------------------
# SQL GAME SECTION
# ----------------------------------------
st.subheader("🧠 Solve the SQL Challenge")

st.markdown(f"### ❓ {selected_question_text}")

user_sql = st.text_area("Write your SQL query here:", height=150)

if st.button("▶️ Run SQL Query"):
    if not user_sql.strip():
        st.warning("Please enter an SQL query first.")
    else:
        try:
            user_df = run_user_query(user_sql)
            correct_df = run_correct_query(selected_question["answer"])

            st.write("### 📊 Your Result")
            st.dataframe(user_df)

            # Compare results
            try:
                user_sorted = user_df.sort_index(axis=1)
                correct_sorted = correct_df.sort_index(axis=1)

                if user_sorted.equals(correct_sorted):
                    st.success("🎉 Correct answer! +10 points")
                    st.session_state.points += 10
                else:
                    st.error("❌ Incorrect. Try again!")
                    st.info("Tip: Check your JOINs, GROUP BY, or WHERE conditions.")
            except:
                st.error("Could not compare results due to mismatched columns or types.")

        except Exception as e:
            st.error(f"SQL Error: {e}")

# ----------------------------------------
# SHOW ANSWER
# ----------------------------------------
if st.sidebar.button("👀 Show Correct Answer"):
    st.sidebar.code(selected_question["answer"], language="sql")

