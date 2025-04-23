import calendar
from datetime import date
from calendar import Calendar
from typing import List, Tuple

class Schedual:
    def __init__(self, year, month, starting, ending, interval):
        self.year = year
        self.month = month
        self.start = starting 
        self.end = ending
        self.interval = interval


    def generate_shifts(self) -> List[List[Tuple[int, int]]]:
        cal = Calendar(firstweekday=0) #0 = Monday, 6 = Sunday
        dates_list = cal.monthdays2calendar(self.year, self.month)
        return dates_list
    
        # return a list of hours interval
    def hour_interval(self) -> List[int]: 
        working_hr = self.end - self.start
        working = []
        for i in range(working_hr):
            working.append([self.start + i, self.start + i + 1])

        return working




        


def main():
    sch = Schedual(2025, 8)
    sch.generate_shift()
    
if __name__ == "__main__":
    main()