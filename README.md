

# CS:GO Market sniper

![alt text](https://img.shields.io/github/last-commit/jcardama/csgo-market-sniper?style=for-the-badge) ![alt text](https://img.shields.io/github/commit-activity/m/jcardama/csgo-market-sniper?style=for-the-badge) ![alt text](https://img.shields.io/github/languages/top/jcardama/csgo-market-sniper?style=for-the-badge)
***

This bot is dedicated to monitoring and purchasing selected weapon skins.

**Please note:** The bot is currently compatible only with **Chromium-based browsers**. Ensure that you install and run the bot on a suitable platform.

While the bot is optimized for weapon skins, it's important to note that it does not currently support stickers and cases. Future updates may address these limitations.

If you encounter any bugs or issues, please open a ticket in the 'Issues' section and they will be addressed promptly.

## Getting Started

These instructions will guide you through the process of setting up and running the bot.
1. **Install Python:** The bot is written in Python. If you don't have Python installed on your system, you can download and install it from the [official website](https://www.python.org/downloads/).
2. **Clone the repository:** Clone this repository to your local machine using `git clone https://github.com/jcardama/csgo-market-sniper.git`.
3. **Install dependencies:** Navigate into the cloned repository and run `pip install -r settings/requirements.txt` to install the necessary dependencies.
4. **Modify the configuration file:** Update the `settings/config.yaml` file to specify the skins you want the bot to monitor and your proxy settings. Refer to the [Configuration](#configuration) section for a detailed explanation.
5. **Run the bot:** Finally, run the bot using the command `python csgo-market-sniper.py`.
6. **Post-launch instructions:** Once the bot has started, you will need to manually log in to your Steam account. After logging in, the bot will start automatically. The bot will then begin to monitor the specified skins and attempt to purchase them according to the criteria specified in the `config.yaml` file.

## Configuration

Your `settings/config.yaml` file should look something like this:

```yaml
proxy_url:
skins:
  - url: https://steamcommunity.com/market/listings/730/StatTrak%E2%84%A2%20SG%20553%20%7C%20Cyberforce%20%28Field-Tested%29
    float:
    price:
    pages: 5
    pattern:
    sort_by_float: asc
```

### Proxy

The `proxy_url` is where you can specify a proxy server that the bot will use for its requests. This might be necessary if you are running many instances of the bot, if your IP has been blocked by the Steam market, or if you need to appear to be in a different geographic location. The format for this setting is `username:password@ip:port`. If you're not using a proxy, you can leave this setting empty.

For example, if you're using a proxy server at IP address `192.0.2.0`, port `1080`, and it requires the username `myuser` and the password `mypassword` for authentication, you would set `proxy_url: myuser:mypassword@192.0.2.0:1080`.

Here are some popular proxy service providers you might consider:
- [Brightdata](https://brightdata.com/): Offers a large number of high-quality residential proxies.
- [Oxylabs](https://oxylabs.io/): Provides residential proxies as well as datacenter proxies.
- [Smartproxy](https://smartproxy.com/): Offers a wide range of residential proxies worldwide.
- [NetNut](https://netnut.io/): Provides residential proxies with direct ISP connectivity for high speed and stability.

### Skins

The `skins` section is where you specify the skins you want the bot to monitor. For each skin, you have several options:
- `url`: This is the URL of the item you want the bot to purchase. It should point to the specific page of the item on the Steam market. For example, `https://steamcommunity.com/market/listings/730/StatTrak%E2%84%A2%20SG%20553%20%7C%20Cyberforce%20%28Field-Tested%29`. 
- `float`: This value represents the "wear and tear" of a skin in CS:GO, ranging from 0 (perfect condition) to 1 (worst condition). If you want the bot to purchase an item with a specific float value, you can set this here. For example, if you want to buy items with a float value of 0.09, you would set `float: 0.09`. If you leave this empty, the bot will not consider float value when purchasing items.
- `price`: This is the price at which you want the bot to purchase an item. It should be set to a decimal value representing the price in your currency. If you leave it empty, the bot will not consider price when purchasing items.
- `pages`: This is the number of Steam market pages from which you want the bot to consider items. For example, if you want the bot to check the first 5 pages of listings for the item, you would set `pages: 5`. If you leave it empty, the bot will check all available pages.
- `pattern`: This is a list of pattern IDs you want the bot to consider. Pattern IDs in CS:GO represent specific pattern variations for skins, and each one is unique. If you want the bot to purchase items with specific patterns, you would set `pattern: 1, 2, 3`. If you leave it empty, the bot will not consider pattern when purchasing items.
- `sort_by_float`: This determines how the bot should sort items based on their float values. If you want the bot to prioritize items with lower float values, you would set `sort_by_float: asc`. If you want the bot to prioritize items with higher float values, you would set `sort_by_float: desc`. If you leave it empty, the bot will not sort items based on float value.

## Planned

- Filter skins with or without stickers (currently limited by the CSGOFloat extension)
- Setting to buy higher than set float skin, not lower only.
- Buy stickers, cases, agents etc.

## Feedback and Support

If you encounter any issues or have any suggestions for improving the bot, please open an issue in the GitHub repository. Your feedback is valuable and helps to enhance the bot for better functionality and user experience.

## Disclaimer

This bot is designed to automate the process of purchasing skins on the CS:GO market. Please use it responsibly and at your own risk. The author is not responsible for any actions you undertake using this bot.

## License

This project is licensed under the GNU General Public License - see the LICENSE.md file for details.