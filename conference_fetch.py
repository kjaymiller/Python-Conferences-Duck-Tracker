from collections import namedtuple
import pathlib
import duckdb
import httpx

from datetime import date
from rich import print as rprint


BASE_URL = (
    "https://raw.githubusercontent.com/python-organizers/conferences/refs/heads/main"
)
THIS_YEAR = f"{BASE_URL}/{date.today().year}.csv"
LAST_YEAR = f"{BASE_URL}/{date.today().year - 1}.csv"

Queries = namedtuple("Queries", ["title", "query"])

queries = (
    Queries(
        "Events Left this Year...",
        f'Select Subject,"Start Date","End Date", Location, Country,"Website URL" FROM read_csv("{THIS_YEAR}") WHERE "Start Date" > current_date',
    ),
    Queries(
        "CFPs Stil Open Remaining...",
        f'Select Subject,"Talk Deadline", Location, Country,"Proposal URL" FROM read_csv("{THIS_YEAR}") WHERE "Talk Deadline" > current_date ORDER BY "Talk Deadline"',
    ),
    Queries(
        "CFPs Stil Open This Time Last Year...",
        f'Select Subject,"Start Date", "Talk Deadline", Location, Country,"Proposal URL" FROM read_csv("{LAST_YEAR}") WHERE "Talk Deadline" > current_date - interval 1 year ORDER BY "Talk Deadline" LIMIT 20',
    ),
)

for query in queries:
    rprint(query.title)
    rprint("-" * 25)
    print(duckdb.sql(query.query))
