from typing import List, Tuple

def read_students_preferences(file_path) -> List[List[str]]:
    """
    Read preferences from a file and return a list of lists each row represents a student references.
    This function assumes that the file contains lines of comma-separated values.
    Each line represents a student's preferences.
    If the file is not found or corrupted, it returns an empty list.
    :param file_path: The path to the file containing student preferences.
    :return: A list of lists, where each inner list contains the preferences of a student in the form: 
    [student_name, student_ID, average_GPA, 1st preference, 2nd preference, ..., 14th preference].
    """
    result: List[List[str]] = []  # the result list to store student preferences
    # Open the file and read its contents
    # Each line in the file is expected to contain a student's preferences separated by commas
    # If the file is not found or corrupted, an empty list will be returned
    # Each line in the file are expected to be in the format:
    # [timestamp, student_name, student_ID, master_GPA, cureent_GPA, avarage_GPA, 1st preference, 2nd preference,..., 14th preference]
    try:
        with open(file_path, 'r') as file:
            preferences: List[str] = file.read().strip().split('\n')
            # Skip the header row (first line)
            for preference in preferences[1:]:
                # Split each line by commas and strip whitespace
                temp_student_preferences: List[str] = [item.strip() for item in preference.split(',')]
                student_preference: List[str] = [temp_student_preferences[1],temp_student_preferences[2],temp_student_preferences[5],temp_student_preferences[6],
                                       temp_student_preferences[7],temp_student_preferences[8],temp_student_preferences[9],temp_student_preferences[10],
                                       temp_student_preferences[11],temp_student_preferences[12],temp_student_preferences[13],temp_student_preferences[14],
                                        temp_student_preferences[15],temp_student_preferences[16],temp_student_preferences[17],temp_student_preferences[18],
                                        temp_student_preferences[19]]
                # Append the list of preferences to the result
                result.append(student_preference)
    except FileNotFoundError:
        print(f"File {file_path} not found or currputed.")
    
    return result


def read_faculties_info(file_path) -> List[List[str]]:
    """
    Read faculty information from a file and return a list of lists each row represents a faculty information.
    This function assumes that the file contains lines of comma-separated values.
    Each line represents a faculty's information.
    If the file is not found or corrupted, it returns an empty list.
    :param file_path: The path to the file containing faculty information.
    :return: A list of lists, where each inner list contains the information of a faculty in the form [faculty_name, current_load, requsted_load]   
    """
    result: List[List[str]] = []  # the result list to store faculty information
    # Open the file and read its contents
    # Each line in the file is expected to contain a faculty's information separated by commas
    # If the file is not found or corrupted, an empty list will be returned
    # Each line in the file are expected to be in the format:
    # [faculty_name, current_load, requsted_load]
    try:
        with open(file_path, 'r') as file:
            info: List[str] = file.read().strip().split('\n')
            # Skip the header row (first line)
            for faculty_information in info[1:]:
                # Split each line by commas and strip whitespace
                faculty_info_list: List[str] = [item.strip() for item in faculty_information.split(',')]
                result.append(faculty_info_list)
    except FileNotFoundError:
        print(f"File {file_path} not found or currputed.")
    
    return result


def assign_students_to_faculties(students_preferences: List[List[str]], faculties_info: List[List[str]]) -> List[Tuple[str, str, str]]:
    """
    Assign students to faculties based on their preferences and faculty availability. It will iterate through each student's preferences and assign them based on their preferences to the first available faculty 
    that still has capacity based on the faculty's requested load and under one condition that the faculty's current load won't surpass 3. If a faculty is already at full capacity, the student will be assigned 
    to the next preferred faculty. If no faculty is available, the student will assigned to the faculty with the lowest current load with a requested load > 0. If two faculties have the same load and their 
    requested load is > 0, the student will be assigned to one of them randomly. Whenever a student is assigned to a faculty, the faculty's current load will be updated, and the number of requested load will be 
    decremented by one until it reaches zero.
    :param students_preferences: A list of lists containing student preferences.
    :param faculties_info: A list of lists containing faculty information.
    :return: A list of tuples, where each tuple contains (student_name, student_ID, assigned_faculty).
    """
    assignment_result: List[Tuple[str, str, str]] = []  # the result list to store the assignment results
    assigned_students: List[List[str]] = []  # to keep track of assigned students
    courtesy: bool = True  # The first student without preferences will be assigned to a faculty from his preferences even if their load is full
    # Iterate through each student's preferences
    for student in students_preferences:
        student_name: str = student[0]
        student_ID: str = student[1]
        assigned: bool = False  # Flag to check if the student has been assigned to a faculty
        # Iterate through each faculty preference of the student
        for preference in student[3:]:
            # Check if the faculty preference is in the faculties_info list
            for faculty in faculties_info:
                if faculty[0] == preference:
                    faculty_name: str = faculty[0]
                    current_load: int = int(faculty[1])
                    requested_load: int = int(faculty[2])
                    # Check if the faculty has capacity to take more students
                    if  current_load < 3 and requested_load > 0:
                        # Assign the student to the faculty
                        assignment_result.append((student_name, student_ID, faculty_name))
                        # Update the faculty's current load and requested load
                        faculty[1] = str(current_load + 1)
                        faculty[2] = str(requested_load - 1)
                        assigned = True
                        assigned_students.append(student)  # Add the student to the assigned students list
                        break
                    elif current_load < 4 and requested_load > 0 and courtesy:
                        # Courtesy: If the first student without preferences will be assigned to a faculty from his preferences even if their load is full
                        assignment_result.append((student_name, student_ID, faculty_name))
                        faculty[1] = str(current_load + 1)
                        faculty[2] = str(requested_load - 1)
                        assigned = True
                        assigned_students.append(student)  # Add the student to the assigned students list
                        courtesy = False  # Disable courtesy for subsequent students
                        break
            if assigned:
                break
        # If the student has not been assigned to any faculty, assign them to the faculty with the least current load and requested load > 0
        # Sort faculties by current load only
        # if two faculties have the same current load, and requested load > 0, the student will be assigned to one of them randomly
        if not assigned:
            # Filter faculties that have capacity to take more students
            available_faculties: List[List[str]] = [faculty for faculty in faculties_info if int(faculty[1]) < 4 and int(faculty[2]) > 0]
            # Sort the available faculties by current load
            available_faculties.sort(key=lambda x: int(x[1]))
            # Check if there are any available faculties
            if available_faculties:
                # Select the faculty with the least current load and requested load > 0
                candidate_faculties: List[List[str]] = [faculty for faculty in available_faculties if int(faculty[1]) == int(available_faculties[0][1])]
                # If there are multiple faculties with the same current load, randomly select one of them
                if len(candidate_faculties) > 1:
                    import random
                    selected_faculty: List[str] = random.choice(candidate_faculties)
                else:
                    # If there is only one faculty with the least current load, select it
                    selected_faculty: List[str] = available_faculties[0]
                faculty_name: str = selected_faculty[0]
                current_load: int = int(selected_faculty[1])
                requested_load: int = int(selected_faculty[2])
                # Assign the student to the faculty
                assignment_result.append((student_name, student_ID, faculty_name))
                # Update the faculty's current load and requested load
                selected_faculty[1] = str(current_load + 1)
                selected_faculty[2] = str(requested_load - 1)
                assigned = True
            else:
                # Select a faculty with lowest current load randomly if no available faculties with current load < 4 
                faculties_info.sort(key=lambda x: int(x[1]))
                candidate_faculties: List[List[str]] = [faculty for faculty in faculties_info if int(faculty[1]) == int(faculties_info[0][1])]
                for preference in student[3:]:
                    # Check if the faculty preference is in the candidate_faculties list
                    if preference in [faculty[0] for faculty in candidate_faculties]:
                        # If the faculty preference is in the candidate faculties, assign the student to that faculty
                        selected_faculty: List[str] = next(faculty for faculty in candidate_faculties if faculty[0] == preference)
                        faculty_name: str = selected_faculty[0]
                        current_load: int = int(selected_faculty[1])
                        requested_load: int = int(selected_faculty[2])
                        # Assign the student to the faculty
                        assignment_result.append((student_name, student_ID, faculty_name))
                        # Update the faculty's current load and requested load
                        selected_faculty[1] = str(current_load + 1)
                        selected_faculty[2] = str(requested_load - 1)
                        assigned = True
                        assigned_students.append(student)  # Add the student to the assigned students list
                        break
                if not assigned:
                    # create a temproray list of all the remaining students
                    temp_remaining_students: List[List[str]] = [s for s in students_preferences if s not in assigned_students + [student]]
                    # create a temproray list of all the preferences of all remaining students
                    # to avoid assigning a faculty that is already in the preferences of a future student
                    temp_future_preferences: List[str] = []
                    for future_student in temp_remaining_students:
                        # Collect future preferences of all remaining students
                        for temp_pref in future_student[3:]:
                            if temp_pref not in temp_future_preferences:
                                temp_future_preferences.append(temp_pref)
                    # Filter the candidate faculties to remove those that are in the future preferences
                    candidate_faculties: List[List[str]] = [faculty for faculty in candidate_faculties if faculty[0] not in temp_future_preferences]
                    # If there are no candidate faculties left, break the loop
                    if not candidate_faculties:
                        candidate_faculties: List[List[str]] = [faculty for faculty in faculties_info if int(faculty[1]) == int(faculties_info[0][1])]
                        import random
                        selected_faculty: List[str] = random.choice(candidate_faculties)
                        faculty_name: str = selected_faculty[0]
                        current_load: int = int(selected_faculty[1])
                        requested_load: int = int(selected_faculty[2])
                        # Assign the student to the faculty
                        assignment_result.append((student_name, student_ID, faculty_name))
                        # Update the faculty's current load and requested load
                        selected_faculty[1] = str(current_load + 1)
                        selected_faculty[2] = str(requested_load - 1)
                        assigned = True
                        break
                    # If there are still candidate faculties left, randomly select one of them 
                    else:
                        import random
                        selected_faculty: List[str] = random.choice(candidate_faculties)
                        faculty_name: str = selected_faculty[0]
                        current_load: int = int(selected_faculty[1])
                        requested_load: int = int(selected_faculty[2])
                        # Assign the student to the faculty
                        assignment_result.append((student_name, student_ID, faculty_name))
                        # Update the faculty's current load and requested load
                        selected_faculty[1] = str(current_load + 1)
                        selected_faculty[2] = str(requested_load - 1)
                        assigned = True
                        break

        # If the student has not been assigned to any faculty, assign them to the faculty with the least current load randomly
        if not assigned:
            print(f"No available faculty for student {student_name} with ID {student_ID}.")  
    
    # Return the assignment result
    # Each item in the list is a tuple of the form (student_name, student_ID, assigned_faculty)
    return assignment_result


def statistics(assignment_result: List[Tuple[str, str, str]], students_preferences: List[List[str]]) -> None:
    """
    Print the statistics of the number of students who get their first preference, second preference, etc. Also, plot a bar chart to show these statistics.
    :param assignment_result: A list of tuples, where each tuple contains (student_name, student_ID, assigned_faculty).
    """
    from collections import Counter
    import matplotlib.pyplot as plt

    # Count the number of students who got their first, second, etc. preferences
    preference_counts: Counter = Counter()
    students_without_preference: int = 0
    for student in students_preferences:
        student_name: str = student[0]
        student_ID: str = student[1]
        assigned_faculty = next((faculty for faculty in assignment_result if faculty[0] == student_name and faculty[1] == student_ID), None)
        if assigned_faculty:
            assigned_faculty_name: str = assigned_faculty[2]
            # Find the index of the assigned faculty in the student's preferences
            try:
                preference_index: int = student[3:].index(assigned_faculty_name) + 1  # +1 to count from 1 instead of 0
                preference_counts[preference_index] += 1
            except ValueError:
                # Faculty not in student's preference list (assigned due to fallback algorithm)
                students_without_preference += 1

    # Print the statistics
    print("\nStatistics of Student Preferences:")
    for preference, count in sorted(preference_counts.items()):
        print(f"Preference {preference}: {count} students")
    # Print the number of students assigned to faculties not in their preferences
    print(f"Students assigned to faculty not in their preferences: {students_without_preference}")
    print()
    print('-------------')
    print()
    
    # print the names of the students who were assigned to faculties not in their preferences
    if students_without_preference > 0:
        print("Students assigned to faculty not in their preferences:")
        for student in students_preferences:
            student_name: str = student[0]
            student_ID: str = student[1]
            assigned_faculty = next((faculty for faculty in assignment_result if faculty[0] == student_name and faculty[1] == student_ID), None)
            if assigned_faculty:
                assigned_faculty_name: str = assigned_faculty[2]
                if assigned_faculty_name not in student[3:]:
                    print(f"Student: {student_name}, ID: {student_ID}, Assigned Faculty: {assigned_faculty_name}")
    
    # print the names of the students who were assigned to their preferences
    count_preference:int = 1
    already_printed: List[str] = []  # To keep track of already printed students
    # Iterate through preferences 1-14
    while count_preference <= 14:
        print(f"\nStudents who were assigned to preference {count_preference}:")
        for student in students_preferences:
            student_name: str = student[0]
            student_ID: str = student[1]
            assigned_faculty = next((faculty for faculty in assignment_result if faculty[0] == student_name and faculty[1] == student_ID), None)
            if assigned_faculty:
                assigned_faculty_name: str = assigned_faculty[2]
                if assigned_faculty_name == student[count_preference+2]:
                    if student_name not in already_printed:
                        already_printed.append(student_name)
                        # Print the student's name, ID, and assigned faculty
                        # This is to avoid printing the same student multiple times if they selected the same faculty in multiple preferences
                        # and were assigned to that faculty
                        print(f"Student: {student_name}, ID: {student_ID}, Assigned Faculty: {assigned_faculty_name}")
        count_preference += 1


    # Plot a bar chart to show the statistics
    # Create lists for preferences 1-14, then add position 0 for students without preferences
    x_positions = list(range(1, 15)) + [0]  # 1-14 for preferences, then 0 for no preference
    y_values = []
    
    # Add counts for preferences 1-14
    for i in range(1, 15):
        y_values.append(preference_counts.get(i, 0))
    
    # Add count for students without preferences at the end (position 0)
    y_values.append(students_without_preference)
    
    plt.bar(x_positions, y_values)
    plt.xlabel('Preference (1-14 = Preference rank, 0 = Not in preferences)')
    plt.ylabel('Number of Students')
    plt.title('Statistics of Student Preferences')
    plt.xticks(x_positions)
    plt.show()


if __name__ == "__main__":
    # read the student preferences and faculty information from the specified files
    students_preferences: List[List[str]] = read_students_preferences('Students_Preferences.csv')
    faculties_info: List[List[str]] = read_faculties_info('faculty_members.csv')

    # the result list to store the assignment results; each item in the list is a tuple of the form (student_name, student_ID, assigned_faculty)
    assignment_result: List[Tuple[str, str, str]] = assign_students_to_faculties(students_preferences, faculties_info) 
    
    # Print the assignment results
    for student_name, student_ID, assigned_faculty in assignment_result:
        print(f"Student: {student_name}, ID: {student_ID}, Assigned Faculty: {assigned_faculty}")
    
    # Print the updated faculties information
    print("\nUpdated Faculty Information:")
    for faculty in faculties_info:
        print(f"Faculty: {faculty[0]}, Current Load: {faculty[1]}, Requested Load: {faculty[2]}")

    # Show the statistics of the assignment results
    statistics(assignment_result, students_preferences)
