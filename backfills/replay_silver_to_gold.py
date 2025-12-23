import sys

START_DATE = sys.argv[1]
END_DATE = sys.argv[2]

print(f"Rebuilding Gold metrics from {START_DATE} to {END_DATE}")

# Trigger Silver → Gold job with adjusted window