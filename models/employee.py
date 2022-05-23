from datetime import date


class Employee:

    def __init__(self, id: int, first_name: str, last_name: str, email: str, role: str, linked_in: str, salary: float,
                 photo: str = '') -> None:
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.role = role
        self.linked_in = linked_in
        self.salary = float(salary)
        self.photo = photo
        self.date_started = date.today()

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name} is started working {self.date_started.strftime("%d.%m.%Y.")}'


# new_emp1 = Employee(None, 'Petar', 'Peric', 'petarperic@example.com',
#                     'Python', 'linkedin', '200')
# print(new_emp1)
