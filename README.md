# Firestone Idle Bot

A bot to play the idle RPG "Firestone" for you while you're AFK. This is very much a WIP and I'm fully aware that this repo is currently a very large mess. I'll be updating it and keeping it maintained better as I move forward.

## Getting Started

### Python 3
This app is written in Python 3. As such, you'll need to install [32-bit Python](https://www.python.org/ftp/python/3.8.1/python-3.8.1.exe) on your system. During installation be sure to to `Install to PATH` and `For ALL USERS`.

### Tesseract OCR
Key features in this bot require the use of Google's Tesseract so that it can "read" what's on the screen. The latest build can be downloaded [HERE](https://github.com/UB-Mannheim/tesseract/wiki). NOTE: Please install the `32-bit` version!

### Prerequisites

Here are the modules you'll need to install to work with this script.

```
pyautogui
pytesseract
opencv-python
requests
```
If you use one of the compiled installers under `Releases`, these modules will be installed for you automatically - if you don't already have them.

## Versioning
We are attempting to use [Semantic Versioning](https://semver.org/)

- Stable releases are packaged with an installer and tagged `-stable`
- Pre-releases of new features or fixes are tagged either `-alpha` or `-beta`
- An `-alpha` pre-release means the feature / fix is being worked on, is incomplete, and likely buggy.
- A `-beta` pre-release means the feature / fix is considered *complete*, but needs more testing and likely made more efficient
- We do not use `-rc` releases. If it makes it out of beta it becomes the latest `-stable` release

Check out the [CHANGELOG](https://github.com/div0ky/fsb_idle/blob/master/CHANGELOG.md) for more information.

## Launching the bot
1) Adjust the configuration file `bot.ini` to suit your needs
2) Load the game up
3) Ensure your upgrades are set to *milestones*
4) Make sure your leader abilities are enabled - if applicable
5) Launch Firestone Bot.exe

NOTE: The bot assumes you used the provided installer. If you did not, you're likely to run into several critical errors that make the bot unusable. Please use a provided installer.

## Author

- **Aaron J. Spurlock** - [div0ky](https://github.com/div0ky)