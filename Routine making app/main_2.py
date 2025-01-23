import pandas as pd
from tabulate import tabulate


class RoutineManager:
    def __init__(self, csv_file):
        # Load the dataset
        self.data = pd.read_csv(csv_file)
        self.draft_routines = {}

    def search_courses(self, course_code=None, title=None, program=None):
        # Search by course code or title
        df = self.data
        if course_code:
            df = df[df['Course Code'].str.contains(course_code, case=False, na=False)]
        if title:
            df = df[df['Title'].str.contains(title, case=False, na=False)]
        if program:
            df = df[df['Program'].str.contains(program, case=False, na=False)]
        return df

    def display_sections(self, course_code):
        # Display all sections of a course
        sections = self.data[self.data['Course Code'] == course_code]
        if sections.empty:
            print("No sections found for the given course code.")
        else:
            print(tabulate(sections, headers='keys', tablefmt='grid'))

    def create_draft_routine(self, routine_name):
        # Create a new draft routine
        if routine_name in self.draft_routines:
            print(f"Routine '{routine_name}' already exists.")
        else:
            self.draft_routines[routine_name] = []
            print(f"Routine '{routine_name}' created.")

    def add_to_routine(self, routine_name, section_index):
        # Add a section to a routine with clash detection
        if routine_name not in self.draft_routines:
            print(f"Routine '{routine_name}' does not exist.")
            return

        try:
            section = self.data.iloc[section_index]
        except IndexError:
            print("Invalid section index.")
            return

        # Check for time clashes
        for existing in self.draft_routines[routine_name]:
            if (
                existing['Day1'] == section['Day1'] and existing['Time1'] == section['Time1'] or
                existing['Day2'] == section['Day2'] and existing['Time2'] == section['Time2']
            ):
                print("Time clash detected. Cannot add this section.")
                return

        # Add to routine
        self.draft_routines[routine_name].append(section)
        print("Section added to routine.")

    def display_routine(self, routine_name):
        # Display a routine
        if routine_name not in self.draft_routines:
            print(f"Routine '{routine_name}' does not exist.")
        else:
            routine = pd.DataFrame(self.draft_routines[routine_name])
            if routine.empty:
                print(f"Routine '{routine_name}' is empty.")
            else:
                print(tabulate(routine, headers='keys', tablefmt='grid'))


def main():
    manager = RoutineManager('Routine making app/courses.csv')

    while True:
        print("\n--- Routine Manager CLI ---")
        print("1. Search Courses")
        print("2. Display Sections")
        print("3. Create Draft Routine")
        print("4. Add Section to Routine")
        print("5. Display Routine")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            course_code = input("Enter Course Code (or leave blank): ")
            title = input("Enter Title (or leave blank): ")
            program = input("Enter Program (or leave blank): ")
            results = manager.search_courses(course_code, title, program)
            print(tabulate(results, headers='keys', tablefmt='grid'))
        elif choice == "2":
            course_code = input("Enter Course Code: ")
            manager.display_sections(course_code)
        elif choice == "3":
            routine_name = input("Enter Routine Name: ")
            manager.create_draft_routine(routine_name)
        elif choice == "4":
            routine_name = input("Enter Routine Name: ")
            section_index = int(input("Enter Section Index (from search results): "))
            manager.add_to_routine(routine_name, section_index)
        elif choice == "5":
            routine_name = input("Enter Routine Name: ")
            manager.display_routine(routine_name)
        elif choice == "6":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
