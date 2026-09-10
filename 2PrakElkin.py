import tkinter as tk
from tkinter import messagebox, ttk
import random
import tempfile, base64, zlib


class PracApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Товары склада")
        self.root.geometry("1000x650")

        ICON = zlib.decompress(
            base64.b64decode("eJxjYGAEQgEBBiDJwZDBysAgxsDAoAHEQCEGBQaIOAg4sDIgACMUj4JRMApGwQgF/ykEAFXxQRc="))

        _, ICON_PATH = tempfile.mkstemp()
        with open(ICON_PATH, "wb") as icon_file:
            icon_file.write(ICON)

        root.iconbitmap(default=ICON_PATH)
        #

        self.products = [
            {"art": "101", "name": "Intel Core i5-14400F OEM", "category": "Процессор", "qty": 15, "min_qty": 5},
            {"art": "102", "name": "AMD Ryzen 9 9950X3D OEM", "category": "Процессор", "qty": 3, "min_qty": 5},
            {"art": "103", "name": "MSI GeForce RTX 5060 VENTUS 2X OC [RTX 5060 8G VENTUS 2X OC]", "category": "Видеокарта", "qty": 8, "min_qty": 10},
            {"art": "104", "name": "PowerColor AMD Radeon RX 9060 XT Reaper [RX9060XT 16G-A]", "category": "Видеокарта", "qty": 25, "min_qty": 8},
            {"art": "105", "name": "Razer Viper V4 Pro [RZ01-05630200-R3G1] белый", "category": "Аксессуары", "qty": 4, "min_qty": 10},
            {"art": "106", "name": "Клавиатура проводная + беспроводная AULA F75 цвет черный", "category": "Аксессуары", "qty": 50, "min_qty": 15},
            {"art": "107", "name": "Razer BlackShark V2 X черный 2022", "category": "Аудио", "qty": 2, "min_qty": 4},
            {"art": "108", "name": "Razer Kraken Kitty V2 BT черный 2023", "category": "Аудио", "qty": 12, "min_qty": 6},]

        self.sort_asc = True

        #ВЕРХ
        top_frame = ttk.Frame(self.root, padding=10)
        top_frame.pack(fill="x")

        top_frame.columnconfigure(0, weight=1)
        top_frame.columnconfigure(1, weight=3)

        #ЛЕВАЯ КОЛОНКА
        left_frame = ttk.Frame(top_frame)
        left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.label_art = ttk.Label(left_frame, text="Введите артикул товара:")
        self.label_art.grid(row=0, column=0, sticky="w", pady=(5, 5))

        self.entry_art = ttk.Entry(left_frame)
        self.entry_art.grid(row=1, column=0, sticky="ew", pady=(5, 5))

        self.btn_search = ttk.Button(left_frame, text="Найти товар", command=self.search_by_art)
        self.btn_search.grid(row=2, column=0, sticky="ew", pady=(5, 5))

        self.entry_result = ttk.Entry(left_frame, state='readonly')
        self.entry_result.grid(row=3, column=0, sticky="ew", pady=(5, 5))

        self.btn_sort = ttk.Button(left_frame, text="Сортировка по количеству", command=self.sort_by_quantity)
        self.btn_sort.grid(row=4, column=0, sticky="ew", pady=(15, 5))

        #ПРАВАЯ КОЛОНКА
        top_right_frame = ttk.Frame(top_frame)
        top_right_frame.grid(row=0, column=1, sticky="nsew")

        top_right_frame.columnconfigure(0, weight=1)
        top_right_frame.columnconfigure(1, weight=1)

        self.var_total_qty = tk.StringVar(value="0")
        self.var_max_stock = tk.StringVar(value="-")
        self.var_low_stock_count = tk.StringVar(value="0")
        self.var_categories = tk.StringVar(value="-")

        #статы
        total_frame = ttk.LabelFrame(top_right_frame, text="Общее кол-во товаров (шт.)")
        total_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        ttk.Label(total_frame, textvariable=self.var_total_qty, font=("Arial", 10, "bold")).pack(padx=10, pady=10)

        max_frame = ttk.LabelFrame(top_right_frame, text="Товар с макс. остатком")
        max_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        ttk.Label(max_frame, textvariable=self.var_max_stock, font=("Arial", 10, "bold")).pack(padx=10, pady=10)

        low_frame = ttk.LabelFrame(top_right_frame, text="Недостаточный остаток (поз.)")
        low_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        ttk.Label(low_frame, textvariable=self.var_low_stock_count, font=("Arial", 10, "bold"), foreground="red").pack(padx=10, pady=10)

        cat_frame = ttk.LabelFrame(top_right_frame, text="Список категорий")
        cat_frame.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
        ttk.Label(cat_frame, textvariable=self.var_categories, font=("Arial", 9), wraplength=200).pack(padx=10, pady=10)

        #НИЖНЯЯ ЧАСТЬ
        bottom_frame = ttk.LabelFrame(self.root, text="Товары на складе", padding=10)
        bottom_frame.pack(fill="both", expand=True, padx=10, pady=10)

        #вывод списка товаров
        columns = ("art", "name", "category", "qty", "min_qty")
        self.tree = ttk.Treeview(bottom_frame, columns=columns, show="headings")

        self.tree.heading("art", text="Артикул")
        self.tree.heading("name", text="Название")
        self.tree.heading("category", text="Категория")
        self.tree.heading("qty", text="Количество")
        self.tree.heading("min_qty", text="Мин. остаток")

        self.tree.column("art", width=100, anchor="center")
        self.tree.column("name", width=200, anchor="w")
        self.tree.column("category", width=150, anchor="w")
        self.tree.column("qty", width=100, anchor="center")
        self.tree.column("min_qty", width=100, anchor="center")

        #подсветочка
        self.tree.tag_configure("low_stock", background="#FADADD")

        self.tree.pack(fill="both", expand=True)

        self.update_ui()

    def search_by_art(self):
        art_input = self.entry_art.get().strip().upper()

        if not art_input:
            messagebox.showerror("Ошибка", "Пожалуйста, введите артикул")
            return

        found = next((item for item in self.products if item["art"].upper() == art_input), None)

        self.entry_result.config(state='normal')
        self.entry_result.delete(0, tk.END)

        if found:
            self.entry_result.insert(0, f"{found['name']} ({found['qty']} шт.)")
        else:
            self.entry_result.insert(0, "Товар не найден")
            messagebox.showwarning("Упси", "Товар с таким артикулом не найден на складе")

        self.entry_result.config(state='readonly')

    def sort_by_quantity(self):
        self.products.sort(key=lambda x: x["qty"], reverse=not self.sort_asc)
        self.sort_asc = not self.sort_asc
        self.update_ui()

    def calculate_statistics(self):
        if not self.products:
            return

        #щбщее кол-во
        total_qty = sum(item["qty"] for item in self.products)
        self.var_total_qty.set(str(total_qty))

        #макс остаток
        max_item = max(self.products, key=lambda x: x["qty"])
        self.var_max_stock.set(f"{max_item['name']} ({max_item['qty']} шт.)")

        #недостаточ остаток
        low_stock_items = [item for item in self.products if item["qty"] < item["min_qty"]]
        self.var_low_stock_count.set(str(len(low_stock_items)))

        #категории
        categories = sorted(list(set(item["category"] for item in self.products)))
        self.var_categories.set(", ".join(categories))

    def update_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for item in self.products:
            tags = ()
            if item["qty"] < item["min_qty"]:
                tags = ("low_stock",)

            self.tree.insert(
                "",
                tk.END,
                values=(item["art"], item["name"], item["category"], item["qty"], item["min_qty"]),
                tags=tags
            )

    def update_ui(self):
        self.calculate_statistics()
        self.update_table()


if __name__ == "__main__":
    root = tk.Tk()
    app = PracApp(root)
    root.mainloop()
