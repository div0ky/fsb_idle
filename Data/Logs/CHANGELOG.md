# Changelog
All notable changes to this project will be documented in this file. We use Explicit Versioning - **BREAKING.FEATURE.FIX.REVISION**.

## [Unreleased]
- Missions
- Tavern
- Auto-Prestige
- Open Chests

## [2.0.2.1830] - 2020-02-11
### Fixed
- After the previous fix, the bot wouldn't crash, but wouldn't exit back to home
- Rapid deployment can be finicky, sorry.

## [2.0.1.1798] - 2020-02-11
### Fixed
- Bot would crash if it couldn't read the timer when no guild expeditions were available

## [2.0.0.1755] - 2020-02-10
### Added
- Support for multi-thredding, some fun features to come with this
- Mouse lockdown feature, if the most goes out of game it'll rebound
- Dynamic resolution support. The bot now automatically adapts to your screen size
- New installers for patch updates; future releases will be via downloadable exe
- User configurable options via `bot.ini`
- Logs now rotate at midnight
### Changed
- Completely gutted the logging and built a new system ground up
- Completely rebuilt how the bot runs, new classes, functions, etc
- Streamlined the farming process
### Deprecated
- You no longer *need* to run the game in 1080
### Fixed
- It shouldn't just randomly stop working on expeditions now; needs more testing

## [1.0.0.7310] - 2020-02-08
### Added
- Bot now handles guild expeditions
- laid some groundwork for auto-prestige
### Changed
- Modified some of the logging features
- **drastically** increased the speed of upgrades

## BUILD [200203.7144]
### Added
- Initial upload of all files in their current state.