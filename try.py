from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime



#employee2
#employee2

#lulu
#3dR12vEL

username = 'test1'
password = "test0001"
hash = generate_password_hash(password)
result = check_password_hash( hash, "test0001")


current_date = datetime.today()
print(current_date.year + 1)