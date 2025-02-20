from collections import namedtuple
import pathlib
import duckdb
import httpx

from datetime import date
from rich import print as rprint


THIS_YEAR = date.today().year
LAST_YEAR = date.today().year - 1

for year in (THIS_YEAR, LAST_YEAR):
    print(f"Downloading Conferences from {year}")
    csv_path = f"conferences_{year}.csv"
    pathlib.Path(csv_path).write_text(
        httpx.get(
            f"https://raw.githubusercontent.com/python-organizers/conferences/refs/heads/main/{year}.csv"
        ).text
    )
    print(f"Downloading Conferences from {csv_path}")

Queries = namedtuple("Queries", ["title", "query"])

queries = (
    Queries(
        "Events Left this Year...",
        f'Select Subject,"Start Date","End Date", Location, Country,"Website URL" FROM read_csv("conferences_{THIS_YEAR}.csv") WHERE "Start Date" > current_date',
    ),
    Queries(
        "CFPs Stil Open Remaining...",
        f'Select Subject,"Talk Deadline", Location, Country,"Proposal URL" FROM read_csv("conferences_{THIS_YEAR}.csv") WHERE "Talk Deadline" > current_date ORDER BY "Talk Deadline"',
    ),
    Queries(
        "CFPs Stil Open This Time Last Year...",
        f'Select Subject,"Start Date", "Talk Deadline", Location, Country,"Proposal URL" FROM read_csv("conferences_{LAST_YEAR}.csv") WHERE "Talk Deadline" > current_date - interval 1 year ORDER BY "Talk Deadline" LIMIT 20',
    ),
)

for query in queries:
    rprint(query.title)
    rprint("-" * 25)
    print(duckdb.sql(query.query))
