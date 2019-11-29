import numpy as np
import pandas as pd
#from pandas import ExcelFile
#install xlrd ???

#Подгружаем эксельку
xls = pd.ExcelFile('C://WebProjects/Bank_Game.xlsx')

#Аналоги фишек
employees_chips = [0 for i in range(5)]
communications_chips = [0 for i in range(5)]
cash_loans_chips = [0 for i in range(5)]
deposits_chips = [0 for i in range(5)]
mortgages_chips = [0 for i in range(5)]

mortgage_development = [0 for i in range(5)] #Этапы развития ипотеки

list_of_players = [i for i in range(5)] #пронумерованные игроки

duration = xls.parse('Duration').duration[0] #длительность игры
q = 1 #нумерация кварталов: шаг игры

capital = [xls.parse('Capital').capital[0] for i in range(5)] #собственный капитал

cities = xls.parse('Cities', usecols = range(5)) #всё про города

city_owner = [ pd.DataFrame({
                'city': [],
                'employees': [],
                'cash_loans': [],
                'deposits': [],
                'mortgages': [],
                'activation': [],
                'mortgage_activation': [],
                'cash_loans_sum': [],
                'deposits_sum': [],
                'mortgages_sum': [],
                'rate_of_cash_loan': [],
                'rate_of_deposit': [],
                'rate_of_mortgage': [],
                'population': []
                }) for i in range(5) ]

def empty_table(duration):
    return pd.DataFrame({
            '0': [float(0) for i in range(duration)],
            '1': [float(0) for i in range(duration)],
            '2': [float(0) for i in range(duration)],
            '3': [float(0) for i in range(duration)],
            '4': [float(0) for i in range(duration)]
                })

interest_income = empty_table(duration)
non_interest_income = empty_table(duration)
income = empty_table(duration)

interest_expense = empty_table(duration)
non_interest_expense = empty_table(duration)
expense = empty_table(duration)

gross_profit = empty_table(duration)
net_profit = empty_table(int(duration / 4))

deposits = empty_table(duration)
mortgages = empty_table(duration)
cash_loans = empty_table(duration)
credits = empty_table(duration) #mortgages + cash_loans

cost_of_marketing = empty_table(duration)
cost_of_branchopening = empty_table(duration)
cost_of_mortgage_part = empty_table(duration)

cost_of_employees_chips = empty_table(duration)
cost_of_communications_chips = empty_table(duration)
cost_of_cash_loans_chips = empty_table(duration)
cost_of_deposits_chips = empty_table(duration)
cost_of_mortgages_chips = empty_table(duration)
cost_of_products_chips = empty_table(duration) #cost_of_cash_loans_chips + cost_of_deposits_chips + cost_of_mortgages_chips

creditsofCB = [0 for i in range(5)]
creditsofCB_change = [0 for i in range(5)]
creditsofCB_payments = empty_table(duration)
creditsofCB_remains = empty_table(duration)
maximum_index = 5
populations = [0 for i in range(5)]

#Цены и базовые ставки
cost_employee = xls.parse('Cost').employee[0]
cost_communication = xls.parse('Cost').communication[0]
cost_cash_loan = xls.parse('Cost').cash_loan[0]
cost_deposit = xls.parse('Cost').deposit[0]
cost_mortgage = xls.parse('Cost').mortgage[0]
cost_mortgage_part = xls.parse('Cost').mortgage_part[0]
cost_branchopening = xls.parse('Cost').branchopening[0]

rate_cash_loan = xls.parse('Rate').cash_loan
rate_deposit = xls.parse('Rate').deposit
rate_mortgage = xls.parse('Rate').mortgage
rate_creditofCB = xls.parse('Rate').creditofCB
rate_creditpreferentialofCB = xls.parse('Rate').creditpreferentialofCB
rate_profit_tax = xls.parse('Rate').profit_tax

deposit_discount = [xls.parse('Deposit_discount')[i][0] for i in range(1, 6)]

#Плюшки для банка с наибольшей численностью
bonus_for_deposit = [float(0) for i in range(5)]
max_index = 5

#Допфункция, которая будет использоваться далее
def nested_function(variable, variable_name, k, i):
    while variable[i] > 0:
        if city_owner[i].empty or city_owner[i][city_owner[i][variable_name] != k].empty:
            break
        else:
            if str(input(str(colored_banks.color[i]) + ", хотите расставить фишки {}? (1-Да; 0-нет): ".format(variable_name))) == "1":
                choice = str(input("Город: "))
                while choice not in city_owner[i][city_owner[i][variable_name] < k].city.values:
                    choice = str(input("Ошибка! Ещё раз, куда поставить фишки: "))
                index = city_owner[i].loc[city_owner[i].city == choice].index[0]
                number = int(input('Сколько поставить? : '))
                while city_owner[i][variable_name][index] + number > k or number not in range(1, variable[i] + 1):
                    number = int(input("Ошибка! Ещё раз, сколько? : "))
                city_owner[i][variable_name][index] += number
                variable[i] -= number
            else:
                break
    print("На этом всё с фишками " + str(variable_name))

#Функции для каждого из возможных действий
def employment(i):
    n = int(input(str(colored_banks.color[i]) + ", количество фишек сотрудников: "))
    while n not in range(4) or capital[i] <= n*cost_employee:
        n = int(input("Ошибка! ещё раз: "))

    cost_of_employees_chips[str(i)][q-1] += n*cost_employee
    capital[i] -= n*cost_employee
    employees_chips[i] += n

    nested_function(employees_chips, 'employees', 3, i)

    print(str(colored_banks.color[i]) + ", ваш ход завершён")

def communication_work(i):
    n = int(input(str(colored_banks.color[i]) + ", количество фишек коммуникаций: "))
    while n not in [0, 2, 4] or capital[i] <= n*cost_communication:
        n = int(input("Ошибка! ещё раз: "))

    cost_of_communications_chips[str(i)][q-1] += n*cost_communication
    capital[i] -= n*cost_communication
    communications_chips[i] += n

    while communications_chips[i] > 0:
        break

    print(str(colored_banks.color[i]) + ", ваш ход завершён")
#Здесь нужно карта, или хотя бы количество необходимых коммуникаций между городами

def product_launch(i):
    print(str(colored_banks.color[i]))
    if mortgage_development == 3:
        cash_loan = int(input("Количество фишек кредитов наличными: "))
        deposit = int(input("Количество фишек депозитов: "))
        mortgage = int(input("Количество фишек ипотеки: "))
        while cash_loan not in range(4) or deposit not in range(4) or mortgage not in range(4) or cash_loan + deposit + mortgage > 3 or capital[i] <= cash_loan*cost_cash_loan + deposit*cost_deposit + mortgage*cost_mortgage:
            cash_loan = int(input("Ошибка! ещё раз, количество фишек кредитов наличными: "))
            deposit = int(input("Ошибка! ещё раз, количество фишек депозитов: "))
            mortgage = int(input("Ошибка! ещё раз, количество фишек ипотеки: "))
    else:
        cash_loan = int(input("Количество фишек кредитов наличными: "))
        deposit = int(input("Количество фишек депозитов: "))
        mortgage = 0
        while cash_loan not in range(4) or deposit not in range(4) or cash_loan + deposit > 3 or capital[i] <= cash_loan*cost_cash_loan + deposit*cost_deposit:
            cash_loan = int(input("Ошибка! ещё раз, количество фишек кредитов наличными: "))
            deposit = int(input("Ошибка! ещё раз, количество фишек депозитов: "))

    capital[i] -= cash_loan*cost_cash_loan + deposit*cost_deposit + mortgage*cost_mortgage
    cost_of_cash_loans_chips[str(i)][q-1] = cash_loan*cost_cash_loan
    cost_of_mortgages_chips[str(i)][q-1] = mortgage*cost_mortgage
    cost_of_deposits_chips[str(i)][q-1] = deposit*cost_deposit

    cash_loans_chips[i] += cash_loan
    deposits_chips[i] += deposit
    mortgages_chips[i] += mortgage

    nested_function(cash_loans_chips, 'cash_loans', 1, i)
    nested_function(deposits_chips, 'deposits', 1, i)
    nested_function(mortgages_chips, 'mortgages', 1, i)

    print(str(colored_banks.color[i]) + ", ваш ход завершён")

def branch_open_and_mortgage_create(i):
    if mortgage_development[i] < 3:
        branch = int(input(str(colored_banks.color[i]) + ", сколько филиалов хотите открыть? : "))
        mortgage_part = int(input("Будете разрабатывать ипотеку? (1-Да; 0-нет): "))
        while [branch, mortgage_part] not in [ [2, 0], [1, 1], [1, 0], [0, 1], [0, 0] ] or capital[i] <= branch*cost_branchopening + mortgage_part*cost_mortgage_part:
            branch = int(input("Ошибка! ещё раз, сколько филиалов хотите открыть: "))
            mortgage_part = int(input("Ошибка! ещё раз, будете разрабатывать ипотеку? (1-Да; 0-нет): "))
    else:
        branch = int(input(str(colored_banks.color[i]) + ", сколько филиалов хотите открыть? : "))
        mortgage_part = 0
        while branch not in [0, 1, 2] or capital[i] <= branch*cost_branchopening + mortgage_part*cost_mortgage_part:
            branch = int(input("Ошибка! ещё раз, сколько филиалов хотите открыть: "))

    capital[i] -= branch*cost_branchopening + mortgage_part*cost_mortgage_part
    cost_of_mortgage_part[str(i)][q-1] += mortgage_part*cost_mortgage_part
    cost_of_branchopening[str(i)][q-1] += branch*cost_branchopening

    mortgage_development[i] += mortgage_part

    while branch > 0:
        global cities
        choice = str(input("В каком городе открываем филиал? : "))
        while choice not in cities.city.values:
            choice = str(input("Ошибка с названием города, напишите ещё раз: "))
        index = cities.loc[cities.city == choice].index[0]
        city_owner[i].loc[city_owner[i].shape[0]] = [cities.city[index], 0, 0, 0, 0, 0, 0, cities.cash_loan[index], cities.deposit[index], cities.mortgage[index], rate_cash_loan[q-1], rate_deposit[q-1] - deposit_discount[i], rate_mortgage[q-1], cities.population[index]]
        capital[i] += cities.deposit[index] - cities.cash_loan[index]
        cities = cities.drop(index)
        branch -= 1

    print(str(colored_banks.color[i]) + ", ваш ход завершён")

def open_office(i):
    nested_function(employees_chips, 'employees', 3, i)
    nested_function(cash_loans_chips, 'cash_loans', 1, i)
    nested_function(deposits_chips, 'deposits', 1, i)
    nested_function(mortgages_chips, 'mortgages', 1, i)

    print(str(colored_banks.color[i]) + ", ваш ход завершён")

    for index in range(city_owner[i].shape[0]):
        if city_owner[i].employees[index] >= 2 and city_owner[i].cash_loans[index] + city_owner[i].deposits[index] == 2:
            city_owner[i].activation[index] = 1
        else:
            pass
        if city_owner[i].employees[index] + city_owner[i].mortgages[index] == 4:
            city_owner[i].mortgage_activation[index] = 1
        else:
            pass

def get_profit(i):
    deposits[str(i)][q-1] = (city_owner[i].activation * city_owner[i].deposits_sum * (city_owner[i].rate_of_deposit - bonus_for_deposit[i])).sum() / 4
    cash_loans[str(i)][q-1] = (city_owner[i].activation * city_owner[i].cash_loans_sum * city_owner[i].rate_of_cash_loan).sum() / 4
    if city_owner[i].shape[0] == city_owner[i].mortgage_activation.sum():
        mortgages[str(i)][q-1] = (city_owner[i].mortgages_sum * city_owner[i].rate_of_mortgage).sum() / 4
    else:
        pass
    credits[str(i)][q-1] = cash_loans[str(i)][q-1] + mortgages[str(i)][q-1]

    cost_of_products_chips[str(i)][q-1] = cost_of_cash_loans_chips[str(i)][q-1] + cost_of_mortgages_chips[str(i)][q-1] + cost_of_deposits_chips[str(i)][q-1]

    interest_income[str(i)][q-1] = credits[str(i)][q-1]
    interest_expense[str(i)][q-1] = deposits[str(i)][q-1]

    #non_interest_income[str(i)][q-1] = 0
    non_interest_expense[str(i)][q-1] = cost_of_products_chips[str(i)][q-1] + cost_of_employees_chips[str(i)][q-1] + cost_of_mortgage_part[str(i)][q-1] + cost_of_communications_chips[str(i)][q-1] + cost_of_marketing[str(i)][q-1] + cost_of_branchopening[str(i)][q-1]

    capital[i] += interest_income[str(i)][q-1] - interest_expense[str(i)][q-1]

    income[str(i)][q-1] = interest_income[str(i)][q-1] + non_interest_income[str(i)][q-1]
    expense[str(i)][q-1] = interest_expense[str(i)][q-1] + non_interest_expense[str(i)][q-1]

    gross_profit[str(i)][q-1] = income[str(i)][q-1] - expense[str(i)][q-1]

#Активатор действий для игроков:
action_vars = {"Офис": open_office, "Найм": employment, "Коммуникации": communication_work, "Продукты": product_launch, "Проценты": get_profit, "Открытие/разработка": branch_open_and_mortgage_create}
def activation():
    if 5-i != 5:
        a = input(str(colored_banks.color[5-i]) + ", Выберите ход {}: ".format(action_vars.keys()))
        if a not in action_vars.keys():
            a = input("Попробуйте ещё раз: ")
    else:
        a = input(str(colored_banks.color[0]) + ", Выберите ход {}: ".format(action_vars.keys()))
        if a not in action_vars.keys():
            a = input("Попробуйте ещё раз: ")

    for p in range(5-i, 5):
        action_vars[a](p)
    for p in range(0, 5-i):
        action_vars[a](p)
    action_vars.pop(a)

#Проверка на бакронтсво
def check_of_players():
    print("Аудит")
    global list_of_players

    for i in list_of_players:
        net_profit[str(i)][q-1] = gross_profit[str(i)][q-4:q].sum()
        if net_profit[str(i)][q-1] > 0:
            net_profit[str(i)][q-1] = (1-rate_profit_tax)*net_profit[str(i)][q-1]
        else:
            pass

    for i in list_of_players:
        if capital[i] < 0.1 * credits[str(i)][q-1]:
            print(str(colored_banks.color[i]) + ", вы получили штраф!")
            capital[i] -= 3 ######################################################################################################################################
        else:
            pass
        if capital[i] < 0:
            list_of_players = list_of_players.remove(i)
            print(str(colored_banks.color[i]) + ", вы выбываете")
        else:
            print("{}: вы продолжаете играть".format(str(colored_banks.color[i])))

#Кредиты ЦБ
def taking_a_loan(i):
    global creditsofCB
    if creditsofCB[i] > 0:
        print("{}, у вас уже есть кредит.".format(str(colored_banks.color[i])))
        print("Осталось выплатить: " + creditsofCB_remains[str(i)][q])
    else:
        if str(input("{}, хотите взять кредит? (1-Да; 0-нет): ".format(str(colored_banks.color[i])))) == "1":
            creditsofCB[i] = float(input("Выберите сумму кредита: "))
            creditsofCB_change[i] = creditsofCB[i]
            capital[i] += creditsofCB[i]
            print("Договорились")
        else:
            print("Хорошо")

def paying_a_loan(i, rate):
        if creditsofCB[i] > 0:
            creditsofCB_payments[str(i)][q] = creditsofCB[i] * rate / 4
            capital[i] -= creditsofCB_payments[str(i)][q]
            creditsofCB_remains[str(i)][q] = creditsofCB_change[i] - creditsofCB_payments[str(i)][q]
            creditsofCB_change[i] -= creditsofCB_payments[str(i)][q]
        else:
            pass
        if creditsofCB_change[i] == 0:
            creditsofCB[i] = 0
        else:
            pass

def identify_preference():
    populations = [city_owner[i]['population'][:q+1].sum() for i in list_of_players]
    max_index = populations.index(max(populations))
    bonus_for_deposit[max_index] = 0.01

##Игра
print("Начнём игру")
print("---------------------------------------------------------------------------------")
#Рекламный аукцион
colored_banks = pd.DataFrame({"color": ["Зелёный банк", "Жёлтый банк", "Красный банк", "Синий банк", "Чёрный банк"], "ads_sum": [0, 0, 0, 0, 0]})

for i in list_of_players:
    colored_banks.ads_sum[i] = float(input(colored_banks.color[i] + ", траты на рекламу: "))
    while colored_banks.ads_sum[i] > xls.parse('Capital').capital[0]:
        colored_banks.ads_sum[i] = float(input(colored_banks.color[i] + ", попробуйте ещё раз: "))

colored_banks = colored_banks.sort_values(by = ['ads_sum'], ascending = False)
colored_banks = colored_banks.reset_index().drop("index", axis = 1)

print("---------------------------------------------------------------------------------")
for i in list_of_players:
    capital[i] -= colored_banks.ads_sum[i]
    print(str(colored_banks.color[i]) + ", ваш остаток: " + str(capital[i]))

#Само действие игры
while q <= duration:
    print("")
    print("---------------------------------------------------------------------------------")
    print("---------------------------------------------------------------------------------")

    action_vars = {"Офис": open_office, "Найм": employment, "Коммуникации": communication_work, "Продукты": product_launch, "Проценты": get_profit, "Открытие/разработка": branch_open_and_mortgage_create}

    print(str(q // 4 + 1) + "-й год, " + str(q) + "-й квартал")
    print("--------------------")
    if q % 4 == 1:
        identify_preference()
    else:
        pass

    for i in list_of_players:
        if i != max_index:
            paying_a_loan(i, rate_creditofCB)
        else:
            paying_a_loan(i, rate_creditpreferentialofCB)
        taking_a_loan(i)
    print("---------------------------------------------------------------------------------")

    for i in list_of_players:
        print("---------------------------------------------------------------------------------")
        activation()
    print("---------------------------------------------------------------------------------")
    print("")

    print("--------------------------------------Итоги--------------------------------------")
    print(str(q // 4 + 1) + "-й год, " + str(q) + "-й квартал")
    print("--------------------")
    print("Фишки:")
    print("Работники про запас")
    print(employees_chips)
    print("Коммуникации про запас")
    print(communications_chips)
    print("Депозиты про запас")
    print(deposits_chips)
    print("Кредиты наличными про запас")
    print(cash_loans_chips)
    print("Ипотеки про запас")
    print(mortgages_chips)
    print("Этапы разработки ипотеки")
    print(mortgage_development)
    print("---------------------------------------------------------------------------------")

    for i in list_of_players:
        print(colored_banks.color[i])
        print("Оставшийся капитал")
        print(capital[i])
        print("Занятые города")
        print(city_owner[i])
        print("Кредиты наличными")
        print(cash_loans[str(i)][0:q])
        print("Ипотеки")
        print(mortgages[str(i)][0:q])
        print("Кредиты")
        print(credits[str(i)][0:q])
        print("Депозиты")
        print(deposits[str(i)][0:q])
        print("Общий доход")
        print(income[str(i)][0:q])
        print("Общий расход")
        print(expense[str(i)][0:q])
        print("Брутто прибыль")
        print(gross_profit[str(i)][0:q])
        print("---------------------------------------------------------------------------------")

    if q % 4 == 0:
        check_of_players()
        print("Чистая прибыль")
        print(net_profit)
    else:
        pass

    q += 1

print("Тестирование окончено")
