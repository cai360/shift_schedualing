from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime


import calendar
from schedual import Schedual


#employee2
#employee2

#lulu
#3dR12vEL

username = 'test1'
password = "test0001"
hash = generate_password_hash(password)
result = check_password_hash( hash, "test0001")


current_date = datetime.today()
#print(current_date.hour + 1)

cal = calendar.Calendar()

monthdates = cal.monthdatescalendar(2023, 3)
monthdays2 = cal.monthdays2calendar(2025, 3)
monthdays = cal.monthdayscalendar(2025, 3)


sch = Schedual(2025, 4, 8, 17, 2)
list = sch.hour_interval()

for i in list:
    print(i)



'''shallow copy
a = [1,2,3]
a_ref = a
a.append(4)
print("a: ", a)
print("a_ref: ", a)


a_list = list(a)
a_index = a[:]
a_copy = a.copy()
a.append(5)
print("Shallow copy")
print("a_list: ", a_list)
print("a_index: ", a_index)
print("a_copy: ", a_copy)
'''