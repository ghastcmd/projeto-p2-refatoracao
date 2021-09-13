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

class WageCommand:
    def __init__(self, employee: Employee):
        self.employee = employee
    
    def run(self):
        raise NotImplemented()

class WageSalariedCommand(WageCommand):
    def run(self):
        return self.employee.monthly_wage

class WageCommissionedCommand(WageCommand):
    def run(self):
        return self.employee.base_salary

class WageHourlyCommand(WageCommand):
    def run(self):
        return self.employee.hourly_wage * 28



class ChangeDataCommand:
    def __init__(self, employee: Employee):
        self.employee = employee
    
    def run(self):
        raise NotImplemented()

class ChangeDataName(ChangeDataCommand):
    def run(self, name:str):
        self.employee.name = name

class ChangeDataAddress(ChangeDataCommand):
    def run(self, address:str):
        self.employee.address = address

class ChangeDataPaymethod(ChangeDataCommand):
    def run(self, paymethod:str):
        self.employee.payment_method = employee_paymethod(paymethod)

class ChangeDataSyndicate(ChangeDataCommand):
    def run(self, syndicate:bool):
        self.employee.syndicate = bool(syndicate)

class ChangeDataSyndicateId(ChangeDataCommand):
    def run(self, syndicate_id:int):
        self.employee.syndicate_id = int(syndicate_id)

class ChangeDataSyndicateCharge(ChangeDataCommand):
    def run(self, syndicate_charge:int):
        self.employee.syndicate_charge = int(syndicate_charge)

def change_data_get_object(name: str):
    dict = {
        'name': ChangeDataName,
        'address': ChangeDataAddress,
        'payment_method': ChangeDataPaymethod,
        'syndicate': ChangeDataSyndicate,
        'syndicate_id': ChangeDataSyndicateId,
        'syndicate_charge': ChangeDataSyndicateCharge,
    }

    return dict[name]


def invalid_employee_id():
    print('Invalid employee id, use list to see employee or search <name>')

class PayrollSystem:
    current_date = datetime.date.today()

    def __init__(self):
        self.count = 1
        self.employees = []
        self.calendar = PCalendar()

        self.current_day = self.calendar.get_day(self.current_date)

    def run_today_payroll(self):
        iter_thru = [(i,x) for i, x in enumerate(self.calendar.get_day(self.current_date)['schedule'])]
        for i, id in reversed(iter_thru):
            employee = self.search_employee(id)
            employee.generate_payment(self.current_date, self.calendar)
            del self.calendar.get_day(self.current_date)['schedule'][i]

    def update_day(self, add_days = 1):
        self.current_date += datetime.timedelta(days=add_days)
        self.current_day = self.calendar.get_day(self.current_date)

    def print_vals(self):
        print('------------ list of employees -------------')
        for i, employee in enumerate(self.employees):
            print(f'{i}: {employee}')

    def create_employee(self, type, name, address, attr, id, date):
        types_to_obj = {
            'salaried': Salaried, 
            'commissioned': Commissioned, 
            'hourly': Hourly
        }

        return types_to_obj[type](name, address, attr, id, date)

    def add_employee(self, name: str, address: str, type: str, attr: int):
        types = ['salaried', 'commissioned', 'hourly']
        assert type in types

        new_employee = self.create_employee(type, name, address, attr, self.count, self.current_date)
        self.employees.append(new_employee)

        self.employees[-1].generate_schedule_paymethod(self.current_date, self.calendar)
        self.employees[-1].payment_method = employee_paymethod('deposit in bank account')

        self.count += 1

    def search_employee(self, id: int):
        try:
            employee = next(x for x in self.employees if x.id == id)
        except:
            invalid_employee_id()
            employee = None
        return employee

    def search_employee_index(self, id: int):
        index = 0
        try:
            index, employee = next((i, x) for i, x in enumerate(self.employees) if x.id == id)
        except:
            invalid_employee_id()
            employee = None
        return index, employee

    def search_get_id_by_name(self, name: str):
        try:
            employee = next(x.id for x in self.employees if x.name == name)
        except:
            print('Invalid employee name')
            employee = None
        return employee

    def del_employee(self, id: int):
        index, employee = self.search_employee_index(id)
        if employee == None:
            return
        self.employees[index].delete(self.calendar)
        del self.employees[index]

    def launch_timecard(self, id: int, hours: int):
        employee = self.search_employee(id)
        if employee == None:
            return
        if employee.type != 'Hourly':
            print('Need to be a hourly type of employee')
            return
        employee.add_hourwage(hours)

    def launch_sell_result(self, id: int, price: int, date = current_date):
        if date == 'current':
            date = self.current_date
        else:
            date = datetime.datetime.strptime(date, '%d/%m/%Y')

        employee = self.search_employee(id)
        if employee == None:
            return
        if employee.type != 'Commissioned':
            print('Need to be a commissioned type of employee')
            return

        self.calendar.get_day(date)['update'].append(('selling', employee.id, price))

    # charge must be a whole value, not a percentage of wage
    def launch_service_charge(self, id: int, charge: int):
        employee = self.search_employee(id)
        if employee == None:
            return
        if employee.syndicate != True:
            print('The employee need to be in the syndicate')
            return

        employee.owing(charge)

    def print_calendar(self):
        self.calendar.print()

    def change_employee_data(self, id: int, change_names: str):
        employee = self.search_employee(id)
        if employee == None:
            return
        
        parsed_changes = change_names.split(' ')
        
        change_data_command = change_data_get_object(parsed_changes[0])(employee)
        change_data_command.run(change_names[len(parsed_changes[0]) + 1:])

    def get_employee_wage(self, employee: Employee):
        obj_dict = {
            'salaried': WageSalariedCommand,
            'commissioned': WageCommissionedCommand,
            'hourly': WageHourlyCommand
        }
        
        get_wage = obj_dict[employee.type.lower()](employee)
        return get_wage.run()

    def change_employee_type(self, id, type):
        type_arr = ['salaried', 'commissioned', 'hourly']

        assert type.lower() in type_arr

        index, employee = self.search_employee_index(id)
        if employee == None:
            return
        
        name = employee.name
        address = employee.address
        wage = self.get_employee_wage(employee)
        special, _, _ = PCalendar.parse_schedule_params(employee.payment_schedule)
        employee.delete(self.calendar)

        new_employee = self.create_employee(type.lower(), name, address, wage, id, self.current_date)
        self.employees[index] = new_employee

        if not special:
            self.employees[index].payment_schedule = employee.payment_schedule
        
        self.employees[index].syndicate = employee.syndicate
        self.employees[index].syndicate_charge = employee.syndicate_charge
        self.employees[index].syndicate_id = employee.syndicate_id
        self.employees[index].generate_schedule_paymethod(self.current_date, self.calendar)
        self.employees[index].payment_method = employee_paymethod('deposit in bank account')

    def change_payment_schedule(self, id, new_schedule):
        PCalendar.parse_schedule_params(new_schedule)

        employee = self.search_employee(id)
        if employee == None:
            return
        
        employee.payment_schedule = new_schedule