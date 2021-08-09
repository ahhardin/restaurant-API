import datetime
import unittest

from data import formatted_data, ordered_day_abbreviations, get_open_restaurants_by_day_and_time

class TestDataFormat(unittest.TestCase):
    '''
    Tests for well-formed data
    '''
    def test_weekday_format(self):
        # make sure all the day strings are presnt in ordered_day_abbreviations
        for r in formatted_data.values():
            for d in r.keys():
                self.assertTrue(d in ordered_day_abbreviations)

    def test_time_interval_format(self):
        # ensure all the time intervals are well-formed (type datetime.time and open time precedes the close time)
        for (r,d) in formatted_data.items():
            for intervals in d.values():
                # assert that each day has at least one time interval (if no intervals day key should not exist)
                self.assertTrue(len(intervals) > 0)
                for time in intervals:
                    # assert all the times are type datetime.time and the starting time is less than the ending time
                    self.assertTrue(isinstance(time[0], datetime.time))
                    self.assertTrue(isinstance(time[1], datetime.time))
                    self.assertTrue(time[0] <= time[1])

class TestKnownHours(unittest.TestCase):
    '''
    Some sample tests to ensure the query works correctly
    '''
    def test_open_at_midnight_any_day(self):
        open_restaurants = set()
        for day in ordered_day_abbreviations:
            open_restaurants.update(get_open_restaurants_by_day_and_time(day, datetime.time(0, 0, 0, 0)))
        actual_open_restaurants = set(["Caffe Luna", "The Cheesecake Factory", "Bonchon", "Taverna Agora","Seoul 116", "Stanbury", "42nd Street Oyster Bar"])
        self.assertTrue(open_restaurants == actual_open_restaurants)

    def test_open_at_one_thirty_am_any_day(self):
        open_restaurants = set()
        for day in ordered_day_abbreviations:
            open_restaurants.update(get_open_restaurants_by_day_and_time(day, datetime.time(1, 30, 0)))
        actual_open_restaurants = set(["Bonchon", "Seoul 116", "42nd Street Oyster Bar"])
        self.assertTrue(open_restaurants == actual_open_restaurants)
    
    def test_open_at_ten_thirty_am_monday(self):
        open_restaurants = set(get_open_restaurants_by_day_and_time('mon', datetime.time(10, 30, 0)))
        actual_open_restaurants = set(["Tupelo Honey", "Dashi", "Mez Mexican"])
        self.assertTrue(open_restaurants == actual_open_restaurants)

    def test_not_open_on_monday(self):
        closed_restaurants = set()
        for name, days in formatted_data.items():
            if not days.get('mon'):
                closed_restaurants.add(name)
            
        actual_closed_restaurants = set(["Garland", ])
        self.assertTrue(closed_restaurants == actual_closed_restaurants)


if __name__ == '__main__':
    unittest.main()