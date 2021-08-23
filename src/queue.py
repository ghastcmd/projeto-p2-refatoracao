from payroll import PayrollSystem
import copy

class QueueSystem:
    def __init__(self):
        payroll = PayrollSystem()
        self.state_save = [payroll]
        self.states_index = [0]
        self.current_index = 1

    def update_get_payroll(self):
        self.overwrite_undo()
        self.current_index += 1
        return copy.deepcopy(self.state_save[-1])

    def add_employee(self, name, address, type, parameter):
        payroll = self.update_get_payroll()
        payroll.add_employee(name, address, type, parameter)
        self.state_save.append(payroll)

    def del_employee(self, id):
        payroll = self.update_get_payroll()
        payroll.del_employee(id)
        self.state_save.append(payroll)
    
    def launch_timecard(self, id, hours):
        payroll = self.update_get_payroll()
        payroll.launch_timecard(id, hours)
        self.state_save.append(payroll)
    
    def launch_selling(self, id, price, date):
        payroll = self.update_get_payroll()
        payroll.launch_sell_result(id, price, date)
        self.state_save.append(payroll)
    
    def launch_service_charge(self, id, charge):
        payroll = self.update_get_payroll()
        payroll.launch_service_charge(id, charge)
        self.state_save.append(payroll)
    
    def change_employee_data(self, id, data: dict):
        payroll = self.update_get_payroll()
        payroll.change_employee_data(id, **data)
        self.state_save.append(payroll)
    
    def change_employee_type(self, id, type):
        payroll = self.update_get_payroll()
        payroll.change_employee_type(id, type)
        self.state_save.append(payroll)

    def run_today_payroll(self):
        payroll = self.update_get_payroll()
        payroll.run_today_payroll()
        self.state_save.append(payroll)

    def update_day(self):
        payroll = self.update_get_payroll()
        payroll.update_day()
        self.state_save.append(payroll)

    def change_payment_schedule(self, id, new_schedule):
        payroll = self.update_get_payroll()
        payroll.change_payment_schedule(id, new_schedule)
        self.state_save.append(payroll)

    def last_payroll(self):
        return self.state_save[self.current_index - 1]

    def print_payroll(self):
        self.last_payroll().print_vals()

    def print_payroll_calendar(self):
        self.last_payroll().print_calendar()

    def search_by_name(self, name: str):
        return self.last_payroll().search_get_id_by_name(name)
    
    def overwrite_undo(self):
        if self.current_index != len(self.state_save):
            inter_arr = [i for i, _ in enumerate(self.state_save[self.current_index:len(self.state_save)])]
            for x in reversed(inter_arr):
                del self.state_save[self.current_index + x]
    
    def undo(self):
        if self.current_index == 1:
            return
        
        self.current_index -= 1


    def redo(self):
        if self.current_index == len(self.state_save):
            return

        self.current_index += 1

if __name__ == '__main__':
    payroll = PayrollSystem()

    payroll.add_employee('simple', 'via st. 11', 'salaried', 1230)
    payroll.add_employee('alelo', 'maritona st. 19', 'hourly', 12)
    payroll.add_employee('another', 'via st. 12', 'salaried', 1240)
    payroll.add_employee('Geredos', 'maritnoa elwoe st. 1', 'commissioned', 13)
    payroll.add_employee('alelo', 'maritona st. 19', 'hourly', 12)

    payroll.print_vals()

    payroll.del_employee(2)

    payroll.print_vals()

    payroll.launch_timecard(5, 9)
    # payroll.launch_sell_result(1, 1200, date_offset=1)
    payroll.update_day()
    payroll.launch_timecard(5, 8)
    payroll.launch_service_charge(1, 100)
    payroll.print_calendar()

    # payroll.change_employee_data(3, name='simple_name', syndicate=True, type='Salaried', payment_method='weekly')
    payroll.print_vals()

    payroll.launch_sell_result(4, 2000, 'current')
    payroll.launch_sell_result(4, 1200, 'current')
    payroll.launch_sell_result(4, 1200, 'current')

    payroll.print_calendar()

    from employee import hash_date

    for _ in range(30):
        payroll.update_day()
        payroll.run_today_payroll()
        print('current_day:', hash_date(payroll.current_date))
        payroll.print_calendar()
