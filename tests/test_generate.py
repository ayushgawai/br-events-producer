import hashlib

import duckdb

from producer.generate import N_EVENTS, N_USERS, generate
from producer.schema import COLUMNS, USER_KEY


def test_schema_and_counts(tmp_path):
    path = generate(tmp_path / "events.parquet")
    con = duckdb.connect()
    described = con.execute(f"DESCRIBE SELECT * FROM '{path}'").fetchall()
    assert [(c[0], c[1]) for c in described] == COLUMNS
    total, users = con.execute(f"SELECT count(*), count(DISTINCT {USER_KEY}) FROM '{path}'").fetchone()
    assert (total, users) == (N_EVENTS, N_USERS)


def test_each_session_has_one_user(tmp_path):
    path = generate(tmp_path / "events.parquet")
    worst = duckdb.connect().execute(f"SELECT max(n) FROM (SELECT count(DISTINCT {USER_KEY}) n FROM '{path}' GROUP BY session_id)").fetchone()[0]
    assert worst == 1


def test_deterministic(tmp_path):
    a = generate(tmp_path / "a.parquet").read_bytes()
    b = generate(tmp_path / "b.parquet").read_bytes()
    assert hashlib.sha256(a).digest() == hashlib.sha256(b).digest()
