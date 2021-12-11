from typing import List

from testConstants import (
    ADVENT_URL,
    HEADER_PREFIX,
    STAR_SYMBOL,
    TABLE_MARKER,
    YEAR,
    SHOW_TIME,
    REVERSE_DAYS,
    SHOW_PAST_YEARS,
)
from progress import get_progress

def remove_existing_table(lines: List[str]) -> List[str]:
    """
    If there's an existing table, it should be between two table markers.
    If that's the case, remove the existing table and return a single table
    marker in its place. If not, just return the original content.
    """
    start = None
    end = None
    for i, line in enumerate(lines):
        if start is None and line.strip() == TABLE_MARKER:
            start = i
            continue
        if start is not None and line.strip() == TABLE_MARKER:
            end = i
            break

    if start is not None and end is not None:
        return lines[:start] + lines[end:]
    return lines


def insert_table(lines: List[str], year: int, first: bool) -> (List[str], bool):
    """
    Search the lines for a table marker, and insert a table there.
    """
    table_location = None
    for i, line in enumerate(lines):
        if line.strip() == TABLE_MARKER:
            table_location = i
            break
    else:
        return lines, True

    stars_info = sorted(list(get_progress(year)), key=lambda p: p.day)
    stars_info = list(reversed(stars_info)) if REVERSE_DAYS else stars_info

    if len(stars_info) == 0:
        return lines, True

    to_insert = [
        TABLE_MARKER,
        f"{HEADER_PREFIX} {year} Results",
        "",
        "| Day | Part 1 | Part 2 |",
        "| :---: | :---: | :---: |",
    ]

    for star_info in stars_info:
        day_url = f"{ADVENT_URL}/{year}/day/{star_info.day}"
        day_text = f"[Day {star_info.day}]({day_url})"
        part_1_text = STAR_SYMBOL if star_info.part_1 else " "
        part_2_text = STAR_SYMBOL if star_info.part_2 else " "

        if SHOW_TIME:
            part_1_text += "<br>"+star_info.part_1_time if star_info.part_1 else ""
            part_2_text += "<br>"+star_info.part_2_time if star_info.part_2 else ""

        to_insert.append(f"| {day_text} | {part_1_text} | {part_2_text} |")

    to_insert.append(TABLE_MARKER if first else "")

    return lines[:table_location] + to_insert + lines[table_location+1:], False


def update_readme(readme: List[str]) -> List[str]:
    """
    Take the contents of a readme file and update them
    """
    new_readme = remove_existing_table(readme)
    first = True
    if SHOW_PAST_YEARS:
        for year in range(2015, YEAR+1):
            new_readme, first = insert_table(new_readme, year, first)
    else:
        new_readme = insert_table(new_readme, YEAR, first)[0]

    return new_readme
