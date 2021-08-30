# Projeto de P2 (programação orientada à objeto) - refatoração

O objetivo do trabalho é refatorar o [projeto inicial] de projeto da disciplina de projeto de software com o assunto dado de **Code Smells** e de **Design Patterns**, para então fazer um código limpo, com este repositório.

[projeto inicial]: <https://github.com/ghastcmd/projeto-p2>

# Os Code Smells encontrados no código

- **Duplicate Code**
  - Código duplicado na classe **Payroll** na função `add_employee` e `change_employee_type`.

- **Long Line Code** 
  - Linha de código longo na classe **Employee** na função `__str__`.

- **Primitive Obsession**
  - A variável **calendar** na classe **PayrollSystem**.

- **Long Method**
  - Na classe **PayrollSystem** na função `change_employee_data`.

- **Especulative Generality**
  - No módulo *payroll* na função `employee_paymethod`.

# Os novos design patterns aplicados no sistema

- **Command design pattern**
  - No módulo *payroll* na função `get_employee_wage`, foi adicionado o novo design pattern.

- **Extract Method**
  - No módulo *payroll* na função `change_employee_type` e `add_employee` havia código duplicado, sanado com uma nova função.

- **Extract Class**
  - Aplicado no módulo *employee* nas classes `Salaried, Commissioned e Hourly`, para que dois campos paramétricos fossem para a inicialização da super classe.