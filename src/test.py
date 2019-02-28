from datetime import datetime, date

date_format = "%Y-%m-%d"
now = datetime.now()#.strftime(date_format)
print(type(now))

before = '2019-02-20'
before = datetime.strptime(before, date_format)
print(type(before))

delta = now - before

print(delta.days)