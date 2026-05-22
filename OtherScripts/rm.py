import os
import sys

def delete_file(file_path):
    try:
        os.remove(file_path)
        print(f"Successfully deleted the file: {file_path}")
    except Exception as e:
        print(f"Could not delete the file: {file_path}")
        print(e)

if len(sys.argv) < 2:
    print("Provide the file path as an argument.")
    sys.exit(1)

file_to_delete = sys.argv[1]
delete_file(file_to_delete)

# We define a delete_file function that attempts to delete the specified file using os.remove().
# We check the command-line arguments, and if there's at least one argument, we assume it's the file path and pass it to the delete_file function.
# If the file is successfully deleted, it prints a success message; otherwise, it prints an error message along with the exception details.
