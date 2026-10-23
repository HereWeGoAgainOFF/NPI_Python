import datetime
import json
import os
import random


class BookAlreadyIssuedError(Exception):
    def __init__(self, book_title):
        super().__init__(f"Ошибка: Книга '{book_title}' уже выдана другому читателю!")
        self.book_title = book_title


class LendingRecord:
    def __init__(self, book_title, reader_name, issue_date, due_date, status="выдана"):
        self.book_title = book_title
        self.reader_name = reader_name
        self.issue_date = issue_date
        self.due_date = due_date
        self.status = status

    def to_dict(self):
        return {
            "book_title": self.book_title,
            "reader_name": self.reader_name,
            "issue_date": self.issue_date,
            "due_date": self.due_date,
            "status": self.status
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            book_title=data["book_title"],
            reader_name=data["reader_name"],
            issue_date=data["issue_date"],
            due_date=data["due_date"],
            status=data["status"]
        )

    def __str__(self):
        return f"Книга: '{self.book_title}' | Читатель: {self.reader_name} | Выдана: {self.issue_date} | Срок: {self.due_date} | Статус: {self.status}"


class LibrarySystem:
    def __init__(self, filename="library_data.json"):
        self.filename = filename
        self.records = []
        self.load_state()

        if not self.records:
            self.generate_random_start_data()

    def generate_random_start_data(self):
        books_pool = [
            "Война и мир", "Преступление и наказание", "Мастер и Маргарита",
            "1984", "Гарри Поттер", "Властелин Колец", "Мертвые души", "Вишневый сад"
        ]
        readers_pool = ["Иван Иванов", "Анна Смирнова", "Пётр Петров", "Елена Васильева", "Дмитрий Соколов"]

        count = random.randint(3, 5)
        chosen_books = random.sample(books_pool, min(count, len(books_pool)))

        today = datetime.date.today()
        for book in chosen_books:
            reader = random.choice(readers_pool)
            days_offset = random.randint(-5, 10)
            issue_date = today - datetime.timedelta(days=abs(days_offset) + 5)
            due_date = issue_date + datetime.timedelta(days=10)
            status = random.choice(["выдана", "возвращена"])

            record = LendingRecord(
                book_title=book,
                reader_name=reader,
                issue_date=issue_date.isoformat(),
                due_date=due_date.isoformat(),
                status=status
            )
            self.records.append(record)
        self.save_state()

    def issue_book(self, book_title, reader_name, days_to_return=14):
        for record in self.records:
            if record.book_title.lower() == book_title.lower() and record.status == "выдана":
                raise BookAlreadyIssuedError(book_title)

        issue_date = datetime.date.today()
        due_date = issue_date + datetime.timedelta(days=days_to_return)

        new_record = LendingRecord(
            book_title=book_title,
            reader_name=reader_name,
            issue_date=issue_date.isoformat(),
            due_date=due_date.isoformat(),
            status="выдана"
        )
        self.records.append(new_record)
        self.save_state()
        print(f"\n[Успех] Книга '{book_title}' выдана читателю '{reader_name}' до {due_date.isoformat()}.")

    def return_book(self, book_title, reader_name):
        found = False
        for record in self.records:
            if (record.book_title.lower() == book_title.lower() and
                    record.reader_name.lower() == reader_name.lower() and
                    record.status == "выдана"):
                record.status = "возвращена"
                found = True
                break

        if found:
            self.save_state()
            print(f"\n[Успех] Книга '{book_title}' успешно возвращена в библиотеку.")
        else:
            print(f"\n[Ошибка] Активная выдача книги '{book_title}' для читателя '{reader_name}' не найдена.")

    def find_overdue_books(self):
        today = datetime.date.today()
        overdue_records = []
        for record in self.records:
            if record.status == "выдана":
                due_date = datetime.date.fromisoformat(record.due_date)
                if today > due_date:
                    overdue_records.append(record)
        return overdue_records

    def find_reader_books(self, reader_name):
        return [
            record for record in self.records
            if record.reader_name.lower() == reader_name.lower() and record.status == "выдана"
        ]

    def show_all_records(self):
        if not self.records:
            print("\nФонд пуст.")
            return
        print("\n--- Все записи библиотечного фонда ---")
        for i, record in enumerate(self.records, 1):
            print(f"{i}. {record}")

    def save_state(self):
        try:
            data = [record.to_dict() for record in self.records]
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except IOError as e:
            print(f"Ошибка сохранения файла: {e}")

    def load_state(self):
        """Загрузка из JSON файла"""
        if not os.path.exists(self.filename):
            return
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.records = [LendingRecord.from_dict(d) for d in data]
        except (json.JSONDecodeError, IOError) as e:
            print(f"Ошибка загрузки файла: {e}")


def main():
    library = LibrarySystem()

    while True:
        print("СИСТЕМА УЧЕТА БИБЛИОТЕЧНОГО ФОНДА")
        print("1. Посмотреть все записи")
        print("2. Выдать книгу (ввести свои данные)")
        print("3. Вернуть книгу")
        print("4. Найти просроченные книги")
        print("5. Найти книги конкретного читателя")
        print("6. Сбросить данные и запустить рандомайзер заново")
        print("0. Выход")

        choice = input("\nВыберите пункт меню: ").strip()

        if choice == "1":
            library.show_all_records()

        elif choice == "2":
            book_title = input("Введите название книги: ").strip()
            reader_name = input("Введите ФИО читателя: ").strip()
            if not book_title or not reader_name:
                print("[Ошибка] Поля не могут быть пустыми!")
                continue

            try:
                days_input = input("Срок возврата в днях (нажмите Enter для значения по умолчанию — 14): ").strip()
                days = int(days_input) if days_input else 14
                library.issue_book(book_title, reader_name, days)
            except ValueError:
                print("[Ошибка] Введите корректное число для дней!")
            except BookAlreadyIssuedError as e:
                print(f"\n[Исключение перехвачено] {e}")

        elif choice == "3":
            book_title = input("Введите название возвращаемой книги: ").strip()
            reader_name = input("Введите ФИО читателя: ").strip()
            library.return_book(book_title, reader_name)

        elif choice == "4":
            overdue = library.find_overdue_books()
            print("\n--- Список просроченных книг ---")
            if overdue:
                for record in overdue:
                    print(record)
            else:
                print("Просроченных книг нет.")

        elif choice == "5":
            reader_name = input("Введите ФИО читателя для поиска: ").strip()
            books = library.find_reader_books(reader_name)
            print(f"\n--- Книги на руках у читателя '{reader_name}' ---")
            if books:
                for record in books:
                    print(record)
            else:
                print("У данного читателя нет активных книг на руках.")

        elif choice == "6":
            if os.path.exists("library_data.json"):
                os.remove("library_data.json")
            library.records = []
            library.generate_random_start_data()
            print("[Успех] Старые данные удалены, сгенерированы новые случайные записи.")

        elif choice == "0":
            print("\nВыход из программы. До свидания!")
            break
        else:
            print("[Ошибка] Неверный выбор. Попробуйте от 0 до 6.")


if __name__ == "__main__":
    main()
