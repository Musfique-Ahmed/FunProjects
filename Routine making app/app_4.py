import pandas as pd
import streamlit as st


class RoutineManager:
    def __init__(self, csv_file):
        # Load the dataset
        self.data = pd.read_csv(csv_file)

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

    def add_to_routine(self, routine_name, section):
        # Add a section to a routine
        if routine_name not in st.session_state.draft_routines:
            return False, "Routine does not exist."

        # Check for time clashes
        for existing in st.session_state.draft_routines[routine_name]:
            if (
                existing['Day1'] == section['Day1'] and existing['Time1'] == section['Time1']
            ):
                return False, "Time clash detected. Cannot add this section."

        # Add section to the routine
        st.session_state.draft_routines[routine_name].append(section)
        return True, "Section added successfully."

    def get_routine(self, routine_name):
        # Retrieve the routine as a DataFrame
        if routine_name not in st.session_state.draft_routines or len(st.session_state.draft_routines[routine_name]) == 0:
            return pd.DataFrame()
        return pd.DataFrame(st.session_state.draft_routines[routine_name])


# Initialize Streamlit app
st.title("Routine Manager with Streamlit")

# Initialize session state for draft routines
if "draft_routines" not in st.session_state:
    st.session_state.draft_routines = {}

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
    if routine_name_input in st.session_state.draft_routines:
        st.sidebar.error(f"Routine '{routine_name_input}' already exists.")
    else:
        st.session_state.draft_routines[routine_name_input] = []
        st.sidebar.success(f"Routine '{routine_name_input}' created.")

# Select existing routine
selected_routine = st.sidebar.selectbox("Select a Routine", options=list(st.session_state.draft_routines.keys()))
if selected_routine:
    st.sidebar.subheader(f"Routine: {selected_routine}")

    # Display Routine Button
    if st.sidebar.button("Display Routine"):
        routine_df = manager.get_routine(selected_routine)
        if routine_df.empty:
            st.sidebar.info("This routine is currently empty.")
        else:
            st.sidebar.write("Routine Details:")
            st.sidebar.dataframe(routine_df)

# Main Search Area
st.header("Search Courses")

# Search Inputs
course_code = st.text_input("Search by Course Code:")
title = st.text_input("Search by Title:")
program = st.text_input("Search by Program:")

# Search Results
if st.button("Search Courses"):
    results = manager.search_courses(course_code, title, program)
    if results.empty:
        st.warning("No courses found. Please check your input.")
    else:
        st.write("Search Results:")
        # Display search results with the index for manual selection
        results_display = results.drop(columns=["Credit"]).reset_index()
        st.dataframe(results_display)

        # Input index to select a section
        section_index = st.number_input(
            "Enter the index of the section to add:", 
            min_value=0, 
            max_value=len(results_display)-1, 
            step=1
        )

        # Add section to routine
        if st.button("Add Section to Routine"):
            if not selected_routine:
                st.error("Please select a routine from the sidebar.")
            else:
                try:
                    section = results.iloc[section_index].to_dict()
                    success, message = manager.add_to_routine(selected_routine, section)
                    if success:
                        st.success(f"Section added to routine: {selected_routine}")
                    else:
                        st.error(message)
                except IndexError:
                    st.error("Invalid index. Please select a valid section index.")

# Faculty Search
st.header("Search by Faculty")
faculty_name = st.text_input("Enter Faculty Name:")

if st.button("Search Faculty"):
    faculty_results = manager.search_faculty(faculty_name)
    if faculty_results.empty:
        st.warning("No courses found for this faculty.")
    else:
        st.write(f"Courses taught by {faculty_name}:")
        # Display faculty results without the "Credit" column
        st.dataframe(faculty_results.drop(columns=["Credit"]))
        # Display credits separately
        st.write(f"Total Credits for Courses Taught: {faculty_results['Credit'].sum()}")
