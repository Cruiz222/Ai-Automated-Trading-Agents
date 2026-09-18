from datetime import datetime, timezone, timedelta

from app.data.time_utils import normalize_to_utc


timestamp = datetime(
    2026,
    9,
    1,
    13,
    0,
    tzinfo=timezone(timedelta(hours=1)),
)

result = normalize_to_utc(timestamp)

print("Original:", timestamp)
print("Normalized:", result)

print("\nTesting naive timestamp:")

try:
    normalize_to_utc(
        datetime(2026, 9, 1, 13, 0)
    )
except ValueError as error:
    print("Rejected:", error)