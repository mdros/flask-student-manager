from http import HTTPStatus
from operator import itemgetter

from flask_restx import Namespace, Resource, fields, marshal, reqparse
from sqlalchemy import select
from sqlalchemy.orm import Session

from extensions.database import db
from models.student import Student

api = Namespace("students", description="Students API namespace")

student_model = api.model(
    "Student",
    {
        "id": fields.Integer(readonly=True, required=False),
        "name": fields.String(required=True),
        "age": fields.Integer(required=True),
    },
)

body_parser = reqparse.RequestParser()
body_parser.add_argument("name", type=str, location="json")
body_parser.add_argument("age", type=int, location="json")

query_parser = reqparse.RequestParser()
query_parser.add_argument("name", type=str, location="args")
query_parser.add_argument("age", type=int, location="args")

session: Session = db.session


@api.route("")
class StudentList(Resource):
    @api.doc("list_students")
    @api.expect(query_parser)
    @api.marshal_list_with(student_model)
    def get(self):
        name, age = itemgetter("name", "age")(query_parser.parse_args())
        stmt = select(Student)
        if name:
            stmt = stmt.where(Student.name == name)
        if age:
            stmt = stmt.where(Student.age == age)
        students = session.execute(stmt).scalars().all()
        return students, HTTPStatus.OK

    @api.doc("post_student")
    @api.expect(body_parser)
    @api.marshal_with(student_model, code=HTTPStatus.CREATED)
    def post(self):
        name, age = itemgetter("name", "age")(body_parser.parse_args())
        student = Student(name=name, age=age)
        session.add(student)
        session.commit()
        return student, HTTPStatus.CREATED


@api.route("/<int:id>")
class StudentObject(Resource):
    @api.response(code=HTTPStatus.OK, model=student_model, description="Success")
    @api.response(code=HTTPStatus.NOT_FOUND, description="Not found")
    def get(self, id: int):
        student = session.get(Student, id)
        if student:
            return marshal(student, student_model), HTTPStatus.OK
        return {"message": "Not found"}, HTTPStatus.NOT_FOUND

    @api.response(code=HTTPStatus.OK, model=student_model, description="Success")
    @api.response(code=HTTPStatus.NOT_FOUND, description="Not found")
    def put(self, id: int):
        student = session.get(Student, id)
        if student:
            name, age = itemgetter("name", "age")(body_parser.parse_args())
            student.name = name
            student.age = age
            session.commit()
            return marshal(student, student_model), HTTPStatus.OK

        return {"message": "Not found"}, HTTPStatus.NOT_FOUND

    @api.response(code=HTTPStatus.OK, description="Success")
    def delete(self, id: int):
        student = session.get(Student, id)
        if student:
            session.delete(student)
            session.commit()
        return "", HTTPStatus.OK
