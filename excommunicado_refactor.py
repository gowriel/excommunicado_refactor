import os
import shutil
import logging
from datetime import datetime
import subprocess

# List of subdirectories to ignore
IGNORE_SUBDIRS = [
    'Unknown'
]

# Ensure the log directory exists
log_directory = 'logs_excommunicado'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Generate a timestamped log file name
timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
log_filename = os.path.join(log_directory, f'file_excommunicado_refactor_at_{timestamp}.log')

# Configure logging
logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_exif_data(file_path):
    result = subprocess.run(['exiftool', '-DateTimeOriginal', '-Model', file_path], capture_output=True, text=True)
    exif_data = {}
    for line in result.stdout.splitlines():
        if ':' in line:
            key, value = line.split(':', 1)
            exif_data[key.strip()] = value.strip()
    return exif_data

def get_creation_date(file_path):
    result = subprocess.run(['mdls', '-name', 'kMDItemFSCreationDate', file_path], capture_output=True, text=True)
    for line in result.stdout.splitlines():
        if 'kMDItemFSCreationDate' in line:
            key, value = line.split('=', 1)
            return value.strip()
    return None

def get_ffprobe_data(file_path):
    result = subprocess.run(['ffprobe', '-v', 'quiet', '-show_entries', 'format_tags=creation_time', '-of', 'default=noprint_wrappers=1:nokey=1', file_path], capture_output=True, text=True)
    return result.stdout.strip()

def create_unique_filename(directory, base_name, ext):
    counter = 1
    new_file_name = f"{base_name}{ext}"
    new_file_path = os.path.join(directory, new_file_name)
    while os.path.exists(new_file_path):
        new_file_name = f"{base_name}-{counter}{ext}"
        new_file_path = os.path.join(directory, new_file_name)
        counter += 1
    return new_file_name

def parse_date(date_time_str):
    for fmt in ('%Y:%m:%d %H:%M:%S', '%Y-%m-%d %H:%M:%S %z', '%Y-%m-%dT%H:%M:%S.%fZ', '%Y:%m:%d %H:%M:%S%z'):
        try:
            return datetime.strptime(date_time_str, fmt)
        except ValueError:
            continue
    raise ValueError(f"Date format not recognized: {date_time_str}")

def process_files(directory):
    # for root, _, files in os.walk(directory):
    for root, dirs, files in os.walk(directory):
        # Modify dirs in-place to skip ignored directories
        dirs[:] = [d for d in dirs if d not in IGNORE_SUBDIRS]

        for file in files:
            file_path = os.path.join(root, file)
            try:
                exif_data = get_exif_data(file_path)
            except Exception as e:
                message = f"Error getting EXIF data for {file_path}: {e}"
                logging.error(message)
                print(message)
                continue
            
            try:
                if 'Date/Time Original' not in exif_data:
                    creation_date_str = get_creation_date(file_path)
                    if creation_date_str:
                        date_time = parse_date(creation_date_str)
                    else:
                        ffprobe_date_str = get_ffprobe_data(file_path)
                        if ffprobe_date_str:
                            date_time = parse_date(ffprobe_date_str)
                        else:
                            message = f"Skipping file {file_path} due to missing EXIF data, creation date, and ffprobe data."
                            logging.warning(message)
                            print(message)
                            continue
                else:
                    date_time_str = exif_data['Date/Time Original']
                    date_time = parse_date(date_time_str)
            except ValueError as ve:
                message = f"Skipping file {file_path} due to invalid date format: {ve}"
                logging.warning(message)
                print(message)
                continue
            except Exception as e:
                message = f"Error processing date for {file_path}: {e}"
                logging.error(message)
                print(message)
                continue
            
            try:
                # Determine the model name or set to 'Unknown_Device'
                model = exif_data.get('Camera Model Name', 'Unknown Device')

                date_str = date_time.strftime('Y%Y-M%m-D%d')
                hour_str = date_time.strftime('h%H-m%M-s%S')
                base_name = f"{date_str}_{hour_str}_IMG"

                ext = os.path.splitext(file_path)[1].lower()
                model_dir = os.path.join(directory, model)
                os.makedirs(model_dir, exist_ok=True)

                new_file_name = create_unique_filename(model_dir, base_name, ext)
                new_file_path = os.path.join(model_dir, new_file_name)

                # Check if the file is already in the correct directory and has the desired name
                if root == model_dir and file == new_file_name:
                    message = f"File {file_path} already satisfies the condition."
                    logging.info(message)
                    print(message)
                    continue

                shutil.move(file_path, new_file_path)
                message = f"Moved {file_path} to {new_file_path}"
                logging.info(message)
                print(message)
            except Exception as e:
                message = f"Error moving file {file_path}: {e}"
                logging.error(message)
                print(message)
                continue

if __name__ == "__main__":
    media_dir = '/path/to/media_dir'  # Replace with your directory path
    process_files(media_dir)