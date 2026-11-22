
from monitor import detect_changes

MONITORED_DIRECTORY = "monitored_files"
BASELINE_FILE = "baseline/file_hashes.json"

detect_changes(MONITORED_DIRECTORY, BASELINE_FILE)
