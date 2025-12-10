def check_answer(user_df, correct_df):
    # Sort columns for reliable comparison
    try:
        user_df_sorted = user_df.sort_index(axis=1)
        correct_df_sorted = correct_df.sort_index(axis=1)
        return user_df_sorted.equals(correct_df_sorted)
    except:
        return False
