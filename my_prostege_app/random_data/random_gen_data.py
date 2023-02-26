import random
from faker import Faker


courses = [
    'Math',
    'Physics',
    'Computer Science',
    'Geography',
    'Biology',
    'History',
    'Art',
    'Music',
    'Philosophy',
    'Law']
fake = Faker()
random.seed(0)


def group_names() -> list:
    """
    Generate 10 groups with random names
    :return: list
    """
    groups_ = []
    for i in range(10):
        group_name = fake.lexify(text='??') + '_' + fake.numerify(text='##')
        groups_.append(group_name)
    return groups_


groups = group_names()


def first_last_names() -> [list, list]:
    """
    Generate a list of 20 first names and 20 last names
    :return: [list, list]
    """
    first_names = []
    last_names = []
    for i in range(20):
        first_names.append(fake.first_name())
        last_names.append(fake.last_name())
    return first_names, last_names


def students(first_last_names: [list, list]) -> list:
    """
    Generate 200 students with randomly combined first and last names
    :param first_last_names: [list, list]
    :return: list
    """
    students = []
    first_names, last_names = first_last_names()
    for i in range(200):
        student_name = random.choice(
            first_names) + ' ' + random.choice(last_names)
        students.append(student_name)
    return students


students = students(first_last_names)


def assign_students_to_groups(group_names: list, students: list) -> dict:
    """
    Randomly assign students to groups
    :param group_names: list
    :return: dict
    """
    group_assignments = {}
    for student in students:
        group = random.choice(group_names)
        if group not in group_assignments:
            group_assignments[group] = []
        group_assignments[group].append(student)
    return group_assignments


def create_test_data_for_see():
    """Def shows data which generation"""
    assign_students_to_groups_ = assign_students_to_groups(groups, students)
    for group in assign_students_to_groups_:
        print(f'Group {group}:')
        for student in assign_students_to_groups[group]:
            print(f'- {student}')
        print()
