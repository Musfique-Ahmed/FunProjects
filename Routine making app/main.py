import pandas as pd

# Load the dataset
df = pd.read_csv('Routine making app/Untitled spreadsheet - Sheet1.csv')

# Function to search for a course by code or title
def search_course(df, search_query, program):
    return df[(df['Program'] == program) & ((df['Course Code'] == search_query) | (df['Title'] == search_query))]

# Function to display all sections of a course
def display_sections(course_info):
    for index, row in course_info.iterrows():
        print(f"Section: {row['Section']}, Room: {row['Room1']}, Day: {row['Day1']}, Time: {row['Time1']}, Faculty: {row['Faculty Name']}")

# Function to add a section to the routine and check for clashes
def add_to_routine(routine, course_info, section):
    section_info = course_info[course_info['Section'] == section]
    day_time_pairs = [(row['Day1'], row['Time1']) for index, row in section_info.iterrows()]
    
    for day, time in day_time_pairs:
        if any((day == r_day and time == r_time) for r_day, r_time in routine):
            print(f"Class clash detected for day: {day}, time: {time}")
            return False
    routine.extend(day_time_pairs)
    print(f"Section {section} added to your routine.")
    return True

# Function to display the finalized routine in a table format
def display_final_routine(routine):
    print("Your Class Routine:")
    routine_df = pd.DataFrame(routine, columns=['Day', 'Time'])
    print(routine_df)

# Main function to run the program
def main():
    routine = []

    search_query = input("Enter course code or title: ")
    program = input("Enter your program: ")

    course_info = search_course(df, search_query, program)
    display_sections(course_info)

    section = input("Enter section to add: ")
    add_to_routine(routine, course_info, section)

    # Display the final routine
    display_final_routine(routine)

# Run the main function
if __name__ == "__main__":
    main()
