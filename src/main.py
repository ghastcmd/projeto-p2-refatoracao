from queue import QueueSystem

# Link do github: https://github.com/ghastcmd/projeto-p2

if __name__ == '__main__':
    system = QueueSystem()

    system.add_employee('simple', 'via st. 11', 'salaried', 1230)
    system.add_employee('alelo', 'maritona st. 19', 'hourly', 12)
    system.add_employee('another', 'via st. 12', 'salaried', 1240)
    system.add_employee('Geredos', 'maritnoa elwoe st. 1', 'commissioned', 13)
    system.add_employee('alelo', 'maritona st. 19', 'hourly', 12)

    system.del_employee(2)
    system.launch_timecard(5, 9)

    system.update_day()

    simple_id = system.search_by_name('simple')

    system.launch_timecard(5, 8)
    system.change_employee_data(simple_id, {'syndicate': True, 'syndicate_charge': 100, 'syndicate_id': 2})
    system.launch_service_charge(1, 100)

    system.launch_selling(4, 2000, 'current')
    system.launch_selling(4, 1200, 'current')
    system.launch_selling(4, 1200, 'current')

    for _ in range(2):
        system.update_day()
        system.run_today_payroll()

    # system.print()

    system.add_employee('zinael', 'via str. 1', 'commissioned', 12)
    system.undo()
    system.undo()
    system.redo()

    system.change_employee_data(3, {'name': 'Ramon', 'syndicate': True, 'syndicate_charge': 100, 'syndicate_id': 1})

    system.print_payroll_calendar()
    system.print_payroll()
    system.change_employee_type(3, 'commissioned')
    system.change_payment_schedule(3, 'weekly 1 friday')
    system.print_payroll()
    # system.last_payroll().employees[]