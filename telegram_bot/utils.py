import os
import uuid
from pathlib import Path

# Define the upload directory
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)  # Create the directory if it doesn't exist

def save_file(file_content: bytes, original_filename: str) -> str:
    """
    Save the file to the uploads directory with a unique name.
    Returns the file path relative to the project root.
    """
    # Generate a unique filename using UUID
    file_extension = original_filename.rsplit('.', 1)[-1] if '.' in original_filename else ''
    file_name = original_filename.rsplit('.', 1)[0] if '.' in original_filename else ''
    unique_filename = f"{file_name}_{uuid.uuid4()}.{file_extension}"
    file_path = UPLOAD_DIR / unique_filename

    # Save the file
    with open(file_path, "wb") as f:
        f.write(file_content)

    # Return the relative path as a string
    return str(file_path)

def remove_file(file_path: str):
    """
    Remove the file at the given file_path if it exists.
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        print(f"Error removing file {file_path}: {str(e)}")