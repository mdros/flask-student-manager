from typing import List

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ARRAY, DateTime, Integer, String
from sqlalchemy.sql import func

from extensions.database import db


class Student(db.Model):
    id: int = db.Column(Integer, primary_key=True)
    email: str = db.Column(String(40), nullable=False)
    first_name: str = db.Column(String(40), nullable=False)
    last_name: int = db.Column(String(40), nullable=False)
    gender: str = db.Column(String(8), nullable=False)
    time_spent_in_books: int = db.Column(Integer, nullable=True)
    created: DateTime = db.Column(DateTime, nullable=False, server_default=func.now())

    def __repr__(self):
        return f"{self.id} - {self.email} - {self.first_name} - {self.last_name} - {self.gender} - {self.favorite_subjects} - {self.time_spent_in_books} - {self.created}"
