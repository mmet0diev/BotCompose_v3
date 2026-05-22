import os
import sys

def delete_directory(directory):
    try:
        # List all items (files and subdirectories) in the directory
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            
            # Check if it's a file and remove it
            if os.path.isfile(item_path):
                os.remove(item_path)
                
            # If it's a directory, recursively delete its contents
            elif os.path.isdir(item_path):
                delete_directory(item_path)
        
        # Finally, remove the empty directory itself
        os.rmdir(directory)
        print(f"Successfully deleted the directory: {directory}")
    
    except Exception as e:
        print(f"Could not delete the directory: {directory}")
        print(e)

if len(sys.argv) < 2:
    print("Provide at least 1 argument.")
    sys.exit(1)

dir_to_delete = sys.argv[1]
delete_directory(dir_to_delete)


# We define a delete_directory function that recursively deletes the contents of a directory and then removes the directory itself.
# We use os.listdir() to list all items (files and subdirectories) within the given directory.
# We check if each item is a file or a directory and handle them accordingly.
# If it's a file, we use os.remove() to delete the file.
# If it's a directory, we recursively call delete_directory() to delete its contents.
# Finally, after deleting all contents, we use os.rmdir() to remove the empty directory.
