# Firestone Idle Bot

## Last Updated: 20-03-01 [01:43:05] 
As of `v3.0.0-stable` I'm going to take a pause from adding new game features and focus on some "Quality of Life" improvements first. This will include bug fixes, performance enhancements, and other new features that don't increase functionality but make the bot nicer to use. 

## Summary
A bot to play the idle RPG "Firestone" for you while you're AFK. This is very much a WIP and I'm fully aware that this repo is currently a very large mess. I'll be updating it and keeping it maintained better as I move forward.

## Getting Started

### Python 3
This app is written in Python 3. As such, you'll need to install [32-bit Python](https://www.python.org/ftp/python/3.8.1/python-3.8.1.exe) on your system. During installation be sure to to `Install to PATH` and `For ALL USERS`.

### Prerequisites

#### Tesseract OCR
Key features in this bot require the use of Google's Tesseract so that it can "read" what's on the screen. The latest build can be downloaded [HERE](https://github.com/UB-Mannheim/tesseract/wiki). NOTE: Please install the `32-bit` version!

## Versioning
We are attempting to use [Semantic Versioning](https://semver.org/)

- Stable releases are packaged with an installer and tagged `-stable`
- Pre-releases are tagged with `-dev.x`

- We do not use `alpha`, `beta`, or `rc` releases. If it makes it out of dev it becomes the latest `-stable` release

Check out the [CHANGELOG](https://github.com/div0ky/fsb_idle/blob/master/CHANGELOG.md) for more information.

## Launching the bot
1) Load the game up
2) Ensure your upgrades are set to *milestones*
4) Make sure your leader abilities are enabled - if applicable
5) Launch Firestone Bot.exe

NOTE: The bot assumes you used the provided installer. If you did not, you're likely to run into several critical errors that make the bot unusable. Please use a provided binary.

## Author

- **Aaron J. Spurlock** - [div0ky](https://github.com/div0ky)