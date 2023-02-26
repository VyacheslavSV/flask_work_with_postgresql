from sqlalchemy import ForeignKey, String, Integer, Column, create_engine, text
from sqlalchemy.orm import relationship, declarative_base


APPOINTED_USER = 'decan'
APPOINTED_PASS = 'qwerty'
APPOINTED_DB_NAME = 'studentdb'
Base = declarative_base()

engine = create_engine(
    f"postgresql://{APPOINTED_USER}:{APPOINTED_PASS}@/{APPOINTED_DB_NAME}")


class GroupModel(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    students = relationship('StudentModel', back_populates='group')


class StudentModel(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey('groups.id'))
    first_name = Column(String)
    last_name = Column(String)

    group = relationship('GroupModel', back_populates='students')
    courses = relationship(
        'CourseModel',
        secondary='student_course',
        overlaps='students')


class CourseModel(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

    students = relationship(
        'StudentModel',
        secondary='student_course',
        overlaps='courses')


class StudentCourse(Base):
    __tablename__ = 'student_course'

    student_id = Column(Integer, ForeignKey('students.id'), primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.id'), primary_key=True)


def add_tables():
    """ Add tables to the db """
    engine.connect().execute(text('SET search_path TO public'))

    Base.metadata.create_all(engine)
