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
# SESSION STATE VARIABLES
# ----------------------------------------
if "points" not in st.session_state:
    st.session_state.points = 0

if "current_question_index" not in st.session_state:
    st.session_state.current_question_index = 0

# Utility
def get_current_question():
    question_text = question_list[st.session_state.current_question_index]
    return next(q for q in QUESTIONS if q["question"] == question_text)


# ----------------------------------------
# SIDEBAR CONTENT
# ----------------------------------------
st.sidebar.header("🎯 Game Controls")

current_q = get_current_question()

st.sidebar.write("### Current Question:")
st.sidebar.write(current_q["question"])

st.sidebar.write("**Difficulty:**", current_q.get("difficulty", "Unknown"))

st.sidebar.metric("⭐ Points", st.session_state.points)

# Skip / Next Question button
if st.sidebar.button("⏭ Next Question"):
    if st.session_state.current_question_index < len(question_list) - 1:
        st.session_state.current_question_index += 1
    else:
        st.success("You've completed all questions!")
        st.balloons()


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
    selected_schema_table = st.selectbox("Choose a table to view schema:", all_tables)
    st.write(f"Schema for **{selected_schema_table}**:")
    st.dataframe(get_table_schema(selected_schema_table))

with tabs[2]:
    selected_preview_table = st.selectbox("Choose a table to preview:", all_tables)
    st.write(f"Preview of **{selected_preview_table}**:")
    st.dataframe(get_table_preview(selected_preview_table))


# ----------------------------------------
# SQL GAME SECTION
# ----------------------------------------
st.subheader("🧠 Solve the SQL Challenge")

st.markdown(f"### ❓ {current_q['question']}")

user_sql = st.text_area("Write your SQL query here:", height=150)

# RUN SQL BUTTON
if st.button("▶️ Run SQL Query"):
    if not user_sql.strip():
        st.warning("Please enter an SQL query first.")
    else:
        try:
            # Run user query
            user_df = run_user_query(user_sql)
            st.write("### 📊 Your Result")
            st.dataframe(user_df)

            # Run correct query
            correct_df = run_correct_query(current_q["answer"])

            # Compare results
            try:
                user_sorted = user_df.sort_index(axis=1)
                correct_sorted = correct_df.sort_index(axis=1)

                if user_sorted.equals(correct_sorted):
                    st.success("🎉 Correct answer! +10 points")
                    st.session_state.points += 10

                    # Move to next question automatically
                    if st.session_state.current_question_index < len(question_list) - 1:
                        st.session_state.current_question_index += 1
                        st.info("➡️ Moving to next question...")
                    else:
                        st.balloons()
                        st.success("🎉 You've completed all questions!")
                else:
                    st.error("❌ Incorrect. Try again!")
                    st.info("Hint: Compare columns, joins, and filters.")

            except:
                st.error("Could not compare results (different columns or data types).")

        except Exception as e:
            st.error(f"SQL Error: {e}")

# ----------------------------------------
# SHOW ANSWER BUTTON
# ----------------------------------------
if st.sidebar.button("👀 Show Correct Answer"):
    st.sidebar.code(current_q["answer"], language="sql")
