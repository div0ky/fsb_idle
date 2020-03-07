# Changelog
All notable changes to this project will be documented in this file. We are attempting to use [Semantic Versioning](https://semver.org/). We are also attempting to follow the guidelines laid out at [keep a changelog](https://keepachangelog.com).

## [Unreleased]
- Tavern
- Open Chests

## [5.0.0-dev.2] - 2020-03-06

## Added
- Support for licensing

## Changed
- BOT NOW REQUIRES A VALID LICENSE KEY TO OPERATE; hence the bump to 5.0.0
- ConfigManager now checks for a license key and updates older config files to support this

## Fixed
- Auto updater wasn't working as expected
- Main window didn't reappear after choosing NOT to update
- Version numbers are now parsing correctly

## [4.1.2-dev.1] - 2020-03-05

### Added
- Bot now uses SQLite3

### Removed
- No longer using text file and Shelve for memory

### Fixed
- Window naming convention was breaking the bot wrapper

## [4.1.1] - 2020-03-03

## Added
- Better handling of internal configuration settings

## [4.1.0-stable] - 2020-03-03

### Added
- Status box to inform user what the bot is thinking / doing

### Fixed
- Auto prestige toggle wasn't properly setting prestige state

## [4.0.4-dev.13] - 2020-03-01

### Fixed
- Modifying party configuration would cause a crash on save
- Cleaned up imports to optimize runtime

## [4.0.0-dev.9] - 2020-03-1

### Fixed
- Mouse was locking prematurely when trying to edit configuration

## [4.0.0-dev.8] - 2020-03-01

### Changed
- The mouse is now disabled while the bot runs
- Alert box now times out when bot terminates

### Fixed
- The launcher / wrapper now exits gracefully if the bot crashes

## [4.0.0-dev.5] - 2020-02-29

### Added
- Error alerts if invalid party selections are made
- Bot window floats above all other windows now
- Additional map mission nodes

### Changed
- Better window handling
- Deployment structure and method
- Completely rebuilt the auto-update function
- Update is now optional and asks the user
- Users are no longer required to install Python to run the bot
- New app icons

### Fixed
- Guild Missions toggle now works in `General Options`
- Launcher / Wrapper properly refocuses and terminates 

## [3.1.0-alpha.3] - 2020-02-27

### Fixed
- Windows weren't sizing properly all the time for some reason

## [3.1.0-alpha.0] - 2020-02-27

### Added
- GUI interface for changing configuration options
- Additional map mission nodes
- Callback feature
### Changed
- GUI window now auto-centers itself on screen

## [3.0.0-stable] - 2020-02-27
I've decided to release this as the latest `stable` version. It's been running on my test machine for days now and I've had no serious glitches or bugs.
### Added
- Added additional map mission points
### Changed
- Now caching update installers to `LocalData` instead of Documents. This file removes itself after installation.
### Fixed
- OCR screenshots were causing crashes as the directory has changed. 
- Not calculating time correctly on Guild Expedition refreshes; band-aid for now
- Doesn't do upgrades if user clears the notification; went back to old way for now

## [3.0.2-alpha.0] - 2020-02-21 [YANKED]
### Fixed
- Not calculating time correctly on Guild Expedition refreshes; band-aid for now
- Doesn't do upgrades if user clears the notification; went back to old way for now

## [3.0.0-alpha.0] - 2020-02-20
### Added
- Auto-update feature requires an additional module. This is a "breaking" change. The compiled installers will take care of this dependency automatically.
### Changed
- Only checks for updates on startup now
- New system for persistent variables; aka how it "remembers." This one should be more stable.
- We now click known spawn points for missions on the map, and more accurately track how many troops are available

## [2.2.0-alpha.1] - 2020-02-19
### Added
- Groundwork for map missions. They work... sort of.
- Groundwork for auto-updating; may be a "breaking" change
- Groundwork for auto-restarting to keep guild refreshed
- Bot now has a "memory" and can remember things through restarts; buggy
### Fixed
- OCR tweaks make it even more reliable now

## [2.2.0-alpha.0] - 2020-02-16
### Added
- Groundwork for selling to Exotic Merchant

## [2.1.0-stable] - 2020-02-16
### Changed
- Really just changing status of `2.1.0-beta.1` to a `stable` release

## [2.1.0-beta.1] - 2020-02-16
### Changed
- Upgrades no longer use image recognition, this provides more accurate results across resolutions
- Dynamic coordinates for screen resolution are calculated more accurately now
- Made some tweaks to OCR... should hopefully be more consistant moving forward
- Moved bot.ini (config file) to user's documents to avoid admin permissions to modify it
- Logs now have their own folder in user's documents to clean things up a bit
### Fixed
- Upgrade progression switches work as expected now
- Bot properly reads user settings for prestige amount from config now
- Guild expedition timer used to count hours as minutes. It now properly calculates time remaining to refresh.
- A check on OCR was causing failures when checking if no expeditions are left... it should fail less now

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