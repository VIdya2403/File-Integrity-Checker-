#File Integrity Checker (FIC)

A lightweight, built-from-scratch cybersecurity tool written in Python that monitors and diagnoses directory tampering using cryptographic hashing. 

*This project establishes a "Known Good State" (a security baseline) of your local directory and actively flags unauthorized file modifications, creations, or deletions mimicking the core logic used by enterprise integrity tools like Tripwire.

#How It Works

The system operates in two core phases to detect anomalies:

1. Baseline Snapshot Mode (`Option 1`)
   The core script,`checker.py`, acts as a digital security guard walking through your specified directory.It reads every file and passes its data through the SHA-256 a hashing algorithm.This generates a unique 64-character alphanumeric string that serves as the file's permanent digital fingerprint. These fingerprints, along with their exact file paths, are written to a secure ledger file named `baseline.txt`.

2. Integrity Monitoring Mode (`Option 2`)
   When active, the script loads the trusted snapshots from `baseline.txt` and performs a live re-scan of the folder.It recalculates the SHA-256 hashes of all current files and compares them against the ledger. 

# Alert Triggers & Diagnosis

If the tool detects a discrepancy during comparison, it immediately isolates the anomaly and raises a specific flag in the terminal:

*ALERT: File MODIFIED! — Triggered via the Avalanche Effect. If a malicious actor or ransomware alters even a single character or space inside a file, its live cryptographic hash changes completely, breaking parity with the baseline ledger.

*WARNING: New untrusted file detected! — Triggered when a brand new file is introduced to the directory that was not present during the baseline snapshot phase.

*ALERT: File DELETED — Triggered when a file securely documented in the `baseline.txt` registry goes missing from the active directory.

Core Cyber Security Concepts Learned
*Cryptographic Hashing: Implementing industry-standard SHA-256 algorithms to ensure data immutability.

*The Baseline Strategy: Establishing a rigid security posture to reliably measure system drift and suspicious anomalies.

*Automation & System Traversal: Utilizing Python's native `os` library to securely audit file systems while dynamically filtering out background processes and script self-tracking.



# How To Run

#Setup
Ensure you have Python 3.x installed on your system.No external package dependencies are required, as this project is built entirely on Python's native standard libraries (`os` and `hashlib`).

#Execution
1. Open your terminal or command prompt inside the project folder.
2. Initialize the tool by running:
   ```bash
   python checker.py
