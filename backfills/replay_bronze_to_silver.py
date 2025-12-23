import sys
from datetime import datetime

START_DATE = sys.argv[1]   # yyyy-mm-dd
END_DATE = sys.argv[2]     # yyyy-mm-dd

print(f"Replaying Bronze → Silver from {START_DATE} to {END_DATE}")

# In practice:
# - Set PROCESSING_LOOKBACK_HOURS dynamically
# - Re-run existing Bronze → Silver Glue job