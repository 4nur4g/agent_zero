from datetime import date, datetime

import pendulum

import pendulum


def extract_date_parts(date_input, fmt: str = "YYYY-MM-DD") -> dict:
    """
    Accepts either:
      - a string (parsed according to `fmt`)
      - a datetime.date or datetime.datetime instance
    and returns a dict with numeric day, month, and full year.

    :param date_input: e.g. "2025-04-10" or date.today() + timedelta(days=1)
    :param fmt:        pendulum token format (default "YYYY-MM-DD")
    :return:           {"date": int, "month": int, "year": int}
    """
    if isinstance(date_input, (date, datetime)):
        # turn built-in date/datetime into a Pendulum object
        dt = pendulum.instance(date_input)
    else:
        # parse string
        dt = pendulum.from_format(str(date_input), fmt)

    return {
        "date": dt.day,
        "month": dt.month,
        "year": dt.year,
    }