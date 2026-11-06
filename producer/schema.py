# The name of the user key column in events.parquet. Downstream teams read it.
USER_KEY = "user_id"

COLUMNS = [
    ("event_id", "VARCHAR"),
    (USER_KEY, "VARCHAR"),
    ("session_id", "VARCHAR"),
    ("event_type", "VARCHAR"),
    ("event_ts", "TIMESTAMP"),
    ("page", "VARCHAR"),
    ("revenue_usd", "DOUBLE"),
]
