
from baseline import create_baseline
from monitor import detect_changes, monitor_continuously


# Project configuration
MONITORED_DIRECTORY = "monitored_files"
BASELINE_FILE = "baseline/file_hashes.json"



def display_menu():

    print("\n========================================")
    print("FILE INTEGRITY MONITORING SYSTEM")
    print("========================================")
    print("1. Create File Integrity Baseline")
    print("2. Scan Files for Integrity Changes")
    print("3. Start Continuous Monitoring")
    print("4. Update Baseline (Accept Current State)")
    print("5. Exit")
    print("========================================")


def main():

    while True:

        display_menu()

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":

            print("\n[INFO] Creating initial baseline...")
            create_baseline(
                MONITORED_DIRECTORY,
                BASELINE_FILE
            )

        elif choice == "2":

            print("\n[INFO] Starting integrity scan...")
            detect_changes(
                MONITORED_DIRECTORY,
                BASELINE_FILE
            )

        elif choice == "3":

            monitor_continuously(
                MONITORED_DIRECTORY,
                BASELINE_FILE,
                interval=5
            )

        elif choice == "4":

            confirmation = input(
                "\n[WARNING] This will replace the existing baseline. "
                "Accept current file states? (yes/no): "
            ).strip().lower()

            if confirmation == "yes":

                create_baseline(
                    MONITORED_DIRECTORY,
                    BASELINE_FILE
                )

            else:
                print("[INFO] Baseline update cancelled.")

        elif choice == "5":

            print("\n[INFO] Exiting File Integrity Monitoring System.")
            break

        else:

            print("\n[WARNING] Invalid choice. Please select 1, 2, 3, 4, or 5.")


if __name__ == "__main__":
    main()

