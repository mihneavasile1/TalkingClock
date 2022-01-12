import unittest
from datetime import datetime
from unittest import mock

from TalkingClock.TalkClock import IncorrectTimeFormatException, check_time_format, convert_to_json, make_clock_talk, \
    extract_time


class MakeClockTalkTest(unittest.TestCase):
    def test_make_clock_talk(self):
        # cases - e.g. :
        #   - 11:00 --> "Eleven o'clock"
        #   - 10:23 --> "Twenty-three past ten"
        #   - 10:55 --> "Five to eleven"
        #   - 10:30 --> "Half past ten"
        #   - 00:04 --> Four past twelve
        #   - 01:21 --> Twenty-one past one
        #   - 00:00 --> Twelve o'clock

        times = ["11:00", "10:23", "10:55", "10:30", "00:04", "01:21", "00:00"]
        expected_texts = ["Eleven o'clock", "Twenty-three past ten", "Five to eleven", "Half past ten",
                          "Four past twelve", "Twenty-one past one", "Twelve o'clock"]

        for i, time in enumerate(times):
            self.assertEqual(expected_texts[i], make_clock_talk(now=time, json=""))


    @mock.patch('TalkClock.extract_time')
    def test_make_clock_talk_json_off(self, extract_time_mock):
        extract_time_mock.return_value = "23:12", "23", "12"
        now = extract_time_mock.return_value[0]

        expected_friendly_time = "Twelve past eleven"

        self.assertEqual(expected_friendly_time, make_clock_talk(now=now, json=""))
        self.assertNotEqual(expected_friendly_time, make_clock_talk(now=now, json="on"))

    @mock.patch('TalkClock.convert_to_json')
    @mock.patch('TalkClock.extract_time')
    def test_make_clock_talk_json_on(self, extract_time_mock, convert_to_json_mock):
        extract_time_mock.return_value = "23:45", "23", "45"
        now = extract_time_mock.return_value[0]

        expected_friendly_time = "Fifteen to twelve"
        convert_to_json_mock.return_value = {"Human Friendly Time": expected_friendly_time}

        self.assertEqual(convert_to_json_mock.return_value, make_clock_talk(now=now, json="on"))
        self.assertNotEqual(expected_friendly_time, make_clock_talk(now=now, json="on"))


class ConvertToJsonTest(unittest.TestCase):
    # cases:
    #   - json is ""        --> return time as string
    #   - json is not ""    --> return time as json
    def test_convert_to_json_on(self):
        fake_json = "on"
        fake_time = "Twelve past eleven"

        self.assertEqual({"Human Friendly Time": fake_time}, convert_to_json(time=fake_time, json=fake_json))

    def test_convert_to_json_off(self):
        fake_json = ""
        fake_time = "Twelve past eleven"

        self.assertEqual(fake_time, convert_to_json(time=fake_time, json=fake_json))


class CheckTimeFormatTest(unittest.TestCase):
    def test_check_time_format_fail(self):
        """
        Given an invalid time format:
        e.g.:
            - asd
            - as:fd
            - 12:ff
            - fd:23
            - 25:12
            - 23:414
            - 233:12

        It raises and IncorrectTimeFormatException
        """
        test_cases = ["asd", "as:fd", "12:ff", "d:23", "25:12", "23:414", "233:12"]

        # check_time_format("233:12")

        for test_case in test_cases:
            with self.assertRaises(IncorrectTimeFormatException):
                check_time_format(test_case)

    def test_check_time_format_pass(self):
        """
        Given a valid time format
        It  does not raise IncorrectTimeFormatException
        """
        test_cases = ["12:51", "10:30", "9:13", "08:24", "00:12", "21:46"]

        for test_case in test_cases:
            check_time_format(test_case)


class ExtractTimeTest(unittest.TestCase):

    def test_extract_time_datetime_object(self):
        now = datetime(2013,1,13,13,23,34)
        expected = "13:23", "13", "23"

        self.assertEqual(expected, extract_time(now))

    def test_extract_time_user_string(self):
        now = "13:53"
        expected = "13:53", "13", "53"

        self.assertEqual(expected, extract_time(now))
