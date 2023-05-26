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
        "email": fields.String(required=True),
        "first_name": fields.String(required=True),
        "last_name": fields.String(required=True),
        "gender": fields.String(required=True),
        "time_spent_in_books": fields.Integer(required=False),
        "created": fields.DateTime(readonly=True, required=False),
    },
)

body_parser = reqparse.RequestParser()
body_parser.add_argument(reqparse.Argument("email", type=str, location="json"))
body_parser.add_argument(reqparse.Argument("first_name", type=str, location="json"))
body_parser.add_argument(reqparse.Argument("last_name", type=str, location="json"))
body_parser.add_argument(
    reqparse.Argument("gender", type=str, location="json", choices=["MALE", "FEMALE"])
)
body_parser.add_argument(
    reqparse.Argument("time_spent_in_books", type=int, location="json")
)

query_parser = reqparse.RequestParser()
query_parser.add_argument("last_name", type=str, location="args")
query_parser.add_argument("gender", type=str, location="args")

session: Session = db.session


@api.route("")
class StudentList(Resource):
    @api.doc("list_students")
    @api.expect(query_parser)
    @api.marshal_list_with(student_model)
    def get(self):
        last_name, gender = itemgetter("last_name", "gender")(query_parser.parse_args())
        stmt = select(Student)
        if last_name:
            stmt = stmt.where(Student.last_name == last_name)
        if gender:
            stmt = stmt.where(Student.gender == gender)
        students = session.execute(stmt).scalars().all()
        return students, HTTPStatus.OK

    @api.doc("post_student")
    @api.expect(body_parser)
    @api.marshal_with(student_model, code=HTTPStatus.CREATED)
    def post(self):
        email, first_name, last_name, gender, time_spent_in_books = itemgetter(
            "email", "first_name", "last_name", "gender", "time_spent_in_books"
        )(body_parser.parse_args())
        student = Student(
            email=email,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            time_spent_in_books=time_spent_in_books,
        )
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
            email, first_name, last_name, gender, time_spent_in_books = itemgetter(
                "email", "first_name", "last_name", "gender", "time_spent_in_books"
            )(body_parser.parse_args())
            student.email = email
            student.first_name = first_name
            student.last_name = last_name
            student.gender = gender
            student.time_spent_in_books = time_spent_in_books
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
