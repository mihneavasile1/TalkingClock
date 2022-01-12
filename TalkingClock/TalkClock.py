#!/usr/bin/env python
import re
from datetime import datetime
import inflect
import argparse


class IncorrectTimeFormatException(Exception):
    """
    Time format is incorrect
    """
    pass


def extract_time(now):
    if not isinstance(now, datetime):
        check_time_format(now)
        now = datetime.strptime(now, '%H:%M').time()

    current_time = now.strftime("%H:%M")
    current_hour = now.strftime("%H")
    current_min = now.strftime("%M")

    return current_time, current_hour, current_min


def make_clock_talk(now, json):
    current_time, current_hour, current_min = extract_time(now)

    hour_lookup = {"thirteen": "one", "fourteen": "two", "fifteen": "three", "sixteen": "four", "seventeen": "five",
                   "eighteen": "six", "nineteen": "seven", "twenty": "eight", "twenty-one": "nine", "twenty-two": "ten",
                   "twenty-three": "eleven", "twenty-four": "twelve", "twelve": "twelve", "zero": "twelve",
                   "one": "one",
                   "two": "two", "three": "three", "four": "four", "five": "five", "six": "six", "seven": "seven",
                   "eight": "eight", "nine": "nine", "ten": "ten", "eleven": "eleven"}

    p = inflect.engine()
    p.number_to_words(1234567890)

    hour = hour_lookup[p.number_to_words(current_hour)]
    minutes = p.number_to_words(current_min)

    if int(current_min) == 0:
        return convert_to_json(hour.capitalize() + " o'clock", json)

    elif int(current_min) < 30:
        return convert_to_json(minutes.capitalize() + " past " + hour, json)

    elif int(current_min) > 30:
        next_h = int(current_hour)
        next_h += 1
        next_h_word = p.number_to_words(next_h)
        next_h_word = hour_lookup[next_h_word]
        new_min = 60 - int(current_min)
        next_min_word = p.number_to_words(new_min)
        return convert_to_json(next_min_word.capitalize() + " to " + next_h_word, json)

    else:
        return convert_to_json("Half past " + hour, json)


def convert_to_json(time, json):
    if json:
        return {"Human Friendly Time": time}
    else:
        return time


def check_time_format(time):
    x = re.findall("[0-2]?[0-9]:[0-9]{2}", time)

    if len(x) == 0:
        raise IncorrectTimeFormatException(time,
                                           "is an invalid time format. Please enter a valid time hours:minutes (HH:MM), e.g. 12:42")

    hours_mins = time.split(":")

    if len(hours_mins) > 2:
        raise IncorrectTimeFormatException(time,
                                           "is an invalid time format. Please enter a valid time hours:minutes (HH:MM), e.g. 12:42")

    if len(hours_mins[0]) > 2 or len(hours_mins[1]) > 2:
        raise IncorrectTimeFormatException(time,
                                           "is an invalid time format. Please enter a valid time hours:minutes (HH:MM), e.g. 12:42")

    if int(time[0]) == 2 and int(time[1]) >= 4:
        raise IncorrectTimeFormatException(time,
                                           "is an invalid time format. Please enter a valid time hours:minutes (HH:MM), e.g. 12:42")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # e.g -t 21:13
    parser.add_argument("-t", "--time", help="time", default=datetime.now())
    # by default it doesn't return json format, to enable it add -j <whatever_sring> (e.g. -j on)
    parser.add_argument("-j", "--json", help="json", default="")
    args = parser.parse_args()

    result = make_clock_talk(args.time, args.json)
    print(result)
