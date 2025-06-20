# Changelog

<!--
Changelog Categories:
- "Added" for new features.
- "Changed" for changes in existing functionality.
- "Removed" for now-removed features.
- "Fixed" for any bug fixes.
-->

## [1.0.0] - 2025-06-20

### Added
- **Initial Release**: The first version of the Photo Organizer & Tidier application.
- **Core Functionality**:
    - GUI for selecting a directory and a processing mode (`Organize` or `Tidy`).
    - **Organize Photos Mode**: Sorts `.cr2` and `.jpg` files into `RAW` and `JPG` subdirectories and creates a `JPG - Edit 1` copy for editing.
    - **Tidy Photos Mode**: Cleans up the `RAW` folder by removing files that do not have a corresponding edited version in `JPG - Edit 1`, then renames `RAW` to `RAW - Edit 1`.
- **User Experience**:
    - Background threading for file operations to keep the UI responsive.
    - Progress bar and status messages to provide feedback during processing.
    - Informative dialog boxes for success and error messages.
- **Logging & Documentation**:
    - On-demand log file (`log.txt`) creation in the selected directory to track all operations.
    - Project documentation including `README.md`, `requirements.txt`, and this `CHANGELOG.md`.