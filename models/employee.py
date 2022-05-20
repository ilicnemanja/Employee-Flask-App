from datetime import date


class Employee:

    def __init__(self, first_name: str, last_name: str, email: str, role: str, linked_in: str, salary: float,
                 photo: str = 'No image') -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.role = role
        self.linked_in = linked_in
        self.salary = salary
        self.photo = photo
        self.date_started = date.today().strftime("%d.%m.%Y.")

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name} is started working {self.date_started}'
