import pandas as pd
import streamlit as st


class RoutineManager:
    def __init__(self, csv_file):
        # Load the dataset
        self.data = pd.read_csv(csv_file)
        self.draft_routines = {}

    def search_courses(self, course_code=None, title=None, program=None):
        # Filter the dataset based on search criteria
        df = self.data
        if course_code:
            df = df[df['Course Code'].str.contains(course_code, case=False, na=False)]
        if title:
            df = df[df['Title'].str.contains(title, case=False, na=False)]
        if program:
            df = df[df['Program'].str.contains(program, case=False, na=False)]
        return df

    def create_draft_routine(self, routine_name):
        # Create a new routine
        if routine_name in self.draft_routines:
            return False  # Routine already exists
        self.draft_routines[routine_name] = []
        return True

    def add_to_routine(self, routine_name, section):
        # Add a section to a routine
        if routine_name not in self.draft_routines:
            return False, "Routine does not exist."

        # Check for time clashes
        for existing in self.draft_routines[routine_name]:
            if (
                existing['Day1'] == section['Day1'] and existing['Time1'] == section['Time1'] or
                existing['Day2'] == section['Day2'] and existing['Time2'] == section['Time2']
            ):
                return False, "Time clash detected. Cannot add this section."

        # Add section to the routine
        self.draft_routines[routine_name].append(section)
        return True, "Section added successfully."

    def get_routine(self, routine_name):
        # Retrieve the routine as a DataFrame
        if routine_name not in self.draft_routines or len(self.draft_routines[routine_name]) == 0:
            return pd.DataFrame()
        return pd.DataFrame(self.draft_routines[routine_name])


# Initialize Streamlit app
st.title("Routine Manager with Streamlit")

# Load data
DATA_FILE = "courses.csv"
try:
    manager = RoutineManager(DATA_FILE)
except FileNotFoundError:
    st.error(f"Could not find the file '{DATA_FILE}'. Please ensure it exists.")
    st.stop()

# Sidebar for Routine Management
st.sidebar.header("Routine Management")
routine_name_input = st.sidebar.text_input("Enter Routine Name:")
if st.sidebar.button("Create Routine"):
    if manager.create_draft_routine(routine_name_input):
        st.sidebar.success(f"Routine '{routine_name_input}' created.")
    else:
        st.sidebar.error(f"Routine '{routine_name_input}' already exists.")

# Select existing routine
selected_routine = st.sidebar.selectbox("Select a Routine", options=list(manager.draft_routines.keys()), index=0 if manager.draft_routines else -1)
if selected_routine:
    st.sidebar.subheader(f"Routine: {selected_routine}")
    routine_df = manager.get_routine(selected_routine)
    if routine_df.empty:
        st.sidebar.info("This routine is currently empty.")
    else:
        st.sidebar.dataframe(routine_df)

# # Main Search Area
# st.header("Search Courses")

# # Search Inputs
# course_code = st.text_input("Search by Course Code:")
# title = st.text_input("Search by Title:")
# program = st.text_input("Search by Program:")

# # Search Results
# if st.button("Search"):
#     results = manager.search_courses(course_code, title, program)
#     if results.empty:
#         st.warning("No courses found. Please check your input.")
#     else:
#         st.write("Search Results:")
#         st.dataframe(results)

#         # Select a section to add
#         section_index = st.number_input("Select Section Index to Add to Routine:", min_value=0, max_value=len(results)-1, step=1)
#         if st.button("Add Section to Routine"):
#             if not selected_routine:
#                 st.error("Please select a routine from the sidebar.")
#             else:
#                 section = results.iloc[section_index].to_dict()
#                 success, message = manager.add_to_routine(selected_routine, section)
#                 if success:
#                     st.success(message)
#                 else:
#                     st.error(message)

# Main Search Area
st.header("Search Courses")

# Search Inputs
course_code = st.text_input("Search by Course Code:")
title = st.text_input("Search by Title:")
program = st.text_input("Search by Program:")

# Search Results
if st.button("Search"):
    results = manager.search_courses(course_code, title, program)
    if results.empty:
        st.warning("No courses found. Please check your input.")
    else:
        st.write("Search Results:")
        st.dataframe(results)

        # Select a section to add
        section_index = st.number_input("Select Section Index to Add to Routine:", min_value=0, max_value=len(results)-1, step=1)
        if st.button("Add Section to Routine"):
            if not selected_routine:
                st.error("Please select a routine from the sidebar.")
            else:
                section = results.iloc[int(section_index)].to_dict()  # Ensure section_index is an integer
                success, message = manager.add_to_routine(selected_routine, section)
                if success:
                    st.success(message)
                else:
                    st.error(message)