import os
import yara

# Define the directory of the current script file
current_directory = os.path.dirname(os.path.abspath(__file__))

# Define the path to the Yara rules file located in the same directory as the script
yara_rules_file = os.path.join(current_directory, "yara_rules.yar")

# Load Yara rules from the specified file
rules = yara.compile(filepath=yara_rules_file)

def scan_filesystem(directory):
    """
    Recursively scan the filesystem for files and scan them using Yara rules.
    """
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                # Open the file and scan it with Yara rules
                matches = rules.match(file_path)
                if matches:
                    print(f"Potential malware detected in file: {file_path}")
                    for match in matches:
                        print(f"Match: {match}")
            except Exception as e:
                # Handle exceptions, such as permission issues
                print(f"Error scanning file {file_path}: {e}")

# Define the starting directory for the scan (e.g., root directory)
starting_directory = "/"

# Start the filesystem scan from the starting directory
scan_filesystem(starting_directory)
