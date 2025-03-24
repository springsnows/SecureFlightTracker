import time
from datetime import datetime

# Get current time in seconds since the Unix epoch
current_time_seconds = int(time.time())
print(current_time_seconds)

# Convert to a human-readable UTC time format
current_time_readable = datetime.utcfromtimestamp(current_time_seconds).strftime('%Y-%m-%d %H:%M:%S')

# Print the current system time (Unix timestamp and formatted)
print("Current Unix timestamp:", current_time_seconds)
print("Current time (UTC):", current_time_readable)
