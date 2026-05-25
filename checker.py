import os
import hashlib

def calculate_file_hash(file_path):
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception:
        return None

def create_baseline(target_folder, baseline_file):
    print(f"\n[+] Creating baseline snapshot for: {target_folder}...")
    with open(baseline_file, "w") as baseline:
        for root, dirs, files in os.walk(target_folder):
            for file in files:
                if file in [baseline_file, "checker.py"]:
                    continue
                full_path = os.path.join(root, file)
                file_hash = calculate_file_hash(full_path)
                if file_hash:
                    baseline.write(f"{full_path}|{file_hash}\n")
    print("Baseline snapshot created successfully!")

def monitor_integrity(target_folder, baseline_file):
    """Phase 2: Compares current files against the saved baseline."""
    print(f"\n[] Starting Integrity Monitoring Mode...")
    
    if not os.path.exists(baseline_file):
        print(f" Error: Baseline file '{baseline_file}' not found. Run baseline mode first.")
        return

    baseline_dict = {}
    with open(baseline_file, "r") as f:
        for line in f:
            if line.strip():
                path, saved_hash = line.strip().split("|")
                baseline_dict[path] = saved_hash

    current_files = set()

    for root, dirs, files in os.walk(target_folder):
        for file in files:
            if file in [baseline_file, "checker.py"]:
                continue
            full_path = os.path.join(root, file)
            current_files.add(full_path)
            current_hash = calculate_file_hash(full_path)

            # Case 1: File is in baseline, let's check if it changed
            if full_path in baseline_dict:
                if current_hash != baseline_dict[full_path]:
                    print(f" ALERT: File MODIFIED! -> {full_path}")
            # Case 2: File is brand new (not in baseline)
            else:
                print(f" WARNING: New untrusted file detected! -> {full_path}")

    for saved_path in baseline_dict:
        if saved_path not in current_files:
            print(f"ALERT: File DELETED! -> {saved_path}")

if __name__ == "__main__":
    print("=== FILE INTEGRITY CHECKER ===")
    print("1) Create a new baseline snapshot")
    print("2) Monitor folder for changes")
    choice = input("Choose an option (1 or 2): ")
    if choice == "1":
        create_baseline(".", "baseline.txt")
    elif choice == "2":
        monitor_integrity(".", "baseline.txt")
    else:
        print("Invalid choice. Exiting.")
