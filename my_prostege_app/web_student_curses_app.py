from xml.dom.minidom import parseString

from dicttoxml import dicttoxml
from flasgger import swag_from
from flask import Blueprint, request, jsonify, render_template, abort
from flask_restful import Api, Resource
from my_prostege_app.querys.orm_queries import find_all_groups, find_all_students, add_new_student, \
    delete_student_for_id, add_student_to_course, remove_student_from_courses


bp = Blueprint('web_student_curses_app', __name__)
api = Api(bp)


def prepare_responce(format_: str, data: list):
    """ Prepares a response for the given format and data.
        :param format_ (str): The format of the response, either json or xml.
        :param data (list): The data to be included in the response.
        :return: json response, or xml response, or a 404 error.
    """
    if format_ == 'json':
        return jsonify(data)
    elif format_ == 'xml':
        return parseString(dicttoxml(data, custom_root='report')).toprettyxml(), 200
    return abort(404, description="Please input correct format: json or xml")


@bp.route('/groups/')
def get_groups_with_fewer_students():
    student_count = request.args.get('student_count')
    groups = find_all_groups(student_count)
    return render_template('all_groups.html', groups=groups)


@bp.route('/students/', methods=['GET', 'POST', 'DELETE'])
def get_students_in_course():
    course_name = request.args.get('course_name')
    new_student = request.args.get('new_student')
    student_id = request.args.get('del_student')
    if course_name:
        students = find_all_students(course_name)
        return render_template('all_students.html', students=students)
    if new_student:
        add_student = add_new_student(new_student)
        return render_template('new_student.html', student=add_student)
    if student_id:
        delete_student = delete_student_for_id(student_id)
        return render_template('delete_students.html', delete_student=delete_student)


@bp.route('/courses/', methods=['GET', 'POST', 'DELETE'])
def add_student_to_course_route():
    add_student = request.args.get('add_student')
    course_name = request.args.get('course_name')
    remove_student = request.args.get('remove_student')
    if add_student:
        add_student_ = add_student_to_course(add_student, course_name)
        return render_template('add_student_to_course.html', add_student=add_student_)
    if remove_student:
        remove_student_ = remove_student_from_courses(remove_student, course_name)
        return render_template('remove_student_from_courses.html', remove_student=remove_student_)


class ApiGroups(Resource):
    @swag_from('groups.yml')
    def get(self):
        student_count = request.args.get('student_count')
        format_ = request.args.get('format')
        groups = find_all_groups(student_count)
        current_dict_groups = [{'id_group': id_number, 'name': group.name} for id_number, group in enumerate(groups, 1)]
        return prepare_responce(format_, current_dict_groups)


class ApiStudents(Resource):
    @swag_from('students.yml')
    def get(self):

        course_name = request.args.get('course_name')
        new_student = request.args.get('new_student')
        student_id = request.args.get('del_student')
        format_ = request.args.get('format')
        if course_name:
            students = find_all_students(course_name)
            current_dict_groups = [
                {'id_student': id_number, 'first_name': student.first_name, 'last_name': student.last_name} for
                id_number, student in enumerate(students, 1)]
            return prepare_responce(format_, current_dict_groups)
        if new_student:
            add_student = add_new_student(new_student)
            current_dict_groups = [{'info_string': add_student}]
            return prepare_responce(format_, current_dict_groups)
        if student_id:
            delete_student = delete_student_for_id(student_id)
            current_dict_groups = [{'info_string': delete_student}]
            return prepare_responce(format_, current_dict_groups)


class ApiCourses(Resource):
    @swag_from('courses.yml')
    def get(self):
        add_student = request.args.get('add_student')
        course_name = request.args.get('course_name')
        remove_student = request.args.get('remove_student')
        format_ = request.args.get('format')
        if add_student:
            add_student_ = add_student_to_course(add_student, course_name)
            current_dict_groups = [{'info_string': add_student_}]
            return prepare_responce(format_, current_dict_groups)
        if remove_student:
            remove_student_ = remove_student_from_courses(remove_student, course_name)
            current_dict_groups = [{'info_string': remove_student_}]
            return prepare_responce(format_, current_dict_groups)


api.add_resource(ApiGroups, '/api/v1/groups/')
api.add_resource(ApiStudents, '/api/v1/students/')
api.add_resource(ApiCourses, '/api/v1/courses/')
