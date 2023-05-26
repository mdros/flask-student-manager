import json

import pytest
from flask import Flask
from flask.testing import FlaskClient
from flask_restx import marshal

from apis.student import student_model
from extensions.database import db
from models import Student

base_students = [
    Student(
        id=1,
        email="email1@gmail.com",
        first_name="name1",
        last_name="lastname1",
        gender="MALE",
    ),
    Student(
        id=2,
        email="email2@gmail.com",
        first_name="name2",
        last_name="lastname2",
        gender="FEMALE",
        time_spent_in_books=12031345235,
    ),
]


@pytest.fixture(autouse=True)
def add_test_students(app: Flask):
    with app.app_context():
        db.session.add_all(base_students)
        db.session.commit()


def test_get_all_students(client: FlaskClient):
    expected_data = marshal(base_students, student_model)

    response = client.get("/students")
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data == expected_data


def test_get_all_students_last_name_filter(client: FlaskClient):
    expected_data = marshal(
        list(filter(lambda s: s.last_name == "lastname1", base_students)), student_model
    )

    response = client.get("/students", query_string="last_name=lastname1")
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data == expected_data


def test_get_all_students_gender_filter(client: FlaskClient):
    expected_data = marshal(
        list(filter(lambda s: s.gender == "FEMALE", base_students)), student_model
    )

    response = client.get("/students", query_string="gender=FEMALE")
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data == expected_data


def test_add_student(client: FlaskClient):
    new_student = Student(
        email="email3@gmail.com",
        first_name="name3",
        last_name="lastname3",
        gender="MALE",
        time_spent_in_books=141234,
    )

    response = client.post(
        "/students",
        json=marshal(new_student, student_model),
    )
    data = json.loads(response.data)

    assert response.status_code == 201
    assert data["email"] == new_student.email
    assert data["first_name"] == new_student.first_name
    assert data["last_name"] == new_student.last_name
    assert data["gender"] == new_student.gender
    assert data["time_spent_in_books"] == new_student.time_spent_in_books


def test_update_student(client: FlaskClient):
    old_student_data = json.loads(client.get("/students/1").data)
    updated_student = Student(
        email=old_student_data["email"],
        first_name=old_student_data["first_name"],
        last_name="updated-last-name",
        gender=old_student_data["gender"],
        time_spent_in_books=12312312,
    )

    old_id = old_student_data["id"]
    response = client.put(
        f"/students/{old_id}", json=marshal(updated_student, student_model)
    )
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data["id"] == old_id
    assert data["first_name"] == old_student_data["first_name"]
    assert data["last_name"] == "updated-last-name"
    assert data["gender"] == old_student_data["gender"]
    assert data["time_spent_in_books"] == 12312312


def test_update_student_not_found(client: FlaskClient):
    updated_student = Student(
        email="email3@gmail.com",
        first_name="name3",
        last_name="lastname3",
        gender="FEMALE",
    )
    response = client.put("/students/10", json=marshal(updated_student, student_model))
    data = json.loads(response.data)

    assert response.status_code == 404
    assert data["message"] == "Not found"
