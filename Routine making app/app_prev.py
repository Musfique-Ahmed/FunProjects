import pandas as pd
import streamlit as st


class RoutineManager:
    def __init__(self, csv_file):
        self.data = pd.read_csv(csv_file)
        self.draft_routines = {}

    def search_courses(self, course_code=None, title=None, program=None):
        df = self.data
        if course_code:
            df = df[df['Course Code'].str.contains(course_code, case=False, na=False)]
        if title:
            df = df[df['Title'].str.contains(title, case=False, na=False)]
        if program:
            df = df[df['Program'].str.contains(program, case=False, na=False)]
        return df

    def create_draft_routine(self, routine_name):
        if routine_name in self.draft_routines:
            return False  # Routine already exists
        self.draft_routines[routine_name] = []
        return True

    def add_to_routine(self, routine_name, section_index):
        if routine_name not in self.draft_routines:
            return False, "Routine does not exist."

        try:
            section = self.data.iloc[section_index]
        except IndexError:
            return False, "Invalid section index."

        # Check for time clashes
        for existing in self.draft_routines[routine_name]:
            if (
                existing['Day1'] == section['Day1'] and existing['Time1'] == section['Time1'] or
                existing['Day2'] == section['Day2'] and existing['Time2'] == section['Time2']
            ):
                return False, "Time clash detected. Cannot add this section."

        self.draft_routines[routine_name].append(section.to_dict())
        return True, "Section added successfully."

    def get_routine(self, routine_name):
        if routine_name not in self.draft_routines:
            return None
        return pd.DataFrame(self.draft_routines[routine_name])


# Initialize Streamlit app
st.title("Routine Manager with Streamlit")

# Initialize RoutineManager with CSV
manager = RoutineManager("Routine making app/courses.csv")

# Sidebar for Routine Management
st.sidebar.header("Routine Management")
routine_name = st.sidebar.text_input("Enter Routine Name", "")
if st.sidebar.button("Create Routine"):
    if manager.create_draft_routine(routine_name):
        st.sidebar.success(f"Routine '{routine_name}' created.")
    else:
        st.sidebar.error(f"Routine '{routine_name}' already exists.")

selected_routine = st.sidebar.selectbox("Select Routine", list(manager.draft_routines.keys()))
if st.sidebar.button("View Routine") and selected_routine:
    routine = manager.get_routine(selected_routine)
    if routine is not None and not routine.empty:
        st.sidebar.write(f"Routine: {selected_routine}")
        st.sidebar.dataframe(routine)
    else:
        st.sidebar.warning("Routine is empty.")

# Main Section
st.header("Search Courses")

# Search Inputs
course_code_input = st.text_input("Search by Course Code", "")
title_input = st.text_input("Search by Title", "")
program_input = st.text_input("Search by Program", "")

# Perform Search
if st.button("Search"):
    results = manager.search_courses(course_code_input, title_input, program_input)
    if results.empty:
        st.warning("No courses found. Please check your input.")
    else:
        st.write("Search Results:")
        st.dataframe(results)
        section_index = st.number_input("Enter Section Index to Add to Routine", min_value=0, max_value=len(results)-1, step=1)

        # Add section to routine
        if st.button("Add to Routine"):
            if not selected_routine:
                st.error("Please select a routine from the sidebar.")
            else:
                success, message = manager.add_to_routine(selected_routine, section_index)
                if success:
                    st.success(message)
                else:
                    st.error(message)
