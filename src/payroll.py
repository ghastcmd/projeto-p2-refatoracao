from employee import *
from unidecode import unidecode

# * Starting payroll system * #

def employee_paymethod(paymethod):
    paymethod_arr = [
        'deposit in bank account', 'check by mail', 'check by hand',
        'deposito em conta bancaria', 'cheque pelo correio',
        'cheque em maos'
    ]

    assert unidecode(paymethod.lower()) in paymethod_arr

    paymethod_dict = {
        'deposit in bank account': 'Deposit in bank account', 
        'check by mail': 'Check by mail',
        'check by hand': 'Check by hand',
        'deposito em conta bancaria': 'Depósito em conta bancária',
        'cheque pelo correio': 'Cheque pelo correio',
        'cheque em maos': 'Cheque em mãos',
    }

    return paymethod_dict[unidecode(paymethod.lower())]


class PayrollSystem:
    current_date = datetime.date.today()

    def __init__(self):
        self.count = 1
        self.employees = []
        self.calendar = {}
        for i in range(366):
            self.calendar[i] = {'schedule': [], 'update': []}

        self.current_day = self.calendar[hash_date(self.current_date)]

    def run_today_payroll(self):
        iter_thru = [(i,x) for i, x in enumerate(self.calendar[hash_date(self.current_date)]['schedule'])]
        for i, id in reversed(iter_thru):
            employee = self.search_employee(id)
            employee.generate_payment(self.current_date, self.calendar)
            del self.calendar[hash_date(self.current_date)]['schedule'][i]

    def update_day(self, add_days = 1):
        self.current_date += datetime.timedelta(days=add_days)
        self.current_day = self.calendar[hash_date(self.current_date)]

    def print_vals(self):
        print('------------ list of employees -------------')
        for i, employee in enumerate(self.employees):
            print(f'{i}: {employee}')

    def add_employee(self, name: str, address: str, type: str, attr: int):
        types = ['salaried', 'commissioned', 'hourly']
        assert type in types

        if type == 'salaried':
            self.employees.append(Salaried(name, address, attr, self.count))
        elif type == 'commissioned':
            self.employees.append(Commissioned(name, address, attr, self.current_date, self.count))
        elif type == 'hourly':
            self.employees.append(Hourly(name, address, attr, self.count))
        
        self.employees[-1].generate_schedule_paymethod(self.current_date, self.calendar)
        self.employees[-1].payment_method = employee_paymethod('deposit in bank account')

        self.count += 1

    def search_employee(self, id: int):
        return next(x for x in self.employees if x.id == id)

    def search_employee_index(self, id: int):
        return next((i, x) for i, x in enumerate(self.employees) if x.id == id)

    def search_get_id_by_name(self, name: str):
        return next(x.id for x in self.employees if x.name == name)

    def del_employee(self, id: int):
        index, _ = self.search_employee_index(id)
        self.employees[index].delete(self.calendar)
        del self.employees[index]

    def launch_timecard(self, id: int, hours: int):
        employee = self.search_employee(id)
        employee.add_hourwage(hours)

    def launch_sell_result(self, id: int, price: int, date = current_date):
        if date == 'current':
            date = self.current_date
        employee = self.search_employee(id)
        if employee.type != 'Commissioned':
            raise Exception('Incorrect employee type')
        self.calendar[hash_date(date)]['update'].append(('selling', employee.id, price))

    # charge must be a whole value, not a percentage of wage
    def launch_service_charge(self, id: int, charge: int):
        employee = self.search_employee(id)
        assert employee.syndicate == True
        employee.owing(charge)

    def print_calendar(self):
        print('---------------- calendar ------------------')
        for key in self.calendar:
            if self.calendar[key] != {'schedule':[], 'update':[]}:
                print(str(key) + ':', self.calendar[key])

    def change_employee_data(self, id: int, name: str = 0, address: str = 0, payment_method: str = 0, syndicate: bool = 0, syndicate_id: int = 0, syndicate_charge: int = 0):
        employee = self.search_employee(id)
        if name:
            employee.name = name
        if address:
            employee.address = address
        if payment_method:
            employee.payment_method = employee_paymethod(payment_method)
        
        employee.syndicate = syndicate

        if syndicate_id:
            employee.syndicate_id = syndicate_id
        if syndicate_charge:
            employee.syndicate_charge = syndicate_charge
    
    def get_employee_wage(self, employee: Employee):
        if employee.type.lower() == 'salaried':
            return employee.monthly_wage
        elif employee.type.lower() == 'commissioned':
            return employee.base_salary
        elif employee.type.lower() == 'hourly':
            return employee.hourly_wage * 28

    def change_employee_type(self, id, type):
        type_arr = ['salaried', 'commissioned', 'hourly']

        assert type.lower() in type_arr

        index, employee = self.search_employee_index(id)
        name = employee.name
        address = employee.address
        wage = self.get_employee_wage(employee)
        special, _, _ = get_schedule_params(employee.payment_schedule)
        employee.delete(self.calendar)

        if type.lower() == 'salaried':
            self.employees[index] = Salaried(name, address, wage, id)
        elif type.lower() == 'commissioned':
            self.employees[index] = Commissioned(name, address, wage, self.current_date, id)
        elif type.lower() == 'hourly':
            self.employees[index] = Hourly(name, address, wage, id)
        
        if not special:
            self.employees[index].payment_schedule = employee.payment_schedule
        
        self.employees[index].syndicate = employee.syndicate
        self.employees[index].syndicate_charge = employee.syndicate_charge
        self.employees[index].syndicate_id = employee.syndicate_id
        self.employees[index].generate_schedule_paymethod(self.current_date, self.calendar)
        self.employees[index].payment_method = employee_paymethod('deposit in bank account')

    def change_payment_schedule(self, id, new_schedule):
        get_schedule_params(new_schedule)

        employee = self.search_employee(id)
        employee.payment_schedule = new_schedule