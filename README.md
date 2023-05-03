
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
4. **Add the CSGOFloat Extension:** Download the CSGOFloat Extension `.crx` file as explained in the section "Acquiring the CSGOFloat Extension". Add the path of your downloaded `.crx` file to the `chrome_options.add_extension` function in the `functions.py` file. Example:
```python
options.add_extension('path_to_your_crx_file.crx')
```
5. **Modify the configuration file:** Update the `settings/config.yaml` file to specify the skins you want the bot to monitor. Here is an example of the configuration file:
```yaml
skins:
  - url: https://steamcommunity.com/market/listings/730/MP7%20%7C%20Army%20Recon%20%28Field-Tested%29
    float: # Leave empty for ANY
    price: 100
    pages: 2
    pattern: 502, 800
```
6. **Run the bot:** Finally, run the bot using the command `python main.py`.
7. **Post-launch instructions:** Once the bot has started, you will need to manually log in to your Steam account. After logging in, you can press 'Enter' in the console to start the bot. Please ensure that you're ready to start and you're logged into Steam. The bot will then begin to monitor the specified skins and attempt to purchase them according to the rules specified in the `config.yaml` file.

## Acquiring the CSGOFloat Extension

Follow these steps to download the `.crx` file for the CSGOFloat extension:

1. Visit the [Chrome extension downloader](https://chrome-extension-downloader.com/) website.
2. Navigate to the CSGOFloat extension page on the [Chrome Web Store](https://chrome.google.com/webstore/detail/csgofloat-market-checker/jjicbefpemnphinccgikpdaagjebbnhg?hl=en) and copy the URL.
3. Paste the URL into the input field on the Chrome extension downloader website and click on "Download extension". This will download the `.crx` file for the CSGOFloat extension.

Once you have the `.crx` file, update the `add_extension` method in the `functions.py` file to point to the location of the `.crx` file.

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