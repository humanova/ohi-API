import datetime
from datetime import timezone

acc_type = 1

now = datetime.datetime.now()
end_date = now
if acc_type == 1: end_date = now + datetime.timedelta(days=30)
elif acc_type == 2: end_date = now + datetime.timedelta(days=90)
elif acc_type == 3: end_date = now + datetime.timedelta(days=1095)
else: end_date = now + datetime.timedelta(days=30)

print(end_date.strftime("%Y-%m-%d %H:%M:%S"))


timestamp = end_date.replace(tzinfo=timezone.utc).timestamp()
print(timestamp)