.PHONY: test generate
test:
	uv run pytest -q --junitxml=.reports/junit.xml

generate:
	uv run python -m producer.generate --out data/events.parquet
