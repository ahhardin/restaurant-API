import calendar
import csv
import re
import datetime


#
# constants #
#

# assume any closing hours before 4:30 am can be attributed to the next day
time_cutoff = datetime.time(4, 30) 
ordered_day_abbreviations = [c.lower() for c in calendar.day_abbr]
# regex patterns for extracting days, day intervals, and time intervals
day_interval_pattern = f"({'|'.join(ordered_day_abbreviations)})-({'|'.join(ordered_day_abbreviations)})"
single_day_pattern = f"(?<!-)({'|'.join(ordered_day_abbreviations)})(?!-)"
time_pattern = "((?:(?<!:|[0-9])[0-9]{1,2}\s(?:am|pm))|(?:(?<!:|[0-9])[0-9]{1,2}:[0-9]{2}\s(?:am|pm)))\s-\s((?:(?<!:|[0-9])[0-9]{1,2}\s(?:am|pm))|(?:(?<!:|[0-9])[0-9]{1,2}:[0-9]{2}\s(?:am|pm)))"


#
# helper functions #
#

def check_after_midnight(interval):
    # if a day is after midnight, append that time interval onto the following day
    # assume any hours earlier than time_cutoff should be wrapped to the next day
    # will return a tuple of (today_interval, tomorrow_interval) where tomorrow_interval may be None
    if interval[1] < time_cutoff:
        today_interval = (interval[0], datetime.time(23, 59, 59, 999999))
        tomorrow_interval = (datetime.time(0,0), interval[1])
        return today_interval, tomorrow_interval
    return interval, None

def add_hours(restaurant, day, hours):
    if restaurant.get(day):
        restaurant[day].extend(hours)
    else:
        restaurant[day] = [h for h in hours] # copy so we don't mutate later
    return restaurant

def get_tomorrow(day):
    index = ordered_day_abbreviations.index(day)
    return ordered_day_abbreviations[(index + 1) % 7]

def get_weekday_and_time(date):
    weekday = ordered_day_abbreviations[date.weekday()]
    time = date.time()
    return weekday, time

def get_open_restaurants_by_day_and_time(weekday, time):
    open_restaurants = []
    for key, val in formatted_data.items():
        time_intervals = val.get(weekday)
        if time_intervals:
            for time_interval in time_intervals:
                if (time >= time_interval[0]) and (time <= time_interval[1]):
                    open_restaurants.append(key) 
    return open_restaurants

def get_open_restaurants_by_date(date):
    return get_open_restaurants_by_day_and_time(*get_weekday_and_time(date))

# initialize
formatted_data = {}

with open('data.csv') as data:
    csvreader = csv.reader(data)
    next(csvreader)
    for line in csvreader:
        # extract data from the line
        name = line[0]
        open_hours = line[1]
        # unpack hours into days with time intervals in an array
        intervals = [str(h.lower().strip()) for h in open_hours.split("/")]
        formatted_data[name] = {}
        
        for interval in intervals:
            interval = interval.replace('tues', 'tue')
            # unpack times
            hour_intervals = re.findall(time_pattern, interval)
            hours = []
            tomorrow_hours = []
            for h in hour_intervals:
                # store intervals in datetime.time objects
                try: start = datetime.datetime.time(datetime.datetime.strptime(h[0], '%I:%M %p'))
                except: start = datetime.datetime.time(datetime.datetime.strptime(h[0], '%I %p'))
                try: end = datetime.datetime.time(datetime.datetime.strptime(h[1], '%I:%M %p'))
                except: end = datetime.datetime.time(datetime.datetime.strptime(h[1], '%I %p'))

                # handle midnight times
                today, tomorrow = check_after_midnight((start, end))
                hours.append(today)
                if tomorrow:
                    tomorrow_hours.append(tomorrow)
            
            # unpack days
            days = []
            # look for day intervals (sepearated by a dash), and fill in missing weekdays
            day_intervals = re.findall(day_interval_pattern, interval)
            if day_intervals:
                for int in day_intervals:
                    idx_start = ordered_day_abbreviations.index(int[0])
                    idx_end = ordered_day_abbreviations.index(int[1])
                    days += [d for idx, d in enumerate(ordered_day_abbreviations) if idx >= idx_start and idx <= idx_end]

            # if no dash, assign single day
            single_days = re.findall(single_day_pattern, interval)
            if single_days:
                for day in single_days:
                    days += [day]
            
            for day in days:
                formatted_data[name] = add_hours(formatted_data[name], day, hours)
                if tomorrow_hours:
                    formatted_data[name] = add_hours(formatted_data[name], get_tomorrow(day), tomorrow_hours)

   

