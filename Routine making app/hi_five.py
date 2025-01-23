import pandas as pd
import streamlit as st
from itertools import combinations

# Function to check if two time intervals overlap
def is_overlapping(interval1, interval2):
    start1, end1 = interval1
    start2, end2 = interval2
    return max(start1, start2) < min(end1, end2)

# Function to check if a routine has any overlapping classes
def is_valid_routine(routine):
    for i in range(len(routine)):
        for j in range(i + 1, len(routine)):
            if is_overlapping(routine[i][1], routine[j][1]):
                return False
    return True

# Load the CSV file
@st.cache_resource
def load_data(file):
    return pd.read_csv(file)

# Main function
def main():
    st.title("Automatic Routine Making App")

    # Upload CSV file
    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
    if uploaded_file is not None:
        data = load_data(uploaded_file)
        st.write("Data loaded successfully!")
        st.write(data)

        # Input courses and program
        courses = st.multiselect("Select your courses", data['Title'].unique())
        program = st.text_input("Enter your program")

        if st.button("Generate Routines"):
            # Filter data based on selected courses
            filtered_data = data[data['Title'].isin(courses)]

            # Generate all possible combinations of classes
            all_combinations = []
            for r in range(1, len(filtered_data) + 1):
                all_combinations.extend(combinations(filtered_data.iterrows(), r))

            # Filter valid routines
            valid_routines = [comb for comb in all_combinations if is_valid_routine([row[1]['Time'] for row in comb])]

            st.write(f"Found {len(valid_routines)} valid routines")
            for routine in valid_routines:
                st.write(pd.DataFrame([row[1] for row in routine]))

if __name__ == "__main__":
    main()