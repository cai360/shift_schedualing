import calendar
from datetime import date
from calendar import Calendar

class Schedual:
    def __init__(self, year, month):
        self.year = year
        self.month = month


    def generate_shifts(self):
        cal = Calendar()
        dates_list = cal.monthdays2calendar(self.year, self.month)
        return dates_list




        


def main():
    sch = Schedual(2025, 8)
    sch.generate_shift()
    
if __name__ == "__main__":
    main()