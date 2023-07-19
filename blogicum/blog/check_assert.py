class Contact:

    def __init__(self, name, year_birth, is_programmer):
        self.name = name
        self.year_birth = year_birth
        self.is_programmer = is_programmer

    def age_define(self):
        if 1946 < self.year_birth < 1980:
            return 'Олдскул'
        if self.year_birth >= 1980:
            return 'Молодой'
        return 'Старейшина'

    def programmer_define(self):
        if self.is_programmer:
            return 'Программист'
        return 'Нормальный'

    def show_contact(self):
        return (f'{self.name}, '
                f'категория: {self.age_define()}, '
                f'статус: {self.programmer_define()}')
    
bill_gates = Contact(name='Билл Гейтс', year_birth=1955, is_programmer=True)

print(bill_gates.show_contact())

# Создаём экземпляр класса Contact
mike = Contact('Михаил Булгаков', 1891, False)

# Заготавливаем строку, которую по ожиданию должен вернуть метод show_contact():
expected_string = 'Михаил Булгаков, категория: Старейшина, статус: Нормальный'

# Пишем утверждение: 
# "вызов метода show_contact объекта mike вернёт строку, сохранённую в expected_string"
assert mike.show_contact() == expected_string, 'Метод show_contact работает некорректно!'
