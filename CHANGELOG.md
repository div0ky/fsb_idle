# Changelog
All notable changes to this project will be documented in this file. We are attempting to use [Semantic Versioning](https://semver.org/). We are also attempting to follow the guidelines laid out at [keep a changelog](https://keepachangelog.com).

## [Unreleased]
- Missions
- Tavern
- Open Chests

## [2.1.0-beta.0] - 2020-02-14
### Added
- The bot can now auto-prestige. How about that? Needs more testing, though.
- User config is now fully implemented. Modify `bot.ini` to set user options.
- Launcher now checks to make sure the game is running - if it can't find it, it exists.
- Comments to `bot.ini` to explain the settings / options.

## [2.1.0-alpha.0] - 2020-02-13
### Added
- You can now press the Escape key to kill the bot
- The bot now automatically switches focus to the game

## [2.0.4-stable] - 2020-02-13
### Added
- Some interal code for better debugging
### Fixed
- Guild Missions are now stable

## [2.0.4.1010] - 2020-02-12
### Added
- More user config options and verification for the new options
- Logging support for OCR success rate
### Fixed
- Okay, now Guild Missions really shouldn't confuse the bot. Seriously. We mean it.

## [2.0.3.5455] -2020-02-12
### Added
- Some changes to this CHANGELOG regarding v2.0.2

## [2.0.3.5455] - 2020-02-12
### Fixed
- Guild Missions shouldn't randomly confuse the bot now
- Bot now waits 5sec before starting as expected

## [2.0.2.1830] - 2020-02-11
### Fixed
- After the previous fix, the bot wouldn't crash, but wouldn't exit back to home
- Rapid deployment can be finicky, sorry.
- Bot now properly adjusts upgrade interval when going back to farm

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