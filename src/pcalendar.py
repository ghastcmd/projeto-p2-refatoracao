import datetime
import calendar

class PCalendar:
    def __init__(self):
        self.c_calendar = {}
        for i in range(366):
            self.c_calendar[i] = {'schedule': [], 'update': []}

    def get_day(self, date: datetime.date):
        return self.c_calendar[PCalendar.hash_date(date)]

    def hash_date(date: datetime.date):
        months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        days = 0
        for i in range(date.month):
            days += months[i]
        days += date.day
        is_leap = calendar.isleap(date.year)
        if days > 31 + 28:
            days += int(is_leap)
        
        return days
    
    def print(self):
        print('---------------- calendar ------------------')
        for key in self.c_calendar:
            if self.c_calendar[key] != {'schedule':[], 'update':[]}:
                print(str(key) + ':', self.c_calendar[key])
    
    def next_month(date: datetime.date):
        maxmonth = calendar.monthrange(date.year, date.month)[1]
        next_maxmonth = calendar.monthrange(date.year, date.month + 1)[1]
        next_days = maxmonth
        if next_maxmonth < maxmonth:
            next_days -= maxmonth - next_maxmonth
        another_month = date + datetime.timedelta(days=next_days)
        return another_month

    def get_day_of_month(date: datetime.date, date_to_get: int):
        day = date_to_get
        if day == -1:
            day = calendar.monthrange(date.year, date.month)[1]
        
        another_date = datetime.date(date.year, date.month, day)

        if another_date <= date:
            another_date = PCalendar.next_month(another_date)
        return another_date

    def get_day_of_week(date: datetime.date, quantity, weekday):
        this_month = calendar.monthcalendar(date.year, date.month)
        this_day = date.day

        date_location_on_month = (0,0) # get week and day number of current date
        for row, week in enumerate(this_month):
            done = False
            for column, day in enumerate(week):
                if day == this_day:
                    date_location_on_month = (row, column)
                    done = True
                    break
            if done:
                break
        
        other_day = 0
        outofbounds = False
        zero_at_end_of_month = ~bool(this_month[-1][-1])

        day_already_passed_weekday = this_day >= this_month[date_location_on_month[0]][weekday]
        index = date_location_on_month[0] - 1 + day_already_passed_weekday
        for _ in range(quantity):
            index += 1
            try:
                other_day = this_month[index][weekday]
            except:
                outofbounds = True
                index = zero_at_end_of_month
            if other_day == 0:
                index = 0
            if other_day == 0 or outofbounds:
                outofbounds = False
                date = PCalendar.next_month(date)
                this_month = calendar.monthcalendar(date.year, date.month)
                zero_at_end_of_month = ~bool(this_month[-1][-1])
                other_day = this_month[index][weekday]
        
        return datetime.date(date.year, date.month, other_day)

    def parse_schedule_params(entry: str):
        func_dict = {
            'monthly': 'monthly', 'weekly': 'weekly',
            'mensalmente': 'monthly', 'semanalmente': 'weekly',
            'mensal': 'monthly', 'semanal': 'weekly'
        }

        weekday_dict = {
            'segunda': 0, 'terca': 1, 'quarta': 2, 'quinta': 3,
            'sexta': 4, 'sabado': 5, 'domingo': 6,
            'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3,
            'friday': 4, 'saturday': 5, 'sunday': 6
        }

        special_dict = {
            'monthly': 'monthly $', 'weekly': 'weekly 1 friday',
            'bi-weekly': 'weekly 2 friday', 'mensalmente': 'monthly $',
            'semanalmente': 'weekly 1 friday', 'bi-semanalmente': 'weekly 2 friday'
        }

        special = False # if it's a special case of shceduling
        parsed_entry = entry.split(' ')
        if len(parsed_entry) == 1: # if it have only one word, its a special case
            special = True
            entry = special_dict[entry]
            parsed_entry = entry.split(' ')

        type_of_schedule = func_dict[parsed_entry[0]]

        if parsed_entry[1] != '$':
            entry_first_arg = int(parsed_entry[1])
        else:
            entry_first_arg = -1

        if type_of_schedule == 'monthly':
            return special, type_of_schedule, [entry_first_arg]
        elif type_of_schedule == 'weekly':
            return special, type_of_schedule, (entry_first_arg, weekday_dict[parsed_entry[2]])

    def schedule_paymethod(date: datetime.date, entry: str):
        _, func_selection, args = PCalendar.parse_schedule_params(entry)

        func_selection_dict = {
            'monthly': PCalendar.get_day_of_month,
            'weekly': PCalendar.get_day_of_week,
        }

        out_date = func_selection_dict[func_selection](date, *args)

        return out_date

    def add_schedule_date(self, id: int, date: datetime.date):
        self.get_day(date)['schedule'].append(id)