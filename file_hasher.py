
import hashlib

def calculate_file_hash(file_path):
    sha256 = hashlib.sha256()

    try:
        with open(file_path, "rb") as file:
            for chunk in iter(lambda: file.read(4096), b""):
                sha256.update(chunk)

        return sha256.hexdigest()

    except (OSError, PermissionError) as error:
        print(f"[ERROR] Cannot read {file_path}: {error}")
        return None
