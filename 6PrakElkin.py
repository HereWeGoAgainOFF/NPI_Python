from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from enum import Enum
import functools
import contextlib


class CourseStatus(Enum):
    OPEN = "открыт"
    CLOSED = "закрыт"
    ARCHIVED = "архивирован"


@dataclass
class Student:
    student_id: int
    full_name: str
    grades: Dict[str, int] = field(default_factory=dict)


@dataclass
class Teacher:
    teacher_id: int
    full_name: str
    discipline: str


@dataclass
class Course:
    course_code: str
    title: str
    teacher: Teacher
    status: CourseStatus
    students: List[Student] = field(default_factory=list)


def action_logger(func):
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        result = func(*args, **kwargs)
        return result

    return wrapper


@contextlib.contextmanager
def university_session(system_instance: Any):
    try:
        yield system_instance
    finally:
        pass


class UniversitySystem:
    def __init__(self) -> None:
        self.courses: List[Course] = []
        self.students: List[Student] = []
        self.teachers: List[Teacher] = []

    @action_logger
    def add_teacher(self, teacher: Teacher) -> None:
        self.teachers.append(teacher)

    @action_logger
    def edit_teacher(self, teacher_id: int, new_name: str, new_discipline: str) -> bool:
        for teacher in self.teachers:
            if teacher.teacher_id == teacher_id:
                teacher.full_name = new_name
                teacher.discipline = new_discipline
                return True
        return False

    @action_logger
    def delete_teacher(self, teacher_id: int) -> bool:
        for teacher in self.teachers:
            if teacher.teacher_id == teacher_id:
                self.teachers.remove(teacher)
                return True
        return False

    @action_logger
    def add_student(self, student: Student) -> None:
        self.students.append(student)

    @action_logger
    def edit_student(self, student_id: int, new_name: str) -> bool:
        for student in self.students:
            if student.student_id == student_id:
                student.full_name = new_name
                return True
        return False

    @action_logger
    def delete_student(self, student_id: int) -> bool:
        for student in self.students:
            if student.student_id == student_id:
                self.students.remove(student)
                for course in self.courses:
                    if student in course.students:
                        course.students.remove(student)
                return True
        return False

    @action_logger
    def add_course(self, course: Course) -> None:
        self.courses.append(course)

    @action_logger
    def edit_course(self, course_code: str, new_title: str, new_status: CourseStatus) -> bool:
        for course in self.courses:
            if course.course_code == course_code:
                course.title = new_title
                course.status = new_status
                return True
        return False

    @action_logger
    def delete_course(self, course_code: str) -> bool:
        for course in self.courses:
            if course.course_code == course_code:
                self.courses.remove(course)
                return True
        return False

    @action_logger
    def enroll_student(self, course_code: str, student_id: int) -> bool:
        target_course = None
        for course in self.courses:
            if course.course_code == course_code:
                target_course = course
                break

        target_student = None
        for student in self.students:
            if student.student_id == student_id:
                target_student = student
                break

        if target_course and target_student and target_course.status == CourseStatus.OPEN:
            if target_student not in target_course.students:
                target_course.students.append(target_student)
                return True
        return False

    def calculate_average_score(self, course_code: str) -> float:
        total_sum = 0
        total_count = 0
        for course in self.courses:
            if course.course_code == course_code:
                for student in course.students:
                    if course_code in student.grades:
                        total_sum += student.grades[course_code]
                        total_count += 1
        if total_count == 0:
            return 0.0
        return total_sum / total_count

    def find_popular_courses(self) -> List[Course]:
        if not self.courses:
            return []
        max_students = max(len(course.students) for course in self.courses)
        return [course for course in self.courses if len(course.students) == max_students]


def main():
    system = UniversitySystem()

    teacher_1 = Teacher(teacher_id=1, full_name="Иванов И.И.", discipline="Математика")
    student_1 = Student(student_id=101, full_name="Алексей Смирнов", grades={"MATH101": 5})
    course_1 = Course(course_code="MATH101", title="Высшая математика", teacher=teacher_1, status=CourseStatus.OPEN,
                      students=[student_1])

    system.add_teacher(teacher_1)
    system.add_student(student_1)
    system.add_course(course_1)

    with university_session(system) as session:
        while True:
            print("\nСИСТЕМА УПРАВЛЕНИЯ УНИВЕРСИТЕТСКИМИ КУРСАМИ")
            print("1. Показать все курсы")
            print("2. Добавить курс")
            print("3. Редактировать курс")
            print("4. Удалить курс")
            print("5. Записать студента на курс")
            print("6. Посчитать средний результат курса")
            print("7. Найти наиболее популярные курсы")
            print("0. Выход")

            choice = input("\nВыберите пункт меню: ").strip()

            if choice == "1":
                print("\nСписок курсов")
                if not session.courses:
                    print("Курсов нет.")
                for c in session.courses:
                    print(
                        f"Код: {c.course_code} | Название: {c.title} | Статус: {c.status.value} | Преподаватель: {c.teacher.full_name} | Студентов: {len(c.students)}")

            elif choice == "2":
                code = input("Введите код курса: ").strip()
                title = input("Введите название курса: ").strip()
                t_name = input("ФИО преподавателя: ").strip()
                t_disc = input("Дисциплина преподавателя: ").strip()
                t_id = len(session.teachers) + 1
                new_teacher = Teacher(teacher_id=t_id, full_name=t_name, discipline=t_disc)
                session.add_teacher(new_teacher)

                new_course = Course(course_code=code, title=title, teacher=new_teacher, status=CourseStatus.OPEN)
                session.add_course(new_course)
                print("Курс успешно добавлен!")

            elif choice == "3":
                code = input("Введите код курса для редактирования: ").strip()
                new_title = input("Новое название курса: ").strip()
                print("Выберите статус (1 - открыт, 2 - закрыт, 3 - архивирован): ")
                s_choice = input("Ваш выбор: ").strip()
                status_map = {"1": CourseStatus.OPEN, "2": CourseStatus.CLOSED, "3": CourseStatus.ARCHIVED}
                new_status = status_map.get(s_choice, CourseStatus.OPEN)

                success = session.edit_course(code, new_title, new_status)
                if success:
                    print("Курс успешно обновлен!")
                else:
                    print("Курс с таким кодом не найден.")

            elif choice == "4":
                code = input("Введите код курса для удаления: ").strip()
                success = session.delete_course(code)
                if success:
                    print("Курс удален!")
                else:
                    print("Курс не найден.")

            elif choice == "5":
                code = input("Введите код курса: ").strip()
                s_name = input("ФИО студента: ").strip()
                s_id = len(session.students) + 1
                new_student = Student(student_id=s_id, full_name=s_name, grades={code: 4})
                session.add_student(new_student)

                success = session.enroll_student(code, s_id)
                if success:
                    print("Студент успешно записан на курс!")
                else:
                    print("Не удалось записать студента (курс закрыт или не найден).")

            elif choice == "6":
                code = input("Введите код курса для расчета среднего результата: ").strip()
                avg = session.calculate_average_score(code)
                print(f"Средний результат по курсу {code}: {avg}")

            elif choice == "7":
                popular = session.find_popular_courses()
                print("\nСамые популярные курсы")
                if not popular:
                    for p in popular:
                        print(f"- {p.title} (Студентов: {len(p.students)})")

            elif choice == "0":
                print("Выход из программы.")
                break
            else:
                print("Неверный ввод, попробуйте снова.")


if __name__ == "__main__":
    main()
