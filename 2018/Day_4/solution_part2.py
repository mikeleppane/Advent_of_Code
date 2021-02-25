#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from collections import Counter
from dataclasses import dataclass

import re
import sys
from datetime import datetime
from typing import List

INPUT_FILE = "input.txt"


@dataclass
class Record:
    timestamp: datetime
    guard_info: str


def find_best_minute(records: List[Record]):
    guard_id_regex = re.compile(r"Guard #(\d{1,4})")
    sleep_time = None
    guard_asleep_frequencies = {}
    guard_ids = {
        guard_id_regex.match(record.guard_info).groups()[0]
        for record in records
        if "begins shift" in record.guard_info
    }
    for guard_id in guard_ids:
        correct_guard = False
        asleep_times = list()
        for record in records:
            if "begins shift" in record.guard_info and guard_id in record.guard_info:
                correct_guard = True
            elif (
                "begins shift" in record.guard_info
                and guard_id not in record.guard_info
            ):
                correct_guard = False
            if correct_guard and "falls asleep" in record.guard_info:
                sleep_time = record.timestamp
            elif correct_guard and "wakes up" in record.guard_info:
                if sleep_time:
                    for time in list(range(sleep_time.minute, record.timestamp.minute)):
                        asleep_times.append(time)
                    sleep_time = None
        if asleep_times:
            guard_asleep_frequencies[int(guard_id)] = Counter(asleep_times).most_common(1)[0]
    print(guard_asleep_frequencies)


def read_records() -> List[Record]:
    records = []
    record_regex = re.compile(r"\[(\d{4}\-\d{2}\-\d{2}\s\d{2}:\d{2})\]\s([^\n]+)")
    with open(INPUT_FILE, "r") as f_handle:
        for line in f_handle:
            if line:
                matches = record_regex.match(line.rstrip()).groups()
                if len(matches) == 2:
                    record = Record(
                        timestamp=datetime.strptime(matches[0], "%Y-%m-%d %H:%M"),
                        guard_info=matches[1],
                    )
                    records.append(record)
                else:
                    raise ValueError(f"Incorrect record found from line: {line}")

    return records


def main():
    records = sorted(read_records(), key=lambda r: r.timestamp)
    find_best_minute(records)


if __name__ == "__main__":
    sys.exit(main())
