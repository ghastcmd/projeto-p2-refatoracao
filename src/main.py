from queue import QueueSystem

# Link do github: https://github.com/ghastcmd/projeto-p2

def list_commands():
    print('Adicionar um empregado:')
    print('  add <nome> <endereço> <tipo> <parametro>\n')

    print('Listar os empregados:')
    print('  list\n')

    print('Procurar o id do empragdo por nome:')
    print('  search <nome do empregado>\n')
    
    print('Remover um empregado:')
    print('  del <id do empregado>\n')

    print('Lançar um cartão de ponto:')
    print('  launch timecard <id do empregado> <horas trabalhadas>\n')

    print('Lançar uma taxa de serviço')
    print('  launch service charge <id do emprgado> <taxa>\n')

    print('Lançar um resultado de venda:')
    print('  launch sell result <id do empregado> <resultado de venda> <data da venda>')
    print('  Para lançar uma venda na data atual coloque a data como "current"\n')

    print('Mudar os dados do empregado:')
    print('  change employee data <id do empregado> <dado a mudar> <novo valor>')
    print('  Os dados que podem ser modificados são:\n  name, address, payment_method, syndicate, syndicate_id, syndicate_charge\n')

    print('Mudar o tipo do empregado:')
    print('  change employee type <id do empregado> <novo tipo>\n')

    print('Mudar a agenda de pagamento do empreagdo:')
    print('  change payment schedule <id do empregado> <nova agenda>\n')

    print('Rodar as folhas de pagamento para hoje:')
    print('  run payroll\n')

    print('Desfazer a última alteração:')
    print('  undo\n')

    print('Refazer a última alteração:')
    print('  redo\n')

    print('Para sair do programa:\n  exit\n')

def invalid_command():
    print('Invalid command, type help for usage')

def invalid_employee_type():
    print('Invalid employee type')
    print('  Available types: salaried, hourly, commissioned')

def unify_string(first, last, arr):
    ret_str = ''
    for i in range(first, last):
        ret_str += arr[i] + ' '
    return ret_str.strip()

if __name__ == '__main__':
    system = QueueSystem()

    print('Bem vindos ao sistema de folha de pagamento')
    print('Para obter ajuda, digite o comando help')

    types = ['salaried', 'hourly', 'commissioned']

    while True:
        uin = input('> ')
        uin = uin.strip().split(' ')
        uinl = len(uin)
        
        if uinl == 1 and uin[0] == 'exit':
            break
        elif uinl == 1 and uin[0] == 'help':
            list_commands()
        elif uinl == 1 and uin[0] == 'list':
            system.print_payroll()
        elif uinl == 1 and uin[0] == 'undo':
            system.undo()
        elif uinl == 1 and uin[0] == 'redo':
            system.redo()
        elif uinl == 1 and uin[0] == 'calendar':
            system.print_payroll_calendar()
        elif uinl == 2 and uin[0] == 'search':
            print(system.search_by_name(uin[1]))
        elif uinl >= 5 and uin[0] == 'add':
            new_str = unify_string(2, uinl - 2, uin)
            type = uin[-2].lower()
            if type not in types:
                invalid_employee_type()
                continue
            system.add_employee(uin[1], new_str, type, int(uin[-1]))
        elif uinl == 2 and uin[0] == 'del':
            system.del_employee(int(uin[1]))
        elif uinl == 2 and unify_string(0, 2, uin) == 'run payroll':
            system.run_today_payroll()
        elif uinl == 4 and unify_string(0, 2, uin) == 'launch timecard':
            system.launch_timecard(int(uin[2]), int(uin[3]))
        elif uinl == 5 and unify_string(0, 3, uin) == 'launch service charge':
            system.launch_service_charge(int(uin[3]), int(uin[4]))
        elif uinl == 6 and unify_string(0, 3, uin) == 'launch sell result':
            system.launch_selling(int(uin[3]), int(uin[4]), uin[5])
        elif uinl >= 6 and unify_string(0, 3, uin) == 'change employee data':
            system.change_employee_data(int(uin[3]), {uin[4]: unify_string(5, uinl, uin)})
        elif uinl == 5 and unify_string(0, 3, uin) == 'change employee type':
            type = uin[4].lower()
            if type not in types:
                invalid_employee_type()
                continue
            system.change_employee_type(int(uin[3]), type)
        elif uinl >= 4 and unify_string(0, 3, uin) == 'change payment schedule':
            system.change_payment_schedule(int(uin[3]), unify_string(4, uinl, uin))
        else:
            invalid_command()
    
    exit()
    system.add_employee('simple', 'via st. 11', 'salaried', 1230)
    system.add_employee('alelo', 'maritona st. 19', 'hourly', 12)
    system.add_employee('another', 'via st. 12', 'salaried', 1240)
    system.add_employee('Geredos', 'maritnoa elwoe st. 1', 'commissioned', 13)
    system.add_employee('alelo', 'maritona st. 19', 'hourly', 12)

    system.del_employee(2)
    system.launch_timecard(5, 9)

    system.run_today_payroll()

    simple_id = system.search_by_name('simple')

    system.launch_timecard(5, 8)
    system.change_employee_data(simple_id, {'syndicate': True, 'syndicate_charge': 100, 'syndicate_id': 2})
    system.launch_service_charge(1, 100)

    system.launch_selling(4, 2000, 'current')
    system.launch_selling(4, 1200, 'current')
    system.launch_selling(4, 1200, 'current')

    for _ in range(2):
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