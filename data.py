import calendar
import csv
import re
from datetime import datetime

# initialize
formatted_data = {}

ordered_day_abbreviations = [c.lower() for c in calendar.day_abbr]

# regex patterns for extracting days, day intervals, and time intervals
day_interval_pattern = f"({'|'.join(ordered_day_abbreviations)})-({'|'.join(ordered_day_abbreviations)})"
single_day_pattern = f"(?<!-)({'|'.join(ordered_day_abbreviations)})(?!-)"
time_pattern = "((?:(?<!:|[0-9])[0-9]{1,2}\s(?:am|pm))|(?:(?<!:|[0-9])[0-9]{1,2}:[0-9]{2}\s(?:am|pm)))\s-\s((?:(?<!:|[0-9])[0-9]{1,2}\s(?:am|pm))|(?:(?<!:|[0-9])[0-9]{1,2}:[0-9]{2}\s(?:am|pm)))"

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
            for h in hour_intervals:
                # store intervals in datetime.time objects
                try: start = datetime.time(datetime.strptime(h[0], '%I:%M %p'))
                except: start = datetime.time(datetime.strptime(h[0], '%I %p'))
                try: end = datetime.time(datetime.strptime(h[1], '%I:%M %p'))
                except: end = datetime.time(datetime.strptime(h[1], '%I %p'))
                hours.append((start, end))
            
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
                # set the hour interval(s) computed for each day identified
                if not formatted_data[name].get('day'):
                    formatted_data[name][day] = hours

            
            

            

                

