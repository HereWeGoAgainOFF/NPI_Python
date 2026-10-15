import random
import sys
from PyQt6 import QtWidgets, uic


class RailwayCar:
    def __init__(self, number, weight, year):
        self.number = number
        self.weight = weight
        self.year = year

    def capacity(self):
        pass


class PassengerCar(RailwayCar):
    def __init__(self, number, weight, year, wifi, conditioner):
        super().__init__(number, weight, year)
        self.wifi = wifi
        self.conditioner = conditioner
        self.seats_per_section = [random.randint(2, 5) for _ in range(16)]

    def capacity(self):
        return sum(self.seats_per_section)


class CargoCar(RailwayCar):
    def __init__(self, number, weight, year, cargo_type, capacities):
        super().__init__(number, weight, year)
        self.cargo_type = cargo_type
        self.capacities_per_section = capacities

    def capacity(self):
        return sum(self.capacities_per_section)


class Train:
    def __init__(self):
        self.passenger_cars = []
        self.cargo_cars = []
        self.generate_train()

    def generate_train(self):
        wifi_options = ["Есть", "Нет"]
        cond_options = ["Есть", "Нет"]
        for i in range(1, 9):
            car = PassengerCar(
                number=i,
                weight=random.randint(40, 65),
                year=random.randint(1995, 2024),
                wifi=random.choice(wifi_options),
                conditioner=random.choice(cond_options)
            )
            self.passenger_cars.append(car)

        cargo_types = ["Контейнер", "Насыпной", "Цистерна", "Платформа"]
        for i in range(1, 9):
            sections = [random.randint(3, 8) for _ in range(16)]
            car = CargoCar(
                number=i,
                weight=random.randint(25, 50),
                year=random.randint(1990, 2023),
                cargo_type=random.choice(cargo_types),
                capacities=sections
            )
            self.cargo_cars.append(car)


class LabaWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        uic.loadUi("form.ui", self)

        self.train = Train()
        self.init_ui()

    def init_ui(self):
        for car in self.train.passenger_cars:
            self.comboBox.addItem(f"Вагон № {car.number}")

        for car in self.train.cargo_cars:
            self.comboBox_2.addItem(f"Вагон № {car.number}")

        self.comboBox.currentIndexChanged.connect(self.update_passenger_info)
        self.comboBox_2.currentIndexChanged.connect(self.update_cargo_info)
        self.update_passenger_info(0)
        self.update_cargo_info(0)
        self.fill_tab_labels()

    def update_passenger_info(self, index):
        if index < 0 or index >= len(self.train.passenger_cars):
            return
        car = self.train.passenger_cars[index]

        self.RailwayCar.setText(f"Пассажирский вагон № {car.number}")
        self.kolvo_mest.setText(f"Общее кол-во мест: {car.capacity()}")
        self.year_vipuska_pessanger.setText(f"Год выпуска: {car.year}")
        self.weight_of_the_passenger_carriage.setText(f"Вес вагона: {car.weight} т")
        self.wi_fi.setText(f"Wi-Fi: {car.wifi}")
        self.conditioner.setText(f"Кондиционер: {car.conditioner}")

    def update_cargo_info(self, index):
        if index < 0 or index >= len(self.train.cargo_cars):
            return
        car = self.train.cargo_cars[index]

        self.CargCar.setText(f"Грузовой вагон № {car.number}")
        self.gruzopodiomnost.setText(f"Общая грузоподъемность: {car.capacity()} т")
        self.year_vipyska_gruz.setText(f"Год выпуска: {car.year}")
        self.weight_of_a_cargo_car.setText(f"Вес вагона: {car.weight} т")
        self.type_cargo.setText(f"Тип груза: {car.cargo_type}")

    def fill_tab_labels(self):
        pass_labels_row1 = [
            self.railcar1, self.railcar2, self.railcar3, self.railcar4,
            self.railcar5, self.railcar6, self.railcar7, self.railcar8
        ]
        pass_labels_row2 = [
            self.label_32, self.label_31, self.label_33, self.label_35,
            self.label_36, self.label_37, self.label_34, self.label_30
        ]

        for i, car in enumerate(self.train.passenger_cars):
            if i < len(pass_labels_row1):
                pass_labels_row1[i].setText(f"Вагон {car.number}\nМест: {car.capacity()}")
            if i < len(pass_labels_row2):
                pass_labels_row2[i].setText(f"Секций: {len(car.seats_per_section)}")

        cargo_labels_row1 = [
            self.label_38, self.label_39, self.label_40, self.label_41,
            self.label_42, self.label_43, self.label_44, self.label_45
        ]
        for i, car in enumerate(self.train.cargo_cars):
            if i < len(cargo_labels_row1):
                cargo_labels_row1[i].setText(f"Вагон {car.number}\nГруз: {car.capacity()}т")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = LabaWindow()
    window.show()
    sys.exit(app.exec())
