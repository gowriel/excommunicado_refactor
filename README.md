# Excommunicado Structure Refactoring Script

This Python script organizes files within a specified directory based on their metadata. It primarily focuses on images and videos, sorting them into directories named after the camera model and renaming them with timestamps derived from their metadata.

## Features

- **Organizes Files**: Moves files into directories named after the camera model.
- **Renames Files**: Names files using a timestamp derived from their metadata
> **Example** `Y{YEAR}-M{MONTH}-D{DAY}_h{HOUR}-m{MINUTE}-s{SECOND}_IMG`
- **Logging**: Creates logs of operations and errors.
- **Supports Various Metadata**: Uses EXIF, file creation dates, and ffprobe data for file organization.

## Prerequisites

The script requires several dependencies and external tools:

- **Python 3.9**
- **macOS**
- **External tools**: `exiftool`, `mdls`, `ffprobe`

## Installation

### 1. Install Dependencies

Run `install_deps.sh` script to install the required Python libraries and tools.

### 2. Install External Tools

Make sure you have the following tools installed on your system:
- **exiftool**: Available via package managers like `brew` on macOS or `apt` on Linux.
- **mdls**: Part of macOS. Ensure you are running this on macOS.
- **ffprobe**: Part of the `ffmpeg` suite, available via package managers.

### 3. Usage

1. Clone this repository or download the script.

    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2. Perform install_deps.sh

    ```bash
    ./install_deps.sh
    ```

3. Modify the `media_dir` variable in the script to point to the directory containing the files you want to organize.
4. Run the script using:

    ```bash
    python3 excommunicado_refactor.py
    ```

## Configuration

- **media_dir**: Set this variable in the script to the directory where your files are located and you want to refactor the structure.

## Logging

Logs are stored in `logs_excommunicado/*.log` directory with a timestamped filename.

## Example of final structure

Initial workspace:
```bash
/path/to/media_dir
│
├── IMG_1234.jpg
├── IMG_5678.heif
├── IMG_xyz.jpg
├── photo_123.jpg
├── video.mp4
```

After performing the script:
```bash
/path/to/media_dir
│
├── iPhone 16 Pro
│   ├── IMG_1234.jpg
│   ├── IMG_5678.heif
│   └── video.mp4
│
├── NIKON
│   └── photo_123.jpg
│
└── Unknown Device
    └── IMG_xyz.jpg
```