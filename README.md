# CS:GO Market sniper
***
![alt text](https://img.shields.io/github/last-commit/sotolko/csgo-market-sniper) ![alt text](https://img.shields.io/github/commit-activity/m/sotolko/csgo-market-sniper) ![alt text](https://img.shields.io/github/languages/top/sotolko/csgo-market-sniper)
***
This bot will monitor skins of your choice, and then purchase them automatically.
At the moment it works only with **CHROMIUM BASED BROWSERS!**
This bot will not work with stickers and cases, keep this in mind. *(Maybe I will implement that in the future)*

## Features

- Skin monitoring
- Automatic purchase
- Logging into file after purchase
- You can choose specific patterns or floats for bot to find
- Buy only skins with/without stickers
- You can set max price for skin
***
## Installation

![alt text](https://i.imgur.com/GGd8EiT.png)

```
pip install selenium & pip install requests & pip install chromedriver-autoinstaller
```
***
## Usage
Open skins.txt file ,and put skin URLs into this file like below. Remember to put every URL to new line.
![alt text](https://i.imgur.com/D0YzKmL.png)

Then, start the program

![alt text](https://i.imgur.com/NXjOBnz.png)

```
python csgo-market-sniper.py
```
Chrome window with steam login page will open. **LOGIN INTO STEAM FIRST!**
***
## Example
I want to buy **USP-S | Orion (Minimal Wear)** with float better than **0.13** and with pattern **763**
![alt text](https://i.imgur.com/WgeVfLA.gif)

