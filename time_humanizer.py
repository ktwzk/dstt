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
    return " ".join([i for i in parts if (i[0] != '0' or i[1] == intervals_names[-1])])


def dehumanize(string):
    """Jira-style time parser

    Translates Jira-style timestring (like 5h 3m 45s) to difference of
    timestamps

    Args:
        string (str): Jira-style timestring

    Returns:
        int: Time in seconds

    """
    return sum(
        int(amount[:-1]) * working_intervals[
            intervals_names.index(amount[-1])
        ] for amount in string.split()
    )
