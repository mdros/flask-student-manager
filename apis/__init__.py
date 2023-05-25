from flask_restx import Api

from .student import api as student_namespace

api = Api(
    title="Students Api",
    version="1.0",
    description="Student management API",
)

api.add_namespace(student_namespace)
