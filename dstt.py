import json
import os
import time

import fire

from time_humanizer import humanize


class TimeTracker:

    """Damn simple/small Time Tracker"""

    def __init__(self):
        try:
            self.read()
        except FileNotFoundError:
            self.data = {}
            self.write()

    def write(self):
        with open(os.getcwd() + '/.time.json', 'w') as outfile:
            json.dump(self.data, outfile)

    def read(self):
        self.data = json.load(open(os.getcwd() + '/.time.json'))

    def __str__(self):
        log = self.data.get('worklog', [])
        total_time = sum([
            entry.get(
                'f', int(time.time())
            ) - entry.get(
                's', int(time.time())
            ) for entry in log])
        return humanize(total_time)

    def start(self):
        log = self.data.get('worklog', [])
        try:
            if 's' in log[-1] and 'f' not in log[-1]:
                return f"Already started.\nYou've worked {str(self)} on this"
            else:
                self.data['worklog'].append({'s': int(time.time())})
        except IndexError:
            self.data['worklog'] = [{'s': int(time.time())}]
        self.write()
        return "Started!"

    def stop(self):
        log = self.data.get('worklog', [])
        try:
            if 'finish' in log[-1]:
                return f"Already finished.\nYou've worked {str(self)} on this"
            else:
                self.data['worklog'][-1].update({'f': int(time.time())})
        except IndexError:
            return "Nothing started"
        this_log = self.data.get('worklog', [])[-1]
        self.write()
        return (f"Finished!\nYou've worked {str(self)} on this\n" +
                f"This log: {humanize(this_log['f']-this_log['s'])}")

    def show(self):
        return f"You've worked:\n{str(self)}"


if __name__ == '__main__':
    fire.Fire(TimeTracker)
