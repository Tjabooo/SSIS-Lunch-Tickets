# SSIS-Lunch-Tickets

A small school project: a console program that tracks lunch tickets with tags. A tag reader connected over a serial port sends tag UIDs; the program stores registered tags and scans in a SQLite database and allows one lunch per tag per day. Messages are in Swedish.

Status: prototype, not maintained. It is hard-wired to a specific kind of serial tag reader, and has not been tested beyond the original setup.

## Requirements
- Python 3.10+ (uses `match`)
- A tag reader that writes tag UIDs to a serial port (9600 baud), read through [pyMultiSerial](https://pypi.org/project/pyMultiSerial/)
- `pip install -r requirements.txt`

## Configuration
Copy `.env.example` to `.env`:

| Variable | Meaning |
| --- | --- |
| `DB_NAME` | SQLite file name (informational) |
| `DB_URL` | SQLAlchemy database URL, e.g. `sqlite:///lunch.db` |

## Run
```bash
python3 main.py
```
Pick a mode:
1. Scan: a registered tag gets a lunch once per day.
2. Register: scanned tags are added as valid.
3. Count: number of scans on a given date (`DD/MM/YY`).

## Known limitations
- Dates are compared as `DD/MM/YY` strings and the current date/time is captured once at start-up, so the program should be restarted each day.
- Tag/date filtering in `check()` uses Python `and` inside SQL `where` clauses, which does not combine both conditions as intended.
