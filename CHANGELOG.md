# Changelog

<!--
Changelog Categories:
- "Added" for new features.
- "Changed" for changes in existing functionality.
- "Removed" for now-removed features.
- "Fixed" for any bug fixes.
-->

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2025-06-20

### Added

- **Disk Space Tracking**: Added functionality to calculate and display the amount of disk space saved when deleting RAW files during the "Tidy Photos" operation.
  - Total disk space saved is calculated and displayed in both logs and success popup
  - Human-readable file size formatting (B, KB, MB, GB) for better readability

## [0.1.0] - 2025-06-20

### Added

- **Initial Beta Release**: The first version of the Photo Organizer & Tidier application.
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
