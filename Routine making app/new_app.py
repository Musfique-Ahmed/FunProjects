import pandas as pd
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

# Standalone script for testing without Streamlit
def main():
    print("=== Automatic Routine Maker ===")
    file_path = input("Enter the path to your routine CSV file: ")
    try:
        df = pd.read_csv(file_path)
        print("\nRoutine Data Loaded:")
        print(df.head())

        program = input("Enter your Program: ")
        selected_program_courses = df[df['Program'] == program]['Course Code'].unique()

        print(f"\nAvailable Courses for {program}: {list(selected_program_courses)}")
        selected_courses = input("Enter the courses you want to take (comma-separated): ").split(',')

        routines = generate_routines(selected_courses, df)
        if routines:
            print("\nGenerated Non-Conflicting Routines:")
            for i, routine in enumerate(routines):
                print(f"\nRoutine {i + 1}:")
                print(routine)
        else:
            print("No non-conflicting routines found.")

    except FileNotFoundError:
        print("Error: File not found. Please check the file path.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
