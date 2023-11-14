import sys
from datetime import datetime
import matplotlib.pyplot as plt
import numpy
import pandas as pd
from io import StringIO

from pandas import DataFrame


def input_handling():
    # timetable_csv = sys.argv[1]
    timetable_csv = """
    id,start,stop,project,tags
    cc2d596,2023-11-13 08:30:00,2023-11-13 12:15:00,PythonCourse,AXXES_BEACH
    020b20f,2023-11-13 13:00:00,2023-11-13 15:00:00,PythonCourse,AXXES_BEACH
    b65561b,2023-11-13 15:00:00,2023-11-13 16:45:00,GildedTros,AXXES_BEACH
    ce6eecd,2023-11-13 16:45:00,2023-11-13 17:45:00,PortfolioWebsite,AXXES_BEACH
    e7031be,2023-11-14 08:30:00,2023-11-14 12:30:00,Voorbereiding_Vandevelde,AXXES_BEACH
    e7031be,2023-11-14 13:30:00,2023-11-14 17:30:00,Voorbereiding_Vandevelde,AXXES_BEACH
    """

    df: DataFrame = pd.read_csv(StringIO(timetable_csv), parse_dates=['start', 'stop'])
    if len(sys.argv) > 2:
        return df, int(float(sys.argv[2])), int((float(sys.argv[2]) * 60) % 60)
    else:
        return df, 38, 0


def get_rest_of_week():
    remaining_days = []
    current = datetime.now()
    while current.weekday() < 4:
        current = current.replace(day=current.day + 1)
        remaining_days.append(current.strftime("%A"))
    return remaining_days


timetable, required_hours, required_minutes = input_handling()

timetable['duration'] = timetable['stop'] - timetable['start']
total_time = timetable['duration'].sum()

total_hours_worked, remainder = divmod(total_time.seconds, 3600)
total_minutes_worked, seconds = divmod(remainder, 60)

minutes_to_work = required_minutes - total_minutes_worked
carry = 0
if minutes_to_work < 0:
    minutes_to_work += 60
    carry = -1
hours_to_work = required_hours - total_hours_worked + carry

rest_week = get_rest_of_week()

hours_to_work_per_day, remainder = divmod(hours_to_work, len(rest_week))
minutes_to_work_per_day = (minutes_to_work + (remainder / 60)) / len(rest_week)

working_hours_data = numpy.array([float(hours_to_work + minutes_to_work / 60),
                                  float(total_hours_worked + total_minutes_worked / 60)])


def plot():
    def get_value_from_percentage(val):
        arr = numpy.array(working_hours_data)
        a = numpy.round(val / 100. * arr.sum(), 2)
        return a

    plt.pie(working_hours_data, labels=['Hours to work', 'Hours worked'], shadow=True, autopct=get_value_from_percentage)
    plt.show()


print(
    "Worked: {} hours, {} minutes! \nTo work: {} hours, {} minutes! \nThis comes down to {} hours, {} minutes per day!".format(
        total_hours_worked, total_minutes_worked, hours_to_work, minutes_to_work, hours_to_work_per_day,
        minutes_to_work_per_day))
plot()
