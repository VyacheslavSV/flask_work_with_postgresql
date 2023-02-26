import random

from sqlalchemy import func
from sqlalchemy.orm import sessionmaker

from models import engine, GroupModel, StudentModel, CourseModel, add_tables
from my_prostege_app.random_data.random_gen_data import groups, students, courses

Session = sessionmaker(bind=engine)
session = Session()


def add_the_groups_to_database():
    """
    Add the groups to the database
    """
    for group_name in groups:
        group = GroupModel(name=group_name)
        session.add(group)


# Add the students to the database
def add_the_students_to_database():
    """
    Add the students to the database
    """
    for student_name in students:
        first_name, last_name = student_name.split()
        group = session.query(GroupModel).order_by(func.random()).first()
        student = StudentModel(
            first_name=first_name,
            last_name=last_name,
            group=group)
        session.add(student)


def add_the_courses_to_database():
    """
    Add the courses to the database
    """
    for course_name in courses:
        course = CourseModel(
            name=course_name,
            description='This is a course about ' +
                        course_name)
        session.add(course)


def add_the_courses_assignments_to_students_to_database():
    """
    Add the course assignments to the students
    """
    for student in session.query(StudentModel):
        num_courses = random.randint(1, 3)
        for i in range(num_courses):
            course = session.query(CourseModel).order_by(func.random()).first()
            student.courses.append(course)


def main():
    """
    Add all tables to db,
    add test data to db
    """
    add_tables()
    add_the_groups_to_database()
    add_the_students_to_database()
    add_the_courses_to_database()
    add_the_courses_assignments_to_students_to_database()
    session.commit()


if __name__ == '__main__':
    main()
