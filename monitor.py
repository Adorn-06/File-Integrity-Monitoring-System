
import json
import time
from pathlib import Path

from file_hasher import calculate_file_hash
from alert_logger import log_event

def load_baseline(baseline_file):

    try:
        with open(baseline_file, "r", encoding="utf-8") as file:
            data = json.load(file)

        return data["files"]

    except (OSError, json.JSONDecodeError, KeyError, TypeError) as error:
        print(f"[ERROR] Unable to load baseline: {error}")
        return None


def scan_current_files(directory):

    directory = Path(directory)
    current_files = {}
    scan_complete = True

    if not directory.exists() or not directory.is_dir():
        print("[ERROR] Monitoring directory does not exist.")
        return None, False

    try:
        for file_path in directory.rglob("*"):

            if file_path.is_file():

                file_hash = calculate_file_hash(file_path)

                if file_hash is None:
                    scan_complete = False
                    continue

                relative_path = file_path.relative_to(directory).as_posix()
                current_files[relative_path] = file_hash

    except OSError as error:
        print(f"[ERROR] Unable to complete directory scan: {error}")
        scan_complete = False

    return current_files, scan_complete


def detect_changes(directory, baseline_file):

    baseline = load_baseline(baseline_file)

    if baseline is None:
        return

    current_files, scan_complete = scan_current_files(directory)

    if current_files is None:
        return

    print("\n========== FILE INTEGRITY SCAN ==========")

    modified_files = []
    new_files = []
    deleted_files = []

    # Detect new and modified files
    for file_path, current_hash in current_files.items():

        if file_path not in baseline:
            new_files.append(file_path)

        elif current_hash != baseline[file_path]:
            modified_files.append(file_path)

    # Detect deleted files only if the scan is complete
    if scan_complete:

        for file_path in baseline:

            if file_path not in current_files:
                deleted_files.append(file_path)

    else:
        print("[WARNING] Scan incomplete. Deleted-file detection skipped.")

    # Display and log modified files
    if modified_files:

        for file_path in modified_files:
            print(f"[ALERT] Modified file: {file_path}")
            log_event("MODIFIED FILE", file_path)

    # Display and log new files
    if new_files:

        for file_path in new_files:
            print(f"[ALERT] New file detected: {file_path}")
            log_event("NEW FILE", file_path)

    # Display and log deleted files
    if deleted_files:

        for file_path in deleted_files:
            print(f"[ALERT] Deleted file: {file_path}")
            log_event("DELETED FILE", file_path)

    # Display safe message
    if not modified_files and not new_files and not deleted_files:
        print("[SAFE] No file integrity changes detected.")

    # Display scan summary
    print("\n========== SCAN SUMMARY ==========")
    print(f"Modified files: {len(modified_files)}")
    print(f"New files: {len(new_files)}")
    print(f"Deleted files: {len(deleted_files)}")
    print("==================================")

def monitor_continuously(directory, baseline_file, interval=5):

    print("\n[INFO] Continuous monitoring started.")
    print(f"[INFO] Scan interval: {interval} seconds")
    print("[INFO] Press CTRL+C to stop monitoring.\n")

    previous_files, scan_complete = scan_current_files(directory)

    if previous_files is None:
        return

    if scan_complete:
        detect_changes(directory, baseline_file)
    else:
        print("[WARNING] Initial scan incomplete.")

    try:

        while True:

            time.sleep(interval)

            current_files, scan_complete = scan_current_files(directory)

            if current_files is None:
                return

            if not scan_complete:
                print("[WARNING] Scan incomplete. Retrying...")
                continue

            if previous_files is None or current_files != previous_files:

                print("\n[INFO] File changes detected. Running integrity check...")

                detect_changes(directory, baseline_file)

                previous_files = current_files

    except KeyboardInterrupt:

        print("\n[INFO] Continuous monitoring stopped by user.")

