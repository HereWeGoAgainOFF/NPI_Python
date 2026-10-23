import datetime
import random


class LibraryRecord:
    def __init__(self, book_title, reader_name, issue_date, due_date, book_status):
        self.book_title = book_title
        self.chitatel = reader_name
        self.issue_date = issue_date
        self.srok_vozvrata = due_date
        self.book_status = book_status


class LibraryIterator:
    def __init__(self, records_collection):
        self.spisok_zapisey = records_collection
        self.current_index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_index < len(self.spisok_zapisey):
            element = self.spisok_zapisey[self.current_index]
            self.current_index += 1
            return element
        else:
            raise StopIteration


class LibraryManager:
    def __init__(self):
        self.vse_zapiski = []
        self._initialize_random_data()

    def _initialize_random_data(self):
        knigi_pool = ["Война и мир", "1984", "Мастер и Маргарита", "Идиот", "Кобзар", "Гамлет"]
        chitateli_pool = ["Иванов", "Петров", "Сидорова", "Смирнов", "Кузнецов"]

        today_date = datetime.date.today()
        for _ in range(6):
            b_title = random.choice(knigi_pool)
            r_name = random.choice(chitateli_pool)

            vydacha_d = today_date - datetime.timedelta(days=random.randint(1, 25))
            vozvrata_srok = vydacha_d + datetime.timedelta(days=10)
            status_val = random.choice(["выдана", "возвращена"])

            rec = LibraryRecord(
                book_title=b_title,
                reader_name=r_name,
                issue_date=vydacha_d.isoformat(),
                due_date=vozvrata_srok.isoformat(),
                book_status=status_val
            )
            self.vse_zapiski.append(rec)

    def _apply_filter(self, predicate_func):
        return list(filter(predicate_func, self.vse_zapiski))

    def filter_overdue_books(self):
        tekushchaya_data = datetime.date.today()
        is_overdue = lambda r: r.book_status == "выдана" and datetime.date.fromisoformat(
            r.srok_vozvrata) < tekushchaya_data
        return self._apply_filter(is_overdue)

    def get_readers_names(self):
        names_mapping = map(lambda item: item.chitatel, self.vse_zapiski)
        return list(set(names_mapping))

    def sort_by_due_date(self):
        return sorted(
            self.vse_zapiski,
            key=lambda item_rec: datetime.date.fromisoformat(item_rec.srok_vozvrata)
        )

    def count_issued_books(self):
        schetchik_vydannykh = sum(1 for item in self.vse_zapiski if item.book_status == "выдана")
        return schetchik_vydannykh

    def has_any_overdue(self):
        tekushchiy_den = datetime.date.today()
        proverka_prosrochki = any(
            item.book_status == "выдана" and datetime.date.fromisoformat(item.srok_vozvrata) < tekushchiy_den
            for item in self.vse_zapiski
        )
        return proverka_prosrochki

    def reader_books_generator(self, target_reader):
        for current_record in self.vse_zapiski:
            if current_record.chitatel.lower() == target_reader.lower() and current_record.book_status == "выдана":
                yield current_record


if __name__ == "__main__":
    manager = LibraryManager()

    print("ИТЕРАЦИЯ ПО ФОНДУ")
    iterator_obj = LibraryIterator(manager.vse_zapiski)
    for zapisi_item in iterator_obj:
        print(f"Книга: {zapisi_item.book_title} | Читатель: {zapisi_item.chitatel} | Статус: {zapisi_item.book_status}")

    print("\nПОЛУЧЕНИЕ ИМЕН ЧИТАТЕЛЕЙ")
    print(manager.get_readers_names())

    print("\nСОРТИРОВКА ПО СРОКУ ВОЗВРАТА")
    otsortirovannye = manager.sort_by_due_date()
    for s_item in otsortirovannye:
        print(f"Срок: {s_item.srok_vozvrata} | Книга: {s_item.book_title} ({s_item.chitatel})")

    print(f"\nКОЛИЧЕСТВО ВЫДАННЫХ КНИГ: {manager.count_issued_books()}")
    print(f"ЕСТЬ ЛИ ПРОСРОЧЕННЫЕ: {manager.has_any_overdue()}")

    print("\nФИЛЬТРАЦИЯ ПРОСРОЧЕННЫХ КНИГ")
    prosrochennye = manager.filter_overdue_books()
    if prosrochennye:
        for p in prosrochennye:
            print(f"Просрочена: {p.book_title} | Читатель: {p.chitatel} | Срок: {p.srok_vozvrata}")
    else:
        print("Нет просроченных книг.")

    print("\nГЕНЕРАТОР КНИГ КОНКРЕТНОГО ЧИТАТЕЛЯ")
    target_name = "Иванов"
    print(f"Активные книги для читателя '{target_name}':")
    gen_obj = manager.reader_books_generator(target_name)
    found = False
    for g_book in gen_obj:
        print(f"  -> {g_book.book_title} (Срок: {g_book.srok_vozvrata})")
        found = True
    if not found:
        print(" У данного читателя нет активных книг на руках.")
