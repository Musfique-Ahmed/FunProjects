import pandas as pd
import streamlit as st
from itertools import combinations

# Function to check if two time slots conflict
def times_conflict(time1, time2):
    def parse_time_range(time_range):
        start, end = time_range.split(" – ")
        return pd.to_datetime(start, format="%I:%M:%p"), pd.to_datetime(end, format="%I:%M:%p")

    start1, end1 = parse_time_range(time1)
    start2, end2 = parse_time_range(time2)
    return not (end1 <= start2 or end2 <= start1)

# Function to generate non-conflicting routines
def generate_routines(selected_courses, df):
    filtered_courses = df[df['Course Code'].isin(selected_courses)]
    grouped_courses = [group for _, group in filtered_courses.groupby('Course Code')]

    possible_combinations = list(combinations(grouped_courses, len(grouped_courses)))
    valid_routines = []

    for combination in possible_combinations:
        routine = pd.concat(combination)
        routine_conflict = False

        for i, row1 in routine.iterrows():
            for j, row2 in routine.iterrows():
                if i != j and row1['Day1'] == row2['Day1'] and times_conflict(row1['Time1'], row2['Time1']):
                    routine_conflict = True
                    break
            if routine_conflict:
                break

        if not routine_conflict:
            valid_routines.append(routine)

    return valid_routines

# Streamlit App
def main():
    st.title("Automatic Routine Maker")

    st.sidebar.header("Upload Routine CSV")
    uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("## Routine Data")
        st.dataframe(df)

        # User Inputs
        st.sidebar.header("Inputs")
        programs = df['Program'].unique()
        selected_program = st.sidebar.selectbox("Select Program", programs)

        courses = df[df['Program'] == selected_program]['Course Code'].unique()
        selected_courses = st.sidebar.multiselect("Select Courses", courses)

        if selected_courses:
            routines = generate_routines(selected_courses, df)

            if routines:
                st.write("## Generated Non-Conflicting Routines")
                for i, routine in enumerate(routines):
                    st.write(f"### Routine {i + 1}")
                    st.dataframe(routine)
            else:
                st.warning("No non-conflicting routines found for the selected courses.")

if __name__ == "__main__":
    main()
