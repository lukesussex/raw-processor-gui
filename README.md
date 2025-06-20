# Photo Organizer & Tidier

A Python GUI application for organizing and tidying photo collections containing both .jpg and .cr2 (RAW) files.

## Features

- **Organize Photos Mode**: Automatically sorts photos into organized folders
- **Tidy Photos Mode**: Removes unused RAW files after editing
- Clean, intuitive GUI interface
- Progress tracking and status updates
- Error handling and user feedback

## Requirements

- Python 3.6 or higher
- No additional packages required (uses only Python standard library)

## Installation

1. Ensure you have Python 3.6+ installed
2. Download the `photo_organizer.py` file
3. No additional installation required

## Usage

### Running the Application

```bash
python photo_organizer.py
```

### Workflow

#### Step 1: Organize Photos
1. Launch the application
2. Click "Browse" to select your photo directory
3. Select "Organize Photos" mode
4. Click "Run"

The application will:
- Create a `RAW` folder and move all `.cr2` files there
- Create a `JPG` folder and move all `.jpg` files there
- Create a `JPG - Edit 1` folder as a copy of the JPG folder

#### Step 2: Edit Your Photos
- Navigate to the `JPG - Edit 1` folder
- Edit the photos using your preferred photo editing software
- Save the edited photos back to the same folder

#### Step 3: Tidy Photos
1. Return to the Photo Organizer application
2. Select the same directory as before
3. Select "Tidy Photos" mode
4. Click "Run"

The application will:
- Keep only `.cr2` files in the `RAW` folder that have corresponding `.jpg` files in `JPG - Edit 1`
- Remove `.cr2` files that don't have edited `.jpg` equivalents

## File Structure After Organization

```
Your_Photo_Directory/
├── RAW/                    # Contains .cr2 files
├── JPG/                    # Contains original .jpg files
└── JPG - Edit 1/          # Contains edited .jpg files
```

## Safety Features

- The application only moves files within the selected directory
- Original `.jpg` files are preserved in the `JPG` folder
- Only `.cr2` files without corresponding edited `.jpg` files are removed during tidying
- Progress indicators and status messages keep you informed

## Troubleshooting

- **"RAW folder not found"**: Make sure you've run "Organize Photos" first
- **"JPG - Edit 1 folder not found"**: Make sure you've run "Organize Photos" first
- **Permission errors**: Ensure you have write permissions for the selected directory

## Notes

- The application processes files in a separate thread to keep the UI responsive
- File operations are performed using the `pathlib` library for cross-platform compatibility
- All file extensions are handled case-insensitively (.jpg, .JPG, .cr2, .CR2)