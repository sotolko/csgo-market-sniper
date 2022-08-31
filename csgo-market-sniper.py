import os
import time
import logging
import sys
import requests
import chromedriver_autoinstaller

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.chrome.options import Options

chromedriver_autoinstaller.install()
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=chrome_options)

urls = []


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def check_user_balance():
    """Function that is checking user balance"""

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


def check_stickers(json, quantity):
    """Function that will check if skin have stickers"""

    if len(json["iteminfo"]['stickers']) != quantity:
        return False
    elif 'stickers' not in json["iteminfo"] or len(json["iteminfo"]['stickers']) == 0:
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
        time.sleep(5)
    except NoSuchElementException:
        print("Something went wrong, skipping to next skin!")
        return


def find_next_page():
    """Function that will find next page and will go there"""

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
    """Function that will load purchase buttons from page"""

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

        try:
            price_text_num = []
            for price in prices:
                price_text_num.append(int(''.join(c for c in price.text if c.isdigit())) / 100)
        except (StaleElementReferenceException, ValueError):
            break

        for idx, btn in enumerate(buttons):
            # Check if max price is reached
            if not check_max_price(idx, price_text_num):
                max_price_reached = True
                break

            # Save JSON information
            try:
                item_name, item_float, item_pattern, whole_json = save_json_response(btn)
            except (NoSuchElementException, StaleElementReferenceException):
                print("Something went wrong, trying next skin...")
                continue

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

            # Check if float and pattern match with user input
            if check_item_parameters(item_float, item_pattern, whole_json) is False:
                continue

            # Buy skin
            buy_skin(buy_now[idx])

            # Save information to file
            buy_log(item_name, item_float, item_pattern, price_text_num[idx])

        # Search for next page
        if not find_next_page() or max_price_reached:
            break


def save_json_response(button):
    """Function that will save JSON into variables"""

    driver.execute_script("arguments[0].click();", button)
    popup = driver.find_element("css selector", "#market_action_popup_itemactions > a")
    href = popup.get_attribute('href')

    response = requests.get('https://api.csgofloat.com/?url=' + href)
    response.raise_for_status()
    json_response = response.json()
    json_response_name = str(json_response["iteminfo"]["full_item_name"])
    json_response_float = float(json_response["iteminfo"]["floatvalue"])
    json_response_pattern = int(json_response["iteminfo"]["paintseed"])
    return json_response_name, json_response_float, json_response_pattern, json_response


def check_item_parameters(item_float, item_pattern, whole):
    """Function that will compare user set parameters with skin"""
    match = False

    if item_float > float(url_info[count][0]):
        return False

    if item_pattern != -1:
        for pattern in url_info[count][1]:
            if int(pattern) != -1 and int(pattern) != item_pattern:
                continue
            else:
                match = True

        if not match:
            return False

    if url_info[count][2] != -1:
        if not check_stickers(whole, url_info[count][2]):
            return False

    return True


def check_max_price(order, price):
    if float(url_info[count][3]) >= float(price[order]) or float(url_info[count][3]) == -1.0:
        return True

    return False


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
url_info = [[0 for x in range(4)] for y in range(len(urls))]

# User input for each url
for x in range(len(urls)):
    while True:
        try:
            url_info[x][0] = float(input("Input float for skin No. " + str(x + 1) + " (0 to 1/enter for any): ") or "1")
            if url_info[x][0] > 1 or url_info[x][0] < 0:
                raise ValueError

            url_info[x][1] = list(map(int, input("Input pattern(s) for skin No. " + str(x + 1) + " (enter for any): ").split()))
            if len(url_info[x][1]) <= 0:
                url_info[x][1].append(-1)

            url_info[x][2] = int(input("How many stickers on skin No. " + str(x + 1) + " (0 to 4/enter for any): ") or "-1")
            if url_info[x][2] > 4 or url_info[x][2] < -1:
                raise ValueError

            url_info[x][3] = float(input("Input max price for skin No. " + str(x + 1) + "? (enter for any): ") or "-1")
            if url_info[x][3] < -1:
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
    print("Reading URL No. {}...".format(count))
    driver.get(urls[count])
    check_whole_page()
    count += 1
    cls()
