from extensions.database import db


class Student(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(40), nullable=False)
    age: int = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"{self.id} - {self.name} - {self.age}"
