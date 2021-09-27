from django import template
import datetime as dt
dtt = dt.datetime
import jpholiday
from work_time.models import Worktime, User
from dateutil.relativedelta import relativedelta
register = template.Library()

@register.filter(name="jpholiday")
def jpholiday_judge(day):
   val = jpholiday.is_holiday(day)

   return val

def time_count(start,end):
    start_time = dtt.combine(dt.date(2000, 1, 1), start)
    if end <= dt.time(hour=5):
        end_time = dtt.combine(dt.date(2000, 1, 2), end)
    else:
        end_time = dtt.combine(dt.date(2000, 1, 1), end)
    night_time = dtt.combine(dt.date(2000, 1, 1), dt.time(hour=22))
    if end_time >= night_time:
        end_time_night = end_time - night_time
        time_list = [end_time - start_time,end_time_night]
        work_time = [[int(str(time).split(':')[0]),
             int(str(time).split(':')[1])] for time in time_list]
        return work_time
    else:
        time = [end_time - start_time]
        time_list = str(time[0]).split(':')
        work_time = [int(time_list[0]),int(time_list[1])]
        return work_time

@register.filter(name="work_time")
def work_time(object):
    start_time = object.start_time
    end_time = object.end_time
    night_time = dt.time(hour=22)
    if end_time >= night_time or end_time <= dt.time(hour=5):
        work_time = time_count(object.start_time,object.end_time)[0]
    else:
        work_time = time_count(object.start_time,object.end_time)
    time = str(work_time[0])+'時間'+str(work_time[1])+'分'
    return time

@register.filter(name="work_time_sum")
def work_time(object_list):
    time_hour_sum = 0
    time_minutes_sum = 0
    night_hour_sum = 0
    night_minutes_sum = 0
    over_hour_sum = 0
    over_minutes_sum = 0
    for object in object_list:
        start_time = object.start_time
        end_time = object.end_time
        night_time = dt.time(hour=22)
        if end_time >= night_time or end_time <= dt.time(hour=5):
            time_list = time_count(start_time,end_time)
            time_hour_sum += time_list[0][0]
            time_minutes_sum += time_list[0][1]
            night_hour_sum += time_list[1][0]
            night_minutes_sum += time_list[1][1]
            if time_list[0][0] >= 8:
                over_hour_sum += time_list[0][0] - 8
                over_minutes_sum += time_list[0][1]
        else:
            time_list = time_count(start_time,end_time)
            time_hour_sum += time_list[0]
            time_minutes_sum += time_list[1]
            if time_list[0] >= 8:
                over_hour_sum += time_list[0] - 8
                over_minutes_sum += time_list[1]
    time_sum = (str(time_hour_sum + time_minutes_sum//60)+'時間'+
                str(time_minutes_sum%60)+'分')
    night_sum = (str(night_hour_sum + night_minutes_sum//60)+'時間'+
                str(night_minutes_sum%60)+'分')
    over_sum = (str(over_hour_sum + over_minutes_sum//60)+'時間'+
                str(over_minutes_sum%60)+'分')
    sum_list = [time_sum,night_sum,over_sum]

    return sum_list

@register.filter(name="date_filter")
def date_range_filter(object,args):
    if  len(args) == 21:
        startdate = args.split(',')[0]
        enddate = args.split(',')[1]
        post_qs = object.filter(date__range=[startdate,enddate])
        return post_qs
    else:
        return object

@register.filter(name="day_my_shift")
def day_my_shift(day,user):
    if Worktime.objects.filter(date=day,name=user).exists():
        qs_list = Worktime.objects.filter(date=day,name=user)
        return qs_list
    else:
        return False
