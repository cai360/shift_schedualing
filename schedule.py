import calendar
from datetime import date
from calendar import Calendar
from typing import List, Tuple

class Schedule:
    def __init__(self, year, month, starting, ending, interval):
        self.year = year
        self.month = month
        self.start = starting 
        self.end = ending
        self.interval = interval
        self.working = []
        self.working_dates = []
        


    def generate_shifts(self) -> List[List[Tuple[int, int]]]:
        cal = Calendar(firstweekday=0) #0 = Monday, 6 = Sunday
        dates_list = cal.monthdays2calendar(self.year, self.month)
        
        self.working_dates = [
            day for week in dates_list
                    for day in week
                        if day[0] != 0
        ]
        return self.working_dates
    
        # return a list of hours interval
    def hour_interval(self) -> List[int]: 
        working_hr = self.end - self.start
        working = []
        for i in range(0 ,working_hr, self.interval):
            working.append([self.start + i, self.start + i + self.interval])
        self.working = working
        return working
    

        #remove the regular rest daytes
    def rest_dates(self, free_w_list):
        for day in self.working_dates:
            if day[1] in free_w_list:
                self.working_dates.remove(day)
        return self.working_dates






        


def main():
    sch = Schedule(2025, 8)
    sch.generate_shift()
    
if __name__ == "__main__":
    main()