from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any


class IEvaluatable(ABC):
    @abstractmethod
    def evaluate(self, student_id: int, grade: float) -> None:
        pass

    @abstractmethod
    def get_grade(self, student_id: int) -> Optional[float]:
        pass


class INonEvaluatable(ABC):
    @abstractmethod
    def get_material_info(self) -> str:
        pass


@dataclass
class Student:
    student_id: int
    full_name: str


@dataclass
class EvaluatedAssignment(IEvaluatable):
    title: str
    max_score: float
    grades: Dict[int, float] = field(default_factory=dict)

    def evaluate(self, student_id: int, grade: float) -> None:
        if 0 <= grade <= self.max_score:
            self.grades[student_id] = grade
        else:
            raise ValueError("Invalid grade range")

    def get_grade(self, student_id: int) -> Optional[float]:
        return self.grades.get(student_id)


@dataclass
class ReadingMaterial(INonEvaluatable):
    title: str
    content_url: str

    def get_material_info(self) -> str:
        return f"Reading material: {self.title}"


@dataclass
class Course:
    course_code: str
    title: str
    students: List[Student] = field(default_factory=list)
    components: List[Any] = field(default_factory=list)


class CourseManager:
    def __init__(self) -> None:
        self.courses: List[Course] = []

    def create_course(self, course_code: str, title: str) -> Course:
        course = Course(course_code=course_code, title=title)
        self.courses.append(course)
        return course

    def add_component_to_course(self, course_code: str, component: Any) -> bool:
        for course in self.courses:
            if course.course_code == course_code:
                course.components.append(component)
                return True
        return False


class EnrollmentService:
    @staticmethod
    def enroll_student(course: Course, student: Student) -> bool:
        if student not in course.students:
            course.students.append(student)
            return True
        return False


class GradingService:
    @staticmethod
    def assign_grade(assignment: IEvaluatable, student_id: int, grade: float) -> None:
        assignment.evaluate(student_id, grade)


class ResultReportingService:
    @staticmethod
    def generate_result(course: Course, student_id: int) -> Dict[str, Any]:
        earned_score = 0.0
        total_possible = 0.0

        for component in course.components:
            if isinstance(component, IEvaluatable):
                score = component.get_grade(student_id)
                if score is not None:
                    earned_score += score
                    total_possible += component.max_score

        return {
            "student_id": student_id,
            "course_code": course.course_code,
            "course_title": course.title,
            "earned_score": earned_score,
            "total_possible": total_possible
        }


if __name__ == "__main__":
    manager = CourseManager()

    course = manager.create_course("CS101", "Introduction to Python")

    student_1 = Student(student_id=1, full_name="Alex Smith")
    EnrollmentService.enroll_student(course, student_1)

    assignment = EvaluatedAssignment(title="Homework 1", max_score=10.0)
    material = ReadingMaterial(title="Lecture 1 Notes", content_url="http://example.com/lec1")

    manager.add_component_to_course("CS101", assignment)
    manager.add_component_to_course("CS101", material)

    GradingService.assign_grade(assignment, student_1.student_id, 9.5)

    result = ResultReportingService.generate_result(course, student_1.student_id)
    print("Course Result:", result)
