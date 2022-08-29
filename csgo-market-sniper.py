import time
import logging
import sys
import requests
import chromedriver_autoinstaller

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.options import Options

chromedriver_autoinstaller.install()
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=chrome_options)

debug = False
urls = []
price_text_num = []


def check_user_balance():
    """Function that is checking user balance"""

    print("Checking user balance...")
    user_balance = driver.find_element("id", "header_wallet_balance")
    user_balance_edit = (''.join(c for c in user_balance.text if c.isdigit()))
    return user_balance_edit


def buy_log(item_name, item_float, item_pattern, item_price):
    """Function that will save information about purchase to logfile"""

    logger = logging.getLogger('BUYLOGGER')
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler("purchaseHistory.log", mode='a')
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s%(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S%p %Z')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.info(
        "Item name: {} , Float: {} , Pattern: {} , Price: {}".format(item_name, item_float, item_pattern, item_price))


def check_stickers(json):
    """Function that will check if skin have stickers"""

    if 'stickers' not in json["iteminfo"] or len(json["iteminfo"]['stickers']) == 0:
        return False
    else:
        return True


def buy_skin(buy_button):
    """Function that will buy skin"""

    # Buy now button
    driver.execute_script("arguments[0].click();", buy_button)

    # Execute order
    try:
        check_box = driver.find_element("id", "market_buynow_dialog_accept_ssa")
        driver.execute_script("arguments[0].click();", check_box)

        buy_button = driver.find_element("id", "market_buynow_dialog_purchase")
        driver.execute_script("arguments[0].click();", buy_button)

        close_button = driver.find_element("id", "market_buynow_dialog_close")
        driver.execute_script("arguments[0].click();", close_button)

        print("Purchase executed\n")
    except NoSuchElementException:
        print("Something went wrong, skipping to next skin!")
        return


def find_next_page():
    # Search for next page
    try:
        print("Checking next page...")
        next_page = driver.find_element('xpath', '//span[@id="searchResults_btn_next" and @class="pagebtn"]')
        driver.execute_script("arguments[0].click();", next_page)
        time.sleep(speed)
        return True
    except NoSuchElementException:
        print("No next page, going to next URL...")
        return False


def load_purchase_buttons():
    try:
        inspect_button = driver.find_elements("class name", "market_actionmenu_button")
        buy_buttons = driver.find_elements("class name", "item_market_action_button")
        prices_box = driver.find_elements('xpath', '//span[@class="market_listing_price market_listing_price_with_fee"]')
        return inspect_button, buy_buttons, prices_box
    except NoSuchElementException:
        print("Something went wrong, trying again...")
        return


def check_whole_page():

    max_price_reached = False

    while True:
        try:
            buttons, buy_now, prices = load_purchase_buttons()
        except NoSuchElementException:
            continue

        for price in prices:
            price_text_num.append(int(''.join(c for c in price.text if c.isdigit())) / 100)

        for idx, btn in enumerate(buttons):
            # Check item float and save JSON
            try:
                driver.execute_script("arguments[0].click();", btn)
                popup = driver.find_element("css selector", "#market_action_popup_itemactions > a")
                href = popup.get_attribute('href')

                response = requests.get('https://api.csgofloat.com/?url=' + href)
                response.raise_for_status()
                json_response = response.json()
            except NoSuchElementException:
                print("Something went wrong, trying next skin...")
                continue
            else:
                json_response_name = str(json_response["iteminfo"]["full_item_name"])
                json_response_float = float(json_response["iteminfo"]["floatvalue"])
                json_response_pattern = int(json_response["iteminfo"]["paintseed"])

            # Check user balance
            try:
                user_bal_num = float(check_user_balance()) / 100
            except ValueError:
                print("Cant get user balance. Are you logged in?")
                driver.quit()
                sys.exit()

            # Check if user have enough money for skin
            if user_bal_num < price_text_num[idx]:
                print("You dont have enough money for this skin, checking next...")
                continue
            else:
                print("Enough funds, continue...")

            # Check if float and pattern match with user input
            if float(urlinfo[count][3]) >= float(price_text_num[idx]) or float(urlinfo[count][3]) == -1.0:

                if json_response_float < float(urlinfo[count][0]):

                    if int(urlinfo[count][1]) == -1 or json_response_pattern == int(urlinfo[count][1]):

                        if urlinfo[count][2] == 'yes' and check_stickers(json_response):
                            print("Found skin with stickers")
                        elif urlinfo[count][2] == 'no' and not check_stickers(json_response):
                            print("Found skin without stickers")
                        elif urlinfo[count][2] == 'any':
                            print("Found skin")
                        else:
                            print("Your preference dont match this skin...")
                            continue

                    else:
                        print("Your pattern dont match this skin...")
                        continue
                else:
                    print("Your float dont match this skin...")
                    continue
            else:
                print("Max price reached!")
                max_price_reached = True
                break

            # Buy skin
            buy_skin(buy_now[idx])

            # Save information to file
            buy_log(json_response_name, json_response_float, json_response_pattern, price_text_num[idx])
            time.sleep(speed)

        # Clear information about previous page
        price_text_num.clear()

        # Search for next page
        if not find_next_page() or max_price_reached or debug:
            break


# Login page load
driver.get("https://steamcommunity.com/login/home/?goto=market%2Flistings%2F730")
print("Login into STEAM first!")

# Request time set from user
while True:
    try:
        speed = float(input("How much wait time in seconds after each search (enter for default) : ") or "2")
    except ValueError:
        print("Wrong input, try again.")
        continue
    else:
        break

# Reading URLs
try:
    with open('skins.txt', 'r', encoding="utf-8") as find_values:
        for line in find_values:
            line = line.rstrip()
            if line.startswith('https://steamcommunity.com/market/listings/730/'):
                urls.append(line)
            else:
                continue
except FileNotFoundError:
    print("Create skins.txt file and populate it with URLs!")
    driver.quit()
    sys.exit()

# Make default array for url information
urlinfo = [[0 for x in range(4)] for y in range(len(urls))]

# User input for each url
for x in range(len(urls)):
    while True:
        try:
            urlinfo[x][0] = float(input("Input float for skin No. " + str(x + 1) + " (enter for any): ") or "1")
            urlinfo[x][1] = int(input("Input pattern for skin No. " + str(x + 1) + " (enter for any): ") or "-1")
            urlinfo[x][2] = str(input("Do you want stickers on skin No. " + str(x + 1) + "? (yes/no/any): ") or "any")
            urlinfo[x][3] = float(input("Input max price for skin No. " + str(x + 1) + "? (enter for any): ") or "-1")

            if (urlinfo[x][2] != "yes") and (urlinfo[x][2] != "no") and (urlinfo[x][2] != "any"):
                raise ValueError

        except ValueError:
            print("Wrong input, try again.")
            continue
        else:
            break
    print("\n")

count = 0

# Search loop
while True:
    if count == len(urls):
        count = 0
    print("Reading URL...")
    driver.get(urls[count])
    check_whole_page()