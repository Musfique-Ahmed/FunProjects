import pandas as pd
import streamlit as st
import json

# Initialize routines in session state if not already done
if 'routines' not in st.session_state:
    st.session_state.routines = {}


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
        if routine_name in st.session_state.routines:
            st.session_state.routines[routine_name].append(section)
            self.save_routines_to_file()
            return True, "Section added successfully."
        else:
            return False, "Routine not found."

    def save_routines_to_file(self, file_path="routines.json"):
        with open(file_path, "w") as f:
            json.dump(st.session_state.routines, f, indent=4)
        return True

    def get_routine(self, routine_name):
        # Retrieve the routine as a DataFrame
        if routine_name not in st.session_state.routines or len(st.session_state.routines[routine_name]) == 0:
            return pd.DataFrame()
        return pd.DataFrame(st.session_state.routines[routine_name])




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
    if routine_name_input in st.session_state.routines:
        st.sidebar.error(f"Routine '{routine_name_input}' already exists.")
    else:
        st.session_state.routines[routine_name_input] = []
        st.sidebar.success(f"Routine '{routine_name_input}' created.")

# Display Routine Button
if st.sidebar.button("Display All Routines"):
    for routine_name, sections in st.session_state.routines.items():
        st.sidebar.subheader(f"Routine: {routine_name}")
        routine_df = pd.DataFrame(sections)
        if routine_df.empty:
            st.sidebar.info(f"Routine '{routine_name}' is empty.")
        else:
            st.sidebar.dataframe(routine_df)

# Save Routines Button
if st.sidebar.button("Save Routines"):
    if manager.save_routines_to_file():
        st.sidebar.success("Routines saved to routines.json")

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
        results_display = results.drop(columns=["Credit"]).reset_index(drop=True)
        st.dataframe(results_display)

        # Input index to select a section
        section_index = st.number_input(
            "Enter the index of the section to add:",
            min_value=0,
            max_value=len(results_display) - 1,
            step=1,
        )

        # Dropdown to select a routine
        routine_to_add = st.selectbox(
            "Select Routine to Add Section To:", options=list(st.session_state.routines.keys())
        )

        # Add section to routine
        if st.button("Add Section to Routine"):
            if not routine_to_add:
                st.error("Please select a routine from the dropdown.")
            else:
                try:
                    st.write(f"Selected section index: {section_index}")
                    st.write(f"Selected routine: {routine_to_add}")
                    section = results_display.iloc[section_index].to_dict()
                    st.write(f"Section to add: {section}")
                    success, message = manager.add_to_routine(routine_to_add, section)
                    if success:
                        st.success(f"Section added to routine: {routine_to_add}")
                    else:
                        st.error(message)
                except IndexError:
                    st.error("Invalid index. Please select a valid section index.")

# Faculty Search
st.header("Search by Faculty")
faculty_name = st.text_input("Enter Faculty Name:")

if st.button("Search Faculty"):
    faculty_results = manager.search_courses(title=None, program=None)
    if faculty_results.empty:
        st.warning("No courses found for this faculty.")
    else:
        st.write(f"Courses taught by {faculty_name}:")
        st.dataframe(faculty_results.drop(columns=["Credit"]))





















# import streamlit as st
# import pandas as pd
# import json

# # Initialize routines in session state if not already done
# if 'routines' not in st.session_state:
#     st.session_state.routines = {}

# class RoutineManager:
#     def __init__(self, data_file):
#         self.data_file = data_file
#         self.load_data()

#     def load_data(self):
#         self.data = pd.read_csv(self.data_file)

#     def add_to_routine(self, routine_name, section):
#         if routine_name in st.session_state.routines:
#             st.session_state.routines[routine_name].append(section)
#             self.save_routines_to_file()
#             return True, "Section added successfully."
#         else:
#             return False, "Routine not found."

#     def save_routines_to_file(self, file_path="routines.json"):
#         with open(file_path, "w") as f:
#             json.dump(st.session_state.routines, f, indent=4)
#         return True

# # Initialize Streamlit app
# st.title("Routine Manager with Streamlit")

# # Load data
# DATA_FILE = "courses.csv"
# try:
#     manager = RoutineManager(DATA_FILE)
# except FileNotFoundError:
#     st.error(f"Could not find the file '{DATA_FILE}'. Please ensure it exists.")
#     st.stop()

# # Sidebar for Routine Management
# st.sidebar.header("Routine Management")
# routine_name_input = st.sidebar.text_input("Enter Routine Name:")
# if st.sidebar.button("Create Routine"):
#     if routine_name_input in st.session_state.routines:
#         st.sidebar.error(f"Routine '{routine_name_input}' already exists.")
#     else:
#         st.session_state.routines[routine_name_input] = []
#         st.sidebar.success(f"Routine '{routine_name_input}' created.")

# # Main section
# st.dataframe(manager.data)

# # Input index to select a section
# section_index = st.number_input(
#     "Enter the index of the section to add:",
#     min_value=0,
#     max_value=len(manager.data) - 1,
#     step=1,
# )

# # Dropdown to select a routine
# routine_to_add = st.selectbox(
#     "Select Routine to Add Section To:", options=list(st.session_state.routines.keys())
# )

# # Add section to routine
# if st.button("Add Section to Routine"):
#     if not routine_to_add:
#         st.error("Please select a routine from the dropdown.")
#     else:
#         try:
#             st.write(f"Selected section index: {section_index}")
#             st.write(f"Selected routine: {routine_to_add}")
#             section = manager.data.iloc[section_index].to_dict()
#             st.write(f"Section to add: {section}")
#             success, message = manager.add_to_routine(routine_to_add, section)
#             if success:
#                 st.success(f"Section added to routine: {routine_to_add}")
#             else:
#                 st.error(message)
#         except IndexError:
#             st.error("Invalid index. Please select a valid section index.")