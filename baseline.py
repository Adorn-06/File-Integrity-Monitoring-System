
import json
from pathlib import Path
from datetime import datetime

from file_hasher import calculate_file_hash


def create_baseline(directory, baseline_file):

    directory = Path(directory)
    baseline_file = Path(baseline_file)

    file_hashes = {}

    if not directory.exists() or not directory.is_dir():
        print("[ERROR] Monitoring directory does not exist.")
        return

    print("\n[INFO] Creating file integrity baseline...\n")

    for file_path in directory.rglob("*"):

        if file_path.is_file():

            file_hash = calculate_file_hash(file_path)

            if file_hash:
                relative_path = file_path.relative_to(directory).as_posix()
                file_hashes[relative_path] = file_hash

                print(f"[SCANNED] {relative_path}")

    baseline_data = {
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "algorithm": "SHA-256",
        "files": file_hashes
    }

    baseline_file.parent.mkdir(parents=True, exist_ok=True)

    with open(baseline_file, "w", encoding="utf-8") as file:
        json.dump(baseline_data, file, indent=4)

    print("\n[SUCCESS] Baseline created successfully.")
    print(f"[INFO] Total files recorded: {len(file_hashes)}")
    print(f"[INFO] Baseline saved at: {baseline_file}")
