import datetime
from dataclasses import dataclass
from typing import Generator

import pytz as pytz
import requests

from constants import SESSION_COOKIE, STARS_ENDPOINT, USER_ID, ADVENT_URL

@dataclass(frozen=True, eq=True)
class DayProgress:
    day: int
    part_1: bool
    part_1_time: str
    part_2: bool
    part_2_time: str

def calculate_solve_time(year: int, day: int, timestamp: int) -> str:
    release_time = pytz.timezone("EST").localize(datetime.datetime(year, 12, day, 0, 0, 0))

    submit_time = pytz.timezone("UTC").localize(datetime.datetime.utcfromtimestamp(timestamp))

    solve_time = submit_time - release_time
    #print("day:", day, "\ttimestamp:", timestamp, "\tsubmit_time:", submit_time, "\trelease_time:", release_time, "\tsolve_time:", solve_time, "\tLOCAL_TIMEZONE:", LOCAL_TIMEZONE)
    return f"{solve_time}"

def get_progress(year: int) -> Generator[DayProgress, None, None]:
    res = requests.get(f"{ADVENT_URL}/{year}/{STARS_ENDPOINT}", cookies={"session": SESSION_COOKIE})
    res.raise_for_status()

    leaderboard_info = res.json()

    #print(leaderboard_info)

    stars = leaderboard_info["members"][USER_ID]["completion_day_level"]

    for day, parts in stars.items():
        completed = parts.keys()
        yield DayProgress(
            day=int(day),
            part_1="1" in completed,
            part_1_time="" if "1" not in completed else calculate_solve_time(year, int(day), int(parts["1"]["get_star_ts"])),
            part_2="2" in completed,
            part_2_time="" if "2" not in completed else calculate_solve_time(year, int(day), int(parts["2"]["get_star_ts"])),
        )
