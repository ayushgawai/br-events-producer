# br-events-producer

Owner: Ayush Gawai (@ayushgawai)

Writes `data/events.parquet`, the events table three downstream teams read: 10,000 events from 500 users, the same bytes every run.

The user key column name lives in one line, `producer/schema.py`: `USER_KEY = "user_id"`.

```
make generate   # write data/events.parquet
make test       # schema, counts, determinism
```

Part of [Blast Radius](https://github.com/ayushgawai/blast-radius). Its `main` requires the `blast-radius` check, which the Switch impact coordinator sets once every downstream owner has approved.
