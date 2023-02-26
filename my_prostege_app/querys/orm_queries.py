import argparse

from sqlalchemy import func
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import sessionmaker

from my_prostege_app.db_tool.models import GroupModel, StudentModel, CourseModel, engine
Session = sessionmaker(engine)
session = Session()


def find_all_groups(student_count: int) -> list:
    """
    Find all groups with less or equals student count.
    :param student_count: int
    :return: list
    """
    try:
        groups = session.query(GroupModel).outerjoin(
            GroupModel.students).group_by(
            GroupModel.id).having(
            func.count(
                StudentModel.id) <= student_count).all()
        return groups
    except Exception as e:
        return f"Error finding groups with less than or equal to {student_count} students: {e}"


def find_all_students(course_name: str) -> list:
    """
    Find all students related to the course with a given name
    :param course_name: str
    :return: list
    """
    try:
        students = session.query(StudentModel).join(
            CourseModel.students and StudentModel.courses).filter(
            CourseModel.name == course_name).all()
        return students
    except Exception as e:
        return f"Error getting students for course {course_name}: {e}"


def add_new_student(new_student_: str) -> str:
    """
    Add new student
    :param new_student_: str
    :return: str
    """
    try:
        first_name, last_name, group_id = new_student_.split()
        existing_student = session.query(StudentModel).filter_by(
            first_name=first_name, last_name=last_name).first()
        if existing_student:
            return f"Student with ID {new_student_} already exists."
        new_student = StudentModel(
            first_name=first_name,
            last_name=last_name,
            group_id=group_id)
        session.add(new_student)
        session.commit()
        return f"New student with ID {new_student_} has been added."
    except ValueError:
        return "Error: invalid input format. Please provide a string in the format 'First Last GroupID'."
    except Exception as e:
        session.rollback()
        return f"Error adding new student with ID {new_student_}: {e}"


def delete_student_for_id(student_id: int) -> str:
    """
    Delete student for student id
    :param student_id: int
    :return: str
    """
    try:
        student = session.query(StudentModel).get(student_id)
        session.delete(student)
        session.commit()
        return f"Student with ID {student_id} has been deleted."
    except Exception as e:
        session.rollback()
        return f"Error deleting student with ID {student_id}: {e}"


def add_student_to_course(new_student: str, course_name: int) -> str:
    """
    Add a student to the course (from a list)
    :param new_student: str
    :param course_name: int
    :return: str
    """
    try:
        course = session.query(CourseModel).filter(
            CourseModel.name == course_name).first()
        if not course:
            return f"Course {course_name} does not exist."
        first_name, last_name, group_id = new_student.split()
        student = session.query(StudentModel).filter_by(
            first_name=first_name, last_name=last_name, group_id=group_id).first()
        if not student:
            return f"Student {new_student} does not exist."
        course.students.append(student)
        session.commit()
        return f"{new_student} added to the course {course_name} successfully."
    except ValueError:
        return "Error: invalid input format. Please provide a string in the format 'First Last GroupID'."
    except Exception as e:
        session.rollback()
        return f"Error occurred while adding student to course: {str(e)}"


def remove_student_from_courses(student_full_name, course_name):
    """
    Remove the student from one of their courses.
    :param student_full_name: str
    :param course_name: str
    :return: str
    """
    try:
        first_name, last_name = student_full_name.split()
        student = session.query(StudentModel).filter_by(
            first_name=first_name, last_name=last_name).first()
        course = session.query(CourseModel).filter_by(name=course_name).first()
        if course not in student.courses:
            return f"{first_name} {last_name} is not enrolled in {course_name}."
        student.courses.remove(course)
        session.commit()
        return f"Removed {first_name} {last_name} from {course_name} successfully."
    except NoResultFound:
        return f"Could not find student {student_full_name} or course {course_name}."


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--find_all_groups',
        type=int,
        help='Find all groups with less or equals student count')
    parser.add_argument(
        '--find_all_students',
        type=str,
        help='Find all students related to the course with a given name')
    parser.add_argument(
        '--add_new_student',
        type=str,
        help='Add new student. Provide first name and last name')
    parser.add_argument(
        '--delete_student_for_id',
        type=int,
        help='Delete student by STUDENT_ID')
    parser.add_argument(
        '--add_student_to_course',
        nargs=2,
        help='Add a student to the course. Provide course name and student name (first name and last name)')
    parser.add_argument(
        '--remove_student_from_courses',
        nargs=2,
        help='Remove the student from one of his or her courses.'
             ' Provide student name (first name and last name) and course name')
    args = parser.parse_args()
    if args.find_all_groups:
        groups = find_all_students(args.find_all_groyps)
        print(groups)
    if args.find_all_students:
        students = find_all_students(args.find_all_students)
        print(students)
    if args.add_new_student:
        result = add_new_student(args.add_new_student)
        print(result)
    if args.delete_student_for_id:
        student_id = args.delete_student_for_id
        result = delete_student_for_id(student_id)
        print(result)
    if args.add_student_to_course:
        course_name, new_student = args.add_student_to_course
        result = add_student_to_course(course_name, new_student)
        print(result)
    if args.remove_student_from_courses:
        first_last_name, course_name = args.remove_student_from_courses
        result = remove_student_from_courses(
            first_last_name, course_name)
        print(result)


if __name__ == '__main__':
    main()
