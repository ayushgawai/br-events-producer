"""Write events.parquet: 10,000 events from 500 users, the same bytes every run."""

import argparse
import random
from datetime import datetime, timedelta
from pathlib import Path

import duckdb

from producer.schema import COLUMNS

SEED, N_EVENTS, N_USERS = 42, 10_000, 500
PAGES = ["/", "/pricing", "/docs", "/blog", "/signup", "/login", "/cart", "/checkout"]
START = datetime(2026, 10, 1)


def rows():
    rng = random.Random(SEED)
    sessions = {}  # user -> (session_id, events left in it)
    n_sessions = 0
    for i in range(1, N_EVENTS + 1):
        user = f"u{rng.randint(1, N_USERS):03d}"
        sid, left = sessions.get(user, (None, 0))
        if left == 0:
            n_sessions += 1
            sid, left = f"s{n_sessions:05d}", rng.randint(1, 8)
        sessions[user] = (sid, left - 1)
        kind = rng.choices(["page_view", "click", "purchase"], [70, 25, 5])[0]
        revenue = round(rng.uniform(5, 200), 2) if kind == "purchase" else 0.0
        ts = START + timedelta(seconds=rng.randint(0, 31 * 86400 - 1))
        yield (f"e{i:05d}", user, sid, kind, ts, rng.choice(PAGES), revenue)


def generate(out: Path) -> Path:
    out.parent.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect()
    con.execute("SET threads = 1")
    cols = ", ".join(f"{name} {type_}" for name, type_ in COLUMNS)
    con.execute(f"CREATE TABLE events ({cols})")
    pad = (None,) * (len(COLUMNS) - 7)  # columns added to the schema later start out null
    con.executemany(f"INSERT INTO events VALUES ({', '.join('?' * len(COLUMNS))})", [r + pad for r in rows()])
    con.execute(f"COPY (SELECT * FROM events ORDER BY event_id) TO '{out}' (FORMAT parquet)")
    return out


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--out", default="data/events.parquet")
    print(generate(Path(p.parse_args().out)).resolve())
