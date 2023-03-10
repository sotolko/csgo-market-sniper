# CS:GO Market sniper
***
![alt text](https://img.shields.io/github/last-commit/sotolko/csgo-market-sniper?style=for-the-badge) ![alt text](https://img.shields.io/github/commit-activity/m/sotolko/csgo-market-sniper?style=for-the-badge) ![alt text](https://img.shields.io/github/languages/top/sotolko/csgo-market-sniper?style=for-the-badge)
***
This bot will monitor skins of your choice, and then purchase them automatically.
At the moment it works only with **CHROMIUM BASED BROWSERS!**
This bot will not work with stickers and cases, keep this in mind. *(You can check what is planned at the bottom of README)*. Also consider that I'm working on this project alone, so there's a chance that something won't work as it should. If you find a bug, open a ticket in the issue and I'll try to fix it.

## Features

- Skin monitoring
- Automatic purchase
- Logging into file after purchase
- You can choose specific patterns or floats for bot to find
- Buy only skins with/without stickers
- You can set max price for skin
- You can set max pages to look for
***
## Dependencies

Selenium, PyYAML, Requests, chromedriver-autoinstaller

```
pip install -r /path/to/requirements.txt
```
***
## Usage
Open settinngs/config.yaml file ,and fill this file based on example provided.

```yaml
# Example configuration file for program

skins:
  - url: https://steamcommunity.com/market/listings/730/MP7%20%7C%20Army%20Recon%20%28Field-Tested%29
    float: # Leave empty for ANY
    price: 100 
    number_of_stickers: # Leave empty for ANY
    pages: 2
    pattern: 502, 800
  - url: https://steamcommunity.com/market/listings/730/UMP-45%20%7C%20Urban%20DDPAT%20%28Factory%20New%29
    float: 
    price: 
    number_of_stickers:
    pages: 2
    pattern: 123
```

Then, start the program
```bash
python csgo-market-sniper.py
```
Chrome window with steam login page will open. **LOGIN INTO STEAM FIRST!**
***
## Planned

- Setting to buy higher than set float skin, not lower only.
- Buy stickers, cases, agents etc.
***

