from pcalendar import *

class Employee:
    def __init__(self, name: str, address: str, type:str, payment_schedule:str, id: int = 0):
        self.name = name
        self.address = address

        self.type = type
        self.payment_schedule = payment_schedule

        self.payment_method = ''
        self.syndicate = False
        self.syndicate_id = 0
        self.syndicate_charge = 0
        self.id = id

        self.owing_qnt = 0

    def __str__(self):
        return f'{self.id}, {self.name}, {self.address}, {self.payment_schedule}, {self.type} | syndicate: {self.syndicate}, {self.syndicate_id}, {self.syndicate_charge}'

    def owing(self, owing: int):
        self.owing_qnt += owing

    def generate_schedule_paymethod(self, date, calen: PCalendar):
        payment_date = PCalendar.schedule_paymethod(date, self.payment_schedule)
        calen.add_schedule_date(self.id, payment_date)

        self.scheduled_date = payment_date

        if self.syndicate:
            self.owing(self.syndicate_charge)
    
    def delete(self, calen: PCalendar):
        index = next(i for i, x in enumerate(calen.get_day(self.scheduled_date)['schedule']) if x == self.id)
        del calen.get_day(self.scheduled_date)['schedule'][index]

    def print_generated_payment(self, value: int, date: datetime.date):
        print(f'Generated payment of: {self.name} R$ {value}\n | Payment method: {self.payment_method}\n | Date: {date}')

    def generate_payment(self, current_date, calen):
        raise NotImplementedError()

class Salaried(Employee):
    def __init__(self, name, address, monthly_wage, id = 0, date = 0):
        super().__init__(name, address, 'Salaried', 'monthly', id)

        self.monthly_wage = monthly_wage

    def generate_payment(self, current_date, calen: PCalendar):
        value = self.monthly_wage - self.owing_qnt
        super().print_generated_payment(value, current_date)

        super().generate_schedule_paymethod(current_date, calen)

class Commissioned(Employee):
    def __init__(self, name, address, commission, id = 0, date = 0):
        super().__init__(name, address, 'Commissioned', 'bi-weekly', id)

        self.base_salary = 900
        self.added_price = 0
        self.commission_rate = commission

        self.last_date = date

    def add_commission(self, price):
        value = price * (self.commission_rate / 100)
        self.added_price += value

    def generate_payment(self, current_date, calen: PCalendar):
        while self.last_date != current_date:
            ax = [(i, x) for i, x in enumerate(calen.get_day(self.last_date)['update']) if x[1] == self.id]
            for val in reversed(ax):
                self.add_commission(val[1][2])
                del calen.get_day(self.last_date)['update'][val[0]]
            self.last_date += datetime.timedelta(days=1)
        
        value = self.added_price + self.base_salary - self.owing_qnt
        super().print_generated_payment(value, current_date)
        self.added_price = 0

        super().generate_schedule_paymethod(current_date, calen)

class Hourly(Employee):
    def __init__(self, name, address, hour_wage, id = 0, date = 0):
        super().__init__(name, address, 'Hourly', 'weekly', id)

        self.hour_wage = hour_wage
        self.added_wage = 0

    def add_hourwage(self, hours):
        value = self.hour_wage * (hours - (hours - 8) * (hours > 8))

        if hours - 8 > 0:
            value += (hours - 8) * self.hour_wage * 1.5
        
        self.added_wage += value

    def generate_payment(self, current_date, current_calendar):
        value = self.added_wage - self.owing_qnt
        super().print_generated_payment(value, current_date)

        self.added_wage = 0

        super().generate_schedule_paymethod(current_date, current_calendar)