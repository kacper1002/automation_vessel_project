# Changelog

## [Unreleased]

### Added
- Batch scenario runner
- CSV summary export
- Alarm lifecycle tracking with duration

### Changed
- Refactored scenario handling to config-based structure
- Updated simulation functions to accept scenario-specific initial levels

### Fixed
- Removed noisy zero-duration alarm events from report output
- Fixed scenario config bug where dict was treated as callable

## [0.1.0] - 2026-04-23

### Added
- Initial ballast transfer simulation
- Manual control logic
- Interlocks
- Alarm manager
- Scenario plots
- Pytest scenario coverage