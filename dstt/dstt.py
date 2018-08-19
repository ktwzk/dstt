#!/usr/bin/env python3

import json
import os
import time

import fire

working_intervals = [60*60*8*5, 60*60*8, 60*60, 60, 1]
intervals_names = "wdhms"


def humanize(amount):
    """Jira-style time humanizer

    Translates difference of timestamps to Jira-style string (like 5h 3m 45s)

    Args:
        amount (int): Time in seconds

    Returns:
        str: Jira-style timestring

    """
    parts = []
    for i, interval in enumerate(working_intervals):
        quantity, amount = divmod(amount, interval)
        parts.append(f'{quantity}{intervals_names[i]}')
    return " ".join([i for i in parts if (
        i[0] != '0' or i[1] == intervals_names[-1]
    )])


class TimeTracker:

    def __init__(self):
        try:
            self._read()
        except FileNotFoundError:
            self._data = {}
            self._write()

    def _write(self):
        with open(os.getcwd() + '/.dstt.json', 'w') as outfile:
            json.dump(self._data, outfile)

    def _read(self):
        self._data = json.load(open(os.getcwd() + '/.dstt.json'))

    def _get_last_log(self):
        self._read()
        log = self._data.get('log', [])
        return log[-1].get(
            'f', int(time.time())
        ) - log[-1].get(
            's', int(time.time())
        )

    def __str__(self):
        self._read()
        log = self._data.get('log', [])
        total_time = sum(
            [entry.get('f', int(time.time())) -
             entry.get('s', int(time.time())) for entry in log]
        )
        return humanize(total_time)

    def start(self):
        self._read()
        log = self._data.get('log', [])
        try:
            if 's' in log[-1] and 'f' not in log[-1]:
                return (f"Already started.\n" +
                        f"You've worked {str(self)} in total\n" +
                        f"This log: {humanize(self._get_last_log())}")
            else:
                self._data['log'].append({'s': int(time.time())})
        except IndexError:
            self._data['log'] = [{'s': int(time.time())}]
        self._write()
        return "Started!"

    def stop(self):
        self._read()
        log = self._data.get('log', [])
        try:
            if 'finish' in log[-1]:
                return (f"Already finished.\n" +
                        f"You've worked {str(self)} in total\n" +
                        f"Last log: {humanize(self._get_last_log())}")
            else:
                self._data['log'][-1].update({'f': int(time.time())})
        except IndexError:
            return "Nothing started"
        self._write()
        return (f"Finished!\nYou've worked {str(self)} in total\n" +
                f"This log: {humanize(self._get_last_log())}")

    def show(self):
        self._read()

        def _this_or_last():
            return ["This", "Last"][
                int(
                    'finish' in self._data.get('log', [])[-1]
                )
            ]
        try:
            return (f"You've worked in total:\n{str(self)}\n\n" +
                    f"{_this_or_last()} log:\n" +
                    f"{humanize(self._get_last_log())}")
        except IndexError:
            return "You haven't worked on this folder"


def cli():
    fire.Fire(TimeTracker)


if __name__ == '__main__':
    cli()
