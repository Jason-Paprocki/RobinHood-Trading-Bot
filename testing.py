import zulu
import timedelta
now = zulu.now()
past =  now - timedelta(days-30)

print(past)
