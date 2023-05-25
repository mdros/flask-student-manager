import json
from re import A

import pytest
from flask import Flask
from flask.testing import FlaskClient
from flask_restx import marshal

from apis.student import student_model
from extensions.database import db
from models import Student

base_students = [
    Student(id=1, name="Test1", age=2),
    Student(id=2, name="Test2", age=3),
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


def test_get_all_students_age_filter(client: FlaskClient):
    expected_data = marshal(
        list(filter(lambda s: s.age == 3, base_students)), student_model
    )

    response = client.get("/students", query_string="age=3")
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data == expected_data


def test_get_all_students_name_filter(client: FlaskClient):
    expected_data = marshal(
        list(filter(lambda s: s.name == "Test1", base_students)), student_model
    )

    response = client.get("/students", query_string="name=Test1")
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data == expected_data


def test_add_student(client: FlaskClient):
    new_student = Student(name="Test3", age=4)

    response = client.post(
        "/students",
        json=marshal(new_student, student_model),
    )
    data = json.loads(response.data)

    assert response.status_code == 201
    assert data["name"] == new_student.name
    assert data["age"] == new_student.age


def test_update_student(client: FlaskClient):
    old_student_data = json.loads(client.get("/students/1").data)
    updated_student = Student(
        name=old_student_data["name"], age=old_student_data["age"] + 1
    )

    old_id = old_student_data["id"]
    response = client.put(
        f"/students/{old_id}", json=marshal(updated_student, student_model)
    )
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data["id"] == old_id
    assert data["name"] == old_student_data["name"]
    assert data["age"] == old_student_data["age"] + 1


def test_update_student_not_found(client: FlaskClient):
    updated_student = Student(name="Test", age=1)
    response = client.put("/students/10", json=marshal(updated_student, student_model))
    data = json.loads(response.data)

    assert response.status_code == 404
    assert data["message"] == "Not found"
